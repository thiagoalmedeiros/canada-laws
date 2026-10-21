---
type: "Jurisdiction"
title: "Quebec"
description: "541 Acts and 2540 regulations of Quebec, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.legisquebec.gouv.qc.ca"
tags: ["qc", "jurisdiction"]
jurisdiction: "qc"
acts_en: 541
acts_fr: 541
regulations_en: 1748
regulations_fr: 2540
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.legisquebec.gouv.qc.ca"
    title: "Gouvernement du Québec: official laws website"
    author: "org:qc-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://donneesquebec.ca/recherche/dataset/https-donneesquebec-ca-recherche-dataset-edit-lois-et-reglements-quebec"
    title: "Quebec reuse terms"
    author: "org:qc-government"
---

# Quebec

The Acts and regulations of Quebec (Québec), as published by Gouvernement du Québec on its
[official laws website](https://www.legisquebec.gouv.qc.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [541](acts/en/) | [541](acts/fr/) |
| Regulations / Règlements | [1748](regulations/en/) | [2540](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Gouvernement du Québec. Official bulk data under CC BY-NC-ND 4.0 (credit, non-commercial, no derivatives); see also https://www.quebec.ca/droit-auteur.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Gouvernement du Québec: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Quebec reuse terms
