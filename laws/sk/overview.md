---
type: "Jurisdiction"
title: "Saskatchewan"
description: "506 Acts and 667 regulations of Saskatchewan, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://publications.saskatchewan.ca"
tags: ["sk", "jurisdiction"]
jurisdiction: "sk"
acts_en: 506
acts_fr: 54
regulations_en: 667
regulations_fr: 44
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://publications.saskatchewan.ca"
    title: "Office of the King's Printer, Saskatchewan: official laws website"
    author: "org:sk-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
---

# Saskatchewan

The Acts and regulations of Saskatchewan (Saskatchewan), as published by Office of the King's Printer, Saskatchewan on its
[official laws website](https://publications.saskatchewan.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [506](acts/en/) | [54](acts/fr/) |
| Regulations / Règlements | [667](regulations/en/) | [44](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Office of the King's Printer, Saskatchewan. Terms not confirmed. These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Office of the King's Printer, Saskatchewan: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
