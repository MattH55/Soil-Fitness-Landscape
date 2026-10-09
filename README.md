# Soil Fitness Landscape

A sibling of the [Physiological Fitness Landscape](https://landscape.opensourcemed.info/) (PFL)
for soil. PFL maps blood and functional biomarkers onto mortality-hazard curves, locates a
population on those curves, catalogues interventions that move each marker, and tracks how
markers drift with age. This project does the same for soil indicators, with crop yield and
published soil-health scoring functions standing in for mortality.

| PFL concept | Soil analogue | Where it lives |
|---|---|---|
| Biomarker | Soil indicator (pH, SOC, extractable P/K, CEC, bulk density, active carbon, ...) | `indicator` |
| Mortality hazard curve | Scoring function (Cornell CASH, SMAF) or yield-response model (Maas-Hoffman salinity, SOC-yield plateau) | `response_function` |
| Population distribution (NHANES) | Survey distribution (LUCAS EU topsoil, global compilations, Cornell calibration set) | `distribution` |
| Intervention effect | Practice effect from meta-analyses (cover crops, manure, no-till, biochar, liming, land-use change) | `practice_effect` |
| Age trajectory (HRS, ELSA) | Repeated-survey trend (LUCAS 2009 to 2018) | `trajectory` |
| Target score | Evidence-coverage score per indicator (until enough evidence exists to score value of information) | Targets tab |

## Layout

```
seed/catalog.py        every number in the project, each with a source key
backend/build_db.py    builds data/soil_landscape.db and verifies every DOI on Crossref
backend/build_site.py  compiles dist/index.html and a root index.html (GitHub Pages; single file, Plotly.js from cdnjs)
scripts/browsertest/   headless Chrome probe (puppeteer-core) that checks every chart renders
docs/HANDOFF.md        what to do next, in priority order
```

Build and check:

```
python backend/build_db.py          # add --no-verify to skip Crossref
python backend/build_site.py
cd scripts/browsertest && npm i puppeteer-core@22 && node probe.js
```

## Status (v0.1, October 2026)

- 15 indicators (14 soil indicators plus relative yield as an outcome axis).
- 9 distributions: LUCAS EU topsoil means and medians for pH, CEC, C:N, total N, Olsen P, K and
  carbonates (Ballabio et al. 2019, Table 2); global cropland SOC mean (Hassani et al. 2024);
  Cornell active-carbon calibration mean and SD.
- 7 response functions: CASH cumulative-normal for active carbon (tier A), CASH optimum plateaus
  for pH and P, CASH saturating for K (tier A), SOC-yield plateau at about 20 g/kg (tier B,
  Oldfield et al. 2019), Maas-Hoffman salinity for eight crops (tier B), texture-specific bulk
  density threshold (tier C, shape chosen here).
- 12 practice effects from meta-analyses, two of them qualitative (liming, residue retention).
- 2 trajectories (LUCAS cropland and grassland SOC change 2009 to 2018).
- 23 sources; the 21 with DOIs were resolved on Crossref at build time and their titles matched.

## Caveats

- Where LUCAS reports only mean and median, the site draws a lognormal from those two numbers.
  That shows skew but not the real spread. Fine et al. (2017) and the LUCAS microdata hold the
  actual quantiles; see the handoff.
- The P distribution is Olsen P (LUCAS) while the scoring function is Modified Morgan P (CASH).
  They are not the same extraction, so the "typical soil" marker on the P curve is indicative only.
- Tier C curves are drawn from published thresholds with a shape chosen here. They are dashed on
  the site and should be replaced by published parameters.
- The SOC projection converts carbon stocks (Mg C/ha) to concentration with an assumed bulk
  density and depth. It illustrates rates; it is not a forecast.
- Favourable movement of one indicator is not the same as a better soil: no-till raises topsoil
  SOC and lowers yield by about 5 percent in the same meta-analysis.
