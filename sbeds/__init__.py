"""
SBE/DSR Toolkit — measurement and decision scaffolding for the
Structure-Before-Energy / Dynamic Structural Realism programme.

This package operationalizes *interfaces* from the six Zenodo preprints:
closure metrics, receptivity matrices, stoppable maturity, PDN loop
inductance, mode-purity survival envelopes, and PCNO stage gates.

It does **not** replace Maxwell solvers, lab instruments, or commercial EDA.
"""

from .closure import ClosureResourceVector, RelationalClosureMetric, score_c_rel
from .receptivity import ActualizationTarget, TerminalActualizationMatrix
from .maturity import MaturityLevel, StoppableMaturityGate
from .pdn_boundary import loop_inductance, AblationPlan
from .mode_purity import ModePurityVector, SurvivalEnvelope, evaluate_retreat
from .pcno_gates import PCNOStage, StageGateDecision, evaluate_stage_gate

__version__ = "0.1.0"
__all__ = [
    "ClosureResourceVector",
    "RelationalClosureMetric",
    "score_c_rel",
    "ActualizationTarget",
    "TerminalActualizationMatrix",
    "MaturityLevel",
    "StoppableMaturityGate",
    "loop_inductance",
    "AblationPlan",
    "ModePurityVector",
    "SurvivalEnvelope",
    "evaluate_retreat",
    "PCNOStage",
    "StageGateDecision",
    "evaluate_stage_gate",
]
