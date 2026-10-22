#!/usr/bin/env bash
# Explicitly invoked later by the paid main session; never invoked by exporter.
set -euo pipefail
: "${JUDGE_API_KEY:?Inject JUDGE_API_KEY through the environment}"
: "${JUDGE_BASE_URL:?Inject JUDGE_BASE_URL through the environment}"
: "${JUDGE_MODEL:?Inject JUDGE_MODEL through the environment}"
if test "${JUDGE_API_PROTOCOL:-anthropic}" != anthropic; then
  echo "This package requires the filesystem-capable agent judge over the anthropic protocol." >&2
  exit 2
fi
unset REWARDKIT_JUDGE REWARDKIT_MODEL ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY
case_root="$(cd "$(dirname "$0")" && pwd)"
candidate="${1:?Usage: run_judge.sh candidate.xlsx empty-result-directory}"
result="${2:?Provide a new result directory}"
candidate="$(cd "$(dirname "$candidate")" && pwd)/$(basename "$candidate")"
test -f "$candidate"
if test -e "$result"; then
  echo "Result directory already exists; refusing overwrite" >&2
  exit 2
fi
mkdir -p "$result"
result="$(cd "$result" && pwd)"
docker image inspect "${JUDGE_IMAGE:-office-demo:judge}" >/dev/null
docker run --rm --cpus 2 --memory 4g \
  -e JUDGE_API_KEY -e JUDGE_BASE_URL -e JUDGE_MODEL \
  -e JUDGE_PROVIDER -e JUDGE_API_PROTOCOL -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$case_root/tests:/tests:ro" \
  -v "$candidate:/app/output/answer.xlsx:ro" \
  -v "$result:/logs/verifier" \
  "${JUDGE_IMAGE:-office-demo:judge}" bash /tests/test.sh
python3 - "$result/reward.json" "$case_root/rubrics.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
count = len(json.load(open(sys.argv[2]))["items"])
if r.get("verifier_error") or r.get("criteria_counted") != count:
    raise SystemExit("Judge unavailable or incomplete; do not report this as a valid score")
print(json.dumps(r, ensure_ascii=False))
PY
