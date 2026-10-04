"""
Paper 06 scaffolding — Computational Substrates / PCNO-EDA stage gates.

PCNO-EDA is an upstream inverse-synthesis accelerator and screening layer.
It does NOT replace commercial DRC/LVS/timing/PI sign-off.
Stage 3 requires physical redundancy — software-only healing of open breaks
is rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Mapping


class PCNOStage(IntEnum):
    STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS = 1
    STAGE2_LOCAL_TUNABLE_IMPEDANCE = 2
    STAGE3_ACTIVE_SENSING_RECONFIGURATION = 3


@dataclass(frozen=True)
class StageGateDecision:
    authorized_stage: PCNOStage
    requested_stage: PCNOStage
    allowed: bool
    reasons: tuple[str, ...]


def evaluate_stage_gate(
    requested: PCNOStage,
    *,
    has_pareto_artifacts: bool,
    tuning_faster_than_transient: bool = False,
    injects_emi: bool = False,
    physical_redundancy_present: bool = False,
    claims_replace_signoff_eda: bool = False,
) -> StageGateDecision:
    """
    Authorize the highest stage whose prerequisites hold, then compare
    to the requested stage.
    """
    reasons: List[str] = []

    if claims_replace_signoff_eda:
        return StageGateDecision(
            PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS,
            requested,
            False,
            ("forbidden_claim_replaces_commercial_signoff",),
        )

    authorized = PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS
    if not has_pareto_artifacts:
        reasons.append("stage1_incomplete_without_pareto_or_yield_artifacts")
        # Stage 1 may still be *requested* as the working endpoint, but
        # "complete" authorization requires artifacts.
        stage1_complete = False
    else:
        stage1_complete = True
        reasons = [r for r in reasons if not r.startswith("stage1_")]

    if stage1_complete:
        authorized = PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS

    stage2_ok = (
        stage1_complete
        and tuning_faster_than_transient
        and not injects_emi
    )
    if requested >= PCNOStage.STAGE2_LOCAL_TUNABLE_IMPEDANCE and not stage2_ok:
        if not tuning_faster_than_transient:
            reasons.append("stage2_requires_tuning_faster_than_transient")
        if injects_emi:
            reasons.append("stage2_blocked_while_emi_injection_true")
    if stage2_ok:
        authorized = PCNOStage.STAGE2_LOCAL_TUNABLE_IMPEDANCE

    stage3_ok = stage2_ok and physical_redundancy_present
    if requested >= PCNOStage.STAGE3_ACTIVE_SENSING_RECONFIGURATION and not physical_redundancy_present:
        reasons.append("stage3_requires_physical_redundancy_path")
    if stage3_ok:
        authorized = PCNOStage.STAGE3_ACTIVE_SENSING_RECONFIGURATION

    if requested == PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS:
        allowed = stage1_complete
        if allowed:
            reasons = tuple(r for r in reasons if not r.startswith("stage2") and not r.startswith("stage3"))
        return StageGateDecision(authorized if stage1_complete else PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS, requested, allowed, tuple(reasons))

    allowed = authorized >= requested
    return StageGateDecision(authorized, requested, allowed, tuple(reasons))


def signoff_boundary_statement() -> Mapping[str, str]:
    return {
        "role": "upstream_inverse_synthesis_accelerator_and_screening_layer",
        "does_not_replace": "DRC / LVS / timing / final PI sign-off EDA",
        "stage3_doctrine": "physical redundancy required; reject software-only healing of open circuits",
    }
