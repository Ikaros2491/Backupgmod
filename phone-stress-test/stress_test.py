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
from typing import Callable

from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

# Hard safety ceilings — CLI/GUI values cannot exceed these.
HARD_MAX_CONCURRENT = 10
HARD_MAX_TOTAL_CALLS = 50
HARD_MAX_RING_SECONDS = 30
HARD_MIN_RING_SECONDS = 5

DEFAULT_TWIML_URL = "http://demo.twilio.com/docs/voice.xml"

LogFn = Callable[[str], None]


@dataclass(frozen=True)
class Config:
    account_sid: str
    auth_token: str
    from_number: str
    target_number: str
    concurrent: int
    total_calls: int
    ring_seconds: int
    twiml_url: str = DEFAULT_TWIML_URL


class ConfigError(ValueError):
    """Invalid user-supplied configuration."""


def normalize_e164(value: str, field_name: str) -> str:
    number = value.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not number:
        raise ConfigError(f"{field_name} is required.")
    if not number.startswith("+"):
        raise ConfigError(f"{field_name} must be in E.164 format, e.g. +15551234567.")
    digits = number[1:]
    if not digits.isdigit() or not (10 <= len(digits) <= 15):
        raise ConfigError(f"{field_name} looks invalid. Use E.164 like +15551234567.")
    return number


def build_config(
    *,
    account_sid: str,
    auth_token: str,
    from_number: str,
    target_number: str,
    concurrent: int,
    total_calls: int,
    ring_seconds: int,
    twiml_url: str | None = None,
) -> Config:
    sid = account_sid.strip()
    token = auth_token.strip()
    if not sid:
        raise ConfigError("Twilio Account SID is required.")
    if not token:
        raise ConfigError("Twilio Auth Token is required.")

    try:
        concurrent_i = int(concurrent)
        total_i = int(total_calls)
        ring_i = int(ring_seconds)
    except (TypeError, ValueError) as exc:
        raise ConfigError("Concurrent, total calls, and ring seconds must be numbers.") from exc

    if concurrent_i < 1:
        raise ConfigError("Concurrent calls must be at least 1.")
    if total_i < 1:
        raise ConfigError("Total calls must be at least 1.")
    if ring_i < HARD_MIN_RING_SECONDS:
        raise ConfigError(f"Ring seconds must be at least {HARD_MIN_RING_SECONDS}.")

    concurrent_i = min(concurrent_i, HARD_MAX_CONCURRENT)
    total_i = min(total_i, HARD_MAX_TOTAL_CALLS)
    ring_i = min(ring_i, HARD_MAX_RING_SECONDS)
    if concurrent_i > total_i:
        concurrent_i = total_i

    target = normalize_e164(target_number, "Target number")
    from_num = normalize_e164(from_number, "Twilio from number")
    if target == from_num:
        raise ConfigError(
            "Target number and Twilio from number must differ "
            "(Twilio cannot place a call from a number to itself)."
        )

    url = (twiml_url or DEFAULT_TWIML_URL).strip() or DEFAULT_TWIML_URL

    return Config(
        account_sid=sid,
        auth_token=token,
        from_number=from_num,
        target_number=target,
        concurrent=concurrent_i,
        total_calls=total_i,
        ring_seconds=ring_i,
        twiml_url=url,
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


def run_stress_test(
    config: Config,
    *,
    log: LogFn | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> dict:
    """
    Place capped concurrent calls to config.target_number.

    Returns a summary dict: {ok, failed, elapsed, results, cancelled}.
    """
    _log = log or print

    _log("Phone line stress test (single-target, capped)")
    _log(f"  target:       {config.target_number}")
    _log(f"  from:         {config.from_number}")
    _log(f"  concurrent:   {config.concurrent} (hard max {HARD_MAX_CONCURRENT})")
    _log(f"  total calls:  {config.total_calls} (hard max {HARD_MAX_TOTAL_CALLS})")
    _log(f"  ring timeout: {config.ring_seconds}s (hard max {HARD_MAX_RING_SECONDS})")
    _log("")

    client = Client(config.account_sid, config.auth_token)
    results: list[dict] = []
    started = time.time()
    cancelled = False

    with ThreadPoolExecutor(max_workers=config.concurrent) as pool:
        futures = [
            pool.submit(place_call, client, config, i + 1)
            for i in range(config.total_calls)
        ]
        for future in as_completed(futures):
            if should_cancel and should_cancel():
                cancelled = True
                for pending in futures:
                    pending.cancel()
                _log("Cancelled — waiting for in-flight requests to finish...")
                break
            result = future.result()
            results.append(result)
            label = "OK" if result["ok"] else "FAIL"
            detail = result["sid"] or result["error"]
            _log(f"[{label}] call {result['index']}/{config.total_calls}: {detail}")

    elapsed = time.time() - started
    ok = sum(1 for r in results if r["ok"])
    fail = len(results) - ok

    _log("")
    if cancelled:
        _log(f"Stopped early after {elapsed:.1f}s — placed={ok} failed={fail}")
    else:
        _log(f"Done in {elapsed:.1f}s — placed={ok} failed={fail}")
    _log(
        "Watch the target handset / carrier app for busy behavior, "
        "missed-call logging, and voicemail handling."
    )

    return {
        "ok": ok,
        "failed": fail,
        "elapsed": elapsed,
        "results": results,
        "cancelled": cancelled,
    }


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def load_config_from_args(args: argparse.Namespace) -> Config:
    load_dotenv()
    return build_config(
        account_sid=env_required("TWILIO_ACCOUNT_SID"),
        auth_token=env_required("TWILIO_AUTH_TOKEN"),
        from_number=env_required("TWILIO_FROM_NUMBER"),
        target_number=args.target or env_required("TARGET_NUMBER"),
        concurrent=args.concurrent,
        total_calls=args.total_calls,
        ring_seconds=args.ring_seconds,
        twiml_url=os.getenv("TWIML_URL"),
    )


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
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical interface instead of the CLI",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.gui:
        from gui_app import main as gui_main

        gui_main()
        return 0

    config = load_config_from_args(args)
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

    summary = run_stress_test(config)
    if summary["cancelled"]:
        return 1
    return 0 if summary["failed"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
