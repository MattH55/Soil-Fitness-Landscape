"""Build data/soil_landscape.db from seed/catalog.py and verify every DOI on Crossref.

Usage: python backend/build_db.py [--no-verify]
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request

try:  # Windows consoles default to cp1252; Crossref titles contain Unicode dashes
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from seed.catalog import SOURCES, INDICATORS, DISTRIBUTIONS, RESPONSE_FUNCTIONS, PRACTICES, TRAJECTORIES  # noqa: E402

DB = os.path.join(ROOT, "data", "soil_landscape.db")
SCHEMA = """
CREATE TABLE source (key TEXT PRIMARY KEY, citation TEXT, doi TEXT, url TEXT, year INT, design TEXT, verified INT, crossref_title TEXT);
CREATE TABLE indicator (slug TEXT PRIMARY KEY, name TEXT, unit TEXT, grp TEXT, direction TEXT, inherent INT, optimal_low REAL, optimal_high REAL, domain_min REAL, domain_max REAL, notes TEXT);
CREATE TABLE distribution (id INTEGER PRIMARY KEY, slug TEXT, population TEXT, n INT, mean REAL, median REAL, sd REAL, source TEXT, note TEXT);
CREATE TABLE response_function (id INTEGER PRIMARY KEY, slug TEXT, kind TEXT, outcome TEXT, tier TEXT, params TEXT, source TEXT, note TEXT);
CREATE TABLE practice_effect (id INTEGER PRIMARY KEY, practice TEXT, category TEXT, slug TEXT, effect REAL, unit TEXT, ci_low REAL, ci_high REAL, timeframe TEXT, context TEXT, source TEXT, direction TEXT);
CREATE TABLE trajectory (id INTEGER PRIMARY KEY, slug TEXT, population TEXT, rate REAL, rate_se REAL, unit TEXT, summary TEXT, source TEXT);
"""


def crossref_title(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "SoilFitnessLandscape/0.1 (mailto:mhalma@opensourcemed.info)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            m = json.load(r)["message"]
            return (m.get("title") or [""])[0]
    except Exception:
        return None


def words(s):
    return set(re.findall(r"[a-z]{5,}", (s or "").lower()))


def main(verify=True):
    if os.path.exists(DB):
        os.remove(DB)
    c = sqlite3.connect(DB)
    c.executescript(SCHEMA)
    for k, s in SOURCES.items():
        title = crossref_title(s["doi"]) if (verify and s["doi"]) else None
        if not s["doi"]:
            ok = -1
        else:
            ok = 1 if (title and len(words(title) & words(s["citation"])) >= 3) else 0
        c.execute("INSERT INTO source VALUES (?,?,?,?,?,?,?,?)", (k, s["citation"], s["doi"], s["url"], s["year"], s["design"], ok, title))
        print(f"  {('OK    ' if ok == 1 else ('no-DOI' if ok == -1 else 'FAIL  '))} {k:<24} {(title or '')[:80]}")
    for i in INDICATORS:
        c.execute("INSERT INTO indicator VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (i["slug"], i["name"], i["unit"], i["group"], i["direction"], int(i["inherent"]), i["optimal_low"], i["optimal_high"], i["domain"][0], i["domain"][1], i["notes"]))
    for d in DISTRIBUTIONS:
        c.execute("INSERT INTO distribution (slug,population,n,mean,median,sd,source,note) VALUES (?,?,?,?,?,?,?,?)",
                  (d["slug"], d["population"], d["n"], d["mean"], d["median"], d["sd"], d["source"], d.get("note")))
    for r in RESPONSE_FUNCTIONS:
        c.execute("INSERT INTO response_function (slug,kind,outcome,tier,params,source,note) VALUES (?,?,?,?,?,?,?)",
                  (r["slug"], r["kind"], r["outcome"], r["tier"], json.dumps(r["params"]), r["source"], r["note"]))
    for p in PRACTICES:
        ci = p.get("ci") or (None, None)
        c.execute("INSERT INTO practice_effect (practice,category,slug,effect,unit,ci_low,ci_high,timeframe,context,source,direction) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (p["practice"], p["category"], p["slug"], p["effect"], p["unit"], ci[0], ci[1], p["timeframe"], p["context"], p["source"], p["direction"]))
    for t in TRAJECTORIES:
        c.execute("INSERT INTO trajectory (slug,population,rate,rate_se,unit,summary,source) VALUES (?,?,?,?,?,?,?)",
                  (t["slug"], t["population"], t["rate"], t["rate_se"], t["unit"], t["summary"], t["source"]))
    c.commit()
    print("sources (ok, fail, no-DOI):", c.execute("SELECT SUM(verified=1), SUM(verified=0), SUM(verified=-1) FROM source").fetchone())
    c.close()


if __name__ == "__main__":
    main(verify="--no-verify" not in sys.argv)
