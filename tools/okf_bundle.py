#!/usr/bin/env python3
"""Bundle-level maintenance for the OKF bundle in laws/.

    python3 tools/okf_bundle.py credits <bundle>                 # (re)write credits.md and root index.md
    python3 tools/okf_bundle.py log <bundle> <module|.> <entry>  # add a dated entry to a log.md
    python3 tools/okf_bundle.py check <bundle>                   # validate OKF v0.2 conformance (needs PyYAML)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import okf  # noqa: E402

PRODUCER = "process:canada-laws-bundle"


def credits(root):
    rows = []
    srcs = [{"id": "justice-xml", "resource": "https://github.com/justicecanada/laws-lois-xml",
             "title": "Justice Canada consolidated XML (laws-lois-xml)", "author": "org:justice-canada"},
            {"id": "a2aj", "resource": "https://huggingface.co/datasets/a2aj/canadian-laws",
             "title": "A2AJ Canadian Laws dataset", "author": "org:a2aj"}]
    for code, (name, _, _) in okf.MODULES.items():
        info = okf.JURISDICTION_INFO[code]
        terms = info["terms"] + (f" ([terms]({info['terms_url']}))" if info["terms_url"] else "")
        present = os.path.exists(os.path.join(root, code, "overview.md"))
        site = re.sub(r"^https?://(www\.)?", "", info["site"]).rstrip("/")
        label = f"[{name}]({code}/overview.md)" if present else f"{name} (not yet built)"
        rows.append(f"| {label} | {info['holder']} | [{site}]({info['site']}) | {terms} |")
    fm = okf.frontmatter([
        ("type", "Reference"),
        ("title", "Credits and sources"),
        ("description", "Who publishes each text in this bundle, where it was obtained, and the terms for reusing it."),
        ("tags", ["credits", "licence", "sources"]),
        ("status", "stable"),
        ("generated", okf.generated_yaml(PRODUCER, "")),
        ("sources", okf.sources_yaml(srcs)),
    ])
    body = f"""
# Credits and sources

This bundle only converts other people's work into Markdown. All credit for the texts goes to the
governments that write and publish them, and to the projects that make them available in bulk.

> **For personal and non-commercial use only.** These are unofficial copies, not endorsed by or
> affiliated with any government. Only the versions published by each government are official.

# Federal laws

Converted from the official XML published by the Department of Justice Canada in
[justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml).[^justice-xml]
Text © His Majesty the King in Right of Canada, reproduced under the
[Reproduction of Federal Law Order](https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/).

# Provincial and territorial laws

Collected from each government's official site by [Access to Algorithmic Justice (A2AJ)](https://a2aj.ca),
a research project co-hosted by York University's Osgoode Hall Law School and Toronto Metropolitan
University's Lincoln Alexander School of Law, and published as the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj] A2AJ's own work
is MIT-licensed; the texts remain under each government's terms. Nunavut is not included: no
machine-readable source was found.

# Rights holders and terms

| Jurisdiction | Copyright holder / publisher | Official source | Reuse terms (summary, not legal advice) |
|---|---|---|---|
{chr(10).join(rows)}

Rights holders who would like a jurisdiction's texts removed or presented differently can open an
issue on the repository; it will be done promptly.

[^justice-xml]: Justice Canada consolidated XML (laws-lois-xml)
[^a2aj]: A2AJ Canadian Laws dataset
"""
    with open(os.path.join(root, "credits.md"), "w", encoding="utf-8") as f:
        f.write(fm + body)
    okf.write_root_index(root)


def log(root, module, entry):
    if module in (".", ""):
        okf.prepend_log(os.path.join(root, "log.md"), "Canadian laws: update log", [entry])
    else:
        name = okf.MODULES[module][0]
        okf.prepend_log(os.path.join(root, module, "log.md"), f"{name}: update log", [entry])


def check(root):
    import yaml
    problems = []
    n_concepts = n_index = 0
    types = {}
    link_re = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s]+)\)")
    broken = 0
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(d, f)
            text = open(p, encoding="utf-8").read()
            rel = os.path.relpath(p, root)
            if f in ("index.md", "log.md"):
                n_index += 1
                has_fm = text.startswith("---\n")
                if f == "log.md":
                    if has_fm:
                        problems.append(f"{rel}: log.md must not have frontmatter")
                    for h in re.findall(r"^## (.+)$", text, re.M):
                        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", h):
                            problems.append(f"{rel}: log heading not YYYY-MM-DD: {h}")
                elif has_fm:
                    if rel != "index.md":
                        problems.append(f"{rel}: only the bundle-root index.md may have frontmatter")
                    else:
                        fm = yaml.safe_load(text.split("---\n", 2)[1])
                        if set(fm) - {"okf_version"}:
                            problems.append(f"{rel}: root index frontmatter may only carry okf_version")
                ok = ("# ", "## ", "* ") if f == "log.md" else ("# ", "* [", "---", "okf_version")
                for line in text.splitlines():
                    if line and not line.startswith(ok):
                        problems.append(f"{rel}: unexpected line in {f}: {line[:60]}")
                        break
            else:
                n_concepts += 1
                if not text.startswith("---\n"):
                    problems.append(f"{rel}: no frontmatter")
                    continue
                try:
                    fm = yaml.safe_load(text.split("---\n", 2)[1])
                except yaml.YAMLError as e:
                    problems.append(f"{rel}: unparseable frontmatter: {str(e)[:80]}")
                    continue
                if not isinstance(fm, dict) or not fm.get("type"):
                    problems.append(f"{rel}: missing type")
                    continue
                types[fm["type"]] = types.get(fm["type"], 0) + 1
                g = fm.get("generated")
                if g is not None and not (isinstance(g, dict) and g.get("by")):
                    problems.append(f"{rel}: generated.by missing")
                for s in fm.get("sources") or []:
                    if not s.get("resource"):
                        problems.append(f"{rel}: source without resource")
                if fm.get("translation") and not os.path.exists(os.path.normpath(os.path.join(d, fm["translation"]))):
                    problems.append(f"{rel}: translation target missing: {fm['translation']}")
            for target in link_re.findall(text):
                t = target.split("#")[0]
                if not t:
                    continue
                full = os.path.normpath(os.path.join(root, t.lstrip("/")) if t.startswith("/") else os.path.join(d, t))
                if not os.path.exists(full):
                    broken += 1
                    if broken <= 10:
                        problems.append(f"{rel}: broken link {target}")
    print(f"concepts: {n_concepts}  index/log files: {n_index}")
    print("types: " + ", ".join(f"{k}={v}" for k, v in sorted(types.items())))
    print(f"broken links: {broken}")
    print(f"problems: {len(problems)}")
    for p in problems[:40]:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    cmd, root = sys.argv[1], sys.argv[2]
    if cmd == "credits":
        credits(root)
    elif cmd == "log":
        log(root, sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "check":
        sys.exit(check(root))
    else:
        sys.exit(__doc__)
