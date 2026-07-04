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


if __name__ == "__main__":
    main()
