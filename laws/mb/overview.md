---
type: "Jurisdiction"
title: "Manitoba"
description: "516 Acts and 1091 regulations of Manitoba, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://web2.gov.mb.ca/laws/"
tags: ["mb", "jurisdiction"]
jurisdiction: "mb"
acts_en: 516
acts_fr: 516
regulations_en: 1091
regulations_fr: 994
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://web2.gov.mb.ca/laws/"
    title: "King's Printer for Manitoba: official laws website"
    author: "org:mb-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://www.gov.mb.ca/legislature/copyright.html"
    title: "Manitoba reuse terms"
    author: "org:mb-government"
---

# Manitoba

The Acts and regulations of Manitoba (Manitoba), as published by King's Printer for Manitoba on its
[official laws website](https://web2.gov.mb.ca/laws/).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [516](acts/en/) | [516](acts/fr/) |
| Regulations / Règlements | [1091](regulations/en/) | [994](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© King's Printer for Manitoba. Non-commercial reproduction with acknowledgement; commercial use needs permission.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: King's Printer for Manitoba: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Manitoba reuse terms
