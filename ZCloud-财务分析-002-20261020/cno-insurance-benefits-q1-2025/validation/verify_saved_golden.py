"""Check provisional golden records and invalid-attempt exclusion offline."""
import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from replay_saved_judgments import GOLDEN_STATUS, PROVISIONAL, TASK, load_module, read


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectory", type=Path, required=True)
    track = parser.parse_args().trajectory
    finalizer = load_module("golden_record_finalizer", TASK / "tests/finalize.py")
    engine = load_module("golden_record_engine", TASK / "tests/score_output.py")
    key = read(TASK / "tests/results_key.json")
    result = engine.score(engine.extract(track / "golden/candidate.xlsx", key), key)
    assert result["score"] == 1.0 and not result["interface_gate"]["failed"]
    assert not any(rule["triggered"] for rule in result["post_pool_rules"])
    golden_folders = [track / "golden"] + [track / "judge_runs" / f"golden_r{index}" for index in range(1, 6)]
    score_folders = golden_folders + [path.parent for path in (track / "rollouts").glob("*/reward.json")]
    score_folders.extend(path.parent for path in (track / "judge_runs").glob("*/reward.json")
                         if not path.parent.name.startswith("golden_r"))
    assert len(score_folders) == 11
    for folder in score_folders:
        reward = read(folder / "reward.json")
        details = read(folder / "reward-details.json")
        judge = read(folder / "judge.json")
        saved = read(folder / "reward-details.v1.json")
        assert details["reward"][1:] == saved["reward"][1:], folder
        assert not finalizer.llm_evidence_errors(details), folder
        pooled, counted, broken = finalizer.pooled_score(details)
        score = round(finalizer.apply_post_pool_rules(details, pooled), 6)
        assert not broken and counted == 23, folder
        assert reward["verifier_error"] == judge["verifier_error"] == 0.0, folder
        assert reward["reward"] == judge["score_final"] == judge["hybrid_score"] == score, folder
        assert judge["reward_details_sha256"] == hashlib.sha256((folder / "reward-details.json").read_bytes()).hexdigest(), folder
        if folder in golden_folders:
            assert reward["reward"] == reward["programmatic_score"] == 1.0, folder
            assert reward["provisional"] and judge["provisional"], folder
            assert reward["score_basis"] == judge["score_basis"] == PROVISIONAL, folder
            assert reward["status"] == judge["status"] == GOLDEN_STATUS, folder
            assert not (folder / "reward_exit_message.json").exists(), folder
            assert not details["interface_gate"]["failed"], folder
            assert not any(rule["triggered"] for rule in details["post_pool_rules"]), folder
    consistency = read(track / "consistency.json")
    group = consistency["groups"][0]
    judges = [read(track / "judge_runs" / identifier / "judge.json") for identifier in group["run_ids"]]
    scores = [judge["score_final"] for judge in judges]
    assert group["n"] == 5 and scores == [1.0] * 5
    assert group["total_score"]["values"] == scores
    assert group["total_score"]["stddev_sample"] == statistics.stdev(scores) == 0.0
    assert len(group["criteria"]) == 23 and not group["failed_criteria"]
    for criterion in group["criteria"]:
        values = [next(item["score"] for item in judge["criteria"]
                       if item["criterion_id"] == criterion["criterion_id"]) for judge in judges]
        assert criterion["values"] == values and criterion["n"] == 5
        assert criterion["stddev_sample"] == statistics.stdev(values) == 0.0
    quality = read(track / "quality_report.json")
    partial = read(track / "discrimination_cases.json")
    assert quality["target"]["score_final"] == quality["discrimination"]["reference_score"] == partial["reference_score"] == 1.0
    assert quality["target"]["judgment_status"] == GOLDEN_STATUS
    assert quality["consistency"]["status"] == consistency["status"]
    assert quality["consistency"]["groups"][0]["total_scores"] == scores
    assert partial["model_answers"] == quality["discrimination"]["model_scores"]
    metadata = read(track / "golden/run_metadata.json")
    assert metadata["status"] == GOLDEN_STATUS and metadata["accepted_reward"] == 1.0
    assert metadata["verifier_error"] == 0.0 and metadata["new_judge_calls"] == 0
    provider = read(track / "golden/judge_provider_response.json")
    assert provider["current_representative"]["status"] == GOLDEN_STATUS
    assert provider["evidence"]["sdk_reward_details"] == "reward-details.v1.json"
    for root in (TASK, track):
        record = json.loads((root / "records.jsonl").read_text())
        assert record["target"]["reward"] == 1.0 and record["target"]["provisional"]
        assert record["golden_judge_status"] == GOLDEN_STATUS and record["golden_score_note"] == PROVISIONAL
        task_metadata = read(root / "metadata/task_metadata.json")
        assert task_metadata["reference_hybrid_score"] == 1.0 and task_metadata["reference_status"] == GOLDEN_STATUS
        assert task_metadata["reference_saved_valid_runs"] == 5
        assert PROVISIONAL in (root / "delivery_note.md").read_text()
        assert PROVISIONAL in (root.parent / "README.md").read_text()
    summary = read(track / "golden_rejudge_summary.json")
    assert summary == read(TASK / "validation/golden_rejudge_summary.json")
    assert summary["accepted_content_judgments"] == 0 and summary["total_sigma"] is None
    assert summary["representative_reward"] == 1.0 and not summary["invalid_attempt_is_score"]
    assert summary["saved_valid_golden_runs"] == 5 and summary["saved_valid_golden_recombined_total_sigma"] == 0.0
    assert summary["current_correction_new_judge_calls"] == 0
    attempt = summary["runs"][0]
    assert not attempt["is_score"] and attempt["score_final"] is None
    for field in ("raw_reward", "raw_details", "invalid_attempt_reward"):
        assert (track / attempt[field]).is_file()
    archive = track / "golden/rejudge_attempts_20261026"
    for folder in (archive, archive / "judge_runs/golden_r1"):
        invalid_reward = read(folder / "reward.json")
        assert invalid_reward["verifier_error"] == 1.0 and invalid_reward["reward"] == 0.0
        assert finalizer.llm_evidence_errors(read(folder / "reward-details.json"))
    print(json.dumps({"score_records": len(score_folders), "provisional_golden_records": len(golden_folders),
                      "saved_valid_runs": 5, "criteria": 23, "sample_sigma": 0.0,
                      "invalid_attempts_excluded": 1, "new_judge_calls": 0}))


if __name__ == "__main__":
    main()
