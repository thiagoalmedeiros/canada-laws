#!/usr/bin/env python3
"""Build provincial/territorial modules of the OKF bundle from the A2AJ "canadian-laws" dataset.

Source: https://huggingface.co/datasets/a2aj/canadian-laws (Access to Algorithmic Justice).
A2AJ collects each jurisdiction's laws from its official website; the texts are UNOFFICIAL.

Usage:
    python3 tools/provincial_to_md.py <bundle dir, e.g. laws> [CODE ...]

Codes: ab bc mb nb nl ns nt on pe qc sk yt (default: all). For each code, writes
<bundle>/<code>/{acts,regulations}/{en,fr}/<slug>.md (one OKF concept per law), the
index.md files, the module overview.md, and refreshes the bundle-root index.md.
Needs: pandas, pyarrow, requests.
"""
import io
import os
import re
import shutil
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import okf  # noqa: E402

BASE = "https://huggingface.co/datasets/a2aj/canadian-laws/resolve/main/{ds}/train.parquet"
DATASET = "https://huggingface.co/datasets/a2aj/canadian-laws"
PRODUCER = "process:canada-laws-provincial-converter"
CODES = ["ab", "bc", "mb", "nb", "nl", "ns", "nt", "on", "pe", "qc", "sk", "yt"]


def val(row, col):
    v = row.get(col)
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except (TypeError, ValueError):
        pass
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
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


def disclaimer(code, url):
    info = okf.JURISDICTION_INFO[code]
    name = okf.MODULES[code][0]
    return (f"> **Unofficial version, for personal and non-commercial use only.** "
            f"© {info['holder']}. Not endorsed by or affiliated with the Government of {name}. "
            f"Text obtained from the [official source]({url or info['site']}) via the "
            f"[A2AJ Canadian Laws dataset]({DATASET}). Always check the official version before relying on it.")


def paragraphs(text):
    """Upstream text separates provisions with single newlines, which Markdown would
    merge into one paragraph. Make every line its own paragraph, except inside tables
    and code blocks."""
    out = []
    fence = False
    prev = ""
    for line in okf.clean(text.replace("\r\n", "\n")).split("\n"):
        line = line.rstrip()
        if line.lstrip().startswith("```"):
            fence = not fence
        table = line.lstrip().startswith("|") and prev.lstrip().startswith("|")
        if out and line and prev and not fence and not table:
            out.append("")
        out.append(line)
        prev = line
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    # Bracketed amendment notes like "[(2)](b)" would render as links: escape them.
    return re.sub(r"\]\((?=[^)/:#.\s]{1,8}\))", r"]\\(", text)


def pick(row, field, lang):
    other = "fr" if lang == "en" else "en"
    return val(row, f"{field}_{lang}") or val(row, f"{field}_{other}")


def concept(row, lang, code, kind, slug, has_other):
    name = okf.clean(pick(row, "name", lang))
    cit = okf.clean(pick(row, "citation", lang))
    url = val(row, f"url_{lang}") or val(row, f"url_{'fr' if lang == 'en' else 'en'}")
    if not url:  # some jurisdictions store the link under another column name
        url = next((val(row, k) for k in sorted(row) if "url" in k.lower() and val(row, k).startswith("http")), "")
    text = paragraphs(val(row, f"unofficial_text_{lang}"))
    retrieved = okf.iso_date(val(row, f"scraped_timestamp_{lang}"))
    jname = okf.MODULES[code][0]
    other_lang = "fr" if lang == "en" else "en"
    if kind == "acts":
        desc = f"{jname} Act, {cit}." if lang == "en" else f"Loi ({okf.MODULES[code][1]}), {cit}."
    else:
        desc = f"{jname} regulation, {cit}." if lang == "en" else f"Règlement ({okf.MODULES[code][1]}), {cit}."
    info = okf.JURISDICTION_INFO[code]
    fm = okf.frontmatter([
        ("type", "Act" if kind == "acts" else "Regulation"),
        ("title", name or cit),
        ("description", desc),
        ("resource", url),
        ("tags", [code, "act" if kind == "acts" else "regulation", lang]),
        ("jurisdiction", code),
        ("language", lang),
        ("citation", cit),
        ("document_date", (val(row, f"document_date_{lang}") or "")[:10]),
        ("translation", f"../{other_lang}/{slug}.md" if has_other else ""),
        ("upstream_license", val(row, "upstream_license")),
        ("status", "stable"),
        ("generated", okf.generated_yaml(PRODUCER, retrieved)),
        ("sources", okf.sources_yaml([
            {"id": "official", "resource": url or info["site"], "title": f"{info['holder']}: official text",
             "author": f"org:{code}-government", "last_modified": ""},
            {"id": "a2aj", "resource": f"{DATASET}/blob/main/{'LEGISLATION' if kind == 'acts' else 'REGULATIONS'}-{code.upper()}/train.parquet",
             "title": "A2AJ Canadian Laws dataset", "author": "org:a2aj", "last_modified": retrieved},
        ])),
    ])
    m = re.match(r"^\s*# [^\n]*\n", text)
    if m:  # upstream text already has a title: keep it first
        body = [m.group(0).strip(), ""]
        text = text[m.end():].lstrip()
    else:
        body = [f"# {name or cit}", ""]
        if cit and cit != name:
            body += [f"*{cit}*", ""]
    body += [disclaimer(code, url), "", text, ""]
    return fm + "\n" + "\n".join(body), name or cit, desc


