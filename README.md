# SBE/DSR Toolkit

**Measurement and decision scaffolding for Structure-Before-Energy /
Dynamic Structural Realism engineering interfaces.**

[![Status](https://img.shields.io/badge/status-early--prototype-orange.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()

> An open, work-in-progress toolkit that turns the six SBE/DSR Zenodo
> preprints into *callable interfaces*: closure metrics, receptivity
> matrices, stoppable maturity gates, PDN loop inductance, mode-purity
> survival envelopes, and PCNO-EDA stage gates.

---

## What this is (and what it isn't)

The companion papers propose falsifiable engineering interfaces. This
repository ships the **scaffolding** so those interfaces can be filled
with real measurements or simulations later.

| This IS | This is NOT |
|---|---|
| Early-prototype Python APIs | A finished EM or EDA product |
| Offline demo with synthetic fixtures | Claimed hardware performance data |
| Non-collapsible metric vectors | A single “coherence score” |
| Stage / maturity stop rules | Permission to skip lab vetoes |

**This is a research prototype, not a validation report.** If you need
full-wave solvers, measured S-parameters, or commercial sign-off EDA,
bring your own — this toolkit will not invent them.

Product philosophy matches the earlier
[I-Score Toolkit](https://github.com/bionicaiinc/structural-density)
(LLM consistency scaffolding for the Structure-Before-Energy line of work).

---

## Modules ↔ papers

| Module | Paper |
|---|---|
| `sbeds.closure` | 01 Relational Closure / Mode-First Power Transmission |
| `sbeds.receptivity` | 02 Structural Receptivity / Electromagnetic Actualization |
| `sbeds.maturity` | 03 Field-Defined Infrastructure |
| `sbeds.pdn_boundary` | 04 Boundary-Defined Power Integrity |
| `sbeds.mode_purity` | 05 Mode Purity Beyond Conductor Count |
| `sbeds.pcno_gates` | 06 Computational Substrates / PCNO-EDA |

---

## Install

```bash
git clone https://github.com/bionicaiinc/sbe-dsr-toolkit.git
cd sbe-dsr-toolkit
pip install -r requirements.txt
```

`numpy` is listed for future numerical helpers; current v0.1 APIs are
stdlib + dataclasses.

## Quick start (offline)

```bash
python examples/run_local_demo.py
```

No API key, no network. The demo plugs **synthetic fixtures** into the
real module functions so you can see retreat rules, maturity vetoes, and
stage gates fire.

---

## Epistemic guardrails

- Do not equate ontological `P_sem = I_struct ∗ v_sem` with Watts / Hz / FLOPS.
- Do not collapse `C_rel` or mode-purity vector `M` into one scalar score.
- Reject “return-less / ground-less” interconnect claims.
- PCNO-EDA does **not** replace DRC/LVS/timing/PI sign-off.
- Stage 3 requires a **physical redundancy** path.

---

## Status & roadmap

| Component | State |
|---|---|
| Closure / receptivity / maturity scaffolds | ✅ v0.1 |
| PDN `L_loop` + ablation plan template | ✅ v0.1 |
| Mode-purity retreat rule | ✅ v0.1 |
| PCNO stage gates | ✅ v0.1 |
| Offline demo | ✅ v0.1 |
| Real solver adapters (PEEC / FEM) | 🔜 planned |
| Reference coupons / datasets | 🔜 planned |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Citation

Cite this software and the companion Zenodo preprints (DOIs in
`CITATION.cff`). Conceptually:

```
G., Titan (2026). SBE/DSR Toolkit (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.23143157
```

Related papers (verify live DOIs before relying on them):

- Programme papers 01–06 on Zenodo (SBE/DSR Structural Substrates track)
- Ontology: Dynamic Structural Realism v1.0 — `10.5281/zenodo.22086468`
- Prior LLM scaffolding: https://github.com/bionicaiinc/structural-density
- SSRN companion: https://dx.doi.org/10.2139/ssrn.7307220
- This repository: https://github.com/bionicaiinc/sbe-dsr-toolkit

---

© 2026 BIONIC AI INC.
