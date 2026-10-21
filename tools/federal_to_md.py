#!/usr/bin/env python3
"""Convert Justice Canada consolidated-law XML (justicecanada/laws-lois-xml) to Markdown.

Usage:
    python3 tools/federal_to_md.py <laws-lois-xml checkout> <bundle dir, e.g. laws> [id]

Writes the "federal" module of the OKF bundle (see tools/okf.py):
<bundle>/federal/{acts,regulations}/{en,fr}/<slug>.md, one OKF concept per law,
plus index.md files, the module overview.md and the bundle-root index.md.
Cross-references between laws become relative links; each concept links to its
other-language version through the `translation` key.
"""
import html
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor

from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import okf  # noqa: E402

PRODUCER = "process:canada-laws-federal-converter"

LIMS = "{http://justice.gc.ca/lims}"

SETS = [
    ("en", "acts", "eng/acts", "https://laws-lois.justice.gc.ca/eng/acts/{id}/"),
    ("en", "regulations", "eng/regulations", "https://laws-lois.justice.gc.ca/eng/regulations/{id}/"),
    ("fr", "acts", "fra/lois", "https://laws-lois.justice.gc.ca/fra/lois/{id}/"),
    ("fr", "regulations", "fra/reglements", "https://laws-lois.justice.gc.ca/fra/reglements/{id}/"),
]
XML_URL = "https://github.com/justicecanada/laws-lois-xml/blob/main/{sub}/{file}"

# (lang, kind) -> {source id: slug}, so links only point at files that exist.
EXISTING = {}
# (lang, kind, source id) -> source id of the other-language version
TRANSLATION = {}


def fed_slug(src_id):
    return okf.slug(src_id)

L10N = {
    "en": dict(history="History", repealed="Repealed", footnotes="Footnotes", recent="Recent amendments",
               image="Image", where="where", consolidated="Consolidated", amended="Last amended",
               source="Official source", enabling="Enabling authority", registration="Registration",
               index_acts="Federal Acts (English)", index_regs="Federal Regulations (English)",
               notinforce="not in force",
               notice=("> **Unofficial version.** © His Majesty the King in Right of Canada. Reproduced from the "
                       "[official source]({url}) under the [Reproduction of Federal Law Order]"
                       "(https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/). Only the version on the "
                       "Justice Laws Website is official.")),
    "fr": dict(history="Historique", repealed="Abrogé", footnotes="Notes de bas de page",
               recent="Modifications récentes", image="Image", where="où", consolidated="Codification",
               amended="Dernière modification", source="Source officielle", enabling="Autorité habilitante",
               registration="Enregistrement", index_acts="Lois fédérales (français)",
               index_regs="Règlements fédéraux (français)", notinforce="non en vigueur",
               notice=("> **Version non officielle.** © Sa Majesté le Roi du chef du Canada. Reproduit à partir de la "
                       "[source officielle]({url}) en vertu du [Décret sur la reproduction de la législation fédérale]"
                       "(https://laws-lois.justice.gc.ca/fra/reglements/TR-97-5/). Seule la version du site Web de la "
                       "législation (Justice) fait foi.")),
}

BLOCKS_LIST = ["Paragraph", "Subparagraph", "Clause", "Subclause", "Subsubclause"]