def run(out, codes):
    for code in codes:
        mdir = os.path.join(out, code)
        counts = {}
        for kind, ds in (("acts", f"LEGISLATION-{code.upper()}"), ("regulations", f"REGULATIONS-{code.upper()}")):
            df = fetch(ds)
            if df is None:
                print(f"{ds}: not available")
                continue
            kdir = os.path.join(mdir, kind)
            if os.path.isdir(kdir):
                shutil.rmtree(kdir)  # full refresh so repealed laws disappear
            used = set()
            listing = {"en": [], "fr": []}
            for _, row in df.iterrows():
                row = row.to_dict()
                langs = [l for l in ("en", "fr") if val(row, f"unofficial_text_{l}")]
                if not langs:
                    continue
                base = (val(row, "citation_en") or val(row, "citation_fr") or val(row, "name_en")
                        or val(row, "name_fr"))
                s = okf.slug(base)
                n = 2
                while s in used:
                    s = f"{okf.slug(base)}-{n}"
                    n += 1
                used.add(s)
                for lang in langs:
                    d = os.path.join(kdir, lang)
                    os.makedirs(d, exist_ok=True)
                    text, title, desc = concept(row, lang, code, kind, s, len(langs) == 2)
                    with open(os.path.join(d, s + ".md"), "w", encoding="utf-8") as f:
                        f.write(text)
                    listing[lang].append(okf.index_entry(title, s + ".md", desc))
            for lang, entries in listing.items():
                if entries:
                    counts[(kind, lang)] = len(entries)
                    entries.sort(key=lambda e: e.lower())
                    okf.write_index(os.path.join(kdir, lang), [(okf.KIND_LABEL[(kind, lang)], entries)])
            print(f"{ds}: " + ", ".join(f"{len(v)} {k}" for k, v in listing.items() if v))
        if counts:
            write_overview(mdir, code, counts)
            okf.write_module_index(out, code, counts)
    okf.write_root_index(out)


def write_overview(mdir, code, counts):
    name, fr_name, _ = okf.MODULES[code]
    info = okf.JURISDICTION_INFO[code]
    acts = max(counts.get(("acts", "en"), 0), counts.get(("acts", "fr"), 0))
    regs = max(counts.get(("regulations", "en"), 0), counts.get(("regulations", "fr"), 0))
    srcs = [{"id": "official", "resource": info["site"], "title": f"{info['holder']}: official laws website",
             "author": f"org:{code}-government"},
            {"id": "a2aj", "resource": DATASET, "title": "A2AJ Canadian Laws dataset", "author": "org:a2aj"}]
    if info["terms_url"]:
        srcs.append({"id": "terms", "resource": info["terms_url"], "title": f"{name} reuse terms",
                     "author": f"org:{code}-government"})
    fm = okf.frontmatter([
        ("type", "Jurisdiction"),
        ("title", name),
        ("description", f"{acts} Acts and {regs} regulations of {name}, from the official laws website via the "
                        "A2AJ dataset. Unofficial; personal and non-commercial use."),
        ("resource", info["site"]),
        ("tags", [code, "jurisdiction"]),
        ("jurisdiction", code),
        ("acts_en", counts.get(("acts", "en"), 0)), ("acts_fr", counts.get(("acts", "fr"), 0)),
        ("regulations_en", counts.get(("regulations", "en"), 0)),
        ("regulations_fr", counts.get(("regulations", "fr"), 0)),
        ("status", "stable"),
        ("generated", okf.generated_yaml(PRODUCER, "")),
        ("sources", okf.sources_yaml(srcs)),
    ])
    rows = []
    for kind, label in (("acts", "Acts / Lois"), ("regulations", "Regulations / Règlements")):
        cells = [f"[{counts[(kind, l)]}]({kind}/{l}/)" if counts.get((kind, l)) else "—" for l in ("en", "fr")]
        rows.append(f"| {label} | {cells[0]} | {cells[1]} |")
    terms_ref = "[^terms]" if info["terms_url"] else ""
    body = f"""
# {name}

The Acts and regulations of {name} ({fr_name}), as published by {info['holder']} on its
[official laws website]({info['site']}).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset]({DATASET}).[^a2aj]

| | English | Français |
|---|---|---|
{chr(10).join(rows)}

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© {info['holder']}. {info['terms']}{terms_ref} These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: {info['holder']}: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
""" + (f"[^terms]: {name} reuse terms\n" if info["terms_url"] else "")
    with open(os.path.join(mdir, "overview.md"), "w", encoding="utf-8") as f:
        f.write(fm + body)


if __name__ == "__main__":
    out = sys.argv[1]
    codes = [c.lower() for c in sys.argv[2:]] or CODES
    bad = [c for c in codes if c not in CODES]
    if bad:
        sys.exit(f"unknown jurisdiction(s): {bad}")
    run(out, codes)
