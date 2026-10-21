---
type: "Jurisdiction"
title: "New Brunswick"
description: "422 Acts and 676 regulations of New Brunswick, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://laws.gnb.ca"
tags: ["nb", "jurisdiction"]
jurisdiction: "nb"
acts_en: 422
acts_fr: 422
regulations_en: 676
regulations_fr: 676
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://laws.gnb.ca"
    title: "Government of New Brunswick: official laws website"
    author: "org:nb-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
---

# New Brunswick

The Acts and regulations of New Brunswick (Nouveau-Brunswick), as published by Government of New Brunswick on its
[official laws website](https://laws.gnb.ca).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [422](acts/en/) | [422](acts/fr/) |
| Regulations / Règlements | [676](regulations/en/) | [676](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Government of New Brunswick. Terms not confirmed. These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Government of New Brunswick: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
