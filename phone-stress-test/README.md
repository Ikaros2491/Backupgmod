# Phone line stress test (single target)

Desktop app + CLI to place a **capped** burst of concurrent calls to **one** phone number you own via Twilio. Useful for checking busy behavior, missed-call logging, or voicemail handling on your own line.

This is intentionally **not** a mass dialer: it only calls a single configured target and enforces hard ceilings.

## Windows app (.exe)

1. Download **PhoneLineStressTest.exe** from the GitHub Actions artifact named `PhoneLineStressTest-windows` on this branch/PR, **or** build it locally on Windows (below).
2. Double-click the EXE.
3. Fill in:
   - **Target phone number** — the line you are testing (E.164, e.g. `+15557654321`)
   - **Twilio from number** — your Twilio voice number (must differ from target)
   - **Account SID** / **Auth Token** — from [Twilio Console](https://console.twilio.com)
   - Concurrent / total calls / ring seconds (capped)
4. Click **Save settings** (optional) then **Start stress test**.
5. Confirm the target number when prompted.

### Build the EXE on a Windows PC

```bat
cd phone-stress-test
build_exe.bat
```

Output: `phone-stress-test\dist\PhoneLineStressTest.exe`

A GitHub Action (`.github/workflows/build-phone-stress-exe.yml`) also builds the Windows EXE on every push that touches this folder.

## Limits

| Setting | Default | Hard max |
|---------|---------|----------|
| Concurrent calls | 3 | 10 |
| Total calls | 10 | 50 |
| Ring timeout | 20s | 30s |

## Requirements

1. A [Twilio](https://www.twilio.com) account with a voice-capable number.
2. The destination line must be a number **you own**.
3. Target and from numbers must be different.
4. Outbound voice enabled (trial accounts can usually only call verified numbers).

Carrier terms of service still apply. Keep bursts short and infrequent. Twilio bills per call attempt.

## Run from source (GUI)

```bash
cd phone-stress-test
pip install -r requirements.txt
python gui_app.py
```

Or: `python stress_test.py --gui`

## Run from source (CLI)

```bash
cp .env.example .env
# Edit .env with Twilio SID, token, from-number, and target number
python stress_test.py --concurrent 3 --total-calls 10
```

## Safety notes

- Do not point this at numbers you do not control.
- Do not raise the hard caps in code to turn this into a blast tool.
- Auth token is stored locally only if you click **Save settings** (`%USERPROFILE%\.phone_stress_test_gui.json` on Windows).
