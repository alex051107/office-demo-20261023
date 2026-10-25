"""Recompute program criteria and pool unchanged saved text judgments offline."""
import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import statistics
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook

sys.dont_write_bytecode = True
TASK = Path(__file__).resolve().parents[1]
REVISION = "office-review-v2-20261026"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def backup(path):
    destination = path.with_name(path.stem + ".v1" + path.suffix)
    if not destination.exists():
        shutil.copyfile(path, destination)
    return destination


def write(path, data):
    if path.exists():
        backup(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def load_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def statistic(values):
    deviation = statistics.stdev(values) if len(values) > 1 else None
    return {"values": values, "n": len(values), "mean": statistics.mean(values),
            "min": min(values), "max": max(values),
            "stddev_population": statistics.pstdev(values), "stddev_sample": deviation,
            "pass_stddev_lt_0_05": deviation < 0.05 if deviation is not None else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectory", type=Path, required=True)
    arguments = parser.parse_args()
    track = arguments.trajectory
    engine = load_module("saved_replay_engine", TASK / "tests/score_output.py")
    finalizer = load_module("saved_replay_finalizer", TASK / "tests/finalize.py")
    key = read(TASK / "tests/results_key.json")
    criteria = key["rows"] + key["tables"] + key["checks"]
    rubric_digest = digest(TASK / "rubrics.json")
    rows = []
    scored = {}
    for reward_path in sorted(track.rglob("reward.json")):
        folder = reward_path.parent
        label = folder.name
        if label == "golden" or label.startswith("golden_r"):
            candidate = track / "golden/candidate.xlsx"
        else:
            model = label.removesuffix("_r1")
            candidate = track / "rollouts" / model / "candidate.xlsx"
        old_reward = read(backup(reward_path))
        old_judge = read(backup(folder / "judge.json"))
        saved_details = read(backup(folder / "reward-details.json"))
        saved_blocks = saved_details["reward"]
        saved_blocks = saved_blocks if isinstance(saved_blocks, list) else [saved_blocks]
        text_blocks = [copy.deepcopy(block) for block in saved_blocks if block.get("kind") != "programmatic"]
        saved_ids = {item.get("name", item.get("id")) for block in text_blocks for item in block["criteria"]}
        assert saved_ids == {"L01", "L02", "L03"}, (label, saved_ids)
        extracted = engine.extract(candidate, key)
        result = engine.score(extracted, key)
        program = {"kind": "programmatic", "score": result["score"], "criteria": []}
        for criterion in criteria:
            identifier = criterion["criterion_id"]
            credit = result["verdicts"][identifier]["credit"]
            program["criteria"].append({"name": identifier, "raw": credit,
                                       "value": 1 - credit if criterion["weight"] < 0 else credit,
                                       "weight": abs(criterion["weight"]), "negate": criterion["weight"] < 0,
                                       "description": criterion["description"]})
        provenance = {"revision": REVISION, "evaluated_at": datetime.now().astimezone().isoformat(),
                      "mode": "offline_program_replay_with_saved_text_judgments", "new_judge_calls": 0,
                      "saved_text_details": "reward-details.v1.json", "saved_candidate_sha256": old_judge["candidate_sha256"],
                      "candidate_changed_since_saved_text_judgment": digest(candidate) != old_judge["candidate_sha256"]}
        details = {"reward": [program] + text_blocks, "offline_revision": provenance,
                   "interface_gate": result["interface_gate"]}
        pooled, counted, broken = finalizer.pooled_score(details)
        assert broken == 0 and counted == len(criteria) + 3
        score = round(pooled, 6)
        reward = dict(old_reward, reward=score, graded_score=score, criteria_counted=float(counted),
                      verifier_error=0.0, programmatic_score=result["score"], scorer_revision=REVISION,
                      text_judgments="reused_saved; not newly evaluated")
        current_criteria = []
        for index, criterion in enumerate(criteria):
            identifier = criterion["criterion_id"]
            verdict = result["verdicts"][identifier]
            current_criteria.append({"criterion_id": identifier, "score": verdict["credit"],
                                     "raw": verdict["credit"], "sdk_value": program["criteria"][index]["value"],
                                     "weight": criterion["weight"], "negate": criterion["weight"] < 0,
                                     "kind": "programmatic", "description": criterion["description"],
                                     "evidence": verdict.get("evidence", verdict.get("observed")),
                                     "reason": None, "source_pointer": f"reward-details.json#/reward/0/criteria/{index}"})
        current_criteria.extend(copy.deepcopy(item) for item in old_judge["criteria"] if item["criterion_id"] in saved_ids)
        weighted = sum(criterion["weight"] * result["verdicts"][criterion["criterion_id"]]["credit"] for criterion in criteria)
        weighted -= sum(item["weight"] * (1 - item["value"]) for block in text_blocks for item in block["criteria"])
        judge = dict(old_judge, candidate_sha256=digest(candidate), rubric_sha256=rubric_digest,
                     weighted_sum=weighted, raw_score=pooled, score_final=score, reward=score,
                     graded_score=score, criteria_counted=counted, criteria=current_criteria,
                     programmatic_score=result["score"], interface_gate=result["interface_gate"],
                     offline_revision=provenance)
        write(folder / "reward-details.json", details)
        write(folder / "reward.json", reward)
        write(folder / "judge.json", judge)
        assert details["reward"][1:] == text_blocks
        record = {"candidate": label, "folder": str(folder.relative_to(track)),
                  "old_score": old_reward["reward"], "new_program_score": result["score"],
                  "new_final_score": score, "criteria_counted": counted,
                  "candidate_sha256": digest(candidate), "interface_gate": result["interface_gate"],
                  "penalties_triggered": [criterion["criterion_id"] for criterion in criteria if criterion["weight"] < 0 and result["verdicts"][criterion["criterion_id"]]["credit"]]}
        rows.append(record)
        scored[str(folder.relative_to(track))] = record
    assert len(rows) == 11
    partial = read(backup(track / "discrimination_cases.json"))
    with tempfile.TemporaryDirectory(prefix="partial_", dir=TASK / "validation") as temporary:
        for case in partial["cases"]:
            workbook = load_workbook(TASK / "solution/golden/answer.xlsx")
            for change in case["changed_cells"]:
                sheet, coordinate = change["cell"].split("!")
                workbook[sheet][coordinate] = change["set_to"]
            path = Path(temporary) / "answer.xlsx"
            workbook.save(path)
            workbook.close()
            result = engine.score(engine.extract(path, key), key)
            case["programmatic_total"] = result["score"]
            case["positive_credit"] = {criterion["criterion_id"]: result["verdicts"][criterion["criterion_id"]]["credit"] for criterion in criteria if criterion["weight"] > 0}
            case["penalties_triggered"] = [criterion["criterion_id"] for criterion in criteria if criterion["weight"] < 0 and result["verdicts"][criterion["criterion_id"]]["credit"]]
    model_scores = {model: scored["rollouts/" + model]["new_final_score"] for model in ("gpt-5.6-sol", "claude-opus-4-8", "qwen3.8-max")}
    partial.update(model_answers=model_scores, scorer_revision=REVISION,
                   text_judgment_scope="partial-credit controls have no new text judgment; reported scores are programmatic only")
    write(track / "discrimination_cases.json", partial)
    consistency = read(backup(track / "consistency.json"))
    for group in consistency["groups"]:
        judges = [read(track / "judge_runs" / run / "judge.json") for run in group["run_ids"]]
        group["total_score"] = statistic([judge["score_final"] for judge in judges])
        per_criterion = []
        for criterion in judges[0]["criteria"]:
            identifier = criterion["criterion_id"]
            values = [next(item["score"] for item in judge["criteria"] if item["criterion_id"] == identifier) for judge in judges]
            per_criterion.append(dict(criterion_id=identifier, kind=criterion["kind"], weight=criterion["weight"], **statistic(values)))
        group["criteria"] = per_criterion
        group["failed_criteria"] = [item["criterion_id"] for item in per_criterion if not item["pass_stddev_lt_0_05"]]
        group["criterion_requirement_status"] = "OFFLINE_REPLAY_PASS" if not group["failed_criteria"] else "FAIL"
    consistency.update(status="OFFLINE_REPLAY_PASS_SAVED_TEXT_ONLY", scorer_revision=REVISION,
                       unit="deterministic program replay combined with five saved text judgments; not five new judge calls")
    consistency["limitations"].append("本次仅重算程序判据并复用历史五份文字判定；修订后的参考说明未重新送文字裁判，不构成新版混合裁判的独立稳定性验证。")
    write(track / "consistency.json", consistency)
    quality = read(backup(track / "quality_report.json"))
    quality["rubric_sha256"] = rubric_digest
    quality["target"].update(sha256=digest(track / "golden/candidate.xlsx"), score_final=scored["golden"]["new_final_score"])
    for item in quality["rollout_summary"]["models"]:
        item["score_final"] = model_scores[item["model"]]
    quality["rollout_summary"]["average_score"] = round(statistics.mean(model_scores.values()), 6)
    quality["judge"]["score_basis"] = "评分器v2离线重算全部程序判据，严格按finalize.py合并各答卷已保存文字判据；未执行新裁判或新求解。"
    quality["consistency"]["status"] = consistency["status"]
    quality["consistency"]["groups"] = [{"candidate": group["candidate_label"], "repeats": group["n"],
                                             "total_scores": group["total_score"]["values"],
                                             "total_stddev_sample": group["total_score"]["stddev_sample"],
                                             "max_criterion_stddev_sample": max(item["stddev_sample"] for item in group["criteria"]),
                                             "pass_stddev_lt_0_05": not group["failed_criteria"]} for group in consistency["groups"]]
    quality["discrimination"].update(reference_score=scored["golden"]["new_final_score"], model_scores=model_scores)
    quality["discrimination"]["partial_credit_cases"]["totals"] = {case["case"]: case["programmatic_total"] for case in partial["cases"]}
    quality["limitations"] = [text for text in quality["limitations"] if not text.startswith("rubrics.json 在评分后")]
    quality["limitations"].append("评分器v2新增和落实结构、来源、顺序、记录、单位及精度要求；文字判据的文本、权重、既有判定不变。金标说明有修订，未对新文本重新作文字判定。")
    quality["scorer_revision"] = REVISION
    quality["interface_gate"] = key["interface_gate"]
    write(track / "quality_report.json", quality)
    for path in (TASK / "records.jsonl", track / "records.jsonl"):
        old = backup(path)
        records = [json.loads(line) for line in old.read_text().splitlines() if line.strip()]
        for record in records:
            if "golden" in record:
                record["golden"]["reward"] = scored["golden"]["new_final_score"]
            for item in record.get("rollouts", []):
                model = item["path"].split("/")[1]
                item["reward"] = model_scores[model]
            record["scorer_revision"] = REVISION
            record["score_basis"] = "offline_program_replay_with_saved_text_judgments"
            record["three_model_average_score"] = round(statistics.mean(model_scores.values()), 6)
        path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records))
    report = {"scorer_revision": REVISION, "new_solver_runs": 0, "new_judge_calls": 0,
              "saved_text_criteria_unchanged": True, "rows": rows,
              "partial_scores": {case["case"]: case["programmatic_total"] for case in partial["cases"]}}
    (TASK / "validation/rescore_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"rescored_saved_evaluations": len(rows), "scores": model_scores, "golden": scored["golden"]["new_final_score"], "new_judge_calls": 0}))


if __name__ == "__main__":
    main()
