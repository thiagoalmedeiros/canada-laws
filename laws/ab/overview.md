---
type: "Jurisdiction"
title: "Alberta"
description: "442 Acts and 925 regulations of Alberta, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://kings-printer.alberta.ca"
tags: ["ab", "jurisdiction"]
jurisdiction: "ab"
acts_en: 442
acts_fr: 1
regulations_en: 925
regulations_fr: 0
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://kings-printer.alberta.ca"
    title: "Alberta King's Printer: official laws website"
    author: "org:ab-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://open.alberta.ca/blog/?p=12"
    title: "Alberta reuse terms"
    author: "org:ab-government"
---

# Alberta

The Acts and regulations of Alberta (Alberta), as published by Alberta King's Printer on its
[official laws website](https://kings-printer.alberta.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [442](acts/en/) | [1](acts/fr/) |
| Regulations / Règlements | [925](regulations/en/) | — |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Alberta King's Printer. Statutes and regulations may be reproduced without permission or charge, accurately and with Crown copyright acknowledged.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Alberta King's Printer: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Alberta reuse terms
