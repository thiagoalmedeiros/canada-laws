"""Shared helpers for writing an Open Knowledge Format (OKF v0.2) bundle.

Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

Layout produced by the converters (bundle root = laws/):

    laws/
      index.md                 bundle root index (okf_version: "0.2")
      log.md                   bundle-wide update history
      credits.md               type: Reference (sources, licences)
      <module>/                one module per jurisdiction: federal, ab, bc, ...
        index.md
        log.md
        overview.md            type: Jurisdiction
        acts/
          index.md
          en/ index.md + <id>.md   type: Act
          fr/ index.md + <id>.md
        regulations/
          index.md
          en/ ...                  type: Regulation
          fr/ ...
"""
import datetime as _dt
import json
import os
import re

OKF_VERSION = "0.2"
BUNDLE = "laws"

MODULES = {
    # code: (name, French name, group)
    "federal": ("Canada (federal)", "Canada (fédéral)", "Federal"),
    "ab": ("Alberta", "Alberta", "Provinces"),
    "bc": ("British Columbia", "Colombie-Britannique", "Provinces"),
    "mb": ("Manitoba", "Manitoba", "Provinces"),
    "nb": ("New Brunswick", "Nouveau-Brunswick", "Provinces"),
    "nl": ("Newfoundland and Labrador", "Terre-Neuve-et-Labrador", "Provinces"),
    "ns": ("Nova Scotia", "Nouvelle-Écosse", "Provinces"),
    "on": ("Ontario", "Ontario", "Provinces"),
    "pe": ("Prince Edward Island", "Île-du-Prince-Édouard", "Provinces"),
    "qc": ("Quebec", "Québec", "Provinces"),
    "sk": ("Saskatchewan", "Saskatchewan", "Provinces"),
    "nt": ("Northwest Territories", "Territoires du Nord-Ouest", "Territories"),
    "yt": ("Yukon", "Yukon", "Territories"),
}

KIND_LABEL = {
    ("acts", "en"): "Acts (English)", ("acts", "fr"): "Lois (français)",
    ("regulations", "en"): "Regulations (English)", ("regulations", "fr"): "Règlements (français)",
}


_CP1252 = {"\x91": "‘", "\x92": "’", "\x93": "“", "\x94": "”", "\x96": "–", "\x97": "—", "\x85": "…", "\xa0": " "}


def clean(s):
    """Replace stray Windows-1252 code points and drop other control characters,
    which YAML does not allow and which render as garbage."""
    s = "".join(_CP1252.get(ch, ch) for ch in (s or ""))
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", s)


def ystr(s):
    """A YAML-safe double-quoted scalar (JSON strings are valid YAML)."""
    return json.dumps(clean("" if s is None else str(s)), ensure_ascii=False)


def iso_date(s):
    """'2026-06-14' or a datetime-ish string -> '2026-06-14T00:00:00Z' (or '')."""
    if not s:
        return ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?", str(s))
    if not m:
        return ""
    y, mo, d, h, mi, se = m.groups()
    return f"{y}-{mo}-{d}T{h or '00'}:{mi or '00'}:{se or '00'}Z"


def frontmatter(fields):
    """Render an ordered list of (key, value) pairs. Values that are already
    YAML snippets (flow mappings / block lists) are passed as ('raw', text)."""
    out = ["---"]
    for k, v in fields:
        if v is None or v == "" or v == []:
            continue
        if isinstance(v, tuple) and v[0] == "raw":
            out.append(f"{k}:{v[1]}" if v[1].startswith("\n") else f"{k}: {v[1]}")
        elif isinstance(v, list):
            out.append(f"{k}: [{', '.join(ystr(x) for x in v)}]")
        elif isinstance(v, bool):
            out.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            out.append(f"{k}: {v}")
        else:
            out.append(f"{k}: {ystr(v)}")
    out.append("---")
    return "\n".join(out) + "\n"


