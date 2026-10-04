"""
Paper 04 scaffolding — Boundary-Defined Power Integrity.

Core geometric proxy:
  L_loop = L_pwr + L_gnd - 2 * M_pg
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


def loop_inductance(l_pwr: float, l_gnd: float, m_pg: float) -> float:
    """
    Effective loop inductance for a power/ground via pair (H).

    Args:
        l_pwr: partial inductance of power via path
        l_gnd: partial inductance of ground via path
        m_pg: mutual inductance between the pair
    """
    if min(l_pwr, l_gnd) < 0:
        raise ValueError("partial inductances must be non-negative")
    return float(l_pwr + l_gnd - 2.0 * m_pg)


@dataclass
class AblationPlan:
    """
    Pre-registered single-variable ablation groups (Paper 04).
    Groups are names only; you attach measurement URIs later.
    """

    groups: List[str] = field(
        default_factory=lambda: [
            "via_pair_geometry",
            "plane_perforation",
            "nonperiodic_boundary",
            "decap_count_held_constant",
        ]
    )
    deembedding_standard: str = "IEEE Std 370"
    results: Dict[str, Optional[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for g in self.groups:
            self.results.setdefault(g, None)

    def mark(self, group: str, artifact_uri: str) -> None:
        if group not in self.results:
            raise KeyError(group)
        self.results[group] = artifact_uri

    def coverage(self) -> float:
        done = sum(1 for v in self.results.values() if v)
        return done / max(len(self.results), 1)
