"""Validate a split Excel package. No network, models, or file mutation."""
import hashlib
import json
import sys
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

ALLOWED = {"指令遵循", "内容质量-结论正确性", "内容质量-数值与计算准确性",
           "内容质量-专业规范", "内容质量-分析与论证质量", "内容质量-事实忠实性",
           "结构与组织", "操作与交付安全", "安全合规", "超预期贡献", "视觉美感"}

def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    def file(rel):
        p = PurePosixPath(rel)
        if not rel or p.is_absolute() or ".." in p.parts or "\\" in rel:
            raise ValueError("Unsafe relative reference")
        f = root / rel
        if not f.is_file():
            raise ValueError("Missing reference: " + rel)
        return f
    try:
        if any(p.is_symlink() for p in root.rglob("*")):
            raise ValueError("Symlink in delivery")
        manifest = json.loads((root/"manifest.json").read_text())
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != root/"manifest.json"}
        if actual != {x["path"] for x in manifest["files"]} or len(actual) != manifest["file_count"]:
            raise ValueError("Manifest inventory mismatch")
        for x in manifest["files"]:
            p = file(x["path"])
            if len(p.read_bytes()) != x["bytes"] or hashlib.sha256(p.read_bytes()).hexdigest() != x["sha256"]:
                raise ValueError("Integrity mismatch: " + x["path"])
            if x["zip_path"] != f"{root.parent.name}/{root.name}/{x['path']}":
                raise ValueError("ZIP path mismatch")
        records = [json.loads(l) for l in (root/"records.jsonl").read_text().splitlines() if l.strip()]
        if len(records) != 1:
            raise ValueError("Expected one record")
        r = records[0]
        file(r["metadata"]["path"])
        if (root/"rubrics.json").exists():
            for inp in r["inputs"]:
                p = file(inp["path"])
                if p.stat().st_size != inp["bytes"] or hashlib.sha256(p.read_bytes()).hexdigest() != inp["sha256"]:
                    raise ValueError("Input integrity mismatch")
            file(r["target"]["path"]); file(r["rubric"]["path"])
            rubric = json.loads((root/"rubrics.json").read_text())
            items = rubric["items"]
            if len(items) < 6 or len({x["id"] for x in items}) != len(items):
                raise ValueError("Invalid criterion count or duplicate ID")
            for x in items:
                required = {"id","description","dimension","criterion_type","criterion_necessity","type","weight","negate"}
                if not required <= set(x) or x["dimension"] not in ALLOWED or x["weight"] not in {10,7,3,-3,-7,-10}:
                    raise ValueError("Rubric schema mismatch")
                if x["type"] not in {"binary","gradient"} or x["negate"] != (x["weight"] < 0):
                    raise ValueError("Rubric sign mismatch")
                if x["type"] == "gradient" and set(x.get("levels",{})) != {"1","0.75","0.5","0.25","0"}:
                    raise ValueError("Gradient anchors missing")
            if rubric["metadata"]["scoring"]["s_max"] != sum(x["weight"] for x in items if x["weight"]>0):
                raise ValueError("s_max mismatch")
            meta = json.loads((root/"metadata/task_metadata.json").read_text())
            if r["difficulty_tier"] != meta["difficulty"]:
                raise ValueError("Difficulty label mismatch")
            task=tomllib.loads((root/"task.toml").read_text())
            if task["metadata"]["difficulty_tier"] != meta["difficulty"]:
                raise ValueError("task.toml difficulty label mismatch")
            for rel in ["environment/Dockerfile","solution/solve.sh","tests/test.sh","tests/finalize.py",
                        "tests/rubrics.toml","tests/criterion_adapter.py","tests/__golden_output/answer.xlsx"]:
                file(rel)
        else:
            file(r["golden"]["path"])
            for rollout in r["rollouts"]:
                candidate = file(rollout["path"])
                meta = json.loads(file(rollout["metadata"]).read_text())
                if hashlib.sha256(candidate.read_bytes()).hexdigest() != meta["candidate_sha256"]:
                    raise ValueError("Candidate/metadata mismatch")
                trajectory = candidate.parent/"trajectory/events.jsonl"
                if hashlib.sha256(trajectory.read_bytes()).hexdigest() != meta["exported_log_sha256"]:
                    raise ValueError("Trajectory/metadata mismatch")
                events, invalid = [], []
                for i,l in enumerate(trajectory.read_text().splitlines(),1):
                    try: events.append(json.loads(l))
                    except json.JSONDecodeError: invalid.append(i)
                if invalid != meta["non_json_lines"] or len(events) != meta["event_count"]:
                    raise ValueError("Undeclared non-JSON lines or changed event count")
                if invalid:
                    parsed=[json.loads(l) for l in (trajectory.parent/"parsed_events.jsonl").read_text().splitlines()]
                    diagnostic=[json.loads(l) for l in (trajectory.parent/"non_json_lines.jsonl").read_text().splitlines()]
                    original_lines=trajectory.read_text().splitlines()
                    if parsed != events or diagnostic != [{"line":i,"text":original_lines[i-1]} for i in invalid]:
                        raise ValueError("Parsed/diagnostic sidecars differ from original log")
                if events[-1] != meta["terminal_event"]:
                    raise ValueError("Terminal event mismatch")
                if meta["returncode"] != 0 or meta["status"] != "SESSION_EXITED_OK":
                    raise ValueError("Not a normally completed rollout")
        for p in root.rglob("*"):
            if p.suffix in {".xlsx",".pptx",".docx"}:
                with zipfile.ZipFile(p) as z:
                    if z.testzip():
                        raise ValueError("Office CRC error")
    except Exception as e:
        errors.append(str(e))
    print(("FAIL: " + "; ".join(errors)) if errors else
          "PASS: references, rubric schema, signed weights, manifests, Office CRC, trajectory identity")
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main())
