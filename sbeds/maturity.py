"""
Paper 03 scaffolding — Field-Defined Infrastructure stoppable maturity matrix.

Higher tiers are allowed only after veto tests pass.
Remaining at Level 0/1 can be globally optimal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List


class MaturityLevel(IntEnum):
    L0_MULTI_CONDUCTOR = 0
    L1_CONDUCTOR_MINIMIZED_BUS = 1
    L2_LOCAL_SURFACE_WAVE = 2
    L3_ADAPTIVE_BOUNDARY_NODES = 3
    L4_SPATIAL_MODE_NETWORK = 4
    L5_AUTONOMOUS_FIELD_INFRA = 5


@dataclass
class StoppableMaturityGate:
    """
    Decision gate: propose a target level, list veto results.
    Any failed veto forces stay/downscale.
    """

    current: MaturityLevel
    proposed: MaturityLevel
    veto_results: Dict[str, bool] = field(default_factory=dict)
    # veto_results value True = PASSED (safe to proceed), False = FAILED

    def all_vetoes_passed(self) -> bool:
        if not self.veto_results:
            return False
        return all(self.veto_results.values())

    def decide(self) -> MaturityLevel:
        if self.proposed <= self.current:
            return self.proposed
        if self.all_vetoes_passed():
            return self.proposed
        return self.current

    def rationale(self) -> str:
        decision = self.decide()
        if decision == self.proposed and self.proposed > self.current:
            return (
                f"Advance {self.current.name} -> {decision.name}: "
                "all pre-registered vetoes passed."
            )
        if decision < self.proposed:
            failed = [k for k, v in self.veto_results.items() if not v]
            return (
                f"Hold/downscale at {decision.name}: veto failures={failed}. "
                "Stoppable maturity forbids obligatory upward evolution."
            )
        return f"Remain at {decision.name}."


DEFAULT_VETO_KEYS: List[str] = [
    "emc_exposure_limits",
    "reliability_budget",
    "modal_mismatch_detectable",
    "physical_redundancy_if_adaptive",
]
