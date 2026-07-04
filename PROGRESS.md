# PROGRESS — transcript-qa-demo

Standalone repo, built 2026-07-04. Purpose: minimal transcript-QA harness with planted-error calibration (proof point 3 for the outreach pipeline).

## BLOCKED

- None. (Step 7 was blocked on a missing GEMINI_API_KEY at build time; King supplied the key on 2026-07-04 and the run completed. The key was passed as a process env var only — verified absent from every file in the repo.)

## Steps

- [x] Setup: repo folder, git init, PROGRESS.md
- [x] 1. transcripts/ — 10 synthetic calls (t01–t10), 4 planted errors, ground_truth.json
- [x] 2. rubric.md — 4 one-line criteria
- [x] 3. judge.py — per-transcript LLM call, strict JSON, loud failure
- [x] 4. judge.py — calibration vs ground_truth.json (caught / missed / false alarms)
- [x] 5. judge.py — report.html generation
- [x] 6. README.md — purpose, quickstart, rubric, exclusions
- [x] 7. Real run (2026-07-04, gemini-2.5-flash, one run, no tuning):
  **planted errors caught: 3/4** (t02, t05, t10) · **planted errors missed: 1/4** (t07) · **false alarms on clean transcripts: 0**
  - The t07 miss, with the judge's actual output (criterion 3, verdict PASS): *"The customer's request for a non-working keyboard was correctly escalated by scheduling a technical team callback for the next day, providing a case ID, and noting the preferred contact number and required items…"* — the judge accepted the agent's *note about* the customer's new number as if the number had been collected; it never was. Within the ≤1-miss threshold, so no prompt tuning was done, per the one-honest-run rule.
- [x] 8. **Final: calibration 3/4 caught, 1 missed (t07), 0 false alarms — one honest run, no tuning.** BLOCKED items: none. **Single next manual action for King: review report.html, publish this repo, add its link as proof point 3 in the outreach repo's PROFILE.md** (then re-run /analyze-company Bolna + /audit-pitch Bolna to flip the pitch to SEND-READY).
