# PROGRESS — transcript-qa-demo

Standalone repo, built 2026-07-04. Purpose: minimal transcript-QA harness with planted-error calibration (proof point 3 for the outreach pipeline).

## BLOCKED

- (pending) GEMINI_API_KEY was not set in the build environment at setup time — step 7 (real run) will be blocked unless the key is available by then.

## Steps

- [x] Setup: repo folder, git init, PROGRESS.md
- [x] 1. transcripts/ — 10 synthetic calls (t01–t10), 4 planted errors, ground_truth.json
- [x] 2. rubric.md — 4 one-line criteria
- [x] 3. judge.py — per-transcript LLM call, strict JSON, loud failure
- [x] 4. judge.py — calibration vs ground_truth.json (caught / missed / false alarms)
- [x] 5. judge.py — report.html generation
- [ ] 6. README.md — purpose, quickstart, rubric, exclusions
- [ ] 7. Real run — paste calibration numbers here
- [ ] 8. Final entry — result + next manual action
