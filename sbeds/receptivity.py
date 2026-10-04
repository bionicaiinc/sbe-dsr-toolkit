"""
Paper 02 scaffolding — Structural Receptivity / Electromagnetic Actualization.

Supports reverse-design bookkeeping:
  1) choose organized consequence
  2) declare terminal constraint field properties
  3) match incident mode + feedback plan
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ActualizationTarget(str, Enum):
    DC = "unidirectional_dc"
    HEAT = "reversible_or_irreversible_heat"
    MOTION = "coherent_mechanical_displacement"
    INFO = "repeatable_information_state"


@dataclass
class TerminalActualizationMatrix:
    """
    Intentionally sparse matrix: rows = incident-mode labels,
    columns = ActualizationTarget. Cells hold None until measured.
    """

    mode_labels: List[str]
    cells: Dict[str, Dict[str, Optional[float]]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for m in self.mode_labels:
            self.cells.setdefault(
                m, {t.value: None for t in ActualizationTarget}
            )

    def set_proxy(self, mode: str, target: ActualizationTarget, value: float) -> None:
        if mode not in self.cells:
            raise KeyError(f"unknown mode label: {mode}")
        if not (0.0 <= value <= 1.0):
            raise ValueError("proxy values should be normalized to [0,1] when used")
        self.cells[mode][target.value] = float(value)

    def dominant_target(self, mode: str) -> Optional[ActualizationTarget]:
        row = self.cells[mode]
        filled = {k: v for k, v in row.items() if v is not None}
        if not filled:
            return None
        best = max(filled, key=filled.get)
        return ActualizationTarget(best)

    def completeness(self) -> float:
        total = len(self.mode_labels) * len(ActualizationTarget)
        filled = sum(
            1
            for m in self.mode_labels
            for v in self.cells[m].values()
            if v is not None
        )
        return filled / max(total, 1)


def reverse_design_checklist(
    target: ActualizationTarget,
    constraint_notes: str,
    incident_mode: str,
) -> Dict[str, str]:
    """Paper 02 reverse-design sequence as a fillable checklist."""
    return {
        "step_1_organized_consequence": target.value,
        "step_2_terminal_constraint_field": constraint_notes,
        "step_3_incident_mode_and_feedback": incident_mode,
        "status": "scaffold-only; populate with lab/EM design artifacts",
    }