def sources_yaml(entries):
    """entries: list of dicts with id, resource, title, author, last_modified."""
    lines = []
    for e in entries:
        first = True
        for key in ("id", "resource", "title", "author", "last_modified"):
            v = e.get(key)
            if not v:
                continue
            lines.append(("  - " if first else "    ") + f"{key}: {ystr(v)}")
            first = False
    return ("raw", "\n" + "\n".join(lines)) if lines else None


def generated_yaml(by, at):
    return ("raw", "{ by: " + by + (", at: " + at if at else "") + " }")


def md_link_text(s):
    return (s or "").replace("[", "(").replace("]", ")").replace("\n", " ").strip()


def index_entry(title, href, desc=""):
    desc = (desc or "").replace("\n", " ").strip()
    if len(desc) > 240:
        desc = desc[:237].rstrip() + "…"
    return f"* [{md_link_text(title)}]({href})" + (f" - {desc}" if desc else "")


def write_index(directory, sections, frontmatter_text=""):
    """sections: list of (heading, [entry lines]). Index files carry no frontmatter,
    except okf_version at the bundle root (SPEC §8, §12)."""
    parts = [frontmatter_text] if frontmatter_text else []
    for heading, entries in sections:
        if not entries:
            continue
        parts.append(f"# {heading}\n\n" + "\n".join(entries) + "\n")
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def read_frontmatter(path):
    """Minimal reader for the frontmatter we write (flat keys only)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        if f.readline().rstrip("\n") != "---":
            return out
        for line in f:
            line = line.rstrip("\n")
            if line == "---":
                break
            m = re.match(r"^([A-Za-z_][\w-]*): (.*)$", line)
            if not m:
                continue
            k, v = m.groups()
            if v.startswith('"'):
                try:
                    v = json.loads(v)
                except ValueError:
                    pass
            out[k] = v
    return out


def prepend_log(path, title, entries, date=None):
    """Add entries under today's date in a log.md (newest first, SPEC §9)."""
    date = date or _dt.datetime.now(_dt.timezone.utc).date().isoformat()
    existing = ""
    if os.path.exists(path):
        existing = open(path, encoding="utf-8").read()
    body = re.sub(r"\A# [^\n]*\n+", "", existing)
    new = "\n".join(f"* {e}" for e in entries)
    if body.startswith(f"## {date}\n"):
        body = f"## {date}\n{new}\n" + body[len(f"## {date}\n"):]
    else:
        body = f"## {date}\n{new}\n\n{body}"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{body.rstrip()}\n")


def write_module_index(root, module, counts):
    """Module index.md: overview, then acts/regulations by language.
    counts: {(kind, lang): n}"""
    mdir = os.path.join(root, module)
    name = MODULES[module][0]
    entries = [index_entry("Overview", "overview.md", f"Sources, terms of use and coverage for {name}."),
               index_entry("Update log", "log.md", "History of updates to this module.")]
    content = []
    for kind in ("acts", "regulations"):
        langs = [l for l in ("en", "fr") if counts.get((kind, l))]
        if not langs:
            continue
        content.append(index_entry(kind.capitalize(), f"{kind}/",
                                   ", ".join(f"{counts[(kind, l)]} {l.upper()}" for l in langs) + " documents."))
        write_index(os.path.join(mdir, kind), [(f"{name}: {kind}", [
            index_entry(KIND_LABEL[(kind, l)], f"{l}/", f"{counts[(kind, l)]} documents.") for l in langs])])
    write_index(mdir, [(name, entries), ("Contents", content)])


def write_root_index(root):
    """Bundle-root index.md, built from each module's overview.md frontmatter."""
    groups = {}
    for module, (name, _, group) in MODULES.items():
        ov = os.path.join(root, module, "overview.md")
        if not os.path.exists(ov):
            continue
        fm = read_frontmatter(ov)
        groups.setdefault(group, []).append(index_entry(name, f"{module}/", fm.get("description", "")))
    sections = [("Canadian laws", [
        index_entry("Credits and sources", "credits.md",
                    "Who publishes each text, where it comes from, and the terms for reusing it."),
        index_entry("Update log", "log.md", "History of updates to the whole bundle.")])]
    for g in ("Federal", "Provinces", "Territories"):
        if g in groups:
            sections.append((g, groups[g]))
    write_index(root, sections, frontmatter([("okf_version", OKF_VERSION)]))


