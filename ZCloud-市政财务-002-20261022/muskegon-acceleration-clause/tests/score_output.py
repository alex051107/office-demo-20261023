"""Public scoring entrypoint for the versioned, signed workbook evaluator."""
import importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('s3_frozen_bridge', HERE/'frozen_bridge.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

def extract(answer, key):
    return base.extract(answer, key)

def score(evidence, key):
    return base.score(evidence, key)
