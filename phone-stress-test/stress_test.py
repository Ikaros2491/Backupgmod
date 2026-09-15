#!/usr/bin/env python3
"""
Controlled phone-line stress tester for a single number you own.

Places a capped number of concurrent outbound calls via Twilio to ONE target.
This is intentionally not a mass dialer: multi-destination calling is refused.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

# Hard safety ceilings — CLI values cannot exceed these.
HARD_MAX_CONCURRENT = 10
HARD_MAX_TOTAL_CALLS = 50
HARD_MAX_RING_SECONDS = 30


@dataclass(frozen=True)
class Config:
    account_sid: str
    auth_token: str
    from_number: str
    target_number: str
    concurrent: int
    total_calls: int
    ring_seconds: int
    twiml_url: str


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def load_config(args: argparse.Namespace) -> Config:
    load_dotenv()

    concurrent = min(args.concurrent, HARD_MAX_CONCURRENT)
    total_calls = min(args.total_calls, HARD_MAX_TOTAL_CALLS)
    ring_seconds = min(args.ring_seconds, HARD_MAX_RING_SECONDS)

    if concurrent < 1 or total_calls < 1 or ring_seconds < 5:
        raise SystemExit("concurrent/total_calls must be >= 1 and ring_seconds >= 5")

    if concurrent > total_calls:
        concurrent = total_calls

    target = args.target or env_required("TARGET_NUMBER")
    from_number = env_required("TWILIO_FROM_NUMBER")

    if target == from_number:
        raise SystemExit(
            "TARGET_NUMBER and TWILIO_FROM_NUMBER must differ "
            "(Twilio cannot place a call from a number to itself)."
        )

    # Default TwiML: short silence then hang up — enough to occupy the line briefly.
    twiml_url = os.getenv(
        "TWIML_URL",
        "http://demo.twilio.com/docs/voice.xml",
    )

    return Config(
        account_sid=env_required("TWILIO_ACCOUNT_SID"),
        auth_token=env_required("TWILIO_AUTH_TOKEN"),
        from_number=from_number,
        target_number=target,
        concurrent=concurrent,
        total_calls=total_calls,
        ring_seconds=ring_seconds,
        twiml_url=twiml_url,
    )


def place_call(client: Client, config: Config, index: int) -> dict:
    try:
        call = client.calls.create(
            to=config.target_number,
            from_=config.from_number,
            url=config.twiml_url,
            timeout=config.ring_seconds,
        )
        return {
            "index": index,
            "sid": call.sid,
            "status": call.status,
            "ok": True,
            "error": None,
        }
    except TwilioRestException as exc:
        return {
            "index": index,
            "sid": None,
            "status": "failed",
            "ok": False,
            "error": f"{exc.status} {exc.msg}",
        }


def run(config: Config) -> int:
    print("Phone line stress test (single-target, capped)")
    print(f"  target:       {config.target_number}")
    print(f"  from:         {config.from_number}")
    print(f"  concurrent:   {config.concurrent} (hard max {HARD_MAX_CONCURRENT})")
    print(f"  total calls:  {config.total_calls} (hard max {HARD_MAX_TOTAL_CALLS})")
    print(f"  ring timeout: {config.ring_seconds}s (hard max {HARD_MAX_RING_SECONDS})")
    print()

    confirm = input(
        f'Type the target number "{config.target_number}" to confirm this is YOUR line: '
    ).strip()
    if confirm != config.target_number:
        print("Confirmation mismatch — aborting.")
        return 1

    client = Client(config.account_sid, config.auth_token)
    results: list[dict] = []
    started = time.time()

    with ThreadPoolExecutor(max_workers=config.concurrent) as pool:
        futures = [
            pool.submit(place_call, client, config, i + 1)
            for i in range(config.total_calls)
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            label = "OK" if result["ok"] else "FAIL"
            detail = result["sid"] or result["error"]
            print(f"[{label}] call {result['index']}/{config.total_calls}: {detail}")

    elapsed = time.time() - started
    ok = sum(1 for r in results if r["ok"])
    fail = len(results) - ok

    print()
    print(f"Done in {elapsed:.1f}s — placed={ok} failed={fail}")
    print(
        "Watch the target handset / carrier app for busy behavior, "
        "missed-call logging, and voicemail handling."
    )
    return 0 if fail == 0 else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Stress-test ONE phone number you own via Twilio. "
            f"Hard caps: {HARD_MAX_CONCURRENT} concurrent, "
            f"{HARD_MAX_TOTAL_CALLS} total, {HARD_MAX_RING_SECONDS}s ring."
        )
    )
    parser.add_argument(
        "--target",
        help="E.164 target number you own (else TARGET_NUMBER env)",
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=3,
        help=f"Parallel calls (default 3, max {HARD_MAX_CONCURRENT})",
    )
    parser.add_argument(
        "--total-calls",
        type=int,
        default=10,
        help=f"Total calls to place (default 10, max {HARD_MAX_TOTAL_CALLS})",
    )
    parser.add_argument(
        "--ring-seconds",
        type=int,
        default=20,
        help=f"Ring timeout before give-up (default 20, max {HARD_MAX_RING_SECONDS})",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args)
    return run(config)


if __name__ == "__main__":
    sys.exit(main())
