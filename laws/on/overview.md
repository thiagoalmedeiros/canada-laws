---
type: "Jurisdiction"
title: "Ontario"
description: "856 Acts and 2217 regulations of Ontario, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.ontario.ca/laws"
tags: ["on", "jurisdiction"]
jurisdiction: "on"
acts_en: 856
acts_fr: 855
regulations_en: 2217
regulations_fr: 1575
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.ontario.ca/laws"
    title: "King's Printer for Ontario: official laws website"
    author: "org:on-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://www.ontario.ca/page/copyright-information"
    title: "Ontario reuse terms"
    author: "org:on-government"
---

# Ontario

The Acts and regulations of Ontario (Ontario), as published by King's Printer for Ontario on its
[official laws website](https://www.ontario.ca/laws).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [856](acts/en/) | [855](acts/fr/) |
| Regulations / Règlements | [2217](regulations/en/) | [1575](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© King's Printer for Ontario. Statutes and regulations may be reproduced without permission, accurately, credited, and marked as not official.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: King's Printer for Ontario: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Ontario reuse terms
