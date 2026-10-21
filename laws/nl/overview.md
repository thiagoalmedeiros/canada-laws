---
type: "Jurisdiction"
title: "Newfoundland and Labrador"
description: "403 Acts and 1665 regulations of Newfoundland and Labrador, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://www.assembly.nl.ca/legislation/sr/"
tags: ["nl", "jurisdiction"]
jurisdiction: "nl"
acts_en: 403
acts_fr: 0
regulations_en: 1665
regulations_fr: 0
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://www.assembly.nl.ca/legislation/sr/"
    title: "Government of Newfoundland and Labrador / House of Assembly: official laws website"
    author: "org:nl-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://assembly.nl.ca/CopyrightPrivacyStatement.aspx"
    title: "Newfoundland and Labrador reuse terms"
    author: "org:nl-government"
---

# Newfoundland and Labrador

The Acts and regulations of Newfoundland and Labrador (Terre-Neuve-et-Labrador), as published by Government of Newfoundland and Labrador / House of Assembly on its
[official laws website](https://www.assembly.nl.ca/legislation/sr/).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [403](acts/en/) | — |
| Regulations / Règlements | [1665](regulations/en/) | — |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Government of Newfoundland and Labrador / House of Assembly. Excerpts for education, research and review with credit; other uses need the Speaker's approval.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Government of Newfoundland and Labrador / House of Assembly: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Newfoundland and Labrador reuse terms
