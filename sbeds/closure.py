"""
Paper 01 scaffolding — Relational Closure / Mode-First Power Transmission.

Operationalizes:
  R = (N_c, V_medium, V_env, Q_tune, N_converter)
  C_rel = (C_B, C_M, C_R, C_T)  — non-collapsible metric vector

This module never collapses C_rel into a single "coherence score".
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Mapping


@dataclass(frozen=True)
class ClosureResourceVector:
    """Closure Resource Vector R from Paper 01."""

    n_conductors: float
    v_medium: float
    v_env: float
    q_tune: float
    n_converter: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "N_c": float(self.n_conductors),
            "V_medium": float(self.v_medium),
            "V_env": float(self.v_env),
            "Q_tune": float(self.q_tune),
            "N_converter": float(self.n_converter),
        }

    def total_resource_mass(self) -> float:
        """Sum of declared resources (diagnostic only, not an optimality score)."""
        d = self.as_dict()
        return sum(d.values())


@dataclass(frozen=True)
class RelationalClosureMetric:
    """
    Relational Closure Metric Vector C_rel = (C_B, C_M, C_R, C_T).

    Components are independently reportable in [0, 1] by convention when
    the user supplies normalized proxies. This toolkit does not invent
    physical measurements — you plug measured/simulated proxies in.
    """

    c_b: float  # boundary modal overlap
    c_m: float  # modal confinement
    c_r: float  # total-current loop continuity
    c_t: float  # terminal conversion efficiency

    def as_dict(self) -> Dict[str, float]:
        return {
            "C_B": float(self.c_b),
            "C_M": float(self.c_m),
            "C_R": float(self.c_r),
            "C_T": float(self.c_t),
        }

    def validate_range(self) -> None:
        for k, v in self.as_dict().items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"{k}={v} outside recommended [0,1] proxy range")


def score_c_rel(metric: RelationalClosureMetric) -> Mapping[str, float]:
    """
    Return the vector itself. Explicitly refuses scalar collapse.

    Returns:
        Mapping with keys C_B, C_M, C_R, C_T.
    """
    metric.validate_range()
    return metric.as_dict()


def compare_architectures(
    baseline: RelationalClosureMetric,
    candidate: RelationalClosureMetric,
) -> Dict[str, float]:
    """Component-wise delta (candidate - baseline). Never a weighted scalar."""
    b, c = baseline.as_dict(), candidate.as_dict()
    return {k: c[k] - b[k] for k in b}


def blank_benchmark_row() -> Dict[str, object]:
    """Empty comparative-protocol row for lab notebooks / TR-1 reporting."""
    return {
        "architecture": "",
        "R": asdict(
            ClosureResourceVector(
                n_conductors=0.0,
                v_medium=0.0,
                v_env=0.0,
                q_tune=0.0,
                n_converter=0.0,
            )
        ),
        "C_rel": {"C_B": None, "C_M": None, "C_R": None, "C_T": None},
        "notes": "Fill with measured/simulated proxies. Do not invent numbers.",
        "evidence_tier": "[A]|[B]|[C]|[D]",
    }
