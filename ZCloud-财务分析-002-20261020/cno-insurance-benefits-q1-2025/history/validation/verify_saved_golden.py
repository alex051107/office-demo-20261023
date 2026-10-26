"""Check accepted-run statistics, unavailable scores, and historical exclusion offline."""
import argparse
import hashlib
import importlib.util
import json
import statistics
from pathlib import Path


TASK = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectory", type=Path, required=True)
    track = parser.parse_args().trajectory
    finalizer = load("golden_record_finalizer", TASK / "tests/finalize.py")
    engine = load("golden_record_engine", TASK / "tests/score_output.py")
    key = read(TASK / "tests/results_key.json")
    candidate = track / "golden/candidate.xlsx"
    result = engine.score(engine.extract(candidate, key), key)
    assert result["score"] == 1.0 and not result["interface_gate"]["failed"]
    assert not any(rule["triggered"] for rule in result["post_pool_rules"])
    summary = read(track / "golden_judge_fix_summary.json")
    assert summary == read(TASK / "validation/golden_judge_fix_summary.json")
    consistency = read(track / "consistency.json")
    group = consistency["groups"][0]
    judges = []
    for identifier in group["run_ids"]:
        folder = track / "judge_runs" / identifier
        reward = read(folder / "reward.json")
        details = read(folder / "reward-details.json")
        judge = read(folder / "judge.json")
        assert reward["verifier_error"] == judge["verifier_error"] == 0
        assert finalizer.llm_evidence_errors(details, candidate) == []
        pooled, counted, broken = finalizer.pooled_score(details)
        score = round(finalizer.apply_post_pool_rules(details, pooled), 6)
        assert not broken and counted == len(read(TASK / "rubrics.json")["items"])
        assert reward["reward"] == judge["score_final"] == score
        assert judge["reward_details_sha256"] == hashlib.sha256((folder / "reward-details.json").read_bytes()).hexdigest()
        judges.append(judge)
    scores = [judge["score_final"] for judge in judges]
    expected_sigma = statistics.stdev(scores) if len(scores) > 1 else None
    assert group["n"] == summary["valid_runs"] == len(scores)
    assert group["total_score"]["values"] == scores
    assert group["total_score"]["stddev_sample"] == expected_sigma == summary["total_sigma_sample"]
    assert len(group["criteria"]) == len(read(TASK / "rubrics.json")["items"])
    for criterion in group["criteria"]:
        values = [next(item["score"] for item in judge["criteria"] if item["criterion_id"] == criterion["criterion_id"]) for judge in judges]
        sigma = statistics.stdev(values) if len(values) > 1 else None
        assert criterion["values"] == values and criterion["n"] == len(values)
        assert criterion["stddev_sample"] == sigma
    assert group["requirement_met"] == (len(scores) == 5 and expected_sigma is not None and expected_sigma < 0.05 and all(item["pass_stddev_lt_0_05"] for item in group["criteria"]))
    quality = read(track / "quality_report.json")
    partial = read(track / "discrimination_cases.json")
    new_score = summary["new_score"]
    assert quality["target"]["score_final"] == quality["discrimination"]["reference_score"] == partial["reference_score"] == new_score
    assert quality["consistency"]["status"] == consistency["status"] == summary["status"]
    assert quality["consistency"]["groups"][0]["total_scores"] == scores
    assert partial["model_answers"] == quality["discrimination"]["model_scores"] == summary["new_model_scores"]
    for root in [TASK, track]:
        for line in (root / "records.jsonl").read_text().splitlines():
            record = json.loads(line)
            assert record["reference_score"] == new_score
            assert record["score_status"] == summary["status"]
        metadata = read(root / "metadata/task_metadata.json")
        assert metadata["reference_hybrid_score"] == new_score
        assert metadata["reference_fresh_valid_judge_runs"] == len(scores)
    if not scores:
        reward = read(track / "golden/reward.json")
        judge = read(track / "golden/judge.json")
        assert reward["verifier_error"] == 1 and not reward["score_available"]
        assert judge["score_final"] is None and not judge["judge_completed"]
        assert not list((track / "judge_runs").glob("golden_r[1-5]"))
    history = track / summary["history"]
    assert (history / "golden/reward.json").is_file()
    archived = sorted((history / "judge_runs").glob("golden_r[1-5]/reward-details.json"))
    assert len(archived) == 5
    blind = read(TASK / "validation/judge_fixtures/saved_blind.json")
    assert finalizer.llm_evidence_errors({"reward": blind["agent"]}, candidate)
    for label, score in summary["new_model_scores"].items():
        assert read(track / "rollouts" / label / "reward.json")["reward"] == score
    print(json.dumps({"saved_valid_runs": len(scores), "sample_sigma": expected_sigma,
                      "archived_runs": len(archived), "programmatic_golden": 1.0,
                      "current_score": new_score, "requirement_met": group["requirement_met"]}))


if __name__ == "__main__":
    main()
