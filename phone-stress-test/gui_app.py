#!/usr/bin/env python3
"""Desktop GUI for the single-target phone line stress tester."""

from __future__ import annotations

import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from stress_test import (
    HARD_MAX_CONCURRENT,
    HARD_MAX_RING_SECONDS,
    HARD_MAX_TOTAL_CALLS,
    HARD_MIN_RING_SECONDS,
    ConfigError,
    build_config,
    run_stress_test,
)

APP_TITLE = "Phone Line Stress Test"
CONFIG_PATH = Path.home() / ".phone_stress_test_gui.json"


class StressTestApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(560, 640)
        self.geometry("640x720")
        self.configure(bg="#1a1f24")

        self._cancel = threading.Event()
        self._worker: threading.Thread | None = None

        self._build_style()
        self._build_form()
        self._load_saved_settings()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#1a1f24"
        panel = "#242b33"
        fg = "#e8eef4"
        muted = "#9aa7b5"
        accent = "#2f6fed"

        style.configure(".", background=bg, foreground=fg, fieldbackground=panel)
        style.configure("TFrame", background=bg)
        style.configure("Card.TFrame", background=panel)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=panel, foreground=fg, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=bg, foreground=fg, font=("Segoe UI", 16, "bold"))
        style.configure("Hint.TLabel", background=bg, foreground=muted, font=("Segoe UI", 9))
        style.configure("CardHint.TLabel", background=panel, foreground=muted, font=("Segoe UI", 9))
        style.configure("TEntry", fieldbackground=panel, foreground=fg, insertcolor=fg)
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure(
            "Accent.TButton",
            background=accent,
            foreground="#ffffff",
            padding=(14, 8),
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Accent.TButton", background=[("active", "#2558c7"), ("disabled", "#4a5560")])

    def _labeled_entry(
        self,
        parent: ttk.Frame,
        label: str,
        hint: str,
        show: str | None = None,
    ) -> ttk.Entry:
        block = ttk.Frame(parent, style="Card.TFrame")
        block.pack(fill="x", pady=(0, 10))
        ttk.Label(block, text=label, style="Card.TLabel").pack(anchor="w")
        if hint:
            ttk.Label(block, text=hint, style="CardHint.TLabel").pack(anchor="w", pady=(0, 4))
        entry = ttk.Entry(block, show=show) if show else ttk.Entry(block)
        entry.pack(fill="x", ipady=4)
        return entry

    def _build_form(self) -> None:
        outer = ttk.Frame(self, padding=20)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text=APP_TITLE, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text=(
                f"Single-target load test for a number you own. "
                f"Hard caps: {HARD_MAX_CONCURRENT} concurrent, "
                f"{HARD_MAX_TOTAL_CALLS} total, {HARD_MAX_RING_SECONDS}s ring."
            ),
            style="Hint.TLabel",
            wraplength=580,
        ).pack(anchor="w", pady=(4, 16))

        card = ttk.Frame(outer, style="Card.TFrame", padding=16)
        card.pack(fill="x")

        self.target_entry = self._labeled_entry(
            card,
            "Target phone number (the line you are testing)",
            "E.164 format, e.g. +15557654321",
        )
        self.from_entry = self._labeled_entry(
            card,
            "Twilio from number",
            "Your Twilio voice number in E.164, must differ from target",
        )
        self.sid_entry = self._labeled_entry(
            card,
            "Twilio Account SID",
            "From console.twilio.com",
        )
        self.token_entry = self._labeled_entry(
            card,
            "Twilio Auth Token",
            "Stored only on this computer if you click Save settings",
            show="*",
        )

        knobs = ttk.Frame(card, style="Card.TFrame")
        knobs.pack(fill="x", pady=(4, 0))
        knobs.columnconfigure((0, 1, 2), weight=1)

        self.concurrent_var = tk.StringVar(value="3")
        self.total_var = tk.StringVar(value="10")
        self.ring_var = tk.StringVar(value="20")

        self._knob(knobs, 0, "Concurrent", self.concurrent_var, f"1–{HARD_MAX_CONCURRENT}")
        self._knob(knobs, 1, "Total calls", self.total_var, f"1–{HARD_MAX_TOTAL_CALLS}")
        self._knob(
            knobs,
            2,
            "Ring seconds",
            self.ring_var,
            f"{HARD_MIN_RING_SECONDS}–{HARD_MAX_RING_SECONDS}",
        )

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=16)

        self.save_btn = ttk.Button(actions, text="Save settings", command=self._save_settings)
        self.save_btn.pack(side="left")

        self.start_btn = ttk.Button(
            actions,
            text="Start stress test",
            style="Accent.TButton",
            command=self._on_start,
        )
        self.start_btn.pack(side="right")

        self.cancel_btn = ttk.Button(
            actions,
            text="Cancel",
            command=self._on_cancel,
            state="disabled",
        )
        self.cancel_btn.pack(side="right", padx=(0, 8))

        ttk.Label(outer, text="Log", style="TLabel").pack(anchor="w")
        log_frame = ttk.Frame(outer)
        log_frame.pack(fill="both", expand=True, pady=(6, 0))

        self.log_text = tk.Text(
            log_frame,
            height=14,
            wrap="word",
            bg="#12161a",
            fg="#d7e0ea",
            insertbackground="#d7e0ea",
            relief="flat",
            font=("Consolas", 10),
        )
        scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(state="disabled")

    def _knob(
        self,
        parent: ttk.Frame,
        column: int,
        label: str,
        variable: tk.StringVar,
        hint: str,
    ) -> None:
        cell = ttk.Frame(parent, style="Card.TFrame")
        cell.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
        ttk.Label(cell, text=label, style="Card.TLabel").pack(anchor="w")
        ttk.Label(cell, text=hint, style="CardHint.TLabel").pack(anchor="w", pady=(0, 4))
        ttk.Entry(cell, textvariable=variable).pack(fill="x", ipady=4)

    def _append_log(self, message: str) -> None:
        def _write() -> None:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self.after(0, _write)

    def _set_running(self, running: bool) -> None:
        self.start_btn.configure(state="disabled" if running else "normal")
        self.cancel_btn.configure(state="normal" if running else "disabled")
        state = "disabled" if running else "normal"
        for entry in (
            self.target_entry,
            self.from_entry,
            self.sid_entry,
            self.token_entry,
        ):
            entry.configure(state=state)

    def _collect_config(self):
        return build_config(
            account_sid=self.sid_entry.get(),
            auth_token=self.token_entry.get(),
            from_number=self.from_entry.get(),
            target_number=self.target_entry.get(),
            concurrent=self.concurrent_var.get(),
            total_calls=self.total_var.get(),
            ring_seconds=self.ring_var.get(),
        )

    def _on_start(self) -> None:
        if self._worker and self._worker.is_alive():
            return
        try:
            config = self._collect_config()
        except ConfigError as exc:
            messagebox.showerror("Invalid settings", str(exc), parent=self)
            return

        confirmed = messagebox.askyesno(
            "Confirm your line",
            (
                "This will place outbound Twilio calls to:\n\n"
                f"{config.target_number}\n\n"
                f"{config.total_calls} calls, {config.concurrent} at a time.\n\n"
                "Only continue if this is YOUR phone line."
            ),
            parent=self,
        )
        if not confirmed:
            return

        self._cancel.clear()
        self._set_running(True)
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        def worker() -> None:
            try:
                run_stress_test(
                    config,
                    log=self._append_log,
                    should_cancel=self._cancel.is_set,
                )
            except Exception as exc:  # noqa: BLE001 - show any Twilio/network failure in UI
                self._append_log(f"ERROR: {exc}")
                self.after(
                    0,
                    lambda: messagebox.showerror("Run failed", str(exc), parent=self),
                )
            finally:
                self.after(0, lambda: self._set_running(False))

        self._worker = threading.Thread(target=worker, daemon=True)
        self._worker.start()

    def _on_cancel(self) -> None:
        self._cancel.set()
        self._append_log("Cancel requested...")

    def _save_settings(self) -> None:
        payload = {
            "target_number": self.target_entry.get().strip(),
            "from_number": self.from_entry.get().strip(),
            "account_sid": self.sid_entry.get().strip(),
            "auth_token": self.token_entry.get().strip(),
            "concurrent": self.concurrent_var.get().strip(),
            "total_calls": self.total_var.get().strip(),
            "ring_seconds": self.ring_var.get().strip(),
        }
        try:
            CONFIG_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            messagebox.showinfo(
                "Saved",
                f"Settings saved to:\n{CONFIG_PATH}",
                parent=self,
            )
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc), parent=self)

    def _load_saved_settings(self) -> None:
        if not CONFIG_PATH.exists():
            return
        try:
            payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return

        self._set_entry(self.target_entry, payload.get("target_number", ""))
        self._set_entry(self.from_entry, payload.get("from_number", ""))
        self._set_entry(self.sid_entry, payload.get("account_sid", ""))
        self._set_entry(self.token_entry, payload.get("auth_token", ""))
        if payload.get("concurrent"):
            self.concurrent_var.set(str(payload["concurrent"]))
        if payload.get("total_calls"):
            self.total_var.set(str(payload["total_calls"]))
        if payload.get("ring_seconds"):
            self.ring_var.set(str(payload["ring_seconds"]))

    @staticmethod
    def _set_entry(entry: ttk.Entry, value: str) -> None:
        entry.delete(0, "end")
        entry.insert(0, value)

    def _on_close(self) -> None:
        if self._worker and self._worker.is_alive():
            if not messagebox.askyesno(
                "Quit",
                "A test is still running. Quit anyway?",
                parent=self,
            ):
                return
            self._cancel.set()
        self.destroy()


def main() -> None:
    app = StressTestApp()
    app.mainloop()


if __name__ == "__main__":
    main()
