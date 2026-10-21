#!/usr/bin/env python3
"""Download provincial/territorial laws from the A2AJ "canadian-laws" dataset and write Markdown.

Source: https://huggingface.co/datasets/a2aj/canadian-laws (Access to Algorithmic Justice,
York University). A2AJ scrapes each jurisdiction's official site; texts are UNOFFICIAL.

Usage:
    python3 tools/provincial_to_md.py <output dir> [JURISDICTION ...]

Jurisdiction codes: AB BC MB NB NL NS NT ON PE QC SK YT (default: all).
Writes <out>/provinces/<code>/{acts,regulations}/<slug>.md (+ <slug>.fr.md when a
French text exists) and README indexes. Needs: pandas, pyarrow, requests.
"""
import io
import os
import re
import shutil
import sys
import unicodedata

import pandas as pd
import requests

BASE = "https://huggingface.co/datasets/a2aj/canadian-laws/resolve/main/{ds}/train.parquet"

JURIS = {
    "AB": "Alberta", "BC": "British Columbia", "MB": "Manitoba", "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador", "NS": "Nova Scotia", "NT": "Northwest Territories",
    "ON": "Ontario", "PE": "Prince Edward Island", "QC": "Quebec", "SK": "Saskatchewan",
    "YT": "Yukon",
}

DISCLAIMER = ("> **Unofficial version.** Text obtained from the official {name} website via the "
              "[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws). "
              "Always check the [official source]({url}) before relying on it.")


def slugify(s, maxlen=120):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return (s[:maxlen].rstrip("-") or "untitled")


def yaml_str(s):
    s = "" if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def val(row, col):
    v = row.get(col)
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except (TypeError, ValueError):
        pass
    if hasattr(v, "date"):
        try:
            return v.date().isoformat()
        except Exception:
            pass
    return str(v).strip()


def fetch(ds):
    headers = {}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"
    r = requests.get(BASE.format(ds=ds), headers=headers, timeout=900)
    if r.status_code == 404:
        return None
    if r.status_code in (401, 403):
        sys.exit(f"{ds}: Hugging Face refused the download ({r.status_code}). "
                 "Add an HF_TOKEN repository secret (free account token) and re-run.")
    r.raise_for_status()
    return pd.read_parquet(io.BytesIO(r.content))


def doc(row, lang, code, kind):
    sfx = "en" if lang == "en" else "fr"
    name = val(row, f"name_{sfx}") or val(row, f"name_{'fr' if sfx == 'en' else 'en'}")
    cit = val(row, f"citation_{sfx}") or val(row, f"citation_{'fr' if sfx == 'en' else 'en'}")
    url = val(row, f"url_{sfx}") or val(row, f"url_{'fr' if sfx == 'en' else 'en'}")
    text = val(row, f"unofficial_text_{sfx}")
    fm = ["---", f"title: {yaml_str(name)}", f"citation: {yaml_str(cit)}",
          f"jurisdiction: {yaml_str(JURIS[code])}", f"language: {lang}",
          f"type: {'act' if kind == 'acts' else 'regulation'}",
          f"document_date: {yaml_str(val(row, f'document_date_{sfx}'))}",
          f"retrieved: {yaml_str(val(row, f'scraped_timestamp_{sfx}'))}",
          f"source: {yaml_str(url)}",
          f"upstream_license: {yaml_str(val(row, 'upstream_license'))}", "---", ""]
    body = []
    if not re.match(r"^\s*#\s", text):
        body += [f"# {name or cit}", ""]
        if cit and cit != name:
            body += [f"*{cit}*", ""]
    body += [DISCLAIMER.format(name=JURIS[code], url=url or "#"), "", text.strip(), ""]
    return "\n".join(fm + body), name or cit, cit


def run(out, codes):
    summary = []
    for code in codes:
        root = os.path.join(out, "provinces", code.lower())
        for kind, ds in (("acts", f"LEGISLATION-{code}"), ("regulations", f"REGULATIONS-{code}")):
            df = fetch(ds)
            if df is None:
                print(f"{ds}: not available")
                continue
            d = os.path.join(root, kind)
            if os.path.isdir(d):
                shutil.rmtree(d)  # full refresh so repealed laws disappear
            os.makedirs(d)
            used = set()
            index = []
            for _, row in df.iterrows():
                row = row.to_dict()
                has_en = bool(val(row, "unofficial_text_en"))
                has_fr = bool(val(row, "unofficial_text_fr"))
                if not (has_en or has_fr):
                    continue
                base_name = val(row, "citation_en") or val(row, "citation_fr") or val(row, "name_en") or val(row, "name_fr")
                slug = slugify(base_name)
                n = 2
                while slug in used:
                    slug = f"{slugify(base_name)}-{n}"; n += 1
                used.add(slug)
                files = []
                for lang, has in (("en", has_en), ("fr", has_fr)):
                    if not has:
                        continue
                    fname = f"{slug}.md" if (lang == "en" or not has_en) else f"{slug}.fr.md"
                    text, title, cit = doc(row, lang, code, kind)
                    with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
                        f.write(text)
                    files.append((lang, fname, title, cit))
                index.append(files)
            write_index(d, code, kind, index)
            summary.append((code, kind, len(index)))
            print(f"{ds}: {len(index)} documents")
    write_overview(out, summary)


def write_index(d, code, kind, index):
    rows = sorted(index, key=lambda fs: fs[0][2].lower())
    lines = [f"# {JURIS[code]} — {'Acts' if kind == 'acts' else 'Regulations'}", "",
             f"{len(rows)} documents. Unofficial text; see each file for its official source and licence.", "",
             "| Title | Citation | Files |", "|---|---|---|"]
    for fs in rows:
        lang, fname, title, cit = fs[0]
        links = " · ".join(f"[{l}]({fn})" for l, fn, _, _ in fs)
        lines.append(f"| [{title.replace('|', '/')}]({fname}) | {cit.replace('|', '/')} | {links} |")
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_overview(out, summary):
    path = os.path.join(out, "provinces", "README.md")
    # Merge with counts already recorded for jurisdictions not refreshed in this run.
    counts = {}
    if os.path.exists(path):
        for m in re.finditer(r"^\| \[[^\]]+\]\(([a-z]{2})/\) \| (\d+) \| (\d+) \|", open(path, encoding="utf-8").read(), re.M):
            counts[m.group(1).upper()] = {"acts": int(m.group(2)), "regulations": int(m.group(3))}
    for code, kind, n in summary:
        counts.setdefault(code, {})[kind] = n
    lines = ["# Provincial and territorial laws", "",
             "Unofficial Markdown copies from the [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws). "
             "Nunavut is not covered by that dataset. Licence terms differ by jurisdiction; see the main README.", "",
             "| Jurisdiction | Acts | Regulations |", "|---|---|---|"]
    for code in sorted(counts):
        c = counts[code]
        lines.append(f"| [{JURIS[code]}]({code.lower()}/) | {c.get('acts', 0)} | {c.get('regulations', 0)} |")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    out = sys.argv[1]
    codes = [c.upper() for c in sys.argv[2:]] or sorted(JURIS)
    bad = [c for c in codes if c not in JURIS]
    if bad:
        sys.exit(f"unknown jurisdiction(s): {bad}")
    run(out, codes)
