"""Semantic reference implementation for TPTA.

This module intentionally does not rank options or make human decisions.
It enforces a small set of epistemic and governance invariants.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List


class Posture(str, Enum):
    READY_FOR_HUMAN_DECISION = "READY_FOR_HUMAN_DECISION"
    HOLD = "HOLD"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


VALID_GATE_STATUSES = {"PASS", "FAIL", "UNKNOWN"}
VALID_EVIDENCE_STATUSES = {"SUPPORTED", "CONTRADICTED", "UNKNOWN"}
VALID_VALIDATION_STATUSES = {"PASS", "PARTIAL", "FAIL", "UNKNOWN"}
VALID_INVERSION_STATUSES = {"PROPOSED", "SUPPORTED", "REJECTED", "UNKNOWN"}


def validate_case(case: Dict[str, Any]) -> List[str]:
    """Return semantic validation errors without mutating *case*."""
    errors: List[str] = []

    for required in ("id", "condition", "purpose", "evidence", "gates"):
        if required not in case:
            errors.append(f"missing required field: {required}")

    evidence = case.get("evidence", [])
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
        evidence = []

    evidence_by_id: Dict[str, Dict[str, Any]] = {}
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{index}] must be an object")
            continue
        evidence_id = item.get("id")
        if not evidence_id:
            errors.append(f"evidence[{index}] missing id")
        elif evidence_id in evidence_by_id:
            errors.append(f"duplicate evidence id: {evidence_id}")
        else:
            evidence_by_id[evidence_id] = item
        if item.get("status") not in VALID_EVIDENCE_STATUSES:
            errors.append(f"evidence[{index}] invalid status: {item.get('status')!r}")

    inversion = case.get("inversion")
    if inversion is not None:
        if not isinstance(inversion, dict):
            errors.append("inversion must be an object or null")
        else:
            status = inversion.get("status")
            if status not in VALID_INVERSION_STATUSES:
                errors.append(f"inversion invalid status: {status!r}")
            refs = inversion.get("evidence_ids", [])
            if not isinstance(refs, list) or not refs:
                errors.append("inversion requires at least one evidence reference")
                refs = []
            supported_refs = 0
            for ref in refs:
                if ref not in evidence_by_id:
                    errors.append(f"inversion references unknown evidence id: {ref}")
                elif evidence_by_id[ref].get("status") == "SUPPORTED":
                    supported_refs += 1
            for ref in inversion.get("counterevidence_ids", []):
                if ref not in evidence_by_id:
                    errors.append(f"inversion references unknown counterevidence id: {ref}")
            if not inversion.get("falsification_test"):
                errors.append("inversion requires a falsification_test")
            if status == "SUPPORTED" and supported_refs == 0:
                errors.append("SUPPORTED inversion requires at least one SUPPORTED evidence reference")

    validations = case.get("validations", [])
    if not isinstance(validations, list):
        errors.append("validations must be a list")
        validations = []
    validation_ids = set()
    for index, item in enumerate(validations):
        if not isinstance(item, dict):
            errors.append(f"validations[{index}] must be an object")
            continue
        validation_id = item.get("id")
        if not validation_id:
            errors.append(f"validations[{index}] missing id")
        elif validation_id in validation_ids:
            errors.append(f"duplicate validation id: {validation_id}")
        else:
            validation_ids.add(validation_id)
        status = item.get("status")
        if status not in VALID_VALIDATION_STATUSES:
            errors.append(f"validations[{index}] invalid status: {status!r}")
        refs = item.get("evidence_ids", [])
        for ref in refs:
            if ref not in evidence_by_id:
                errors.append(f"validations[{index}] references unknown evidence id: {ref}")
        if status in {"PASS", "PARTIAL", "FAIL"} and not refs:
            errors.append(f"validations[{index}] status {status} requires evidence references")

    gates = case.get("gates", [])
    if not isinstance(gates, list):
        errors.append("gates must be a list")
        gates = []

    gate_ids = set()
    required_count = 0
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"gates[{index}] must be an object")
            continue
        gate_id = gate.get("id")
        if not gate_id:
            errors.append(f"gates[{index}] missing id")
        elif gate_id in gate_ids:
            errors.append(f"duplicate gate id: {gate_id}")
        else:
            gate_ids.add(gate_id)
        if gate.get("status") not in VALID_GATE_STATUSES:
            errors.append(f"gates[{index}] invalid status: {gate.get('status')!r}")
        if not isinstance(gate.get("required"), bool):
            errors.append(f"gates[{index}] required must be boolean")
        elif gate["required"]:
            required_count += 1

    if required_count == 0:
        errors.append("at least one gate must be required")

    return errors


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate deterministic system posture without inventing authority."""
    errors = validate_case(case)
    if errors:
        raise ValueError("; ".join(errors))

    required_gates = [g for g in case["gates"] if g["required"]]
    failed = [g["id"] for g in required_gates if g["status"] == "FAIL"]
    unknown = [g["id"] for g in required_gates if g["status"] == "UNKNOWN"]

    if failed:
        posture = Posture.HOLD
    elif unknown:
        posture = Posture.INSUFFICIENT_EVIDENCE
    else:
        posture = Posture.READY_FOR_HUMAN_DECISION

    return {
        "case_id": case["id"],
        "comparative_result": case.get("comparative_result"),
        "system_posture": posture.value,
        "controlling_issues": {
            "failed_gates": failed,
            "unknown_gates": unknown,
        },
        "human_decision": case.get("human_decision"),
    }
