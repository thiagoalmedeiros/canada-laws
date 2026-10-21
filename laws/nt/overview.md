---
type: "Jurisdiction"
title: "Northwest Territories"
description: "239 Acts and 563 regulations of Northwest Territories, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.justice.gov.nt.ca/en/legislation/"
tags: ["nt", "jurisdiction"]
jurisdiction: "nt"
acts_en: 239
acts_fr: 239
regulations_en: 563
regulations_fr: 563
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.justice.gov.nt.ca/en/legislation/"
    title: "Government of the Northwest Territories: official laws website"
    author: "org:nt-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
---

# Northwest Territories

The Acts and regulations of Northwest Territories (Territoires du Nord-Ouest), as published by Government of the Northwest Territories on its
[official laws website](https://www.justice.gov.nt.ca/en/legislation/).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [239](acts/en/) | [239](acts/fr/) |
| Regulations / Règlements | [563](regulations/en/) | [563](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Government of the Northwest Territories. Non-commercial use with acknowledgement; commercial use needs consent. These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Government of the Northwest Territories: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
