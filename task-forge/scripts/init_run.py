#!/usr/bin/env python3
"""Create a durable TaskForge run directory without overwriting existing work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize .taskforge/<run-id>.")
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--mode", choices=("STANDARD", "STRICT"), default="STANDARD")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    run_dir = workspace / ".taskforge" / args.run_id
    if run_dir.exists():
        parser.error(f"run directory already exists: {run_dir}")

    references = Path(__file__).resolve().parent.parent / "references"
    run_dir.mkdir(parents=True)
    contract = (references / "task-contract.md").read_text(encoding="utf-8")
    contract = contract.replace("- Run ID:", f"- Run ID: {args.run_id}", 1)
    contract = contract.replace(
        "- Mode: `LITE`, `STANDARD`, or `STRICT`",
        f"- Mode: `{args.mode}`",
        1,
    )
    atomic_write(run_dir / "contract.md", contract)
    atomic_write(
        run_dir / "iterations.md",
        (references / "iteration-log.md").read_text(encoding="utf-8"),
    )
    atomic_write(
        run_dir / "completion.md",
        (references / "completion-report.md").read_text(encoding="utf-8"),
    )

    contract_hash = hashlib.sha256(contract.encode("utf-8")).hexdigest()
    state = {
        "schema_version": 1,
        "run_id": args.run_id,
        "mode": args.mode,
        "status": "AWAITING_CONFIRMATION",
        "contract_sha256": contract_hash,
        "iteration": 0,
        "limits": {
            "max_iterations": 12,
            "max_failures_per_criterion": 3,
            "max_identical_fingerprints": 2,
            "wall_clock_seconds": 3600,
            "token_budget": None,
            "monetary_budget": None,
        },
        "criteria": [],
        "fingerprints": [],
        "verifier_protection": {
            "method": "",
            "paths": [],
            "baseline_sha256": "",
        },
        "approvals": [],
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    atomic_write(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