def ln(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else None


def norm(s):
    return re.sub(r"[ \t\r\n\u00a0]+", " ", s)


def wrap(inner, mark):
    """Wrap in Markdown emphasis, falling back to HTML when the text already
    starts/ends with asterisks (which would produce ambiguous runs)."""
    if not inner:
        return ""
    if inner.startswith("*") or inner.endswith("*"):
        tag = {"*": "em", "**": "strong", "***": "strong"}[mark]
        return f"<{tag}>{inner}</{tag}>"
    return f"{mark}{inner}{mark}"


def esc(s):
    # Escape characters that would accidentally become Markdown syntax.
    s = s.replace("\\", "\\\\")
    s = re.sub(r"([*_`\[\]<>|])", r"\\\1", s)
    return s


class Conv:
    def __init__(self, lang, kind, src_id):
        self.lang = lang
        self.kind = kind
        self.id = src_id
        self.t = L10N[lang]
        self.footnotes = []  # (id, text)
        self.fn_seen = set()
        self.head_level = 1  # level of the most recent structural heading
        self.fn_labels = {}
        self.fn_counter = 0

    # ---------------- inline ----------------
    def inline(self, e, table=False):
        """Render an element's mixed content as one line of Markdown."""
        out = [esc(norm(e.text or ""))]
        for c in e:
            r = self.inline_el(c, table)
            tail = esc(norm(c.tail or ""))
            if r.endswith("]") and tail.startswith("("):
                r += " "
            out.append(r)
            out.append(tail)
        return "".join(out)

    def inline_el(self, c, table=False):
        n = ln(c)
        if n is None:
            return ""
        if n in ("Emphasis",):
            inner = self.inline(c, table).strip()
            if not inner:
                return ""
            st = c.get("style", "italic")
            if "bold" in st:
                return wrap(inner, "**")
            if "smallcaps" in st or "regular" in st or "underline" in st:
                return inner
            return wrap(inner, "*")
        if n in ("DefinedTermEn", "DefinedTermFr", "DefinitionEnOnly", "DefinitionFrOnly"):
            inner = self.inline(c, table).strip()
            return wrap(inner, "***")
        if n == "DefinitionRef":
            inner = self.inline(c, table).strip()
            return wrap(inner, "*")
        if n == "XRefExternal":
            inner = self.inline(c, table)
            target = self.xref(c.get("reference-type"), c.get("link"))
            if target and inner.strip():
                return f"[{inner.strip()}]({target})"
            return inner
        if n == "Sup":
            return f"<sup>{self.inline(c, table).strip()}</sup>"
        if n == "Sub":
            return f"<sub>{self.inline(c, table).strip()}</sub>"
        if n == "FootnoteRef":
            fid = c.get("idref")
            label = self.inline(c, table).strip() or "*"
            if fid:
                key = self.fn_key(fid)
                self.fn_labels[key] = label
                return f"[^{key}]"
            return f"<sup>{label}</sup>"
        if n in ("Leader", "LeaderRightJustified"):
            return " … "
        if n == "LineBreak":
            return "<br>"
        if n == "FormBlank":
            inner = self.inline(c, table).strip()
            return " \\_\\_\\_\\_\\_\\_ " + (f"({inner}) " if inner else "")
        if n == "Repealed":
            return self.inline(c, table)
        if n == "Fraction":
            num = c.find("{*}Numerator")
            den = c.find("{*}Denominator")
            a = self.inline(num, table).strip() if num is not None else ""
            b = self.inline(den, table).strip() if den is not None else ""
            return f"({a})/({b})"
        if n in ("MSub",):
            b = c.find("{*}Base"); s = c.find("{*}Subscript")
            return (self.inline(b, table) if b is not None else "") + (f"<sub>{self.inline(s, table)}</sub>" if s is not None else "")
        if n in ("MSup",):
            b = c.find("{*}Base"); s = c.find("{*}Superscript")
            return (self.inline(b, table) if b is not None else "") + (f"<sup>{self.inline(s, table)}</sup>" if s is not None else "")
        if n == "math" or n == "MathML":
            return esc(norm("".join(c.itertext())))
        if n == "ImageGroup":
            return self.image_text(c)
        if n in ("Footnote",):
            had_id = bool(c.get("id"))
            key = self.add_footnote(c)
            return "" if had_id else f"[^{key}]"
        if n in ("HistoricalNote",):
            return ""
        if n in ("PageBreak", "Separator", "colspec"):
            return ""
        # Block elements that sometimes appear inside text-ish places: flatten.
        if n in ("List",):
            return " " + "; ".join(self.inline(i, table).strip() for i in c if ln(i) == "Item") + " "
        return self.inline(c, table)

    def image_text(self, c):
        alt = c.find("{*}AlternateText")
        txt = norm("".join(alt.itertext())).strip() if alt is not None else ""
        cap = c.find("{*}Caption")
        captxt = self.inline(cap).strip() if cap is not None else ""
        desc = c.find("{*}LongDescription")
        desctxt = norm("".join(desc.itertext())).strip() if desc is not None else ""
        out = f"*[{self.t['image']}{': ' + esc(txt) if txt else ''}]*"
        if captxt:
            out = f"**{captxt}** " + out
        if desctxt:
            out += " " + esc(desctxt)
        return out

    def fn_key(self, fid):
        return re.sub(r"[^A-Za-z0-9_-]", "", fid) or "fn"

    def add_footnote(self, f):
        """Register a footnote; returns its key."""
        fid = f.get("id")
        if not fid:
            self.fn_counter += 1
            fid = f"note-{self.fn_counter}"
        key = self.fn_key(fid)
        if key in self.fn_seen:
            return key
        self.fn_seen.add(key)
        parts = []
        for c in f:
            if ln(c) == "Label":
                continue
            if ln(c) == "Footnote":
                self.add_footnote(c)
                continue
            parts.append(self.inline(c).strip())
        self.footnotes.append((key, " ".join(p for p in parts if p)))
        return key

    def xref(self, rtype, link):
        if not link:
            return None
        if rtype == "act":
            kind = "acts"
        elif rtype == "regulation":
            kind = "regulations"
        else:
            return None
        target = EXISTING.get((self.lang, kind), {}).get(link)
        if not target:
            return None
        fname = target + ".md"
        return fname if kind == self.kind else f"../../{kind}/{self.lang}/{fname}"

    # ---------------- blocks ----------------
    def label(self, e):
        lab = e.find("{*}Label")
        if lab is None:
            return ""
        parts = [lab.text or ""]
        for k in lab:
            if ln(k) != "FootnoteRef":
                parts.append("".join(k.itertext()))
            parts.append(k.tail or "")
        return norm("".join(parts)).strip()

    def label_refs(self, e):
        lab = e.find("{*}Label")
        if lab is None:
            return ""
        return "".join(self.inline_el(k) for k in lab.iter("{*}FootnoteRef"))

    def lab_md(self, e, trailing=" "):
        lab = self.label(e)
        refs = self.label_refs(e)
        if not lab and not refs:
            return ""
        return (f"**{esc(lab)}**" if lab else "") + refs + trailing

    def history(self, e):
        notes = []
        for h in e.findall("{*}HistoricalNote"):
            items = [self.inline(i).strip() for i in h.findall("{*}HistoricalNoteSubItem")]
            items = [i for i in items if i]
            if not items:
                txt = self.inline(h).strip()
                if txt:
                    items = [txt]
            notes.extend(items)
        if notes:
            return [f"<sub>{self.t['history']}: {'; '.join(notes)}</sub>", ""]
        return []

    def heading(self, level, text):
        level = max(1, min(6, level))
        text = text.strip()
        if not text:
            return []
        return ["#" * level + " " + text, ""]

    def blocks(self, e, depth=0):
        """Render the block children of e."""
        lines = []
        for c in e:
            lines.extend(self.block(c, depth))
        return lines

    def text_children(self, e):
        """Text-like children rendered as paragraphs."""
        return [self.inline(t).strip() for t in e.findall("{*}Text")]

    def block(self, c, depth=0):
        n = ln(c)
        if n is None:
            return []
        ind = "  " * depth
        if n in ("Label", "MarginalNote", "HistoricalNote", "Identification", "colspec", "PageBreak",
                 "Separator", "RecentAmendments"):
            return []
        if n == "Footnote":
            if c.get("id"):
                self.add_footnote(c)
                return []
            t = " ".join(self.inline(k).strip() for k in c)
            return [ind + f"<sub>{t.strip()}</sub>", ""] if t.strip() else []
        if n == "Heading":
            lvl = int(c.get("level", "1") or 1)
            self.head_level = lvl + 1
            parts = []
            lab = self.label(c)
            if lab:
                parts.append(esc(lab))
            tt = c.find("{*}TitleText")
            if tt is not None:
                parts.append(self.inline(tt).strip())
            out = self.heading(lvl + 1, " — ".join(p for p in parts if p))
            for note in c.findall("{*}Note"):
                t = self.inline(note).strip()
                if t:
                    out += [wrap(t, "*"), ""]
            mn = c.find("{*}MarginalNote")
            if mn is not None and self.inline(mn).strip():
                out += [wrap(self.inline(mn).strip(), "*"), ""]
            return out + self.history(c)
        if n == "Section":
            return self.section(c)
        if n in ("Subsection",):
            return self.unit(c, depth, list_item=False)
        if n in BLOCKS_LIST:
            return self.unit(c, depth, list_item=True)
        if n == "Definition":
            out = []
            for t in c.findall("{*}Text"):
                txt = self.inline(t).strip()
                if txt:
                    out += [ind + txt, ""]
            for k in c:
                kn = ln(k)
                if kn in ("Text", "MarginalNote", "Label"):
                    continue
                out += self.block(k, depth)
            return out
        if n in ("Text",):
            t = self.inline(c).strip()
            return [ind + t, ""] if t else []
        if n.startswith("Continued"):
            out = []
            for t in c:
                if ln(t) == "Text":
                    s = self.inline(t).strip()
                    if s:
                        out += [ind + s, ""]
                else:
                    out += self.block(t, depth)
            return out
        if n == "Repealed":
            t = self.inline(c).strip()
            return [ind + t, ""] if t else []
        if n in ("List",):
            out = []
            for item in c:
                if ln(item) != "Item":
                    out += self.block(item, depth)
                    continue
                sub = self.blocks(item, depth + 1)
                sub = [s for s in sub]
                # first non-empty line becomes the bullet
                first = next((i for i, s in enumerate(sub) if s.strip()), None)
                if first is None:
                    if self.lab_md(item, ""):
                        out += [ind + "- " + self.lab_md(item, ""), ""]
                    continue
                sub[first] = ind + "- " + self.lab_md(item) + sub[first].strip()
                out += sub
            return out + [""]
        if n == "Provision":
            out = []
            lab = self.label(c)
            mn = c.find("{*}MarginalNote")
            if mn is not None and self.inline(mn).strip():
                out += [ind + wrap(self.inline(mn).strip(), "*"), ""]
            heads = c.findall("{*}ProvisionHeading")
            for h in heads:
                t = self.inline(h).strip()
                if t:
                    out += [ind + f"**{t}**", ""]
            texts = [self.inline(t).strip() for t in c.findall("{*}Text")]
            texts = [t for t in texts if t]
            if texts:
                first = self.lab_md(c) + texts[0]
                out += [ind + first, ""]
                out += sum(([ind + t, ""] for t in texts[1:]), [])
            elif self.lab_md(c, ""):
                out += [ind + self.lab_md(c, ""), ""]
            for k in c:
                if ln(k) in ("Text", "Label", "ProvisionHeading", "MarginalNote", "HistoricalNote"):
                    continue
                out += self.block(k, depth + (1 if c.get("list-item") == "yes" else 0))
            return out + self.history(c)
        if n in ("Schedule", "DocumentInternal", "FormGroup", "BillPiece", "RegulationPiece",
                 "RelatedOrNotInForce", "ConventionAgreementTreaty", "Group", "Group1-Part",
                 "Group2-Division", "Group3-Subdivision", "Body", "Order", "Introduction", "Preamble",
                 "Enacts", "AmendedContent", "SignatureBlock", "ReadAsContent"):
            return self.container(c, depth)
        if n == "BilingualGroup":
            return self.bilingual(c, depth)
        if n in ("BilingualItemEn", "BilingualItemFr"):
            t = self.inline(c).strip()
            return [ind + t, ""] if t else []
        if n == "Reserved":
            t = self.inline(c).strip()
            return [ind + t, ""] if t else []
        if n == "Oath":
            inner = self.container(c, 0)
            if c.text and c.text.strip():
                inner = [esc(norm(c.text)).strip(), ""] + inner
            return [("> " + l) if l else ">" for l in inner] + [""]
        if n in ("ScheduleFormHeading", "GroupHeading"):
            parts = []
            lab = self.label(c)
            if lab:
                parts.append(esc(lab))
            for tt in c.findall("{*}TitleText"):
                if self.inline(tt).strip():
                    parts.append(self.inline(tt).strip())
            out = self.heading(2 if n == "ScheduleFormHeading" else self.head_level + 1, " — ".join(parts))
            o = c.find("{*}OriginatingRef")
            if o is not None and self.inline(o).strip():
                out += [f"*{self.inline(o).strip()}*", ""]
            return out
        if n in ("AmendedText", "ReadAsText", "QuotedText"):
            inner = self.blocks(c, 0)
            return [("> " + l) if l else ">" for l in inner] + [""]
        if n == "SectionPiece":
            return self.section(c, piece=True)
        if n == "TableGroup":
            return self.table_group(c, depth)
        if n == "FormulaGroup":
            return self.formula_group(c, depth)
        if n == "ImageGroup":
            out = [ind + self.image_text(c), ""]
            cap = c.find("{*}Caption")
            return out
        if n in ("SignatureName", "SignatureTitle", "SignatureLine"):
            t = self.inline(c).strip()
            return [ind + t, ""] if t else []
        if n in ("ProvisionHeading", "TitleText", "Caption", "title", "Note", "ReaderNote"):
            t = self.inline(c).strip()
            return [ind + f"*{t}*", ""] if t else []
        # Fallback: if it has block children recurse, otherwise render as text paragraph.
        if any(ln(k) in ("Text", "Provision", "Section", "Paragraph", "List", "TableGroup") for k in c):
            return self.container(c, depth)
        t = self.inline(c).strip()
        return [ind + t, ""] if t else []

    def bilingual(self, g, depth):
        ind = "  " * depth
        out = []
        pend = None
        for k in g:
            kn = ln(k)
            if kn == "BilingualItemEn":
                if pend is not None:
                    out += [ind + "- " + pend, ""]
                pend = self.inline(k).strip()
            elif kn == "BilingualItemFr":
                fr = self.inline(k).strip()
                pair = " — ".join(x for x in (pend, fr) if x)
                if pair:
                    out += [ind + "- " + pair, ""]
                pend = None
            elif kn == "TitleText":
                t = self.inline(k).strip()
                if t:
                    out += [ind + f"**{t}**", ""]
            else:
                out += self.block(k, depth)
        if pend:
            out += [ind + "- " + pend, ""]
        return out

    def container(self, c, depth):
        out = []
        n = ln(c)
        if n in ("Schedule",):
            self.head_level = 2
        for k in c:
            out += self.block(k, depth)
        out += self.history(c)
        return out

    def section(self, s, piece=False):
        out = []
        mn = s.find("{*}MarginalNote")
        if mn is not None:
            t = self.inline(mn).strip()
            if t:
                out += self.heading(min(6, self.head_level + 1), t)
        lab = self.label(s)
        first_done = False
        pending_label = self.lab_md(s)
        for k in s:
            kn = ln(k)
            if kn in ("MarginalNote", "Label", "HistoricalNote"):
                continue
            if kn == "Text":
                t = self.inline(k).strip()
                if t or pending_label:
                    out += [pending_label + t, ""]
                    pending_label = ""
                continue
            if kn == "Subsection" and pending_label:
                sub = self.unit(k, 0, list_item=False, prefix=pending_label)
                pending_label = ""
                out += sub
                continue
            if pending_label and kn in ("Definition", "Paragraph", "Repealed"):
                out += [pending_label.strip(), ""]
                pending_label = ""
            out += self.block(k, 0)
        if pending_label:
            out += [pending_label.strip(), ""]
        out += self.history(s)
        return out

    def unit(self, e, depth, list_item, prefix=""):
        """Subsection / Paragraph / Subparagraph / Clause..."""
        out = []
        ind = "  " * depth
        lab = self.label(e)
        mn = e.find("{*}MarginalNote")
        if mn is not None:
            t = self.inline(mn).strip()
            if t:
                out += [(ind if list_item else "") + wrap(t, "*"), ""]
        labtxt = self.lab_md(e)
        if e.get("in-force") == "no":
            labtxt += f"*[{self.t['notinforce']}]* "
        head = prefix + labtxt
        bullet = "- " if list_item else ""
        first = True
        for k in e:
            kn = ln(k)
            if kn in ("MarginalNote", "Label", "HistoricalNote"):
                continue
            if kn == "Text":
                t = self.inline(k).strip()
                if first:
                    out += [ind + bullet + head + t, ""]
                    first = False
                else:
                    out += [ind + ("  " if list_item else "") + t, ""]
                continue
            if first:
                out += [ind + bullet + head.strip(), ""]
                first = False
            if kn in BLOCKS_LIST:
                out += self.unit(k, depth + 1 if list_item else depth, True)
            elif kn == "Paragraph":
                out += self.unit(k, depth, True)
            else:
                sub = self.block(k, depth + (1 if list_item else 0))
                out += sub
        if first and head.strip():
            out += [ind + bullet + head.strip(), ""]
        out += self.history(e)
        return out

    # ---------------- formulas ----------------
    def formula_group(self, g, depth):
        ind = "  " * depth
        out = []
        for k in g:
            kn = ln(k)
            if kn == "Formula":
                ft = k.find("{*}FormulaText")
                txt = self.inline(ft).strip() if ft is not None else self.inline(k).strip()
                if txt:
                    out += [ind + f"> {txt}", ""]
            elif kn == "FormulaConnector":
                t = self.inline(k).strip()
                if t:
                    out += [ind + t, ""]
            elif kn == "FormulaDefinition":
                out += self.formula_def(k, depth)
            else:
                out += self.block(k, depth)
        return out

    def formula_def(self, d, depth):
        ind = "  " * depth
        out = []
        term = d.find("{*}FormulaTerm")
        tt = self.inline(term).strip() if term is not None else ""
        first = True
        for k in d:
            kn = ln(k)
            if kn == "FormulaTerm":
                continue
            if kn == "Text":
                t = self.inline(k).strip()
                if first:
                    out += [ind + f"- **{tt}** {t}", ""]
                    first = False
                else:
                    out += [ind + "  " + t, ""]
            elif kn in ("FormulaParagraph", "ContinuedFormulaParagraph"):
                if first:
                    out += [ind + f"- **{tt}**", ""]
                    first = False
                out += self.formula_par(k, depth + 1)
            else:
                if first:
                    out += [ind + f"- **{tt}**", ""]
                    first = False
                out += self.block(k, depth + 1)
        if first and tt:
            out += [ind + f"- **{tt}**", ""]
        return out

    def formula_par(self, p, depth):
        ind = "  " * depth
        out = []
        lab = self.label(p)
        first = True
        for k in p:
            kn = ln(k)
            if kn == "Label":
                continue
            if kn == "Text":
                t = self.inline(k).strip()
                if ln(p).startswith("Continued"):
                    out += [("  " * max(depth - 1, 0)) + "  " + t, ""]
                elif first:
                    out += [ind + f"- {self.lab_md(p)}{t}", ""]
                    first = False
                else:
                    out += [ind + "  " + t, ""]
            elif kn in ("FormulaParagraph", "ContinuedFormulaParagraph"):
                out += self.formula_par(k, depth + 1)
            else:
                out += self.block(k, depth + 1)
        return out

    # ---------------- tables ----------------
    def cell(self, entry):
        parts = []
        if entry.text and entry.text.strip():
            parts.append(esc(norm(entry.text)).strip())
        for k in entry:
            kn = ln(k)
            if kn in ("Provision", "List", "TableGroup", "FormulaGroup", "BilingualGroup", "Repealed",
                      "SignatureBlock", "Text", "Language", "ImageGroup", "Definition", "Heading",
                      "GroupHeading", "ScheduleFormHeading", "Group", "Section", "Paragraph"):
                lines = [cell_line(l) for l in self.block(k, 0) if l.strip()]
                if kn in ("Language", "Repealed", "Text") and not lines:
                    lines = [self.inline(k).strip()]
                parts.append("<br>".join(l for l in lines if l))
            else:
                parts.append(self.inline_el(k, True).strip())
            if k.tail and k.tail.strip():
                parts.append(esc(norm(k.tail)).strip())
        txt = " ".join(p for p in parts if p)
        return txt.replace("|", "\\|").replace("\n", " ")

    def table_group(self, tg, depth):
        out = []
        for k in tg:
            kn = ln(k)
            if kn == "table":
                out += self.table(k)
            elif kn in ("Caption", "title"):
                t = self.inline(k).strip()
                if t:
                    out += [f"**{t}**", ""]
            elif kn == "Footnote":
                self.add_footnote(k)
            else:
                out += self.block(k, depth)
        return out

    def table(self, t):
        out = []
        title = t.find("{*}title")
        if title is not None and self.inline(title).strip():
            out += [f"**{self.inline(title).strip()}**", ""]
        for tgroup in t.findall("{*}tgroup"):
            out += self.tgroup(tgroup)
        return out

    def tgroup(self, tg):
        cols = [c.get("colname") for c in tg.findall("{*}colspec")]
        ncols = int(tg.get("cols") or len(cols) or 1)
        head_rows = [r for th in tg.findall("{*}thead") for r in th.findall("{*}row")]
        body_rows = [r for tb in tg.findall("{*}tbody") for r in tb.findall("{*}row")]
        complex_ = False
        for r in head_rows + body_rows:
            for e in r.findall("{*}entry"):
                if e.get("morerows") or e.get("namest"):
                    complex_ = True
            if len(r.findall("{*}entry")) != ncols:
                complex_ = True
        if len(head_rows) > 1:
            complex_ = True
        if not complex_:
            hdr = [self.cell(e) for e in head_rows[0].findall("{*}entry")] if head_rows else [""] * ncols
            lines = ["| " + " | ".join(hdr) + " |", "|" + "---|" * ncols]
            for r in body_rows:
                lines.append("| " + " | ".join(self.cell(e) for e in r.findall("{*}entry")) + " |")
            return lines + [""]
        # HTML fallback for spans
        def span_attrs(e):
            a = ""
            if e.get("morerows"):
                a += f' rowspan="{int(e.get("morerows")) + 1}"'
            if e.get("namest") and e.get("nameend") and cols:
                try:
                    span = cols.index(e.get("nameend")) - cols.index(e.get("namest")) + 1
                    if span > 1:
                        a += f' colspan="{span}"'
                except ValueError:
                    pass
            return a
        lines = ["<table>"]
        if head_rows:
            lines.append("<thead>")
            for r in head_rows:
                lines.append("<tr>" + "".join(f"<th{span_attrs(e)}>{self.cell_html(e)}</th>" for e in r.findall("{*}entry")) + "</tr>")
            lines.append("</thead>")
        lines.append("<tbody>")
        for r in body_rows:
            lines.append("<tr>" + "".join(f"<td{span_attrs(e)}>{self.cell_html(e)}</td>" for e in r.findall("{*}entry")) + "</tr>")
        lines.append("</tbody>")
        lines.append("</table>")
        return lines + [""]

    def cell_html(self, e):
        # Markdown inside raw HTML blocks isn't rendered by GitHub, so convert the
        # few markers we emit to HTML.
        s = self.cell(e).replace("\\|", "|")
        s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\\*])\*(?!\s)(.+?)(?<![\\\s])\*", r"<i>\1</i>", s)
        s = re.sub(r"\[\^([^\]]+)\]",
                   lambda m: f'<sup><a href="#user-content-fn-{m.group(1)}">{html.escape(self.fn_labels.get(m.group(1), "*"))}</a></sup>', s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\\([*_`\[\]<>|\\])", lambda m: html.escape(m.group(1)), s)
        return s

    # ---------------- document ----------------
    def convert(self, root, src_url):
        n = ln(root)
        ident = root.find("{*}Identification")
        g = lambda tag: (self.inline(ident.find("{*}" + tag)).strip() if ident is not None and ident.find("{*}" + tag) is not None else "")
        short = g("ShortTitle")
        long_ = g("LongTitle")
        title = short or long_ or self.id
        number = ""
        if ident is not None:
            ch = ident.find("{*}Chapter")
            if ch is not None:
                parts = []
                for x in ch:
                    if ln(x) == "ConsolidatedNumber":
                        parts.append(norm("".join(x.itertext())).strip())
                    elif ln(x) == "AnnualStatuteId":
                        num = norm(x.findtext("{*}AnnualStatuteNumber") or "").strip()
                        yr = norm("".join(y.text or "" for y in x.iter("{*}YYYY"))).strip()
                        c = "c." if self.lang == "en" else "ch."
                        parts.append(f"{yr}, {c} {num}" if yr and num else norm("".join(x.itertext())).strip())
                number = "; ".join(p for p in parts if p)
            inum = ident.find("{*}InstrumentNumber")
            if inum is not None:
                number = norm("".join(inum.itertext())).strip()
        cur = root.get(LIMS + "current-date") or ""
        last = root.get(LIMS + "lastAmendedDate") or ""
        is_act = n == "Statute"
        in_force = root.get("in-force", "yes")
        enabling = ""
        if ident is not None and ident.find("{*}EnablingAuthority") is not None:
            enabling = strip_md(self.inline(ident.find("{*}EnablingAuthority")).strip())
        if is_act:
            desc = strip_md(long_) if long_ and long_ != title else (
                f"Federal Act {number}." if self.lang == "en" else f"Loi fédérale {number}.")
        else:
            if self.lang == "en":
                desc = f"Federal regulation {number}" + (f", made under the {enabling.title() if enabling.isupper() else enabling}" if enabling else "") + "."
            else:
                desc = f"Règlement fédéral {number}" + (f", pris en vertu de : {enabling.title() if enabling.isupper() else enabling}" if enabling else "") + "."
        other = TRANSLATION.get((self.lang, self.kind, self.id))
        other_lang = "fr" if self.lang == "en" else "en"
        other_slug = EXISTING.get((other_lang, self.kind), {}).get(other) if other else None
        tags = ["federal", "act" if is_act else "regulation", self.lang]
        if in_force == "no":
            tags.append("not-in-force")
        sub = {(l, k): sb for l, k, sb, _ in SETS}[(self.lang, self.kind)]
        fm = okf.frontmatter([
            ("type", "Act" if is_act else "Regulation"),
            ("title", strip_md(title)),
            ("description", desc),
            ("resource", src_url),
            ("tags", tags),
            ("jurisdiction", "federal"),
            ("language", self.lang),
            ("number", number),
            ("source_id", self.id),
            ("current_to", cur),
            ("last_amended", last),
            ("in_force", in_force != "no"),
            ("translation", f"../{other_lang}/{other_slug}.md" if other_slug else ""),
            ("status", "stable"),
            ("generated", okf.generated_yaml(PRODUCER, okf.iso_date(cur))),
            ("sources", okf.sources_yaml([
                {"id": "justice-xml", "resource": XML_URL.format(sub=sub, file=self.id + ".xml"),
                 "title": "Justice Canada consolidated XML (laws-lois-xml)", "author": "org:justice-canada",
                 "last_modified": okf.iso_date(cur)},
                {"id": "justice-laws", "resource": src_url, "title": "Justice Laws Website",
                 "author": "org:justice-canada", "last_modified": okf.iso_date(last)},
            ])),
        ]).split("\n")
        body = [f"# {title}", ""]
        if long_ and long_ != title:
            body += [f"*{long_}*", ""]
        meta = []
        if number:
            meta.append(esc(number))
        if cur:
            meta.append(f"{self.t['consolidated']}: {cur}")
        if last:
            meta.append(f"{self.t['amended']}: {last}")
        if meta:
            body += [" · ".join(meta), ""]
        if ident is not None:
            ea = ident.find("{*}EnablingAuthority")
            if ea is not None and self.inline(ea).strip():
                body += [f"{self.t['enabling']}: {self.inline(ea).strip()}", ""]
            rd = ident.find("{*}RegistrationDate")
            if rd is not None:
                d = rd.find("{*}Date")
                if d is not None:
                    body += [f"{self.t['registration']}: {date_str(d)}", ""]
            for rn in ident.findall("{*}ReaderNote"):
                t = self.inline(rn).strip()
                if t:
                    body += [f"> {t}", ""]
            rmo = ident.find("{*}RegulationMakerOrder")
            if rmo is not None:
                parts = []
                for x in rmo:
                    d = x.find("{*}Date") if ln(x) != "Date" else x
                    if ln(x) == "Date":
                        parts.append(date_str(x))
                    else:
                        parts.append(norm("".join(x.itertext())).strip())
                t = " ".join(p for p in parts if p)
                if t.strip():
                    body += [esc(t.strip()), ""]
        body += [self.t["notice"].format(url=src_url), ""]
        self.head_level = 1
        for k in root:
            kn = ln(k)
            if kn in ("Identification", "RecentAmendments"):
                continue
            body += self.block(k, 0)
        ra = root.find("{*}RecentAmendments")
        if ra is not None:
            items = []
            for a in ra.findall("{*}Amendment"):
                cit = a.find("{*}AmendmentCitation"); dt = a.find("{*}AmendmentDate")
                items.append("- " + " ".join(x for x in [self.inline(cit).strip() if cit is not None else "",
                                                         norm("".join(dt.itertext())).strip() if dt is not None else ""] if x))
            if items:
                body += [f"## {self.t['recent']}", ""] + items + [""]
        if self.footnotes:
            body += ["---", ""]
            for key, txt in self.footnotes:
                body += [f"[^{key}]: {txt or ' '}", ""]
        text = "\n".join(fm + [""] + body)
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Drop empty blockquote runs left by empty amended text.
        text = re.sub(r"(\n>\n)+(\n|$)", r"\n\2", text)
        return text.rstrip() + "\n", title, number, cur


def cell_line(l):
    """Turn one rendered block line into something that fits in a table cell."""
    l = l.strip()
    m = re.match(r"^#{1,6} (.*)", l)
    if m:
        return f"**{m.group(1)}**"
    if l.startswith("- "):
        return "• " + l[2:]
    if l.startswith("> "):
        return l[2:]
    return l


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\\", "").replace("*", "")
    return s


def yaml_str(s):
    return '"' + (s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def date_str(d):
    y = d.findtext("{*}YYYY") or ""; m = d.findtext("{*}MM") or ""; dd = d.findtext("{*}DD") or ""
    try:
        return f"{int(y):04d}-{int(m):02d}-{int(dd):02d}"
    except ValueError:
        return " ".join(x for x in (y, m, dd) if x)


def work(args):
    path, out_path, lang, kind, src_url, existing, translation = args
    EXISTING.update(existing)
    TRANSLATION.update(translation)
    src_id = os.path.splitext(os.path.basename(path))[0]
    try:
        root = etree.parse(path, etree.XMLParser(huge_tree=True, remove_comments=True)).getroot()
        conv = Conv(lang, kind, src_id)
        text, title, number, cur = conv.convert(root, src_url)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        fm = okf.read_frontmatter(out_path)
        return (src_id, strip_md(title), fm.get("description", ""), root.get("in-force", "yes"), None)
    except Exception as ex:  # keep going; report at the end
        return (src_id, "", "", "", f"{type(ex).__name__}: {ex}")


def load_translations(src):
    """Pair English and French versions using Justice Canada's lookup.xml."""
    pairs = {}
    # Acts share the same consolidated number (and file name) in both languages.
    for f in os.listdir(os.path.join(src, "eng/acts")):
        if f.endswith(".xml") and os.path.exists(os.path.join(src, "fra/lois", f)):
            pairs[("en", "acts", f[:-4])] = f[:-4]
            pairs[("fr", "acts", f[:-4])] = f[:-4]
    # Regulations: <Regulation id=".." olid=".."><AlphaNumber>SOR/2007-151</AlphaNumber>
    lk = etree.parse(os.path.join(src, "lookup", "lookup.xml")).getroot()
    regs = {}
    for r in lk.iter("{*}Regulation"):
        an = r.findtext("{*}AlphaNumber") or ""
        regs[r.get("id")] = (r.findtext("{*}Language"), an.replace("/", "-").replace(" ", "_"), r.get("olid"))
    for rid, (lang, fid, olid) in regs.items():
        if olid in regs:
            pairs[(lang, "regulations", fid)] = regs[olid][1]
    return pairs


def main():
    src, out = sys.argv[1], sys.argv[2]
    only = sys.argv[3] if len(sys.argv) > 3 else None
    existing = {}
    for lang, kind, sub, url in SETS:
        d = os.path.join(src, sub)
        existing[(lang, kind)] = {f[:-4]: fed_slug(f[:-4]) for f in os.listdir(d) if f.endswith(".xml")}
    translation = load_translations(src)
    mdir = os.path.join(out, "federal")
    jobs = []
    for lang, kind, sub, url in SETS:
        od = os.path.join(mdir, kind, lang)
        if not only and os.path.isdir(od):
            import shutil
            shutil.rmtree(od)  # full rebuild so repealed laws disappear
        os.makedirs(od, exist_ok=True)
        for f in sorted(os.listdir(os.path.join(src, sub))):
            if not f.endswith(".xml"):
                continue
            sid = f[:-4]
            if only and sid != only:
                continue
            jobs.append((os.path.join(src, sub, f), os.path.join(od, fed_slug(sid) + ".md"), lang, kind,
                         url.format(id=sid), existing, translation))
    results = {}
    errors = []
    with ProcessPoolExecutor() as ex:
        for job, res in zip(jobs, ex.map(work, jobs, chunksize=16)):
            key = (job[3], job[2])
            results.setdefault(key, []).append(res)
            if res[4]:
                errors.append((job[0], res[4]))
    if not only:
        write_indexes(out, results, existing)
    print(f"converted {len(jobs) - len(errors)} / {len(jobs)}")
    for p, e in errors[:50]:
        print("ERROR", p, e)
    if errors:
        sys.exit(1)


def sort_key(title):
    import unicodedata
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    return re.sub(r"^(an |a |the |l'|la |le |les )", "", t)


def write_indexes(out, results, existing):
    mdir = os.path.join(out, "federal")
    counts = {}
    for (kind, lang), rows in results.items():
        rows = sorted((r for r in rows if not r[4]), key=lambda r: sort_key(r[1]))
        counts[(kind, lang)] = len(rows)
        in_force = [r for r in rows if r[3] != "no"]
        not_in_force = [r for r in rows if r[3] == "no"]
        ent = lambda r: okf.index_entry(r[1], existing[(lang, kind)][r[0]] + ".md", r[2])
        heading = {("acts", "en"): "Federal Acts", ("acts", "fr"): "Lois fédérales",
                   ("regulations", "en"): "Federal Regulations", ("regulations", "fr"): "Règlements fédéraux"}[(kind, lang)]
        sections = [(heading, [ent(r) for r in in_force])]
        if not_in_force:
            sections.append(("Not in force" if lang == "en" else "Non en vigueur", [ent(r) for r in not_in_force]))
        okf.write_index(os.path.join(mdir, kind, lang), sections)
    write_overview(mdir, counts)
    okf.write_module_index(out, "federal", counts)
    okf.write_root_index(out)


def write_overview(mdir, counts):
    acts = counts.get(("acts", "en"), 0)
    regs = counts.get(("regulations", "en"), 0)
    fm = okf.frontmatter([
        ("type", "Jurisdiction"),
        ("title", "Canada (federal)"),
        ("description", f"{acts} consolidated federal Acts and {regs} regulations, in English and French, "
                        "converted from Justice Canada's official XML."),
        ("resource", "https://laws-lois.justice.gc.ca/"),
        ("tags", ["federal", "jurisdiction"]),
        ("jurisdiction", "federal"),
        ("acts_en", acts), ("acts_fr", counts.get(("acts", "fr"), 0)),
        ("regulations_en", regs), ("regulations_fr", counts.get(("regulations", "fr"), 0)),
        ("status", "stable"),
        ("generated", okf.generated_yaml(PRODUCER, "")),
        ("sources", okf.sources_yaml([
            {"id": "justice-xml", "resource": "https://github.com/justicecanada/laws-lois-xml",
             "title": "Justice Canada consolidated XML (laws-lois-xml)", "author": "org:justice-canada"},
            {"id": "reproduction-order", "resource": "https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/",
             "title": "Reproduction of Federal Law Order (SI/97-5)", "author": "org:justice-canada"},
        ])),
    ])
    body = f"""
# Canada (federal)

The consolidated Acts and regulations of Canada, as published by the Department of Justice on the
[Justice Laws Website](https://laws-lois.justice.gc.ca/). Each concept is converted from the official
XML in [justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml).[^justice-xml]

| | English | Français |
|---|---|---|
| Acts / Lois | [{acts}](acts/en/) | [{counts.get(("acts", "fr"), 0)}](acts/fr/) |
| Regulations / Règlements | [{regs}](regulations/en/) | [{counts.get(("regulations", "fr"), 0)}](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) with its official URL in `resource`,
its consolidation date in `current_to`, and a `translation` link to the other-language version.
File names follow the official identifiers (`C-46` is the Criminal Code; `SOR-98-106` the Federal
Courts Rules; `C.R.C., c. 870` becomes `CRC-c-870`); the original identifier is kept in `source_id`.

# Terms of use

© His Majesty the King in Right of Canada. Reproduced under the Reproduction of Federal Law
Order,[^reproduction-order] which allows anyone to reproduce federal law without charge or
permission, provided it is reproduced accurately and not represented as an official version.
These are unofficial copies; only the Justice Laws Website versions are official.

[^justice-xml]: Justice Canada consolidated XML (laws-lois-xml)
[^reproduction-order]: Reproduction of Federal Law Order (SI/97-5)
"""
    with open(os.path.join(mdir, "overview.md"), "w", encoding="utf-8") as f:
        f.write(fm + body)


if __name__ == "__main__":
    main()
