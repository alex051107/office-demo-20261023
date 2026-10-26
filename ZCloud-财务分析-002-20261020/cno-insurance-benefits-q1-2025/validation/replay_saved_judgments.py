"""Recombine current program criteria with saved valid text judgments offline."""
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
REVISION = "office-review-v2-round2-20261026"
CORRECTION = "golden-representative-correction-20261026"
PROVISIONAL = "新版金标文字未重新裁判；沿用原有效文字判定"
GOLDEN_STATUS = "PROVISIONAL_SAVED_VALID_TEXT"
ATTEMPT_ARCHIVE = "golden/rejudge_attempts_20261026"


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
    if not values:
        return {"values": [], "n": 0, "mean": None, "min": None, "max": None,
                "stddev_population": None, "stddev_sample": None, "pass_stddev_lt_0_05": None}
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
    reward_paths = [track / "golden/reward.json"]
    reward_paths.extend(sorted((track / "rollouts").glob("*/reward.json")))
    reward_paths.extend(sorted((track / "judge_runs").glob("*/reward.json")))
    for reward_path in reward_paths:
        folder = reward_path.parent
        label = folder.name
        if label == "golden" or label.startswith("golden_r"):
            candidate = track / "golden/candidate.xlsx"
        else:
            model = label.removesuffix("_r1")
            candidate = track / "rollouts" / model / "candidate.xlsx"
        old_reward = read(reward_path.with_name("reward.round1.json"))
        old_judge = read(folder / "judge.round1.json")
        is_golden = label == "golden" or label.startswith("golden_r")
        saved_reward = read(folder / "reward.v1.json")
        saved_judge = read(folder / "judge.v1.json")
        saved_details = read(folder / "reward-details.v1.json")
        assert saved_reward.get("verifier_error") == 0, label
        assert not finalizer.llm_evidence_errors(saved_details), label
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
                      "mode": "program_replay_with_saved_valid_text_judgments", "new_judge_calls": 0,
                      "saved_text_details": "reward-details.v1.json", "saved_candidate_sha256": saved_judge["candidate_sha256"],
                      "saved_rubric_sha256": saved_judge["rubric_sha256"],
                      "candidate_changed_since_saved_text_judgment": digest(candidate) != saved_judge["candidate_sha256"]}
        if is_golden:
            provenance.update(correction=CORRECTION, status=GOLDEN_STATUS, provisional=True,
                              note=PROVISIONAL, new_text_judgment_completed=False)
        details = {"reward": [program] + text_blocks, "offline_revision": provenance,
                   "interface_gate": result["interface_gate"], "post_pool_rules": result["post_pool_rules"]}
        pooled, counted, broken = finalizer.pooled_score(details)
        assert broken == 0 and counted == len(criteria) + 3
        uncapped = pooled
        score = round(finalizer.apply_post_pool_rules(details, pooled), 6)
        evidence_errors = finalizer.llm_evidence_errors(details)
        raw_hybrid_score = score
        assert not evidence_errors, label
        if is_golden:
            assert result["score"] == 1.0 and score == 1.0, label
            assert not result["interface_gate"]["failed"], label
            assert not any(rule["triggered"] for rule in result["post_pool_rules"]), label
        reward = dict(old_reward, reward=score, criteria_counted=float(counted),
                      verifier_error=1.0 if evidence_errors else 0.0, programmatic_score=result["score"], scorer_revision=REVISION,
                      text_judgments=PROVISIONAL if is_golden else "reused_saved; not newly evaluated",
                      llm_evidence_errors=evidence_errors, graded_score=raw_hybrid_score,
                      score_before_post_pool_rules=uncapped, post_pool_rules=result["post_pool_rules"], interface_gate=result["interface_gate"])
        if is_golden:
            reward.update(status=GOLDEN_STATUS, provisional=True, score_basis=PROVISIONAL,
                          offline_revision=provenance)
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
        current_criteria.extend(copy.deepcopy(item) for item in saved_judge["criteria"] if item["criterion_id"] in saved_ids)
        weighted = sum(criterion["weight"] * result["verdicts"][criterion["criterion_id"]]["credit"] for criterion in criteria)
        weighted -= sum(item["weight"] * (1 - item["value"]) for block in text_blocks for item in block["criteria"])
        judge = dict(old_judge, candidate_sha256=digest(candidate), rubric_sha256=rubric_digest,
                     weighted_sum=weighted, raw_score=pooled, score_final=score, reward=score,
                     graded_score=score, hybrid_score=score, criteria_counted=counted, criteria=current_criteria,
                     programmatic_score=result["score"], interface_gate=result["interface_gate"],
                     offline_revision=provenance, post_pool_rules=result["post_pool_rules"], score_before_post_pool_rules=uncapped)
        judge.update(verifier_error=reward['verifier_error'], graded_score=raw_hybrid_score,
                     llm_evidence_errors=evidence_errors, judgment_available=not evidence_errors)
        judge["reward_details_sha256"] = hashlib.sha256((json.dumps(details, ensure_ascii=False, indent=2) + "\n").encode()).hexdigest()
        judge["delivery_rubric_sha256"] = rubric_digest
        if is_golden:
            judge.update(status=GOLDEN_STATUS, provisional=True, score_basis=PROVISIONAL,
                         llm_status="SAVED_VALID_JUDGMENT_REUSED", judge_completed=False,
                         saved_judge_completed=saved_judge.get("judge_completed"),
                         saved_judgment_finished_at=saved_judge.get("finished_at"),
                         saved_judge="judge.v1.json", prompt_sha256=saved_judge.get("prompt_sha256"),
                         started_at=None, finished_at=None,
                         selection_policy="Original valid first judgment recombined offline; invalid round-2 attempt excluded.")
        write(folder / "reward-details.json", details)
        write(folder / "reward.json", reward)
        write(folder / "judge.json", judge)
        assert details["reward"][1:] == text_blocks
        record = {"candidate": label, "folder": str(folder.relative_to(track)),
                  "old_score": old_reward["reward"], "new_program_score": result["score"],
                  "new_final_score": score, "raw_hybrid_score": raw_hybrid_score, "verifier_error": reward['verifier_error'], "criteria_counted": counted,
                  "candidate_sha256": digest(candidate), "interface_gate": result["interface_gate"], "post_pool_rules": result["post_pool_rules"],
                  "penalties_triggered": [criterion["criterion_id"] for criterion in criteria if criterion["weight"] < 0 and result["verdicts"][criterion["criterion_id"]]["credit"]]}
        if is_golden:
            record.update(status=GOLDEN_STATUS, provisional=True, score_basis=PROVISIONAL)
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
                   text_judgment_scope="partial-credit controls have no new text judgment; reported scores are programmatic only",
                   reference_score=scored["golden"]["new_final_score"], reference_status=GOLDEN_STATUS,
                   reference_score_basis=PROVISIONAL, invalid_judge_attempts_excluded=True)
    write(track / "discrimination_cases.json", partial)
    consistency = read(backup(track / "consistency.json"))
    for group in consistency["groups"]:
        run_ids = [f"golden_r{index}" for index in range(1, 6)]
        judges = [read(track / "judge_runs" / identifier / "judge.json") for identifier in run_ids]
        assert all(judge["verifier_error"] == 0 for judge in judges)
        group.update(run_ids=run_ids, n=len(judges), provisional=True, score_basis=PROVISIONAL,
                     new_judge_calls=0, invalid_judge_attempts_excluded=True,
                     excluded_runs=[{"run_id": "round2_golden_r1", "path": ATTEMPT_ARCHIVE,
                                     "reason": "judge:artifact_access_error; not a score"}])
        group["total_score"] = statistic([judge["score_final"] for judge in judges])
        per_criterion = []
        for criterion in judges[0]["criteria"]:
            identifier = criterion["criterion_id"]
            values = [next(item["score"] for item in judge["criteria"] if item["criterion_id"] == identifier) for judge in judges]
            per_criterion.append(dict(criterion_id=identifier, kind=criterion["kind"], weight=criterion["weight"], **statistic(values)))
        group["criteria"] = per_criterion
        group["failed_criteria"] = [item["criterion_id"] for item in per_criterion if item["pass_stddev_lt_0_05"] is False]
        group["criterion_requirement_status"] = "OFFLINE_REPLAY_PASS" if not group["failed_criteria"] else "FAIL"
    consistency.update(status="OFFLINE_REPLAY_PASS_SAVED_VALID_TEXT_ONLY", scorer_revision=REVISION,
                       correction=CORRECTION, provisional=True, score_basis=PROVISIONAL,
                       unit="round-2 program criteria recombined with five saved valid original golden text judgments; zero new judge calls")
    consistency["limitations"] = [PROVISIONAL, "n=5及σ仅描述五份原有效文字判定与第二轮程序结果的离线重组，不是新版金标的五次独立重裁。", "第二轮不可读工作簿的尝试已隔离，不计为分数或一致性样本；该轮新有效文字判定仍为0。", "模型文字判定沿用历史回执，未重跑模型。"]
    write(track / "consistency.json", consistency)
    quality = read(backup(track / "quality_report.json"))
    quality["rubric_sha256"] = rubric_digest
    quality["target"].update(sha256=digest(track / "golden/candidate.xlsx"), score_final=scored["golden"]["new_final_score"])
    quality["target"].update(programmatic_score=scored['golden']['new_program_score'], raw_hybrid_score=scored['golden']['raw_hybrid_score'],
                             verifier_error=scored['golden']['verifier_error'], judgment_status=GOLDEN_STATUS,
                             provisional=True, score_basis=PROVISIONAL, invalid_judge_attempts_excluded=True)
    for item in quality["rollout_summary"]["models"]:
        item["score_final"] = model_scores[item["model"]]
    quality["rollout_summary"]["average_score"] = round(statistics.mean(model_scores.values()), 6)
    quality["judge"]["score_basis"] = PROVISIONAL + "；当前金标、五份原有效重复及模型均按第二轮程序判据离线重组；第二轮裁判错误已归档，不计为分数。本次无网络或付费调用。"
    quality["consistency"]["status"] = consistency["status"]
    quality["consistency"]["groups"] = [{"candidate": group["candidate_label"], "repeats": group["n"],
                                             "total_scores": group["total_score"]["values"],
                                             "total_stddev_sample": group["total_score"]["stddev_sample"],
                                             "max_criterion_stddev_sample": max((item["stddev_sample"] for item in group["criteria"] if item["stddev_sample"] is not None), default=None),
                                             "pass_stddev_lt_0_05": None if group['n'] < 5 else not group["failed_criteria"]} for group in consistency["groups"]]
    quality["discrimination"].update(reference_score=scored["golden"]["new_final_score"], model_scores=model_scores)
    quality['discrimination']['note'] = '参考答案程序分及暂定混合分均为1；' + PROVISIONAL + '。裁判错误不计分；部分分样例仅为程序判据控制，模型沿用保存文字判定，每个模型只有一份答卷。'
    quality["discrimination"]["partial_credit_cases"]["totals"] = {case["case"]: case["programmatic_total"] for case in partial["cases"]}
    quality["limitations"] = [text for text in quality["limitations"] if not text.startswith("rubrics.json 在评分后")]
    quality["limitations"].extend([PROVISIONAL, "第二轮重裁因工作簿不可读而无效并触发费用停止；已隔离，不参与任何分数或σ。新版文字独立验收未完成。"])
    quality["scorer_revision"] = REVISION
    quality["interface_gate"] = key["interface_gate"]
    quality['post_pool_rules'] = key['post_pool_rules']
    quality['overall_delivery_compliance'] = GOLDEN_STATUS
    quality['correction'] = CORRECTION
    write(track / "quality_report.json", quality)
    for path in (TASK / "records.jsonl", track / "records.jsonl"):
        old = path.with_name("records.round1.jsonl")
        records = [json.loads(line) for line in old.read_text().splitlines() if line.strip()]
        for record in records:
            record["target"].update(reward=1.0, programmatic_score=1.0, verifier_error=0.0,
                                    status=GOLDEN_STATUS, provisional=True, score_basis=PROVISIONAL)
            if "golden" in record:
                record["golden"].update(reward=scored["golden"]["new_final_score"], programmatic_score=1.0,
                                        verifier_error=0.0, status=GOLDEN_STATUS, provisional=True,
                                        score_basis=PROVISIONAL)
            for item in record.get("rollouts", []):
                model = item["path"].split("/")[1]
                item["reward"] = model_scores[model]
            record["scorer_revision"] = REVISION
            record["score_basis"] = "round2_program_replay_with_saved_valid_text_judgments"
            record['golden_judge_status'] = GOLDEN_STATUS
            record['golden_score_note'] = PROVISIONAL
            record['invalid_judge_attempts_excluded'] = True
            record["three_model_average_score"] = round(statistics.mean(model_scores.values()), 6)
        path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records))
    for root in (TASK, track):
        path = root / "metadata/task_metadata.json"
        metadata = read(path)
        metadata.update(reference_hybrid_score=1.0, reference_programmatic_score=1.0,
                        reference_judge_mean=1.0, reference_judge_stddev_sample=0.0,
                        reference_status=GOLDEN_STATUS, reference_provisional=True,
                        reference_saved_valid_runs=5, reference_score_note=PROVISIONAL,
                        scorer_revision=REVISION, correction=CORRECTION,
                        score_basis="第二轮程序判据＋原有效文字判定离线重组；" + PROVISIONAL,
                        invalid_judge_attempts_excluded=True)
        path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    report = {"scorer_revision": REVISION, "correction": CORRECTION, "new_solver_runs": 0, "new_judge_calls": 0,
              "golden_status": GOLDEN_STATUS, "golden_score_basis": PROVISIONAL,
              "saved_golden_text_criteria_unchanged": True, "invalid_judge_attempts_excluded": True,
              "saved_model_text_criteria_unchanged": True, "rows": rows,
              "partial_scores": {case["case"]: case["programmatic_total"] for case in partial["cases"]}}
    (TASK / "validation/rescore_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    metadata = read(track / "golden/run_metadata.round1.json")
    metadata.update(candidate_sha256=digest(track / "golden/candidate.xlsx"),
                    current_export_rubric_sha256=rubric_digest, status=GOLDEN_STATUS,
                    evidence_note=PROVISIONAL, provisional=True, score_basis=PROVISIONAL,
                    current_program_score=1.0, raw_hybrid_score=1.0, accepted_reward=1.0,
                    verifier_error=0.0, score_preserved=1.0, this_export_paid_calls=0,
                    new_judge_calls=0, saved_text_judgments="reward-details.v1.json",
                    saved_judge="judge.v1.json", correction=CORRECTION,
                    saved_candidate_sha256=read(track / "golden/judge.v1.json")["candidate_sha256"],
                    invalid_round2_attempt_archive="rejudge_attempts_20261026/",
                    new_judge_summary="../golden_rejudge_summary.json")
    write(track / "golden/run_metadata.json", metadata)
    provider_path = track / "golden/judge_provider_response.json"
    provider = read(provider_path)
    provider.update(evidence={"normalized_judge": "judge.v1.json",
                              "sdk_reward_details": "reward-details.v1.json",
                              "reward_receipt": "reward.v1.json"},
                    current_representative={"judge": "judge.json", "reward": "reward.json",
                                            "status": GOLDEN_STATUS, "score_basis": PROVISIONAL},
                    note="未查到历史上游原始响应；.v1文件是原有效裁判留存，不能冒充原始HTTP响应。当前代表记录为第二轮程序判据加原有效文字判定的离线重组。")
    provider_path.write_text(json.dumps(provider, ensure_ascii=False, indent=2) + "\n")
    summary = read(track / "golden_rejudge_summary.json")
    summary.update(representative_status=GOLDEN_STATUS, representative_reward=1.0,
                   representative_programmatic_score=1.0, representative_score_basis=PROVISIONAL,
                   invalid_attempt_is_score=False, current_correction_new_judge_calls=0,
                   saved_valid_golden_runs=5, saved_valid_golden_recombined_total_sigma=0.0,
                   saved_valid_golden_recombined_per_criterion_sigma={item["criterion_id"]: item["stddev_sample"]
                                                                     for item in consistency["groups"][0]["criteria"]},
                   sigma_reason="New round-2 judgments: no valid sample, sigma null. Separately, five saved valid judgments recombined offline: sigma 0; provisional.")
    for attempt in summary["runs"]:
        attempt.update(is_score=False, score_final=None,
                       raw_reward=ATTEMPT_ARCHIVE + "/judge_runs/golden_r1/reward.raw_judge.json",
                       raw_details=ATTEMPT_ARCHIVE + "/judge_runs/golden_r1/reward-details.raw_judge.json",
                       invalid_attempt_reward=ATTEMPT_ARCHIVE + "/judge_runs/golden_r1/reward.json")
        attempt["error_reward_placeholder"] = attempt.pop("accepted_reward", attempt.get("error_reward_placeholder"))
    write(track / "golden_rejudge_summary.json", summary)
    (TASK / "validation/golden_rejudge_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"rescored_evaluations": len(rows), "scores": model_scores, "golden": scored["golden"]["new_final_score"], "new_judge_calls": 0}))


if __name__ == "__main__":
    main()
