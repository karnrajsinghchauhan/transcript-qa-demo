"""Transcript-QA harness: LLM judge scored against planted ground truth.

Run: GEMINI_API_KEY=... python judge.py   (writes report.html)
"""

import json
import os
import sys
from pathlib import Path

from google import genai

MODEL = "gemini-2.5-flash"
ROOT = Path(__file__).parent

# Which rubric criterion each planted error (ground_truth.json) must trip.
EXPECTED_CRITERION = {"t02": 1, "t05": 2, "t07": 3, "t10": 4}

PROMPT_TEMPLATE = """You are a strict QA judge for customer-support call transcripts.

Evaluate the transcript below against this rubric:

{rubric}

Return STRICT JSON only, no prose, no markdown, exactly this shape:
{{"criteria": [{{"id": 1, "verdict": "PASS", "reason": "<one sentence quoting or pointing to the exact line>"}}, {{"id": 2, ...}}, {{"id": 3, ...}}, {{"id": 4, ...}}]}}

"verdict" must be "PASS" or "FAIL". Give exactly one entry per rubric criterion, ids 1 to 4.

TRANSCRIPT:
{transcript}
"""


def judge_transcript(client: genai.Client, rubric: str, transcript: str) -> list[dict]:
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT_TEMPLATE.format(rubric=rubric, transcript=transcript),
        config={"response_mime_type": "application/json"},
    )
    raw = response.text
    try:
        parsed = json.loads(raw)
        criteria = parsed["criteria"]
        assert len(criteria) == 4
        for c in criteria:
            assert c["id"] in (1, 2, 3, 4)
            assert c["verdict"] in ("PASS", "FAIL")
            assert isinstance(c["reason"], str)
    except Exception as exc:  # unparseable or wrong shape: exit loudly, no repair
        print("FATAL: judge returned unparseable/invalid JSON.", file=sys.stderr)
        print(f"Error: {exc}", file=sys.stderr)
        print("Raw response:\n" + (raw if raw is not None else "<empty>"), file=sys.stderr)
        sys.exit(1)
    return sorted(criteria, key=lambda c: c["id"])


def main() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("FATAL: GEMINI_API_KEY environment variable is not set.")

    client = genai.Client()
    rubric = (ROOT / "rubric.md").read_text(encoding="utf-8")

    results: dict[str, list[dict]] = {}
    for path in sorted((ROOT / "transcripts").glob("t*.txt")):
        tid = path.stem
        print(f"judging {tid} ...")
        results[tid] = judge_transcript(client, rubric, path.read_text(encoding="utf-8"))

    for tid, criteria in results.items():
        verdicts = " ".join(f"{c['id']}:{c['verdict']}" for c in criteria)
        print(f"{tid}  {verdicts}")

    ground_truth = json.loads((ROOT / "ground_truth.json").read_text(encoding="utf-8"))
    caught, missed, false_alarms = calibrate(results, ground_truth)
    print(f"planted errors caught: {len(caught)}/{len(ground_truth)}  {caught}")
    print(f"planted errors missed: {len(missed)}/{len(ground_truth)}  {missed}")
    print(f"false alarms on clean transcripts: {len(false_alarms)}  {false_alarms}")

    n_clean = len(results) - len(ground_truth)
    (ROOT / "report.html").write_text(
        render_report(results, len(caught), len(ground_truth), len(false_alarms), n_clean),
        encoding="utf-8",
    )
    print("wrote report.html")


def calibrate(results: dict, ground_truth: dict) -> tuple[list, list, list]:
    """caught: judge FAILed the expected criterion on a planted transcript.
    missed: it didn't. false_alarms: FAIL verdicts on clean transcripts."""
    caught, missed, false_alarms = [], [], []
    for tid, expected_id in EXPECTED_CRITERION.items():
        fails = {c["id"] for c in results[tid] if c["verdict"] == "FAIL"}
        (caught if expected_id in fails else missed).append(tid)
    for tid, criteria in results.items():
        if tid in ground_truth:
            continue
        for c in criteria:
            if c["verdict"] == "FAIL":
                false_alarms.append(f"{tid}#c{c['id']}")
    return caught, missed, false_alarms


def render_report(results: dict, n_caught: int, n_planted: int, n_false: int, n_clean: int) -> str:
    import html as h

    rows = []
    for tid, criteria in results.items():
        for i, c in enumerate(criteria):
            cell = f'<td class="{c["verdict"].lower()}">{c["verdict"]}</td><td>{h.escape(c["reason"])}</td>'
            if i == 0:
                rows.append(f'<tr><td rowspan="4" class="tid">{tid}</td><td>{c["id"]}</td>{cell}</tr>')
            else:
                rows.append(f'<tr><td>{c["id"]}</td>{cell}</tr>')
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Transcript-QA report</title>
<style>
body {{ font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
       color: #1a1a1a; background: #fff; max-width: 900px; margin: 24px auto; font-size: 13px; }}
h1 {{ font-size: 20px; }} h2 {{ font-size: 15px; margin-top: 20px; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
th, td {{ border: 1px solid #ccc; padding: 4px 8px; text-align: left; vertical-align: top; }}
th {{ background: #f2f2f2; }}
.tid {{ font-weight: 600; }}
.pass {{ color: #0a7a2f; font-weight: 600; }}
.fail {{ color: #b00020; font-weight: 600; }}
.calib {{ border: 2px solid #1a1a1a; padding: 10px 14px; margin-top: 20px; font-size: 14px; }}
@media print {{ body {{ margin: 8mm; }} }}
</style></head><body>
<h1>Transcript-QA report</h1>
<table>
<tr><th>Transcript</th><th>Criterion</th><th>Verdict</th><th>Judge's reason</th></tr>
{chr(10).join(rows)}
</table>
<div class="calib"><strong>Calibration:</strong> Judge caught {n_caught}/{n_planted} planted errors,
{n_false} false alarms on {n_clean} clean transcripts.</div>
</body></html>
"""


if __name__ == "__main__":
    main()
