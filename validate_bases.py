#!/usr/bin/env python3
"""Validate .base files against the Obsidian Bases schema documented at
help.obsidian.md/bases/syntax and obsidian.md/help/bases/views (fetched 2026-10-23).
Exit 0 = all files valid; exit 1 = any violation. Stdlib + PyYAML."""
import sys, glob, yaml

TOP = {"filters", "formulas", "properties", "summaries", "views"}
VIEW_KEYS = {"type", "name", "limit", "groupBy", "groupOrder", "summaries", "order", "filters"}
VIEW_TYPES = {"table", "list", "cards", "kanban", "map"}
LOGIC = {"and", "or", "not"}

def check_filter(f, errs, where):
    if isinstance(f, str):
        if not f.strip():
            errs.append(f"{where}: empty filter string")
        return
    if isinstance(f, dict):
        if len(f) != 1 or next(iter(f)) not in LOGIC:
            errs.append(f"{where}: filter object must have exactly one of and/or/not")
            return
        key, val = next(iter(f.items()))
        if not isinstance(val, list) or not val:
            errs.append(f"{where}: '{key}' needs a non-empty list")
            return
        for i, sub in enumerate(val):
            check_filter(sub, errs, f"{where}.{key}[{i}]")
        return
    errs.append(f"{where}: filter must be a string or object, got {type(f).__name__}")

def validate(path):
    errs = []
    try:
        data = yaml.safe_load(open(path, encoding="utf-8"))
    except Exception as e:
        return [f"YAML parse error: {e}"]
    if not isinstance(data, dict):
        return ["top level must be a mapping"]
    for k in data:
        if k not in TOP:
            errs.append(f"unknown top-level key '{k}'")
    if "filters" in data:
        check_filter(data["filters"], errs, "filters")
    views = data.get("views")
    if not isinstance(views, list) or not views:
        errs.append("'views' must be a non-empty list")
        return errs
    for i, v in enumerate(views):
        w = f"views[{i}]"
        if not isinstance(v, dict):
            errs.append(f"{w}: must be a mapping"); continue
        for k in v:
            if k not in VIEW_KEYS:
                errs.append(f"{w}: unknown view key '{k}'")
        if v.get("type") not in VIEW_TYPES:
            errs.append(f"{w}: type must be one of {sorted(VIEW_TYPES)}, got {v.get('type')!r}")
        if not isinstance(v.get("name"), str) or not v.get("name"):
            errs.append(f"{w}: name required")
        if "limit" in v and not isinstance(v["limit"], int):
            errs.append(f"{w}: limit must be an integer")
        if "groupBy" in v:
            g = v["groupBy"]
            if not isinstance(g, dict) or "property" not in g:
                errs.append(f"{w}: groupBy must be an object with 'property'")
            elif g.get("direction", "ASC") not in ("ASC", "DESC"):
                errs.append(f"{w}: groupBy.direction must be ASC or DESC")
        if "order" in v and not (isinstance(v["order"], list) and all(isinstance(x, str) for x in v["order"])):
            errs.append(f"{w}: order must be a list of property names")
        if "filters" in v:
            check_filter(v["filters"], errs, f"{w}.filters")
    return errs

if __name__ == "__main__":
    paths = sys.argv[1:] or sorted(glob.glob("*.base"))
    bad = 0
    if not paths:
        print("no .base files"); sys.exit(1)
    for p in paths:
        e = validate(p)
        status = "OK" if not e else "FAIL"
        print(f"{status}  {p}" + ("" if not e else "\n      " + "\n      ".join(e)))
        bad += bool(e)
    sys.exit(1 if bad else 0)
