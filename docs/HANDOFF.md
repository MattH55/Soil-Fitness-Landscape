# Handoff: Soil Fitness Landscape

Written 8 October 2026 after the v0.1 seed. The project mirrors the Physiological Fitness
Landscape (PFL) in `../Physiological Fitness Landscape`; read that repo's `docs/PFL_Project_Summary_v2.md`
for the concept and `backend/build_standalone_html.py` for the mature version of the site compiler.

## Rules carried over from PFL

- Every number cites a source key in `seed/catalog.py`; never invent effect sizes. If a paper
  gives only "significant increase", enter the practice with `effect=None` and describe it in `context`.
- Run `python backend/build_db.py` after every catalogue edit. A source whose DOI fails the
  Crossref title match prints `FAIL`; fix the DOI or the citation before building the site.
- After `python backend/build_site.py`, run `scripts/browsertest/probe.js`. Every chart must print `OK`
  and the error count must be 0. Look at the PNGs it writes.
- Stage files explicitly (`git add seed backend docs dist README.md .gitignore`), never `git add -A`.
- Dashboard palette and rules follow the dataviz skill: fixed categorical order (blue, orange, aqua,
  yellow), one axis per chart, legend for two or more series, status colours reserved.

## Priorities

1. **Real spread for the distributions.** Fine, van Es and Schindelbeck (2017, SSSAJ 81:589,
   DOI 10.2136/sssaj2016.09.0286) publish means and SDs per texture group for all CASH indicators
   (n = 5,767). Enter them as additional `DISTRIBUTIONS` rows and as `cnd` response functions
   (tier A) for aggregate stability, respiration, SOC/organic matter, active carbon, P and K.
   The Wiley page returned 403 to automated fetching; download the PDF manually.
2. **LUCAS quantiles.** The LUCAS 2009/2015/2018 topsoil data are free from the ESDAC after
   registration (https://esdac.jrc.ec.europa.eu/). Compute per-land-cover means, SDs and
   percentiles (cropland vs grassland vs woodland) locally and store aggregates only. That gives
   proper "where soils sit" curves and makes P, K and pH comparable to the CASH optima.
3. **SMAF curves.** Andrews, Karlen and Cambardella (2004) give the functional forms
   (more-is-better, less-is-better, optimum) with site-specific parameters for bulk density,
   pH, EC, SOC, microbial biomass, PMN, aggregate stability and water-filled pore space. Replace
   the tier C bulk-density logistic with the SMAF curve.
4. **More practice effects per indicator.** Targets currently need three favourable quantified
   effects to score full modifiability. Gaps: pH (liming dose-response, e.g. the Holland 2019
   data and lime requirement models), P and K (fertiliser and manure build-up rates per kg
   applied), bulk density (controlled traffic, deep tillage, cover crops), aggregate stability
   (cover crops, no-till, organic amendments: several meta-analyses exist), respiration and
   microbial biomass (biochar, compost).
5. **Trajectories beyond SOC.** LUCAS 2009 vs 2015 vs 2018 pH, P and K changes (De Rosa et al.
   cover SOC only); the Rothamsted long-term experiments (e-RA) for pH drift under ammonium
   fertilisation; the US NRCS Soil Health Institute North American Project to Evaluate Soil
   Health Measurements for multi-year indicator responses.
6. **Target score proper.** Once each indicator has a response curve with a slope at the typical
   soil, a distribution SD, at least one practice effect in indicator units and a drift rate,
   port PFL's `backend/build_target_scores.py`: score sensitivity (score change per SD),
   drift (SD per decade), modifiability (best favourable effect in SD), geometric mean of
   percentile ranks. The current Targets tab is an evidence-coverage placeholder and says so.
7. **Unit harmonisation.** Practice effects mix percent, Mg C/ha and g C/kg/yr. Add a
   `stock_to_concentration` helper (bulk density, depth) to the compiler and show every SOC
   effect in g/kg alongside the reported unit, with the assumption printed.

## Data model

Tables in `data/soil_landscape.db` (rebuilt from `seed/catalog.py`; do not edit the DB by hand):
`source(key, citation, doi, url, year, design, verified, crossref_title)`,
`indicator(slug, name, unit, grp, direction, inherent, optimal_low, optimal_high, domain_min, domain_max, notes)`,
`distribution(slug, population, n, mean, median, sd, source, note)`,
`response_function(slug, kind, outcome, tier, params JSON, source, note)`,
`practice_effect(practice, category, slug, effect, unit, ci_low, ci_high, timeframe, context, source, direction)`,
`trajectory(slug, population, rate, rate_se, unit, summary, source)`.

Response-function kinds and their JSON params are evaluated in `respond()` inside
`backend/build_site.py`: `cnd {mean, sd}`, `optimum_plateau {zero_low, plateau_low, plateau_high, zero_high}`,
`saturating {x_zero, x_full, curvature: linear|concave}`, `threshold_slope {crops: {name: [threshold, slope]}, default}`,
`texture_threshold {critical: {texture: value}, default, width}`. Add a new kind in both the
catalogue docstring and `respond()`.

## Not yet done

- No GitHub remote and no deployment. PFL deploys over FTP with credentials passed as
  environment variables (see that repo's `backend/_ftp_deploy.py`); do the same here only when
  the owner provides a host and account for the soil site.
- No automated tests. A minimal `tests/test_catalog.py` should assert that every source key
  referenced by a row exists, every DOI verified, every response function's slug matches an
  indicator, and every practice `direction` is consistent with the indicator `direction`.
