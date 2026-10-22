"""Version-scoped adapter for atomic workbook checks and signed penalties.

The pinned SDK does not transfer programmatic negate into Score. This hook only
changes the explicitly registered penalty functions, preserving all other scores.
It never changes platform test.sh/finalize.py or the installed SDK source.
"""
import importlib.util
import json
from functools import lru_cache
from pathlib import Path
import rewardkit as rk
from rewardkit.reward import Reward

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("office_frozen_scorer", HERE / "score_output.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
KEY = json.loads((HERE / "results_key.json").read_text())
ALL = [c for c in KEY.get("rows", []) + KEY.get("tables", []) + KEY.get("checks", []) if c["weight"] != 0]
PENALTIES = {c["criterion_id"] for c in ALL if c["weight"] < 0}

@lru_cache(maxsize=8)
def result(workspace, size, modified_ns):
    path = Path(workspace) / "output/answer.xlsx"
    extracted = engine.extract(path, KEY)
    if extracted["status"] == "JUDGE_ERROR":
        raise ValueError("Workbook cannot be parsed; scoring unavailable")
    return engine.score(extracted, KEY)

@rk.criterion(description="{criterion_id}: frozen atomic workbook check", shared=True)
def office_atomic(workspace: Path, criterion_id: str) -> float:
    p = workspace / "output/answer.xlsx"
    stat = p.stat() if p.exists() else None
    return result(str(workspace), stat.st_size if stat else 0,
                  stat.st_mtime_ns if stat else 0)["verdicts"][criterion_id]["credit"]

for c in ALL:
    rk.office_atomic(c["criterion_id"], name=c["criterion_id"], weight=abs(c["weight"]))

# Function identity is restricted to this module's registered criterion IDs.
# Hook once even if discovery imports helper modules a second time.
if not getattr(Reward._eval_criterion, "_office_signed_adapter", False):
    original_eval = Reward._eval_criterion

    def signed_eval(self, i, fn, workspace):
        score = original_eval(self, i, fn, workspace)
        if getattr(fn, "_office_penalty", False):
            score.value = 1.0 - score.value
            score.negate = True
        return score

    signed_eval._office_signed_adapter = True
    Reward._eval_criterion = signed_eval

# Identify only our own checks; a coincidentally named criterion is unaffected.
from rewardkit.session import current
for fn, weight in current().criteria:
    if getattr(fn, "_criterion_name", "") in PENALTIES:
        fn._office_penalty = True