def slug(s, maxlen=120):
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.replace("C.R.C.", "CRC")
    s = re.sub(r"[^A-Za-z0-9.]+", "-", s)
    s = re.sub(r"\.(?=-|$)", "", s)  # drop dots that end a token ("c." -> "c")
    s = re.sub(r"-{2,}", "-", s).strip("-.")
    return s[:maxlen].rstrip("-.") or "untitled"


# Copyright holder, official site, and reuse terms (summary, not legal advice) per module.
JURISDICTION_INFO = {
    "federal": dict(
        holder="His Majesty the King in Right of Canada", site="https://laws-lois.justice.gc.ca/",
        terms_url="https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/",
        terms="Reproduction of Federal Law Order: anyone may reproduce federal law without charge or permission, "
              "if reproduced accurately and not represented as an official version."),
    "ab": dict(holder="Alberta King's Printer", site="https://kings-printer.alberta.ca",
               terms_url="https://open.alberta.ca/blog/?p=12",
               terms="Statutes and regulations may be reproduced without permission or charge, accurately and "
                     "with Crown copyright acknowledged."),
    "bc": dict(holder="King's Printer for British Columbia", site="https://www.bclaws.gov.bc.ca",
               terms_url="https://www.bclaws.gov.bc.ca/standards/Licence.html",
               terms="King's Printer Licence: reuse allowed with attribution and a \"not an official version\" notice."),
    "mb": dict(holder="King's Printer for Manitoba", site="https://web2.gov.mb.ca/laws/",
               terms_url="https://www.gov.mb.ca/legislature/copyright.html",
               terms="Non-commercial reproduction with acknowledgement; commercial use needs permission."),
    "nb": dict(holder="Government of New Brunswick", site="https://laws.gnb.ca", terms_url="",
               terms="Terms not confirmed."),
    "nl": dict(holder="Government of Newfoundland and Labrador / House of Assembly",
               site="https://www.assembly.nl.ca/legislation/sr/",
               terms_url="https://assembly.nl.ca/CopyrightPrivacyStatement.aspx",
               terms="Excerpts for education, research and review with credit; other uses need the Speaker's approval."),
    "ns": dict(holder="Province of Nova Scotia", site="https://nslegislature.ca/legislative-business/legislative-documents",
               terms_url="https://www.novascotia.ca/copyright",
               terms="Non-commercial reproduction with credit; commercial use needs a licence."),
    "nt": dict(holder="Government of the Northwest Territories", site="https://www.justice.gov.nt.ca/en/legislation/",
               terms_url="", terms="Non-commercial use with acknowledgement; commercial use needs consent."),
    "on": dict(holder="King's Printer for Ontario", site="https://www.ontario.ca/laws",
               terms_url="https://www.ontario.ca/page/copyright-information",
               terms="Statutes and regulations may be reproduced without permission, accurately, credited, and "
                     "marked as not official."),
    "pe": dict(holder="Government of Prince Edward Island", site="https://www.princeedwardisland.ca/en/legislation",
               terms_url="https://www.assembly.pe.ca/copyright",
               terms="Personal use; other uses need written consent."),
    "qc": dict(holder="Gouvernement du Québec", site="https://www.legisquebec.gouv.qc.ca",
               terms_url="https://donneesquebec.ca/recherche/dataset/https-donneesquebec-ca-recherche-dataset-edit-lois-et-reglements-quebec",
               terms="Official bulk data under CC BY-NC-ND 4.0 (credit, non-commercial, no derivatives); see also "
                     "https://www.quebec.ca/droit-auteur."),
    "sk": dict(holder="Office of the King's Printer, Saskatchewan", site="https://publications.saskatchewan.ca",
               terms_url="", terms="Terms not confirmed."),
    "yt": dict(holder="Government of Yukon", site="https://laws.yukon.ca", terms_url="",
               terms="Non-commercial reproduction with credit, accurately and not presented as official; commercial "
                     "use needs permission."),
}
