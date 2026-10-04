"""
run_local_demo.py
=================
Fully self-contained, OFFLINE demonstration of the SBE/DSR Toolkit.

No API keys. No network. No lab instruments. Synthetic fixtures only —
teaching aids that show how the interfaces behave, NOT claims about
measured hardware.

Run from the repository root:

    python examples/run_local_demo.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbeds.closure import (
    ClosureResourceVector,
    RelationalClosureMetric,
    compare_architectures,
    score_c_rel,
)
from sbeds.receptivity import ActualizationTarget, TerminalActualizationMatrix
from sbeds.maturity import MaturityLevel, StoppableMaturityGate
from sbeds.pdn_boundary import AblationPlan, loop_inductance
from sbeds.mode_purity import ModePurityVector, evaluate_retreat
from sbeds.pcno_gates import PCNOStage, evaluate_stage_gate, signoff_boundary_statement


def main() -> None:
    print("=" * 70)
    print(" SBE/DSR Toolkit — offline demo (synthetic fixtures, no network)")
    print("=" * 70)

    # --- Paper 01 ---------------------------------------------------------
    print("\n[01] Relational closure resources & C_rel vector")
    two_wire = ClosureResourceVector(2, 0.0, 0.0, 0.0, 0.0)
    goubau = ClosureResourceVector(1, 1.0, 0.0, 0.0, 1.0)
    print(f"  two-wire R mass = {two_wire.total_resource_mass():.1f}")
    print(f"  goubau-like R   = {goubau.as_dict()}")

    baseline = RelationalClosureMetric(0.70, 0.65, 0.90, 0.80)
    candidate = RelationalClosureMetric(0.72, 0.80, 0.88, 0.78)
    print(f"  C_rel baseline  = {score_c_rel(baseline)}")
    print(f"  delta (cand-base) = {compare_architectures(baseline, candidate)}")
    print("  (vector kept; no scalar 'coherence score')")

    # --- Paper 02 ---------------------------------------------------------
    print("\n[02] Structural receptivity actualization matrix")
    matrix = TerminalActualizationMatrix(mode_labels=["guided_TE", "surface_wave"])
    matrix.set_proxy("guided_TE", ActualizationTarget.DC, 0.82)
    matrix.set_proxy("guided_TE", ActualizationTarget.HEAT, 0.15)
    print(f"  completeness = {matrix.completeness():.2f}")
    print(f"  dominant(guided_TE) = {matrix.dominant_target('guided_TE')}")

    # --- Paper 03 ---------------------------------------------------------
    print("\n[03] Stoppable maturity gate")
    gate = StoppableMaturityGate(
        current=MaturityLevel.L1_CONDUCTOR_MINIMIZED_BUS,
        proposed=MaturityLevel.L3_ADAPTIVE_BOUNDARY_NODES,
        veto_results={
            "emc_exposure_limits": True,
            "reliability_budget": False,
            "modal_mismatch_detectable": True,
            "physical_redundancy_if_adaptive": False,
        },
    )
    print(f"  decision = {gate.decide().name}")
    print(f"  rationale: {gate.rationale()}")

    # --- Paper 04 ---------------------------------------------------------
    print("\n[04] Boundary-defined PDN loop inductance")
    l_loop = loop_inductance(l_pwr=1.2e-9, l_gnd=1.1e-9, m_pg=0.85e-9)
    print(f"  L_loop = {l_loop*1e9:.3f} nH")
    plan = AblationPlan()
    plan.mark("via_pair_geometry", "file://synthetic/via_pair_ablation.md")
    print(f"  ablation coverage = {plan.coverage():.2f} ({plan.deembedding_standard})")

    # --- Paper 05 ---------------------------------------------------------
    print("\n[05] Mode-purity survival envelope / retreat rule")
    ok_metric = ModePurityVector(0.92, 0.02, 3.0, 15.0, 0.05, 0.01, 0.10, 1e-6)
    leaky = ModePurityVector(0.70, 0.12, 5.0, 10.0, 0.08, 0.04, 0.20, 1e-4)
    print(f"  ok channel  -> {evaluate_retreat(12.0, ok_metric, modulation_declared=True)}")
    print(f"  leaky       -> {evaluate_retreat(12.0, leaky, modulation_declared=True)}")

    # --- Paper 06 ---------------------------------------------------------
    print("\n[06] PCNO-EDA stage gates")
    print(f"  boundary: {signoff_boundary_statement()}")
    d1 = evaluate_stage_gate(
        PCNOStage.STAGE1_PASSIVE_MULTIPHYSICS_SYNTHESIS,
        has_pareto_artifacts=True,
    )
    d3 = evaluate_stage_gate(
        PCNOStage.STAGE3_ACTIVE_SENSING_RECONFIGURATION,
        has_pareto_artifacts=True,
        tuning_faster_than_transient=True,
        injects_emi=False,
        physical_redundancy_present=False,
    )
    print(f"  stage1 allowed={d1.allowed} authorized={d1.authorized_stage.name}")
    print(f"  stage3 allowed={d3.allowed} reasons={d3.reasons}")

    print("\n" + "-" * 70)
    print(" How to read this")
    print("-" * 70)
    print(
        " Numbers above come from synthetic fixtures so the APIs are visible.\n"
        " Replace fixtures with measured/simulated proxies from your lab or\n"
        " solver. Do not cite demo numbers as experimental results.\n"
        " Companion papers: Zenodo SBE/DSR programme (see CITATION.cff)."
    )
    print("=" * 70)


if __name__ == "__main__":
    main()
