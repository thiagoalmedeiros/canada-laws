---
type: "Jurisdiction"
title: "Nova Scotia"
description: "627 Acts and 1507 regulations of Nova Scotia, from the official laws website via the A2AJ dataset. Unofficial; personal and non-commercial use."
resource: "https://nslegislature.ca/legislative-business/legislative-documents"
tags: ["ns", "jurisdiction"]
jurisdiction: "ns"
acts_en: 627
acts_fr: 0
regulations_en: 1507
regulations_fr: 0
status: "stable"
generated: { by: process:canada-laws-provincial-converter }
sources:
  - id: "official"
    resource: "https://nslegislature.ca/legislative-business/legislative-documents"
    title: "Province of Nova Scotia: official laws website"
    author: "org:ns-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
  - id: "terms"
    resource: "https://www.novascotia.ca/copyright"
    title: "Nova Scotia reuse terms"
    author: "org:ns-government"
---

# Nova Scotia

The Acts and regulations of Nova Scotia (Nouvelle-Écosse), as published by Province of Nova Scotia on its
[official laws website](https://nslegislature.ca/legislative-business/legislative-documents).[^official] The texts were collected from that site by the
[A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws).[^a2aj]

| | English | Français |
|---|---|---|
| Acts / Lois | [627](acts/en/) | — |
| Regulations / Règlements | [1507](regulations/en/) | — |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) named after its citation, with the
official page in `resource` and, where both languages exist, a `translation` link to the other
version. Formatting follows the upstream scrape and is plainer than the federal module.

# Terms of use

© Province of Nova Scotia. Non-commercial reproduction with credit; commercial use needs a licence.[^terms] These are unofficial copies provided for personal
and non-commercial use; always check the official version before relying on a provision.

[^official]: Province of Nova Scotia: official laws website
[^a2aj]: A2AJ Canadian Laws dataset
[^terms]: Nova Scotia reuse terms
