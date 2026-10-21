# Canadian laws in Markdown

The consolidated federal, provincial and territorial laws of Canada as an
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
bundle: plain Markdown files with YAML frontmatter, organized in one module per jurisdiction,
ready to read, search, diff, or serve to agents (for example through an MCP server).

> [!IMPORTANT]
> **For personal and non-commercial use only.** These are unofficial copies, provided for reading, study and research. They are not endorsed by or affiliated with any government, and only the versions published by each government are official. Always check the official link in each file before relying on a provision. See [Credits and sources](laws/credits.md) for who publishes each text and their reuse terms.

## What's here

| Module | Acts | Regulations | Source |
|---|---|---|---|
| [`federal`](laws/federal/) | 971 (EN + FR) | 4,897 (EN + FR) | Official XML from [Justice Canada](https://github.com/justicecanada/laws-lois-xml) |
| [`ab`](laws/ab/) Alberta | 442 | 925 | [A2AJ dataset](https://huggingface.co/datasets/a2aj/canadian-laws) |
| [`bc`](laws/bc/) British Columbia | 573 | 1,474 | A2AJ |
| [`mb`](laws/mb/) Manitoba | 516 | 1,091 | A2AJ |
| [`nb`](laws/nb/) New Brunswick | 422 | 676 | A2AJ |
| [`nl`](laws/nl/) Newfoundland and Labrador | 403 | 1,665 | A2AJ |
| [`ns`](laws/ns/) Nova Scotia | 627 | 1,507 | A2AJ |
| [`nt`](laws/nt/) Northwest Territories | 239 | 563 | A2AJ |
| [`on`](laws/on/) Ontario | 856 | 2,217 | A2AJ |
| [`pe`](laws/pe/) Prince Edward Island | 341 | 396 | A2AJ |
| [`qc`](laws/qc/) Quebec | 541 | 2,540 | A2AJ |
| [`sk`](laws/sk/) Saskatchewan | 506 | 667 | A2AJ |
| [`yt`](laws/yt/) Yukon | 279 | 1,355 | A2AJ |

Counts are the larger of the English and French collections; French versions are included wherever the
jurisdiction publishes them. Nunavut is not included (no machine-readable source found).

## Layout

```
laws/                          OKF bundle root
  index.md                     root index (okf_version: "0.2"): lists every module
  log.md                       bundle-wide update history
  credits.md                   type: Reference - publishers, sources, reuse terms
  <module>/                    federal, ab, bc, mb, nb, nl, ns, nt, on, pe, qc, sk, yt
    index.md                   module contents
    log.md                     module update history
    overview.md                type: Jurisdiction - coverage, sources, terms, counts
    acts/
      index.md
      en/  index.md + <id>.md  type: Act        (one concept per law)
      fr/  index.md + <id>.md
    regulations/
      index.md
      en/  ...                 type: Regulation
      fr/  ...
tools/                         converters and bundle tooling (not part of the bundle)
```

Every module has the same shape, so a module can be added, removed or rebuilt on its own.
`index.md` and `log.md` are the OKF reserved files; every other `.md` is a concept with frontmatter.

### Concept frontmatter

```yaml
---
type: "Regulation"                       # Act | Regulation | Jurisdiction | Reference
title: "Federal Courts Rules"
description: "Federal regulation SOR/98-106, made under the Federal Courts Act."
resource: "https://laws-lois.justice.gc.ca/eng/regulations/SOR-98-106/"   # official page
tags: ["federal", "regulation", "en"]
jurisdiction: "federal"
language: "en"
number: "SOR/98-106"                     # provinces use `citation`
current_to: "2025-12-29"                 # federal: consolidation date
translation: "../fr/DORS-98-106.md"      # other-language version, when it exists
status: "stable"
generated: { by: process:canada-laws-federal-converter, at: 2025-12-29T00:00:00Z }
sources:
  - id: "justice-xml"
    resource: "https://github.com/justicecanada/laws-lois-xml/blob/main/eng/regulations/SOR-98-106.xml"
    title: "Justice Canada consolidated XML (laws-lois-xml)"
    author: "org:justice-canada"
    last_modified: "2025-12-29T00:00:00Z"
---
```

The body is the law itself. Federal files keep the full structure: Parts and Divisions as headings,
marginal notes as section headings, numbered sections, subsections and paragraphs as nested lists,
defined terms in ***bold italics***, schedules, tables, formulas, footnotes, amendment history, and
relative links to every other federal law they cite. Provincial files follow the upstream scrape and
are plainer.

## Using it from an MCP server

The bundle is designed to map directly onto a knowledge tree:

| MCP operation | Backed by |
|---|---|
| List jurisdictions | `laws/index.md` (or each `laws/<module>/overview.md` frontmatter) |
| Browse a jurisdiction | `laws/<module>/index.md` → `acts/` / `regulations/` → `en/` / `fr/` |
| List laws in a folder | that folder's `index.md` (`* [Title](file.md) - description`) |
| Read a law | `laws/<module>/<kind>/<lang>/<id>.md` (frontmatter + body) |
| Switch language | the `translation` key |
| Follow citations | relative Markdown links between concepts (federal) |
| Check freshness and provenance | `generated`, `current_to`, `sources`, and each module's `log.md` |

A concept's ID is its path without `.md`, for example `federal/acts/en/C-46` (Criminal Code), which
makes a stable resource URI such as `okf://canada-laws/federal/acts/en/C-46`.

## Keeping it current

Three GitHub Actions workflows maintain the bundle:

- **Update federal laws** (Mondays) rebuilds `laws/federal` from the latest `justicecanada/laws-lois-xml`.
- **Update provincial laws** (Mondays) rebuilds each provincial and territorial module from the A2AJ dataset,
  one module and one commit at a time. Limit it with a repository variable `PROVINCES` (for example `ab bc on`).
  If Hugging Face ever requires authentication, add a free access token as a repository secret named `HF_TOKEN`.
- **Validate OKF bundle** checks every push and pull request for OKF conformance.

Each update adds a dated entry to the module's and the bundle's `log.md`. To run the tools yourself:

```bash
pip install lxml pandas pyarrow requests pyyaml
git clone --depth 1 https://github.com/justicecanada/laws-lois-xml.git /tmp/laws-lois-xml
python3 tools/federal_to_md.py /tmp/laws-lois-xml laws     # rebuild laws/federal
python3 tools/provincial_to_md.py laws ab on               # rebuild some provincial modules (or all)
python3 tools/okf_bundle.py credits laws                   # refresh credits.md and the root index
python3 tools/okf_bundle.py check laws                     # validate OKF conformance
```

## Credits and licence

All credit for the texts goes to the governments that write and publish them: the Department of
Justice Canada for federal laws, and each province and territory for its own. Provincial and
territorial texts were collected by [Access to Algorithmic Justice (A2AJ)](https://a2aj.ca)
(York University's Osgoode Hall Law School and Toronto Metropolitan University's Lincoln Alexander
School of Law). The full list of publishers, sources and reuse terms is in
[laws/credits.md](laws/credits.md).

The code in `tools/` and `.github/` is MIT-licensed (see [LICENSE](LICENSE)); that licence does not
apply to the law texts, which remain under each government's terms. Rights holders who would like a
jurisdiction removed or presented differently can open an issue and it will be done promptly.
