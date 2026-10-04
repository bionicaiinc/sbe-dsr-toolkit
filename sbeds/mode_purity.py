"""
Paper 05 scaffolding — Mode Purity Beyond Conductor Count.

Eight-dimensional metric vector M (non-collapsible) and survival envelope
with mandatory retreat to shielded differential when radiation leaks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping


@dataclass(frozen=True)
class ModePurityVector:
    modal_power_ratio: float
    radiation_leakage: float
    insertion_loss: float
    return_loss: float
    crosstalk: float
    mode_conversion: float
    fabrication_sensitivity: float
    ber: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "modal_power_ratio": float(self.modal_power_ratio),
            "radiation_leakage": float(self.radiation_leakage),
            "insertion_loss": float(self.insertion_loss),
            "return_loss": float(self.return_loss),
            "crosstalk": float(self.crosstalk),
            "mode_conversion": float(self.mode_conversion),
            "fabrication_sensitivity": float(self.fabrication_sensitivity),
            "ber": float(self.ber),
        }


@dataclass(frozen=True)
class SurvivalEnvelope:
    """Packaging-scale envelope defaults from Paper 05 (conceptual bounds)."""

    length_mm_min: float = 5.0
    length_mm_max: float = 30.0
    max_radiation_leakage: float = 0.05  # normalized proxy; user-calibrate
    require_modulation_declared: bool = True


def evaluate_retreat(
    length_mm: float,
    metric: ModePurityVector,
    envelope: SurvivalEnvelope | None = None,
    modulation_declared: bool = False,
) -> Mapping[str, object]:
    """
    Return a decision record. If radiation leakage exceeds threshold or
    length is outside envelope, mandate fallback to shielded differential.
    """
    env = envelope or SurvivalEnvelope()
    reasons = []
    if not (env.length_mm_min <= length_mm <= env.length_mm_max):
        reasons.append("length_outside_5_30mm_window")
    if metric.radiation_leakage > env.max_radiation_leakage:
        reasons.append("radiation_leakage_exceeds_threshold")
    if env.require_modulation_declared and not modulation_declared:
        reasons.append("modulation_ber_budget_not_declared")

    retreat = bool(reasons)
    return {
        "retreat_to_shielded_differential": retreat,
        "reasons": reasons,
        "metric_vector": metric.as_dict(),
        "doctrine": "Reject return-less / ground-less claims; model return via displacement/reference currents.",
    }
