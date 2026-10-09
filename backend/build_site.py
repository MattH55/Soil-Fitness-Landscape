"""Compile dist/index.html - a single-file Soil Fitness Landscape dashboard - from data/soil_landscape.db.

Plotly.js is loaded from cdnjs; everything else (data, CSS, JS) is inlined.
Usage: python backend/build_site.py
"""
from __future__ import annotations

import datetime
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "soil_landscape.db")
OUT = os.path.join(ROOT, "dist", "index.html")
ROOT_COPY = os.path.join(ROOT, "index.html")  # served by GitHub Pages from the branch root


def rows(c, sql):
    c.row_factory = sqlite3.Row
    return [dict(r) for r in c.execute(sql)]


def load():
    c = sqlite3.connect(DB)
    d = dict(
        indicators=rows(c, "SELECT * FROM indicator"),
        distributions=rows(c, "SELECT * FROM distribution"),
        responses=rows(c, "SELECT * FROM response_function"),
        practices=rows(c, "SELECT * FROM practice_effect"),
        trajectories=rows(c, "SELECT * FROM trajectory"),
        sources=rows(c, "SELECT * FROM source ORDER BY year, key"),
    )
    for r in d["responses"]:
        r["params"] = json.loads(r["params"])
    d["built"] = datetime.date.today().isoformat()
    c.close()
    return d


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Soil Fitness Landscape</title>
<meta name="description" content="Soil indicators mapped as a fitness landscape: where soils sit, how each indicator scores, which practices move it, and how it drifts over time. Every number is cited.">
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.0/plotly.min.js"></script>
<style>
:root{--bg:#fcfcfb;--panel:#ffffff;--ink:#1a1a19;--ink2:#4d4d4a;--muted:#8a8a86;--line:#e4e4e0;--grid:#ececea;
 --c1:#2a78d6;--c2:#eb6834;--c3:#1baf7a;--c4:#eda100;--good:#0ca30c;--warn:#fab219;--serious:#ec835a;--critical:#d03b3b;--band:rgba(12,163,12,.10)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1a1a19;--panel:#232322;--ink:#f0efea;--ink2:#c9c8c2;--muted:#8f8e88;--line:#3a3a38;--grid:#2d2d2b;--c1:#3987e5;--band:rgba(12,163,12,.18)}}
:root[data-theme="dark"]{--bg:#1a1a19;--panel:#232322;--ink:#f0efea;--ink2:#c9c8c2;--muted:#8f8e88;--line:#3a3a38;--grid:#2d2d2b;--c1:#3987e5;--band:rgba(12,163,12,.18)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--c1)}
header{padding:20px 16px 0;max-width:1200px;margin:0 auto}
h1{margin:0;font-size:24px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--ink2);margin:4px 0 12px;max-width:820px}
nav{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--line)}
nav button{background:none;border:0;border-bottom:2px solid transparent;padding:8px 12px;color:var(--ink2);font:inherit;cursor:pointer}
nav button.on{color:var(--ink);border-bottom-color:var(--c1);font-weight:600}
nav .spacer{flex:1}
main{max-width:1200px;margin:0 auto;padding:16px}
.view{display:none}.view.on{display:block}
.ind-layout{display:grid;grid-template-columns:260px 1fr;gap:16px}
@media(max-width:800px){.ind-layout{grid-template-columns:1fr}}
aside .grp{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:12px 0 4px}
aside button{display:block;width:100%;text-align:left;background:none;border:0;padding:6px 8px;border-radius:6px;color:var(--ink);font:inherit;cursor:pointer}
aside button.on{background:var(--panel);box-shadow:inset 0 0 0 1px var(--line);font-weight:600}
aside button small{color:var(--muted);display:block;font-size:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:14px}
.card h2{margin:0 0 4px;font-size:18px}
.card h3{margin:0 0 8px;font-size:14px;font-weight:600;color:var(--ink2)}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 8px}
.chip{font-size:12px;padding:2px 8px;border:1px solid var(--line);border-radius:999px;color:var(--ink2)}
.badge{font-size:11px;padding:1px 6px;border-radius:4px;border:1px solid var(--line);color:var(--ink2);white-space:nowrap}
.badge.ok{border-color:var(--good);color:var(--good)}
.badge.A{border-color:var(--good);color:var(--good)}.badge.B{border-color:var(--c1);color:var(--c1)}.badge.C{border-color:var(--warn);color:var(--warn)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:900px){.two{grid-template-columns:1fr}}
.plot{width:100%;height:300px}
.note{color:var(--ink2);font-size:13px;margin:6px 0 0}
.muted{color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:12px}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.bar{display:inline-block;height:8px;border-radius:4px;background:var(--c1);vertical-align:middle}
.pos{color:var(--good)}.neg{color:var(--critical)}
select{font:inherit;padding:3px 6px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink)}
.ctl{display:flex;gap:10px;align-items:center;margin-bottom:6px;font-size:13px;color:var(--ink2)}
footer{max-width:1200px;margin:24px auto;padding:0 16px;color:var(--muted);font-size:12px}
.theme{font-size:12px;color:var(--muted);cursor:pointer;background:none;border:1px solid var(--line);border-radius:6px;padding:2px 8px;align-self:center}
.tbl-wrap{overflow-x:auto}
#targets td:nth-child(3),#targets td:nth-child(4){white-space:nowrap}
</style>
</head>
<body>
<header>
 <h1>Soil Fitness Landscape</h1>
 <p class="sub">Soil indicators as a fitness landscape, mirroring the <a href="https://landscape.opensourcemed.info/" target="_blank" rel="noopener">Physiological Fitness Landscape</a>: where soils sit (survey distributions), how each indicator scores against a function (scoring and yield-response curves), which practices move it (meta-analytic effects) and how it drifts (repeated surveys). Every number carries a citation; DOIs were checked against Crossref at build time.</p>
 <nav id="nav">
  <button data-v="indicators" class="on">Indicators</button>
  <button data-v="practices">Practices</button>
  <button data-v="trajectories">Trajectories</button>
  <button data-v="targets">Targets</button>
  <button data-v="sources">Sources</button>
  <span class="spacer"></span>
  <button class="theme" id="theme">theme: auto</button>
 </nav>
