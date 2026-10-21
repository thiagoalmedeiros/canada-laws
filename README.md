# Canadian laws in Markdown

The consolidated federal, provincial and territorial laws of Canada, converted to Markdown so they can be read, searched, diffed and fed to other tools.

> [!IMPORTANT]
> **For personal and non-commercial use only.** These are unofficial copies, provided for reading, study and research. They are not endorsed by or affiliated with any government, and only the versions published by each government are official. Always check the source link at the top of each file before relying on a provision. If you want to reuse the texts for anything else, check the terms of the jurisdiction concerned (see [Credits and sources](#credits-and-sources)).

## What's here

| Folder | Contents | Source |
|---|---|---|
| [`federal/en/acts`](federal/en/acts/) | 971 federal Acts (English) | [justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml) (official XML) |
| [`federal/en/regulations`](federal/en/regulations/) | 4,898 federal regulations (English) | same |
| [`federal/fr/lois`](federal/fr/lois/) | 971 lois fédérales (français) | same |
| [`federal/fr/reglements`](federal/fr/reglements/) | 4,897 règlements fédéraux (français) | same |
| [`provinces/`](provinces/) | Acts and regulations of AB, BC, MB, NB, NL, NS, NT, ON, PE, QC, SK and YT | [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws), scraped from each official site |

Every folder has a `README.md` index. Nunavut is not included yet (no machine-readable source found).

## Federal files

Converted directly from Justice Canada's official XML with [`tools/federal_to_md.py`](tools/federal_to_md.py). Each file:

- has YAML front matter (title, number, consolidation date, last-amended date, source URL);
- keeps the structure: Parts and Divisions as headings, marginal notes as section headings, then sections, subsections, paragraphs and subparagraphs as nested lists;
- keeps defined terms in ***bold italics***, schedules, tables (Markdown tables, or HTML when cells span rows/columns), formulas, footnotes and the amendment history of each provision (small "History:" lines);
- links cross-references to other federal Acts and regulations within this repo.

File names match the official identifiers (`C-46.md` is the Criminal Code, `SOR-98-106.md` the Federal Courts Rules), so `https://laws-lois.justice.gc.ca/eng/acts/C-46/` corresponds to `federal/en/acts/C-46.md`.

## Provincial files

Taken from the A2AJ dataset (Access to Algorithmic Justice, co-hosted by York University's Osgoode Hall Law School and Toronto Metropolitan University's Lincoln Alexander School of Law), which collects the text from each province's official site. Files are named by citation, with `.fr.md` for French versions where available. The quality depends on the upstream scrape, so formatting is less consistent than the federal files.

## Keeping it current

Two GitHub Actions workflows refresh the content every Monday and can be run by hand from the **Actions** tab:

- **Update federal laws** re-converts from the latest `justicecanada/laws-lois-xml`.
- **Update provincial laws** re-downloads the A2AJ dataset for the jurisdictions in the `PROVINCES` variable (default: all 12), or the ones you type when running it by hand. If Hugging Face ever requires authentication, add a free access token as a repository secret named `HF_TOKEN`.

To run the converters yourself:

```bash
pip install lxml pandas pyarrow requests
git clone --depth 1 https://github.com/justicecanada/laws-lois-xml.git /tmp/laws-lois-xml
python3 tools/federal_to_md.py /tmp/laws-lois-xml .
python3 tools/provincial_to_md.py . AB ON   # or no codes for all
```

## Credits and sources

This project only converts other people's work into Markdown. All credit for the texts goes to the governments that write and publish them, and to the projects that make them available in bulk.

**Federal laws**
- Text © His Majesty the King in Right of Canada, as represented by the Minister of Justice. Official versions: [Justice Laws Website](https://laws-lois.justice.gc.ca/).
- Source data: [justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml), the official XML published by the Department of Justice Canada.
- Reproduced under the [Reproduction of Federal Law Order](https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/), which allows anyone to reproduce federal law without charge or permission, provided it is reproduced accurately and not represented as an official version.

**Provincial and territorial laws**
- Collected by [Access to Algorithmic Justice (A2AJ)](https://a2aj.ca) and published as the [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws) ([tools and documentation](https://github.com/a2aj-ca/canadian-legal-data)). A2AJ's own work is MIT-licensed; the texts remain under each government's terms.
- The texts belong to each government, as listed below. Each file names its official source page and records the licence A2AJ reported in its `upstream_license` field.

| Jurisdiction | Copyright holder / publisher | Official source | Reuse terms (summary, not legal advice) |
|---|---|---|---|
| Alberta | Alberta King's Printer | [kings-printer.alberta.ca](https://kings-printer.alberta.ca) | Statutes and regulations may be reproduced without permission or charge, accurately and with Crown copyright acknowledged. |
| British Columbia | King's Printer for British Columbia | [bclaws.gov.bc.ca](https://www.bclaws.gov.bc.ca) | [King's Printer Licence](https://www.bclaws.gov.bc.ca/standards/Licence.html): reuse allowed with attribution and a "not an official version" notice. |
| Manitoba | King's Printer for Manitoba | [web2.gov.mb.ca/laws](https://web2.gov.mb.ca/laws/) | Non-commercial reproduction with acknowledgement; commercial use needs permission. |
| New Brunswick | Government of New Brunswick | [laws.gnb.ca](https://laws.gnb.ca) | Terms not confirmed. |
| Newfoundland and Labrador | Government of Newfoundland and Labrador / House of Assembly | [assembly.nl.ca](https://www.assembly.nl.ca/legislation/sr/) | [House of Assembly terms](https://assembly.nl.ca/CopyrightPrivacyStatement.aspx): excerpts for education, research and review with credit; other uses need the Speaker's approval. |
| Nova Scotia | Province of Nova Scotia | [nslegislature.ca](https://nslegislature.ca/legislative-business/legislative-documents) | Non-commercial reproduction with credit; commercial use needs a licence. |
| Northwest Territories | Government of the Northwest Territories | [justice.gov.nt.ca](https://www.justice.gov.nt.ca/en/legislation/) | Non-commercial use with acknowledgement; commercial use needs consent. |
| Ontario | King's Printer for Ontario | [ontario.ca/laws](https://www.ontario.ca/laws) | [Ontario copyright terms](https://www.ontario.ca/page/copyright-information): statutes and regulations may be reproduced without permission, accurately, credited, and marked as not official. |
| Prince Edward Island | Government of Prince Edward Island | [princeedwardisland.ca](https://www.princeedwardisland.ca/en/legislation) | [Legislative Assembly terms](https://www.assembly.pe.ca/copyright): personal use; other uses need written consent ([request form](https://www.princeedwardisland.ca/en/service/request-use-of-wordmark-or-copyrighted-material)). |
| Quebec | Gouvernement du Québec | [legisquebec.gouv.qc.ca](https://www.legisquebec.gouv.qc.ca) | Official bulk data under [CC BY-NC-ND 4.0](https://donneesquebec.ca/recherche/dataset/https-donneesquebec-ca-recherche-dataset-edit-lois-et-reglements-quebec) (credit, non-commercial, no derivatives); see also [Québec copyright terms](https://www.quebec.ca/droit-auteur). |
| Saskatchewan | Office of the King's Printer, Saskatchewan | [publications.saskatchewan.ca](https://publications.saskatchewan.ca) | Terms not confirmed. |
| Yukon | Government of Yukon | [laws.yukon.ca](https://laws.yukon.ca) | Non-commercial reproduction with credit, accurately and not presented as official; commercial use needs permission. |

Nunavut is not included: no machine-readable source was found.

**Rights holders:** if you would like a jurisdiction's texts removed or presented differently, please open an issue and it will be done promptly.

## Licence of this repository

The conversion code in `tools/` and `.github/` is MIT-licensed (see [LICENSE](LICENSE)). It does **not** apply to the law texts, which remain under the terms above. The repository is shared for personal and non-commercial use.
