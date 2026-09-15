# Phone line stress test (single target)

Small Twilio-based tool to place a **capped** burst of concurrent calls to **one** phone number you own. Useful for checking busy behavior, missed-call logging, or voicemail handling on your own line.

This is intentionally **not** a mass dialer: it only calls a single configured target and enforces hard ceilings.

## Limits

| Setting | Default | Hard max |
|---------|---------|----------|
| Concurrent calls | 3 | 10 |
| Total calls | 10 | 50 |
| Ring timeout | 20s | 30s |

Before placing calls you must type the target number to confirm it is yours.

## Requirements

1. A [Twilio](https://www.twilio.com) account with a voice-capable number (`TWILIO_FROM_NUMBER`).
2. The destination line must be a number **you own** (`TARGET_NUMBER`).
3. `TARGET_NUMBER` and `TWILIO_FROM_NUMBER` must be different numbers.
4. Outbound voice enabled on the Twilio account (trial accounts can usually only call verified numbers).

Carrier terms of service still apply. Keep bursts short and infrequent. Twilio bills per call attempt.

## Setup

```bash
cd phone-stress-test
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Twilio SID, token, from-number, and target number
```

## Usage

```bash
source .venv/bin/activate
python stress_test.py
```

Optional knobs:

```bash
python stress_test.py --concurrent 5 --total-calls 20 --ring-seconds 15
python stress_test.py --target +15557654321 --concurrent 2 --total-calls 6
```

## What to observe

- Whether the handset shows busy / call-waiting under load
- How many concurrent inbound legs your carrier allows
- Missed-call and voicemail behavior when you do not answer

## Safety notes

- Do not point this at numbers you do not control.
- Do not raise the hard caps in code to turn this into a blast tool.
- If Twilio returns errors (402, 21215, etc.), fix account/number configuration rather than retrying in a tight loop.
