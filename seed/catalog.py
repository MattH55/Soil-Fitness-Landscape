"""
Soil Fitness Landscape - seed catalogue (v0.1, 8 Oct 2026).

Everything here is traceable: each numeric entry cites a source key in SOURCES,
and backend/build_db.py verifies every DOI against Crossref at build time
(source.verified = 1 only when the DOI resolves and the title matches).

Evidence tiers for response functions
  A  published scoring function with parameters (e.g. Cornell CASH cumulative-normal)
  B  published threshold-slope / yield-response model (e.g. Maas-Hoffman salinity)
  C  curve derived here from published thresholds or optimum ranges (shape chosen,
     parameters quoted) - clearly weaker; drawn dashed on the site
"""

SOURCES = {
    "cash_manual_2016": dict(citation="Moebius-Clune BN, Moebius-Clune DJ, Gugino BK, Idowu OJ, Schindelbeck RR, Ristow AJ, van Es HM, Thies JE, Shayler HA, McBride MB, Kurtz KSM, Wolfe DW, Abawi GS. Comprehensive Assessment of Soil Health - The Cornell Framework, 3rd ed. Cornell University, 2016.",
                             doi=None, url="https://www.css.cornell.edu/extension/soil-health/manual.pdf", year=2016, design="scoring framework manual"),
    "fine_2017": dict(citation="Fine AK, van Es HM, Schindelbeck RR. Statistics, Scoring Functions, and Regional Analysis of a Comprehensive Soil Health Database. Soil Sci Soc Am J. 2017;81(3):589-601.",
                      doi="10.2136/sssaj2016.09.0286", url=None, year=2017, design="database analysis, n=5,767 samples (Mid-Atlantic, Midwest, Northeast US)"),
    "andrews_2004": dict(citation="Andrews SS, Karlen DL, Cambardella CA. The Soil Management Assessment Framework: a quantitative soil quality evaluation method. Soil Sci Soc Am J. 2004;68(6):1945-1962.",
                         doi="10.2136/sssaj2004.1945", url=None, year=2004, design="scoring framework"),
    "ballabio_2019": dict(citation="Ballabio C, Lugato E, Fernandez-Ugalde O, Orgiazzi A, Jones A, Borrelli P, Montanarella L, Panagos P. Mapping LUCAS topsoil chemical properties at European scale using Gaussian process regression. Geoderma. 2019;355:113912.",
                          doi="10.1016/j.geoderma.2019.113912", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC6743211/", year=2019, design="EU-wide survey (LUCAS 2009/2012 topsoil, ~20,000 points, all land covers)"),
    "toth_2013": dict(citation="Toth G, Jones A, Montanarella L. The LUCAS topsoil database and derived information on the regional variability of cropland topsoil properties in the European Union. Environ Monit Assess. 2013;185(9):7409-7425.",
                      doi="10.1007/s10661-013-3109-3", url=None, year=2013, design="EU-wide survey (LUCAS 2009 topsoil, ~20,000 samples, 25 Member States)"),
    "hassani_2024": dict(citation="Hassani A, Smith P, Shokri N. Negative correlation between soil salinity and soil organic carbon variability. Proc Natl Acad Sci USA. 2024;121(18):e2317332121.",
                         doi="10.1073/pnas.2317332121", url=None, year=2024, design="global compilation, 43,459 mineral soil samples since 1992"),
    "derosa_2024": dict(citation="De Rosa D, Ballabio C, Lugato E, Fasiolo M, Jones A, Panagos P. Soil organic carbon stocks in European croplands and grasslands: How much have we lost in the past decade? Glob Change Biol. 2024;30(1):e16992.",
                        doi="10.1111/gcb.16992", url=None, year=2024, design="repeated survey (LUCAS 2009, 2015, 2018), quantile GAM"),
    "oldfield_2019": dict(citation="Oldfield EE, Bradford MA, Wood SA. Global meta-analysis of the relationship between soil organic matter and crop yields. SOIL. 2019;5(1):15-32.",
                          doi="10.5194/soil-5-15-2019", url=None, year=2019, design="global meta-analysis (maize, wheat)"),
    "maas_hoffman_1977": dict(citation="Maas EV, Hoffman GJ. Crop salt tolerance - current assessment. J Irrig Drain Div ASCE. 1977;103(2):115-134.",
                              doi="10.1061/JRCEA4.0001137", url="https://www.ars.usda.gov/arsuserfiles/20360500/pdf_pubs/P2246.pdf", year=1977, design="threshold-slope model fitted to ~60 crops"),
    "reichert_2009": dict(citation="Reichert JM, Suzuki LEAS, Reinert DJ, Horn R, Hakansson I. Reference bulk density and critical degree-of-compactness for no-till crop production in subtropical highly weathered soils. Soil Tillage Res. 2009;102(2):242-254.",
                          doi="10.1016/j.still.2008.07.002", url=None, year=2009, design="field experiments, texture-specific critical bulk density"),
    "mallarino_2011": dict(citation="Mallarino AP, Pagani A, Sawyer JE. Corn and soybean response to soil pH level and liming. Proc Integrated Crop Management Conf, Iowa State University, 2011:93-102.",
                           doi=None, url="https://www.agronext.iastate.edu/soilfertility/info/Mallarino_LimeOnFarm_ICM-2011.pdf", year=2011, design="multi-site field trials (Iowa)"),
    "holland_2019": dict(citation="Holland JE, White PJ, Glendining MJ, Goulding KWT, McGrath SP. Yield responses of arable crops to liming - An evaluation of relationships between yields and soil pH from a long-term liming experiment. Eur J Agron. 2019;105:176-188.",
                         doi="10.1016/j.eja.2019.02.016", url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6472519/", year=2019, design="long-term liming experiment (Rothamsted/Woburn)"),
    "poeplau_don_2015": dict(citation="Poeplau C, Don A. Carbon sequestration in agricultural soils via cultivation of cover crops - A meta-analysis. Agric Ecosyst Environ. 2015;200:33-41.",
                             doi="10.1016/j.agee.2014.10.024", url=None, year=2015, design="meta-analysis (30 studies, 37 sites, 139 plots)"),
    "kim_2020": dict(citation="Kim N, Zabaloy MC, Guan K, Villamil MB. Do cover crops benefit soil microbiome? A meta-analysis of current research. Soil Biol Biochem. 2020;142:107701.",
                     doi="10.1016/j.soilbio.2019.107701", url=None, year=2020, design="meta-analysis"),
    "gross_glaser_2021": dict(citation="Gross A, Glaser B. Meta-analysis on how manure application changes soil organic carbon storage. Sci Rep. 2021;11:5516.",
                              doi="10.1038/s41598-021-82739-7", url=None, year=2021, design="meta-analysis"),
    "maillard_angers_2014": dict(citation="Maillard E, Angers DA. Animal manure application and soil organic carbon stocks: a meta-analysis. Glob Change Biol. 2014;20(2):666-679.",
                                 doi="10.1111/gcb.12438", url=None, year=2014, design="meta-analysis (42 articles, 49 sites, 130 observations)"),
    "cui_2024": dict(citation="Cui Y, et al. Effects of no-till on upland crop yield and soil organic carbon: a global meta-analysis. Plant Soil. 2024;499:363-377.",
                     doi="10.1007/s11104-022-05854-y", url=None, year=2024, design="global meta-analysis"),
    "pittelkow_2015": dict(citation="Pittelkow CM, Linquist BA, Lundy ME, Liang X, van Groenigen KJ, Lee J, van Gestel N, Six J, Venterea RT, van Kessel C. When does no-till yield more? A global meta-analysis. Field Crops Res. 2015;183:156-168.",
                           doi="10.1016/j.fcr.2015.07.020", url=None, year=2015, design="global meta-analysis (5,463 paired observations)"),
    "luo_2010": dict(citation="Luo Z, Wang E, Sun OJ. Can no-tillage stimulate carbon sequestration in agricultural soils? A meta-analysis of paired experiments. Agric Ecosyst Environ. 2010;139(1-2):224-231.",
                     doi="10.1016/j.agee.2010.08.006", url=None, year=2010, design="meta-analysis (69 paired experiments)"),
    "jeffery_2011": dict(citation="Jeffery S, Verheijen FGA, van der Velde M, Bastos AC. A quantitative review of the effects of biochar application to soils on crop productivity using meta-analysis. Agric Ecosyst Environ. 2011;144(1):175-187.",
                         doi="10.1016/j.agee.2011.08.015", url=None, year=2011, design="meta-analysis"),
    "jeffery_2017": dict(citation="Jeffery S, Abalos D, Prodana M, Bastos AC, van Groenigen JW, Hungate BA, Verheijen F. Biochar boosts tropical but not temperate crop yields. Environ Res Lett. 2017;12(5):053001.",
                         doi="10.1088/1748-9326/aa67bd", url=None, year=2017, design="meta-analysis (1,125 comparisons, 109 studies)"),
    "kallenbach_grandy_2011": dict(citation="Kallenbach C, Grandy AS. Controls over soil microbial biomass responses to carbon amendments in agricultural systems: A meta-analysis. Agric Ecosyst Environ. 2011;144(1):241-252.",
                                   doi="10.1016/j.agee.2011.08.020", url=None, year=2011, design="meta-analysis (690 experiments)"),
    "bolinder_2020": dict(citation="Bolinder MA, Crotty F, Elsen A, Frac M, Kismanyoky T, Lipiec J, Tits M, Toth Z, Katterer T. The effect of crop residues, cover crops, manures and nitrogen fertilization on soil organic carbon changes in agroecosystems: a synthesis of reviews. Mitig Adapt Strateg Glob Change. 2020;25:929-952.",
                          doi="10.1007/s11027-020-09916-3", url=None, year=2020, design="synthesis of 37 reviews"),
}

# Indicators: the dimensions of the soil landscape.
#   direction: more_is_better | less_is_better | optimum
INDICATORS = [
    dict(slug="ph_h2o", name="Soil pH (1:5 H2O)", unit="pH", group="chemical", direction="optimum", inherent=False,
         optimal_low=6.4, optimal_high=7.3, domain=(3.5, 9.5),
         notes="Cornell CASH assigns the maximum score between pH 6.4-7.3 for most crops (5.3-6.3 for acid-loving crops). Iowa trials show strong yield response up to pH 5.9 and little above 6.5."),
    dict(slug="soc", name="Soil organic carbon", unit="g/kg", group="chemical", direction="more_is_better", inherent=False,
         optimal_low=20.0, optimal_high=None, domain=(0.0, 150.0),
         notes="Oldfield et al. (2019): maize/wheat yields rise with SOC and plateau at roughly 2% SOC (20 g/kg)."),
    dict(slug="total_n", name="Total nitrogen", unit="g/kg", group="chemical", direction="more_is_better", inherent=False,
         optimal_low=2.0, optimal_high=None, domain=(0.0, 20.0), notes="Tracks SOC (C:N ~10-13 in cropland)."),
    dict(slug="cn_ratio", name="C:N ratio", unit="ratio", group="chemical", direction="optimum", inherent=False,
         optimal_low=10.0, optimal_high=14.0, domain=(4.0, 40.0), notes="Mineralisation balance; above ~25 nitrogen is immobilised."),
    dict(slug="p_extractable", name="Extractable phosphorus", unit="mg/kg", group="chemical", direction="optimum", inherent=False,
         optimal_low=3.5, optimal_high=21.5, domain=(0.0, 200.0),
         notes="CASH optimum 3.5-21.5 ppm (Modified Morgan extract); LUCAS reports Olsen P - methods differ, so the EU distribution is context only."),
    dict(slug="k_extractable", name="Extractable potassium", unit="mg/kg", group="chemical", direction="more_is_better", inherent=False,
         optimal_low=74.5, optimal_high=None, domain=(0.0, 1000.0), notes="CASH: >= 74.5 ppm scores 100."),
    dict(slug="cec", name="Cation exchange capacity", unit="cmol(+)/kg", group="chemical", direction="more_is_better", inherent=True,
         optimal_low=15.0, optimal_high=None, domain=(0.0, 60.0), notes="Largely inherent (clay, SOM); SMAF more-is-better."),
    dict(slug="caco3", name="Carbonates (CaCO3)", unit="g/kg", group="chemical", direction="less_is_better", inherent=True,
         optimal_low=None, optimal_high=50.0, domain=(0.0, 800.0), notes="Highly skewed in LUCAS (median 1 g/kg, mean 53)."),
    dict(slug="ec", name="Electrical conductivity (saturation extract)", unit="dS/m", group="chemical", direction="less_is_better", inherent=False,
         optimal_low=None, optimal_high=2.0, domain=(0.0, 20.0),
         notes="Maas-Hoffman threshold-slope: yield unaffected below a crop-specific threshold (maize 1.7, wheat 6.0, barley 8.0 dS/m) then falls linearly."),
    dict(slug="bulk_density", name="Bulk density", unit="g/cm3", group="physical", direction="less_is_better", inherent=False,
         optimal_low=None, optimal_high=1.4, domain=(0.8, 2.0),
         notes="Critical values are texture-specific (Reichert et al.): clay 1.30-1.40, clay loam 1.40-1.50, sandy loam 1.70-1.80 g/cm3."),
    dict(slug="aggregate_stability", name="Wet aggregate stability", unit="%", group="physical", direction="more_is_better", inherent=False,
         optimal_low=None, optimal_high=None, domain=(0.0, 100.0), notes="CASH indicator; texture-specific cumulative-normal scoring (Fine et al. 2017)."),
    dict(slug="active_carbon", name="Active carbon (permanganate-oxidisable C)", unit="mg/kg", group="biological", direction="more_is_better", inherent=False,
         optimal_low=None, optimal_high=None, domain=(0.0, 1500.0),
         notes="CASH medium-texture calibration: mean 531, SD 182 ppm; score = cumulative normal percentile."),
    dict(slug="microbial_biomass_c", name="Microbial biomass carbon", unit="mg/kg", group="biological", direction="more_is_better", inherent=False,
         optimal_low=None, optimal_high=None, domain=(0.0, 2000.0), notes="SMAF more-is-better; responds strongly to organic inputs and cover crops."),
    dict(slug="respiration", name="Soil respiration (4-day CO2 burst)", unit="mg CO2/g", group="biological", direction="more_is_better", inherent=False,
         optimal_low=None, optimal_high=None, domain=(0.0, 2.0), notes="CASH indicator; no texture effect (Fine et al. 2017)."),
    dict(slug="yield", name="Relative crop yield (outcome)", unit="%", group="outcome", direction="more_is_better", inherent=False,
         optimal_low=None, optimal_high=None, domain=(0.0, 150.0), notes="Outcome axis used by practice effects; not an indicator."),
]

# Population distributions (where the landscape is drawn), canonical units.
DISTRIBUTIONS = [
    dict(slug="ph_h2o", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=6.30, median=6.30, sd=None, source="ballabio_2019"),
    dict(slug="cec", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=16.08, median=12.70, sd=None, source="ballabio_2019"),
    dict(slug="cn_ratio", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=13.20, median=10.89, sd=None, source="ballabio_2019"),
    dict(slug="total_n", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=None, median=1.80, sd=None, source="ballabio_2019",
         note="Table 2 prints a mean of 12.10 g/kg that is inconsistent with the median (1.80); the mean is omitted as a likely unit error."),
    dict(slug="p_extractable", population="EU topsoil, LUCAS 2009/12, all land covers (Olsen P)", n=19967, mean=37.61, median=29.10, sd=None, source="ballabio_2019"),
    dict(slug="k_extractable", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=199.17, median=142.20, sd=None, source="ballabio_2019"),
    dict(slug="caco3", population="EU topsoil, LUCAS 2009/12, all land covers", n=19967, mean=52.78, median=1.00, sd=None, source="ballabio_2019"),
    dict(slug="soc", population="Global cropland mineral topsoils (compilation since 1992)", n=43459, mean=18.47, median=None, sd=None, source="hassani_2024",
         note="Cropland mean predicted SOC 18.47 g/kg vs 35.96 g/kg non-cropland; mineral soils with SOC < 150 g/kg."),
    dict(slug="active_carbon", population="US medium-textured agricultural soils, Cornell Soil Health Lab calibration set", n=None, mean=531.0, median=None, sd=182.0, source="cash_manual_2016"),
]

# Response / scoring functions: soil-function score (0-100) or relative yield.
#   kind: cnd | optimum_plateau | threshold_slope | saturating | texture_threshold
RESPONSE_FUNCTIONS = [
    dict(slug="active_carbon", kind="cnd", outcome="CASH soil-health score (0-100)", tier="A", params=dict(mean=531.0, sd=182.0, texture="medium"),
         source="cash_manual_2016", note="Score = cumulative normal percentile of the calibration set; 600 ppm -> 60."),
    dict(slug="ph_h2o", kind="optimum_plateau", outcome="CASH soil-health score (0-100)", tier="A", params=dict(plateau_low=6.4, plateau_high=7.3, zero_low=4.0, zero_high=9.0),
         source="cash_manual_2016", note="Score 100 between 6.4 and 7.3 (most crops); the fall-off to 0 is drawn here, not published (tier C for the tails)."),
    dict(slug="p_extractable", kind="optimum_plateau", outcome="CASH soil-health score (0-100)", tier="A", params=dict(plateau_low=3.5, plateau_high=21.5, zero_low=0.45, zero_high=100.0),
         source="cash_manual_2016", note="Modified Morgan P: 3.5-21.5 ppm scored 100; deficient at <= 0.45 ppm; excessive at >= 100 ppm."),
    dict(slug="k_extractable", kind="saturating", outcome="CASH soil-health score (0-100)", tier="A", params=dict(x_full=74.5, x_zero=0.0, curvature="linear"),
         source="cash_manual_2016", note=">= 74.5 ppm scores 100; linear below (shape assumed)."),
    dict(slug="soc", kind="saturating", outcome="Relative maize/wheat yield (% of plateau)", tier="B", params=dict(x_full=20.0, x_zero=0.0, curvature="concave"),
         source="oldfield_2019", note="Yield rises with SOC and plateaus near 2% SOC; drawn as a concave saturating curve reaching the plateau at 20 g/kg."),
    dict(slug="ec", kind="threshold_slope", outcome="Relative yield (%) - Maas-Hoffman", tier="B",
         params=dict(crops={"maize": [1.7, 12.0], "wheat": [6.0, 7.1], "barley": [8.0, 5.0], "rice": [3.0, 12.0], "soybean": [5.0, 20.0], "potato": [1.7, 12.0], "tomato": [2.5, 9.9], "alfalfa": [2.0, 7.3]}, default="wheat"),
         source="maas_hoffman_1977", note="Yr = 100 - b (ECe - threshold) above the crop threshold; values from the USDA salt-tolerance tables."),
    dict(slug="bulk_density", kind="texture_threshold", outcome="Root growth / yield constraint (0-100)", tier="C",
         params=dict(critical={"clay": 1.35, "clay loam": 1.45, "sandy loam": 1.75}, default="clay loam", width=0.15),
         source="reichert_2009", note="Logistic fall from 100 to 0 centred on the texture-specific critical bulk density (Reichert et al.); shape chosen here."),
]

# Practices (interventions) and their quantified effects on indicators.
PRACTICES = [
    dict(practice="Cover crops", category="agronomic", slug="soc", effect=0.32, unit="Mg C/ha/yr", ci=(0.24, 0.40), timeframe="to ~54 years (mean 22 cm depth)",
         context="139 plots, 37 sites, cover vs bare fallow", source="poeplau_don_2015", direction="favourable"),
    dict(practice="Cover crops", category="agronomic", slug="microbial_biomass_c", effect=27.0, unit="%", ci=None, timeframe="multi-year",
         context="microbial abundance +27%, activity +22%, diversity +2.5% vs no cover", source="kim_2020", direction="favourable"),
    dict(practice="Animal manure (vs control)", category="organic amendment", slug="soc", effect=35.4, unit="%", ci=None, timeframe="multi-year",
         context="SOC stock +35.4% (= 10.7 Mg C/ha) relative to control", source="gross_glaser_2021", direction="favourable"),
    dict(practice="Animal manure (vs unamended control)", category="organic amendment", slug="soc", effect=9.4, unit="Mg C/ha", ci=None, timeframe="mean 18 years",
         context="+9.4 Mg C/ha vs control, +5.6 vs mineral-fertilised; manure-C retention 12 +/- 4%", source="maillard_angers_2014", direction="favourable"),
    dict(practice="Organic amendments (vs mineral fertiliser only)", category="organic amendment", slug="microbial_biomass_c", effect=51.0, unit="%", ci=None, timeframe="multi-year",
         context="690 experiments; farmyard manure largest effect", source="kallenbach_grandy_2011", direction="favourable"),
    dict(practice="No-till (vs conventional tillage)", category="tillage", slug="soc", effect=9.9, unit="%", ci=None, timeframe="multi-year, topsoil",
         context="SOC sequestration +9.9%; gain concentrated in the top layer and shrinks with deeper sampling (Luo et al. 2010)", source="cui_2024", direction="favourable"),
    dict(practice="No-till (vs conventional tillage)", category="tillage", slug="yield", effect=-5.0, unit="%", ci=None, timeframe="multi-year",
         context="upland crop yield -5%; penalty narrows after 3-10 years and with residue retention + rotation (Pittelkow et al. 2015: -5.7% overall)", source="cui_2024", direction="unfavourable"),
    dict(practice="Biochar", category="amendment", slug="yield", effect=10.0, unit="%", ci=None, timeframe="single to few seasons",
         context="grand mean +10%; +14% on acidic, +13% on neutral soils", source="jeffery_2011", direction="favourable"),
    dict(practice="Biochar (tropical soils)", category="amendment", slug="yield", effect=25.0, unit="%", ci=None, timeframe="single to few seasons",
         context="+25% in the tropics via liming and nutrient effects; no significant effect in temperate systems", source="jeffery_2017", direction="favourable"),
    dict(practice="Liming (acid soils)", category="amendment", slug="ph_h2o", effect=None, unit="pH units", ci=None, timeframe="years",
         context="Relative yield of most arable crops rises with pH up to crop-specific critical values; oats and potatoes respond weakly; P fertiliser lowers the critical pH (long-term Rothamsted/Woburn liming experiment)", source="holland_2019", direction="favourable"),
    dict(practice="Cropland converted to permanent grassland", category="land use", slug="soc", effect=0.49, unit="g C/kg/yr", ci=(0.47, 0.51), timeframe="2009-2018",
         context="partial effect of continuous grassland; continuous cropland -0.04 +/- 0.01 g C/kg/yr", source="derosa_2024", direction="favourable"),
    dict(practice="Crop residue retention", category="agronomic", slug="soc", effect=None, unit="qualitative", ci=None, timeframe="multi-year",
         context="synthesis of 37 reviews: residues, cover crops and manure all raise SOC; effect sizes heterogeneous", source="bolinder_2020", direction="favourable"),
]

# Trajectories (repeated surveys / long-term experiments).
TRAJECTORIES = [
    dict(slug="soc", population="EU + UK continuous cropland, LUCAS 2009-2018 (0-20 cm)", rate=-0.04, rate_se=0.01, unit="g C/kg/yr",
         summary="Agricultural topsoil SOC stock (below 1000 m) 9.3 Gt in 2018; change 2009-2018 -0.75%; largest losses in central-northern countries", source="derosa_2024"),
    dict(slug="soc", population="EU + UK continuous grassland, LUCAS 2009-2018 (0-20 cm)", rate=0.49, rate_se=0.02, unit="g C/kg/yr",
         summary="Continuous grassland gains; conversion grassland -> cropland is a main driver of loss", source="derosa_2024"),
]
