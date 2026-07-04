# transcript-qa-demo

a minimal transcript-QA harness — synthetic call transcripts with KNOWN planted errors are scored by an LLM judge against a plain-language rubric, so the judge itself is calibrated against ground truth we control. This is the answer to "who judges the judge": we know the errors because we planted them.

## Quickstart

1. `export GEMINI_API_KEY=<your free-tier key>`
2. `python judge.py`
3. Open `report.html`

## Rubric

1. **Factual consistency** — the agent never contradicts anything the customer stated (dates, order details, amounts, names).
2. **No invented commitments or policies** — the agent offers no policy, refund, or promise that was neither requested by the customer nor stated as existing information in the call.
3. **Task completion** — the customer's request is actually resolved on the call, or correctly escalated with everything needed for the follow-up actually collected.
4. **Language consistency** — the agent stays in the language the customer is speaking throughout the call.

## What this deliberately excludes and why

- **Regression alerts** — wiring alerts to model/prompt changes needs access to a deploy flow this demo doesn't have.
- **Production sampling** — scoring real calls needs PII clearance; synthetic transcripts sidestep that entirely.
- **Per-vertical ground truth (e.g. WER for ASR)** — this demo is the LLM-judge layer only; speech-recognition accuracy is a separate measurement.
