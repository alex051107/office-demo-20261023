"""No rewardkit import or judge invocation. Deterministic subset only."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--candidate", type=Path, default=Path("/app/output/answer.xlsx"))
    p.add_argument("--out", type=Path, default=Path("/logs/verifier/offline"))
    a = p.parse_args()
    here = Path(__file__).resolve().parent
    key = json.loads((here / "results_key.json").read_text())
    engine = load("office_score", here / "score_output.py")
    finalizer = load("office_finalizer", here / "finalize.py")
    extracted = engine.extract(a.candidate, key)
    if extracted["status"] == "JUDGE_ERROR":
        raise RuntimeError("Malformed workbook; verifier unavailable")
    result = engine.score(extracted, key)
    criteria = key["rows"] + key["tables"] + key["checks"]
    detail = {"reward": {"kind": "programmatic", "criteria": [
        {"name": c["criterion_id"], "weight": abs(c["weight"]),
         "negate": c["weight"] < 0,
         "raw": result["verdicts"][c["criterion_id"]]["credit"],
         "value": round(1-result["verdicts"][c["criterion_id"]]["credit"]
                   if c["weight"] < 0 else result["verdicts"][c["criterion_id"]]["credit"], 4)}
        for c in criteria]}}
    pooled, count, broken = finalizer.pooled_score(detail)
    constrained = finalizer.apply_score_rules(pooled, result)
    detail['score_rules'] = result['score_rules']
    detail['pooling'] = {'before_rules': pooled, 'after_rules': constrained}
    if broken or abs(constrained-result["score"]) > 0.0001:
        raise AssertionError("Finalizer and signed scorer disagree")
    a.out.mkdir(parents=True, exist_ok=True)
    for name, value in [("reward-details.json", detail), ("extraction.json", extracted),
                        ("score.json", result), ("reward.json", {
                            "scope": "programmatic_subset_only", "programmatic_score": round(constrained,6),
                            "criteria_counted": count, "hybrid_reward": None, "llm_status": "NOT_RUN"})]:
        (a.out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"programmatic_score": round(constrained,6), "criteria_counted": count,
                      "llm_status": "NOT_RUN", "hybrid_reward": None}))

if __name__ == "__main__":
    main()
