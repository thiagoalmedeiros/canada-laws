---
type: "Jurisdiction"
title: "Prince Edward Island"
description: "341 Acts and 396 regulations of Prince Edward Island, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.princeedwardisland.ca/en/legislation"
tags: ["pe", "jurisdiction"]
jurisdiction: "pe"
acts_en: 341
acts_fr: 1
regulations_en: 396
regulations_fr: 1
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.princeedwardisland.ca/en/legislation"
    title: "Government of Prince Edward Island: official laws website"
    author: "org:pe-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://www.assembly.pe.ca/copyright"
    title: "Prince Edward Island reuse terms"
    author: "org:pe-government"
---

# Prince Edward Island

The Acts and regulations of Prince Edward Island (Île-du-Prince-Édouard), as published by Government of Prince Edward Island on its
[official laws website](https://www.princeedwardisland.ca/en/legislation).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [341](acts/en/) | [1](acts/fr/) |
| Regulations / Règlements | [396](regulations/en/) | [1](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Government of Prince Edward Island. Personal use; other uses need written consent.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Government of Prince Edward Island: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Prince Edward Island reuse terms
