# Canadian laws in Markdown

The consolidated federal, provincial and territorial laws of Canada, converted to Markdown so they can be read, searched, diffed and fed to other tools.

> **These are unofficial copies.** Only the versions published by each government are official. Always check the source link at the top of each file before relying on a provision.

## What's here

| Folder | Contents | Source |
|---|---|---|
| [`federal/en/acts`](federal/en/acts/) | 971 federal Acts (English) | [justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml) (official XML) |
| [`federal/en/regulations`](federal/en/regulations/) | 4,898 federal regulations (English) | same |
| [`federal/fr/lois`](federal/fr/lois/) | 971 lois fédérales (français) | same |
| [`federal/fr/reglements`](federal/fr/reglements/) | 4,897 règlements fédéraux (français) | same |
| [`provinces/`](provinces/) | Acts and regulations of Alberta, British Columbia and Ontario (other provinces available, see below) | [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws), scraped from each official site |

Every folder has a `README.md` index. Nunavut is not included yet (no machine-readable source found).

## Federal files

Converted directly from Justice Canada's official XML with [`tools/federal_to_md.py`](tools/federal_to_md.py). Each file:

- has YAML front matter (title, number, consolidation date, last-amended date, source URL);
- keeps the structure: Parts and Divisions as headings, marginal notes as section headings, then sections, subsections, paragraphs and subparagraphs as nested lists;
- keeps defined terms in ***bold italics***, schedules, tables (Markdown tables, or HTML when cells span rows/columns), formulas, footnotes and the amendment history of each provision (small "History:" lines);
- links cross-references to other federal Acts and regulations within this repo.

File names match the official identifiers (`C-46.md` is the Criminal Code, `SOR-98-106.md` the Federal Courts Rules), so `https://laws-lois.justice.gc.ca/eng/acts/C-46/` corresponds to `federal/en/acts/C-46.md`.

## Provincial files

Taken from the A2AJ dataset (Access to Algorithmic Justice, York University), which collects the text from each province's official site. Files are named by citation, with `.fr.md` for French versions where available. The quality depends on the upstream scrape, so formatting is less consistent than the federal files.

## Keeping it current

Two GitHub Actions workflows refresh the content every Monday and can be run by hand from the **Actions** tab:

- **Update federal laws** re-converts from the latest `justicecanada/laws-lois-xml`.
- **Update provincial laws** re-downloads the A2AJ dataset for the jurisdictions in the `PROVINCES` variable (default AB BC ON), or the ones you type when running it by hand. If Hugging Face ever requires authentication, add a free access token as a repository secret named `HF_TOKEN`.

To run the converters yourself:

```bash
pip install lxml pandas pyarrow requests
git clone --depth 1 https://github.com/justicecanada/laws-lois-xml.git /tmp/laws-lois-xml
python3 tools/federal_to_md.py /tmp/laws-lois-xml .
python3 tools/provincial_to_md.py . AB ON   # or no codes for all
```

## Licences and reuse

The law text belongs to the Crown in right of each government and is reproduced under each one's terms. The conversion scripts in `tools/` are MIT-licensed. **Because this repository is public, it only includes provinces whose terms clearly allow public redistribution (AB, BC, ON).** The converter supports all 12 covered jurisdictions: to include more, set a repository variable `PROVINCES` (Settings → Secrets and variables → Actions → Variables), e.g. `AB BC ON SK`, after checking that jurisdiction's terms.

| Jurisdiction | Terms (summary, not legal advice) |
|---|---|
| Federal | [Reproduction of Federal Law Order](https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/): anyone may reproduce federal laws without charge or permission, if reproduced accurately and not represented as an official version. |
| British Columbia | King's Printer Licence: reuse and redistribution allowed, including commercially, with attribution and a "not an official version" notice. |
| Ontario | Statutes and regulations may be reproduced without permission, accurately, credited to the King's Printer for Ontario, and marked as not official. |
| Alberta | Statutes and regulations may be reproduced without permission or charge, accurately and with Crown copyright acknowledged. |
| Quebec | CC BY-NC-ND 4.0: no commercial use and no derivatives. Converting to Markdown may count as a derivative; get permission before publishing. |
| NS, MB, YT, NT | Generally non-commercial reproduction with credit; commercial use needs permission. |
| PE, NL | Restrictive (personal use / excerpts); written consent needed for wider reproduction. |
| SK, NB | Terms not confirmed. |

Each provincial file also records the licence A2AJ reported for it in its `upstream_license` field.
