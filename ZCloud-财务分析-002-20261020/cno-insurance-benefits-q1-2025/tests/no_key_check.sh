#!/usr/bin/env bash
# Missing credentials must fail closed before any agent or API can be started.
set -uo pipefail
mkdir -p /logs/verifier/graded
if [[ -z "${JUDGE_API_KEY:-${EVAL_API_KEY:-}}" ]]; then
  printf '%s\n' 'AuthenticationError: JUDGE_API_KEY / EVAL_API_KEY missing; LLM judge NOT_STARTED; offline credential preflight.' > /logs/verifier/graded/stderr.txt
  cat /logs/verifier/graded/stderr.txt >&2
  python3 /tests/finalize.py --graded /logs/verifier/graded/reward.json --graded-rc 78 --out /logs/verifier/reward.json
  cat /logs/verifier/reward.json /logs/verifier/reward_exit_message.json
  exit 0
fi
printf '%s\n' 'This diagnostic refuses supplied credentials; no judge launched.' >&2
exit 79
