#!/usr/bin/env python3
"""Validate TaskForge durable state and terminal evidence with no dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


RUN_STATES = {
    "AWAITING_CONFIRMATION",
    "RUNNING",
    "DONE",
    "PARTIAL",
    "NEEDS_APPROVAL",
    "BLOCKED",
}
CRITERION_STATES = {"PENDING", "PASS", "FAIL"}
REQUIRED_HEADINGS_EN = (
    "## 1. Identity and rigor",
    "## 2. Goal and observable outcome",
    "## 5. Constraints and protected invariants",
    "## 6. Acceptance and evidence",
    "## 7. Permissions and approval gates",
    "## 8. Loop control",
    "## 11. Confirmation and amendments",
)
REQUIRED_HEADINGS_ZH = (
    "## 1. 任务身份与严谨度",
    "## 2. 目标与可观察结果",
    "## 5. 约束与受保护内容",
    "## 6. 验收标准与证据",
    "## 7. 权限与审批闸门",
    "## 8. 循环控制",
    "## 11. 确认与修订记录",
)
REQUIRED_FILES = (
    "context.md", "glossary.md", "decisions.md", "contract.md",
    "state.json", "iterations.md", "completion.md",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def positive_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def validate(run_dir: Path) -> list[str]:
    errors: list[str] = []
    contract_path = run_dir / "contract.md"
    state_path = run_dir / "state.json"
    for name in REQUIRED_FILES:
        required = run_dir / name
        if not required.is_file():
            errors.append(f"missing required file: {required.name}")
    if errors:
        return errors

    contract = contract_path.read_text(encoding="utf-8")
    if not all(heading in contract for heading in REQUIRED_HEADINGS_EN) and not all(
        heading in contract for heading in REQUIRED_HEADINGS_ZH
    ):
        errors.append("contract.md must contain the complete English or Chinese heading set")

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return errors + [f"state.json is unreadable: {exc}"]
    if not isinstance(state, dict):
        return errors + ["state.json root must be an object"]

    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(state.get("run_id"), str) or not state["run_id"].strip():
        errors.append("run_id must be a non-empty string")
    mode = state.get("mode")
    if mode != "DEEP":
        errors.append("durable state mode must be DEEP")
    if state.get("document_language") not in {"en", "zh-CN"}:
        errors.append("document_language must be en or zh-CN")
    status = state.get("status")
    if status not in RUN_STATES:
        errors.append("status is invalid")
    expected_hash = sha256_text(contract)
    if state.get("contract_sha256") != expected_hash:
        errors.append("contract_sha256 does not match contract.md")

    limits = state.get("limits")
    if not isinstance(limits, dict):
        errors.append("limits must be an object")
        limits = {}
    for key in ("max_iterations", "max_failures_per_criterion", "max_identical_fingerprints"):
        if not positive_integer(limits.get(key)):
            errors.append(f"limits.{key} must be a positive integer")
    for key in ("wall_clock_seconds", "token_budget", "monetary_budget"):
        value = limits.get(key)
        if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0):
            errors.append(f"limits.{key} must be null or a positive number")

    iteration = state.get("iteration")
    if not isinstance(iteration, int) or isinstance(iteration, bool) or iteration < 0:
        errors.append("iteration must be a non-negative integer")
    elif positive_integer(limits.get("max_iterations")) and iteration > limits["max_iterations"]:
        errors.append("iteration exceeds max_iterations")

    criteria = state.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("criteria must contain at least one criterion")
        criteria = []
    seen: set[str] = set()
    for index, criterion in enumerate(criteria):
        label = f"criteria[{index}]"
        if not isinstance(criterion, dict):
            errors.append(f"{label} must be an object")
            continue
        criterion_id = criterion.get("id")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
        elif criterion_id in seen:
            errors.append(f"duplicate criterion id: {criterion_id}")
        else:
            seen.add(criterion_id)
        criterion_status = criterion.get("status")
        if criterion_status not in CRITERION_STATES:
            errors.append(f"{label}.status is invalid")
        if not isinstance(criterion.get("verifier"), str) or not criterion["verifier"].strip():
            errors.append(f"{label}.verifier must be non-empty")
        evidence = criterion.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"{label}.evidence must be an array")
        elif criterion_status == "PASS" and not evidence:
            errors.append(f"{label} is PASS without evidence")
        failure_count = criterion.get("failure_count")
        if not isinstance(failure_count, int) or isinstance(failure_count, bool) or failure_count < 0:
            errors.append(f"{label}.failure_count must be a non-negative integer")
        elif (
            status == "RUNNING"
            and positive_integer(limits.get("max_failures_per_criterion"))
            and failure_count >= limits["max_failures_per_criterion"]
        ):
            errors.append(f"{label} reached its failure limit while status is RUNNING")

    fingerprints = state.get("fingerprints")
    if not isinstance(fingerprints, list) or any(not isinstance(item, str) or not item for item in fingerprints):
        errors.append("fingerprints must be an array of non-empty strings")
        fingerprints = []
    threshold = limits.get("max_identical_fingerprints")
    if status == "RUNNING" and positive_integer(threshold) and len(fingerprints) >= threshold:
        tail = fingerprints[-threshold:]
        if len(set(tail)) == 1:
            errors.append("no-progress threshold reached while status is RUNNING")

    protection = state.get("verifier_protection")
    if not isinstance(protection, dict):
        errors.append("verifier_protection must be an object")
        protection = {}
    if mode == "DEEP" and any(
        value is not None for value in (
            limits.get("token_budget"),
            limits.get("monetary_budget"),
        )
    ):
        if not isinstance(protection.get("method"), str) or not protection["method"].strip():
            errors.append("budgeted DEEP mode requires verifier_protection.method")
        if not isinstance(protection.get("paths"), list) or not protection["paths"]:
            errors.append("budgeted DEEP mode requires protected verifier paths")

    approvals = state.get("approvals")
    if not isinstance(approvals, list):
        errors.append("approvals must be an array")
        approvals = []
    if status == "DONE":
        if not criteria or any(item.get("status") != "PASS" for item in criteria if isinstance(item, dict)):
            errors.append("DONE requires every criterion to be PASS")
        for index, approval in enumerate(approvals):
            if not isinstance(approval, dict) or approval.get("required") is not True:
                continue
            if approval.get("status") != "APPROVED" or not approval.get("evidence"):
                errors.append(f"approvals[{index}] is required but lacks approval evidence")

    if not isinstance(state.get("updated_at"), str) or not state["updated_at"].strip():
        errors.append("updated_at must be a non-empty string")
    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        run_dir = Path(temporary)
        contract = "\n".join(REQUIRED_HEADINGS_EN) + "\n"
        for name in ("context.md", "glossary.md", "decisions.md"):
            (run_dir / name).write_text(f"# {name}\n", encoding="utf-8")
        (run_dir / "contract.md").write_text(contract, encoding="utf-8")
        (run_dir / "iterations.md").write_text("# Iterations\n", encoding="utf-8")
        (run_dir / "completion.md").write_text("# Completion\n", encoding="utf-8")
        state = {
            "schema_version": 1,
            "run_id": "self-test",
            "mode": "DEEP",
            "document_language": "en",
            "status": "RUNNING",
            "contract_sha256": sha256_text(contract),
            "iteration": 1,
            "limits": {
                "max_iterations": 4,
                "max_failures_per_criterion": 2,
                "max_identical_fingerprints": 2,
                "wall_clock_seconds": 60,
                "token_budget": None,
                "monetary_budget": None,
            },
            "criteria": [{
                "id": "AC-1",
                "status": "PASS",
                "verifier": "self-test",
                "evidence": ["fixture"],
                "failure_count": 0,
            }],
            "fingerprints": ["one"],
            "verifier_protection": {"method": "", "paths": [], "baseline_sha256": ""},
            "approvals": [],
            "updated_at": "2026-08-11T00:00:00Z",
        }
        (run_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
        if validate(run_dir):
            print("self-test failed: valid fixture was rejected")
            return 1
        state["status"] = "DONE"
        state["criteria"][0]["evidence"] = []
        (run_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
        if not validate(run_dir):
            print("self-test failed: invalid fixture was accepted")
            return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a TaskForge run directory.")
    parser.add_argument("run_dir", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.run_dir is None:
        parser.error("run_dir is required unless --self-test is used")
    errors = validate(args.run_dir.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("TaskForge run validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
