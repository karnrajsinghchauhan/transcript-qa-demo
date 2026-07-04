# PROGRESS — transcript-qa-demo

Standalone repo, built 2026-07-04. Purpose: minimal transcript-QA harness with planted-error calibration (proof point 3 for the outreach pipeline).

## BLOCKED

- **Step 7 BLOCKED: GEMINI_API_KEY is not set** (checked both the build shell and a fresh login shell). `python3 judge.py` exits with `FATAL: GEMINI_API_KEY environment variable is not set.` (exit code 1) — the loud-failure path works as specified. **No calibration numbers exist yet; report.html has not been generated.** Fix: `export GEMINI_API_KEY=<free-tier key>` then `python judge.py`.
  - What WAS verified without the key: judge.py syntax; calibration bucketing (caught/missed/false-alarms) and report.html rendering, exercised with synthetic verdicts — caught=[t02,t05,t07], missed=[t10], false=[t01#c4] came out correctly for a constructed test case.

## Steps

- [x] Setup: repo folder, git init, PROGRESS.md
- [x] 1. transcripts/ — 10 synthetic calls (t01–t10), 4 planted errors, ground_truth.json
- [x] 2. rubric.md — 4 one-line criteria
- [x] 3. judge.py — per-transcript LLM call, strict JSON, loud failure
- [x] 4. judge.py — calibration vs ground_truth.json (caught / missed / false alarms)
- [x] 5. judge.py — report.html generation
- [x] 6. README.md — purpose, quickstart, rubric, exclusions
- [x] 7. Real run — **BLOCKED, no key** (see BLOCKED section); attempted, failed loudly as designed. Calibration numbers: none yet.
- [x] 8. **Final: no calibration result — run blocked on missing GEMINI_API_KEY.** BLOCKED items: step 7 only. **Single next manual action for King: get a free-tier Gemini key (aistudio.google.com), run `export GEMINI_API_KEY=<key> && python3 judge.py`, check the calibration block in report.html; if the judge catches ≥3/4 planted errors, publish this repo and add it as proof point 3 in the outreach repo's PROFILE.md.**
