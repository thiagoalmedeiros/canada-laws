---
type: "Jurisdiction"
title: "Yukon"
description: "279 Acts and 1355 regulations of Yukon, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://laws.yukon.ca"
tags: ["yt", "jurisdiction"]
jurisdiction: "yt"
acts_en: 279
acts_fr: 279
regulations_en: 1355
regulations_fr: 1353
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://laws.yukon.ca"
    title: "Government of Yukon: official laws website"
    author: "org:yt-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
---

# Yukon

The Acts and regulations of Yukon (Yukon), as published by Government of Yukon on its
[official laws website](https://laws.yukon.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [279](acts/en/) | [279](acts/fr/) |
| Regulations / Règlements | [1355](regulations/en/) | [1353](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Government of Yukon. Non-commercial reproduction with credit, accurately and not presented as official; commercial use needs permission. These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Government of Yukon: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
