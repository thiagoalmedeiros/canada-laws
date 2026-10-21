---
type: "Jurisdiction"
title: "British Columbia"
description: "573 Acts and 1474 regulations of British Columbia, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.bclaws.gov.bc.ca"
tags: ["bc", "jurisdiction"]
jurisdiction: "bc"
acts_en: 573
acts_fr: 0
regulations_en: 1474
regulations_fr: 0
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.bclaws.gov.bc.ca"
    title: "King's Printer for British Columbia: official laws website"
    author: "org:bc-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://www.bclaws.gov.bc.ca/standards/Licence.html"
    title: "British Columbia reuse terms"
    author: "org:bc-government"
---

# British Columbia

The Acts and regulations of British Columbia (Colombie-Britannique), as published by King's Printer for British Columbia on its
[official laws website](https://www.bclaws.gov.bc.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [573](acts/en/) | — |
| Regulations / Règlements | [1474](regulations/en/) | — |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© King's Printer for British Columbia. King's Printer Licence: reuse allowed with attribution and a "not an official version" notice.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: King's Printer for British Columbia: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: British Columbia reuse terms