</header>
<main>
 <div id="indicators" class="view on"><div class="ind-layout"><aside id="ind-list"></aside><section id="ind-main"></section></div></div>
 <div id="practices" class="view"></div>
 <div id="trajectories" class="view"></div>
 <div id="targets" class="view"></div>
 <div id="sources" class="view"></div>
</main>
<footer>Built __BUILT__ from data/soil_landscape.db · seed catalogue v0.1 · Open Source Medicine. Tier A = published scoring function with parameters; B = published response model; C = curve drawn here from published thresholds (dashed).</footer>
<script>
const D = __DATA__;
const $ = s => document.querySelector(s);
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt = (x, d) => x == null ? '–' : (d != null ? Number(x).toFixed(d) : (Math.abs(x) >= 100 ? Number(x).toFixed(0) : Math.abs(x) >= 10 ? Number(x).toFixed(1) : Number(x).toFixed(2)));
const src = k => D.sources.find(s => s.key === k) || {key: k, citation: k, year: ''};
const surname = c => (c.match(/^[A-Z][\w'-]+(?: [A-Z][a-z]+)?/) || [c.slice(0, 20)])[0];
function cite(k) {
  const s = src(k); const href = s.doi ? 'https://doi.org/' + s.doi : (s.url || '#');
  return `<a class="src" href="${href}" target="_blank" rel="noopener" title="${esc(s.citation)}">${esc(surname(s.citation))} ${s.year || ''}</a>` +
    (s.verified === 1 ? ' <span class="badge ok" title="DOI resolved on Crossref and title matched at build time">DOI ✓</span>' : '');
}
const ind = slug => D.indicators.find(i => i.slug === slug);
const GROUPS = ['chemical', 'physical', 'biological', 'outcome'];
const CFG = {displayModeBar: false, responsive: true};
function axis(extra) { return Object.assign({gridcolor: css('--grid'), zeroline: false, linecolor: css('--line'), tickcolor: css('--line'), ticks: 'outside'}, extra || {}); }
function layout(o) {
  o = o || {};
  return Object.assign({
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: {family: 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif', size: 12, color: css('--ink2')},
    margin: {l: 56, r: 16, t: 28, b: 48}, hovermode: 'closest', showlegend: false,
    legend: {orientation: 'h', y: -0.25, font: {color: css('--ink2')}},
  }, o, {xaxis: axis(o.xaxis), yaxis: axis(o.yaxis)});
}
function erf(x) { const s = Math.sign(x); x = Math.abs(x); const t = 1 / (1 + 0.3275911 * x);
  return s * (1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x)); }
const Phi = z => 0.5 * (1 + erf(z / Math.SQRT2));
const lin = (a, b, n) => Array.from({length: n}, (_, i) => a + (b - a) * i / (n - 1));

// ---------- response / scoring functions ----------
function respond(rf, x, opt) {
  const p = rf.params;
  switch (rf.kind) {
    case 'cnd': return 100 * Phi((x - p.mean) / p.sd);
    case 'optimum_plateau':
      if (x <= p.zero_low || x >= p.zero_high) return 0;
      if (x < p.plateau_low) return 100 * (x - p.zero_low) / (p.plateau_low - p.zero_low);
      if (x <= p.plateau_high) return 100;
      return 100 * (p.zero_high - x) / (p.zero_high - p.plateau_high);
    case 'saturating': { const u = Math.min(1, Math.max(0, (x - p.x_zero) / (p.x_full - p.x_zero)));
      return 100 * (p.curvature === 'concave' ? 1 - (1 - u) * (1 - u) : u); }
    case 'threshold_slope': { const crop = opt && p.crops[opt] ? opt : p.default; const [t, b] = p.crops[crop];
      return x <= t ? 100 : Math.max(0, 100 - b * (x - t)); }
    case 'texture_threshold': { const tex = opt && p.critical[opt] != null ? opt : p.default; const c = p.critical[tex];
      return 100 / (1 + Math.exp((x - c) / (p.width / 4))); }
  }
  return null;
}
function options(rf) {
  if (rf.kind === 'threshold_slope') return {label: 'Crop', keys: Object.keys(rf.params.crops), def: rf.params.default};
  if (rf.kind === 'texture_threshold') return {label: 'Texture', keys: Object.keys(rf.params.critical), def: rf.params.default};
  return null;
}
// ---------- distributions ----------
function density(dist, xs) {
  if (dist.sd != null && dist.mean != null) { const m = dist.mean, s = dist.sd;
    return {kind: 'normal', y: xs.map(x => Math.exp(-0.5 * ((x - m) / s) ** 2) / (s * Math.sqrt(2 * Math.PI))), p95: [m - 1.96 * s, m + 1.96 * s]}; }
  if (dist.mean != null && dist.median != null && dist.mean > dist.median) {
    const mu = Math.log(dist.median), sig = Math.sqrt(2 * Math.log(dist.mean / dist.median));
    return {kind: 'lognormal', sig, y: xs.map(x => x <= 0 ? 0 : Math.exp(-0.5 * ((Math.log(x) - mu) / sig) ** 2) / (x * sig * Math.sqrt(2 * Math.PI))), p95: [Math.exp(mu - 1.96 * sig), Math.exp(mu + 1.96 * sig)]}; }
  return null;
}
function optBand(i) {
  const lo = i.optimal_low, hi = i.optimal_high;
  if (lo == null && hi == null) return [];
  return [{type: 'rect', xref: 'x', yref: 'paper', x0: lo == null ? i.domain_min : lo, x1: hi == null ? i.domain_max : hi, y0: 0, y1: 1, fillcolor: css('--band'), line: {width: 0}, layer: 'below'}];
}
function vline(x, label, color, dash) {
  return {type: 'line', xref: 'x', yref: 'paper', x0: x, x1: x, y0: 0, y1: 1, line: {color, width: 1.5, dash: dash || 'solid'}, label: {text: label, textposition: 'top right', font: {size: 11, color}}};
}

// ---------- Indicators view ----------
let current = 'soc';
function renderIndicatorList() {
  const el = $('#ind-list'); let h = '';
  for (const g of GROUPS) {
    const items = D.indicators.filter(i => i.grp === g); if (!items.length) continue;
    h += `<div class="grp">${g}</div>`;
    for (const i of items) h += `<button data-s="${i.slug}" class="${i.slug === current ? 'on' : ''}">${esc(i.name)}<small>${esc(i.unit)} · ${i.direction.replace(/_/g, ' ')}</small></button>`;
  }
  el.innerHTML = h;
  el.querySelectorAll('button').forEach(b => b.onclick = () => { current = b.dataset.s; renderIndicatorList(); showIndicator(); });
}
function showIndicator() {
  const i = ind(current);
  const dists = D.distributions.filter(d => d.slug === i.slug);
  const rfs = D.responses.filter(r => r.slug === i.slug);
  const prs = D.practices.filter(p => p.slug === i.slug);
  const trs = D.trajectories.filter(t => t.slug === i.slug);
  const opt = i.optimal_low != null || i.optimal_high != null
    ? (i.direction === 'optimum' ? `${fmt(i.optimal_low)}–${fmt(i.optimal_high)}` : i.direction === 'more_is_better' ? `≥ ${fmt(i.optimal_low)}` : `≤ ${fmt(i.optimal_high)}`) + ' ' + i.unit : 'not defined';
  let h = `<div class="card"><h2>${esc(i.name)}</h2><div class="chips"><span class="chip">${i.grp}</span><span class="chip">${i.direction.replace(/_/g, ' ')}</span><span class="chip">target: ${esc(opt)}</span>${i.inherent ? '<span class="chip">largely inherent</span>' : ''}</div><p class="note">${esc(i.notes)}</p></div>`;
  h += '<div class="two">';
  h += `<div class="card"><h3>Where soils sit</h3>${dists.length ? '<div id="p-dist" class="plot"></div>' : '<p class="muted">No population distribution in the catalogue yet.</p>'}` +
       dists.map(d => `<p class="note"><b>${esc(d.population)}</b>${d.n ? ', n = ' + d.n.toLocaleString() : ''}: mean ${fmt(d.mean)}${d.median != null ? ', median ' + fmt(d.median) : ''}${d.sd != null ? ', SD ' + fmt(d.sd) : ''} ${esc(i.unit)} — ${cite(d.source)}${d.note ? '<br><span class="muted">' + esc(d.note) + '</span>' : ''}</p>`).join('') + '</div>';
  const o = rfs.length ? options(rfs[0]) : null;
  h += `<div class="card"><h3>How it scores <span class="badge ${rfs.length ? rfs[0].tier : ''}">${rfs.length ? 'tier ' + rfs[0].tier : 'no curve'}</span></h3>` +
       (o ? `<div class="ctl"><label>${o.label} <select id="rf-opt">${o.keys.map(k => `<option ${k === o.def ? 'selected' : ''}>${k}</option>`).join('')}</select></label></div>` : '') +
       (rfs.length ? '<div id="p-resp" class="plot"></div>' : '<p class="muted">No scoring or response function in the catalogue yet. Candidates: Cornell CASH texture-specific cumulative-normal parameters (Fine et al. 2017), SMAF curves (Andrews et al. 2004).</p>') +
       rfs.map(r => `<p class="note"><b>${esc(r.outcome)}</b> — ${esc(r.note)} ${cite(r.source)}</p>`).join('') + '</div>';
  h += '</div>';
  h += `<div class="card"><h3>Practices that move it</h3>` + (prs.length ? `<div class="tbl-wrap"><table><tr><th>Practice</th><th class="num">Effect</th><th>95% CI</th><th>Timeframe</th><th>Context</th><th>Source</th></tr>` +
       prs.map(p => `<tr><td>${esc(p.practice)}<br><span class="muted">${esc(p.category)}</span></td><td class="num ${p.effect == null ? '' : p.direction === 'favourable' ? 'pos' : 'neg'}">${p.effect == null ? 'qualitative' : (p.effect > 0 ? '+' : '') + fmt(p.effect) + ' ' + esc(p.unit)}</td><td class="num">${p.ci_low != null ? fmt(p.ci_low) + '–' + fmt(p.ci_high) : '–'}</td><td>${esc(p.timeframe)}</td><td>${esc(p.context)}</td><td>${cite(p.source)}</td></tr>`).join('') + '</table></div>' : '<p class="muted">No quantified practice effects yet.</p>') + '</div>';
  if (trs.length) h += `<div class="card"><h3>Trajectory</h3><table><tr><th>Population</th><th class="num">Rate</th><th>Summary</th><th>Source</th></tr>` +
       trs.map(t => `<tr><td>${esc(t.population)}</td><td class="num ${t.rate >= 0 ? 'pos' : 'neg'}">${t.rate > 0 ? '+' : ''}${fmt(t.rate)} ± ${fmt(t.rate_se)} ${esc(t.unit)}</td><td>${esc(t.summary)}</td><td>${cite(t.source)}</td></tr>`).join('') + '</table></div>';
  $('#ind-main').innerHTML = h;
  if (dists.length) plotDist(i, dists);
  if (rfs.length) { plotResp(i, rfs[0], o ? o.def : null); if (o) $('#rf-opt').onchange = e => plotResp(i, rfs[0], e.target.value); }
}
function plotDist(i, dists) {
  const traces = [], shapes = optBand(i); let xmax = i.domain_max;
  const colors = ['--c1', '--c2', '--c3', '--c4'];
  dists.forEach(d => { const probe = density(d, [1]); if (probe) xmax = Math.min(xmax, probe.p95[1] * 1.3); });
  const xs = lin(i.domain_min, xmax, 240);
  dists.forEach((d, k) => {
    const col = css(colors[k % 4]); const dens = density(d, xs); const name = d.population.split(',')[0];
    if (dens) traces.push({x: xs, y: dens.y, type: 'scatter', mode: 'lines', line: {color: col, width: 2}, name, fill: 'tozeroy', fillcolor: col + '22', hovertemplate: '%{x:.3g} ' + i.unit + '<extra>' + esc(name) + ' (' + dens.kind + ' fit)</extra>'});
    if (d.mean != null) shapes.push(vline(d.mean, 'mean ' + fmt(d.mean), col));
    if (d.median != null && d.median !== d.mean) shapes.push(vline(d.median, 'median ' + fmt(d.median), col, 'dot'));
  });
  if (!traces.length) traces.push({x: [i.domain_min, xmax], y: [0, 0], type: 'scatter', mode: 'lines', line: {color: css('--line'), width: 1}, hoverinfo: 'skip'});
  Plotly.newPlot('p-dist', traces, layout({showlegend: dists.length > 1, xaxis: {title: {text: i.unit}, range: [i.domain_min, xmax]}, yaxis: {title: {text: 'density'}, showticklabels: false}, shapes}), CFG);
}
function plotResp(i, rf, opt) {
  const xs = lin(i.domain_min, i.domain_max, 300);
  const ys = xs.map(x => respond(rf, x, opt));
  const tr = {x: xs, y: ys, type: 'scatter', mode: 'lines', line: {color: css('--c2'), width: 2, dash: rf.tier === 'C' ? 'dash' : 'solid'}, name: rf.outcome, hovertemplate: '%{x:.3g} ' + i.unit + ' → %{y:.0f}<extra></extra>'};
  const shapes = optBand(i);
  const dist = D.distributions.find(d => d.slug === i.slug);
  if (dist && (dist.mean != null || dist.median != null)) { const m = dist.median != null ? dist.median : dist.mean; shapes.push(vline(m, 'typical soil ' + fmt(m), css('--c1'), 'dot')); }
  Plotly.newPlot('p-resp', [tr], layout({xaxis: {title: {text: i.unit}, range: [i.domain_min, i.domain_max]}, yaxis: {title: {text: rf.outcome.includes('yield') ? 'relative yield (%)' : 'score (0–100)'}, range: [0, 105]}, shapes}), CFG);
}

// ---------- Practices view ----------
function renderPractices() {
  const pct = D.practices.filter(p => p.unit === '%' && p.effect != null);
  const slugCol = {soc: '--c1', microbial_biomass_c: '--c3', yield: '--c2'};
  const bySlug = {}; pct.forEach(p => (bySlug[p.slug] = bySlug[p.slug] || []).push(p));
  const labels = pct.map(p => p.practice + ' → ' + ind(p.slug).name);
  const traces = Object.keys(bySlug).map(s => ({type: 'bar', orientation: 'h', name: ind(s).name, x: bySlug[s].map(p => p.effect), y: bySlug[s].map(p => p.practice + ' → ' + ind(p.slug).name),
    marker: {color: css(slugCol[s] || '--c4'), line: {color: css('--panel'), width: 2}}, width: 0.6,
    hovertemplate: '%{x:+.1f}%<br>%{customdata}<extra>' + esc(ind(s).name) + '</extra>', customdata: bySlug[s].map(p => esc(p.context) + ' — ' + esc(surname(src(p.source).citation)) + ' ' + src(p.source).year)}));
  let h = `<div class="card"><h3>Relative effects reported as percentages (meta-analyses)</h3><div id="p-prac" class="plot" style="height:${80 + 28 * pct.length}px"></div><p class="note">Effects in absolute units (Mg C/ha, g C/kg/yr) are listed below rather than plotted, so that no bar mixes units. Favourable effects on an indicator are not automatically favourable overall: no-till raises topsoil SOC but costs about 5% yield.</p></div>`;
  h += `<div class="card"><h3>All catalogued practice effects</h3><div class="tbl-wrap"><table><tr><th>Practice</th><th>Category</th><th>Indicator</th><th class="num">Effect</th><th>95% CI</th><th>Timeframe</th><th>Context</th><th>Source</th></tr>` +
    D.practices.map(p => `<tr><td>${esc(p.practice)}</td><td>${esc(p.category)}</td><td>${esc(ind(p.slug).name)}</td><td class="num ${p.effect == null ? '' : p.direction === 'favourable' ? 'pos' : 'neg'}">${p.effect == null ? 'qualitative' : (p.effect > 0 ? '+' : '') + fmt(p.effect) + ' ' + esc(p.unit)}</td><td class="num">${p.ci_low != null ? fmt(p.ci_low) + '–' + fmt(p.ci_high) : '–'}</td><td>${esc(p.timeframe)}</td><td>${esc(p.context)}</td><td>${cite(p.source)}</td></tr>`).join('') + '</table></div></div>';
  $('#practices').innerHTML = h;
  Plotly.newPlot('p-prac', traces, layout({showlegend: true, barmode: 'group', margin: {l: 300, r: 16, t: 10, b: 60}, xaxis: {title: {text: 'change vs control (%)'}, zeroline: true, zerolinecolor: css('--line')}, yaxis: {automargin: true, categoryorder: 'array', categoryarray: labels.slice().reverse()}}), CFG);
}

// ---------- Trajectories view ----------
function renderTrajectories() {
  const soc = D.trajectories.filter(t => t.slug === 'soc');
  const BD = 1.3, DEPTH = 0.2, MASS = BD * DEPTH * 10000; // t soil per ha in the 0-20 cm layer (g/cm3 * m * m2/ha -> t/ha)
  const toGkg = mgC => mgC / MASS * 1000; // Mg C/ha/yr -> g C/kg soil/yr
  const start = D.distributions.find(d => d.slug === 'soc').mean;
  const years = lin(0, 30, 31);
  const scen = [
    {name: 'Continuous cropland (LUCAS trend)', rate: -0.04, col: '--c2'},
    {name: 'Cropland + cover crops', rate: -0.04 + toGkg(0.32), col: '--c1'},
    {name: 'Cropland + manure', rate: -0.04 + toGkg(9.4 / 18), col: '--c4'},
    {name: 'Converted to permanent grassland', rate: 0.49, col: '--c3'},
  ];
  let h = `<div class="two"><div class="card"><h3>Observed SOC change, LUCAS 2009–2018</h3><div id="p-traj" class="plot"></div><p class="note">${soc.map(t => esc(t.population) + ': ' + (t.rate > 0 ? '+' : '') + fmt(t.rate) + ' ± ' + fmt(t.rate_se) + ' ' + esc(t.unit) + '. ' + esc(t.summary) + ' ' + cite(t.source)).join('<br>')}</p></div>` +
    `<div class="card"><h3>30-year projection from the global cropland mean</h3><div id="p-proj" class="plot"></div><p class="note">Starts at the global cropland mean SOC of ${fmt(start)} g/kg (${cite('hassani_2024')}). Cover-crop (+0.32 Mg C/ha/yr, ${cite('poeplau_don_2015')}) and manure (+9.4 Mg C/ha over ~18 y, ${cite('maillard_angers_2014')}) stocks are converted to concentration assuming bulk density ${BD} g/cm³ over 0–20 cm (${fmt(MASS, 0)} t soil/ha), added linearly to the cropland trend, with no saturation. The dotted line is the ~20 g/kg yield plateau (${cite('oldfield_2019')}). This is an illustration of rates, not a forecast.</p></div></div>`;
  $('#trajectories').innerHTML = h;
  Plotly.newPlot('p-traj', [{type: 'bar', x: soc.map(t => t.population.split(',')[0].replace('EU + UK ', '')), y: soc.map(t => t.rate), error_y: {type: 'data', array: soc.map(t => 1.96 * t.rate_se), color: css('--ink2'), thickness: 1.5, width: 6},
    marker: {color: css('--c1'), line: {color: css('--panel'), width: 2}}, width: 0.5, hovertemplate: '%{y:+.2f} g C/kg/yr<extra></extra>'}],
    layout({xaxis: {}, yaxis: {title: {text: 'g C / kg / yr'}, zeroline: true, zerolinecolor: css('--line')}}), CFG);
  const traces = scen.map(s => ({x: years, y: years.map(y => start + s.rate * y), type: 'scatter', mode: 'lines', name: s.name, line: {color: css(s.col), width: 2}, hovertemplate: '%{y:.1f} g/kg<extra>' + esc(s.name) + ' (' + (s.rate > 0 ? '+' : '') + s.rate.toFixed(2) + '/yr)</extra>'}));
  const annotations = scen.map(s => ({x: 30, y: start + s.rate * 30, text: (s.rate > 0 ? '+' : '') + s.rate.toFixed(2) + '/yr', xanchor: 'left', showarrow: false, font: {size: 11, color: css(s.col)}}));
  Plotly.newPlot('p-proj', traces, layout({showlegend: true, hovermode: 'x unified', margin: {l: 56, r: 70, t: 70, b: 50}, legend: {orientation: 'h', x: 0, y: 1.02, yanchor: 'bottom', font: {color: css('--ink2')}}, annotations, xaxis: {title: {text: 'years from now'}}, yaxis: {title: {text: 'SOC (g/kg)'}},
    shapes: [{type: 'line', x0: 0, x1: 30, y0: 20, y1: 20, line: {color: css('--muted'), width: 1, dash: 'dot'}}]}), CFG);
}

// ---------- Targets view ----------
function renderTargets() {
  const tierW = {A: 1, B: 0.75, C: 0.4};
  const rows = D.indicators.filter(i => i.grp !== 'outcome').map(i => {
    const rf = D.responses.find(r => r.slug === i.slug);
    const ds = D.distributions.filter(d => d.slug === i.slug);
    const dScore = ds.some(d => d.sd != null || (d.mean != null && d.median != null && d.mean !== d.median)) ? 1 : ds.length ? 0.5 : 0;
    const quant = D.practices.filter(p => p.slug === i.slug && p.effect != null && p.direction === 'favourable').length;
    const mod = Math.min(1, quant / 3);
    const drift = D.trajectories.some(t => t.slug === i.slug) ? 1 : 0;
    const resp = rf ? tierW[rf.tier] : 0;
    const score = (resp + dScore + mod + drift) / 4;
    return {i, resp, rf, dScore, quant, mod, drift, score, inherent: i.inherent};
  }).sort((a, b) => b.score - a.score);
  const bar = v => `<span class="bar" style="width:${Math.round(60 * v)}px"></span>`;
  $('#targets').innerHTML = `<div class="card"><h3>Evidence coverage by indicator</h3><p class="note">In the physiological landscape an intervention target is a marker that is strongly tied to the outcome, drifts with age and is modifiable. The soil analogue needs, for each indicator, (1) a function linking it to an outcome, (2) a population distribution to locate soils on, (3) quantified practice effects and (4) a measured drift. This table scores how much of that evidence the catalogue currently holds (0–1 each, equal weights). It ranks <em>readiness to be analysed</em>, not importance; the catalogue is young, so gaps dominate.</p>` +
    `<div class="tbl-wrap"><table><tr><th>Indicator</th><th>Outcome function</th><th>Distribution</th><th>Practice effects</th><th>Drift</th><th>Coverage</th><th>What is missing</th></tr>` +
    rows.map(r => {
      const miss = [];
      if (!r.rf) miss.push('scoring or yield-response curve'); else if (r.rf.tier === 'C') miss.push('published curve parameters (current curve is tier C)');
      if (r.dScore < 1) miss.push(r.dScore ? 'spread (SD or quantiles) for the distribution' : 'any survey distribution');
      if (r.quant < 3) miss.push(`${3 - r.quant} more quantified practice effect${3 - r.quant > 1 ? 's' : ''}`);
      if (!r.drift) miss.push('repeated-survey trend');
      if (r.inherent) miss.push('(largely inherent: low modifiability by design)');
      return `<tr><td>${esc(r.i.name)}</td><td>${r.rf ? `<span class="badge ${r.rf.tier}">tier ${r.rf.tier}</span>` : '<span class="muted">none</span>'}</td><td>${bar(r.dScore)} ${r.dScore}</td><td>${bar(r.mod)} ${r.quant}</td><td>${r.drift ? 'yes' : '<span class="muted">no</span>'}</td><td class="num"><b>${r.score.toFixed(2)}</b></td><td class="muted">${miss.join('; ')}</td></tr>`;
    }).join('') + '</table></div></div>';
}

// ---------- Sources view ----------
function renderSources() {
  $('#sources').innerHTML = `<div class="card"><h3>${D.sources.length} sources, ${D.sources.filter(s => s.verified === 1).length} DOIs verified on Crossref at build time</h3><div class="tbl-wrap"><table><tr><th>Key</th><th>Citation</th><th>Design</th><th>DOI / link</th><th>Check</th></tr>` +
    D.sources.map(s => `<tr><td><code>${s.key}</code></td><td>${esc(s.citation)}</td><td class="muted">${esc(s.design)}</td><td>${s.doi ? `<a href="https://doi.org/${s.doi}" target="_blank" rel="noopener">${s.doi}</a>` : ''}${s.url ? `${s.doi ? '<br>' : ''}<a href="${s.url}" target="_blank" rel="noopener">link</a>` : ''}</td><td>${s.verified === 1 ? '<span class="badge ok">title matched</span>' : s.verified === 0 ? '<span class="badge" style="border-color:var(--critical);color:var(--critical)">FAILED</span>' : '<span class="badge">no DOI</span>'}${s.crossref_title ? '<br><span class="muted" style="font-size:11px">' + esc(s.crossref_title) + '</span>' : ''}</td></tr>`).join('') + '</table></div></div>';
}

// ---------- shell ----------
const RENDER = {indicators: () => { renderIndicatorList(); showIndicator(); }, practices: renderPractices, trajectories: renderTrajectories, targets: renderTargets, sources: renderSources};
let view = 'indicators';
function show(v) {
  view = v;
  document.querySelectorAll('nav button[data-v]').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  document.querySelectorAll('.view').forEach(d => d.classList.toggle('on', d.id === v));
  RENDER[v]();
}
document.querySelectorAll('nav button[data-v]').forEach(b => b.onclick = () => show(b.dataset.v));
const THEMES = ['auto', 'light', 'dark']; let ti = 0;
try { ti = Math.max(0, THEMES.indexOf(localStorage.getItem('sfl-theme') || 'auto')); } catch (e) {}
function applyTheme() { const t = THEMES[ti]; if (t === 'auto') document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', t); $('#theme').textContent = 'theme: ' + t; try { localStorage.setItem('sfl-theme', t); } catch (e) {} }
$('#theme').onclick = () => { ti = (ti + 1) % 3; applyTheme(); show(view); };
if (window.matchMedia) window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => show(view));
applyTheme(); show('indicators');
</script>
</body>
</html>
"""


def main():
    d = load()
    html = TEMPLATE.replace("__DATA__", json.dumps(d)).replace("__BUILT__", d["built"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    for path in (OUT, ROOT_COPY):
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(path, f"{len(html):,} bytes")


if __name__ == "__main__":
    main()
