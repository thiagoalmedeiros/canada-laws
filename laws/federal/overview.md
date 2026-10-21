---
type: "Jurisdiction"
title: "Canada (federal)"
description: "971 consolidated federal Acts and 4897 regulations, in English and French, converted from Justice Canada's official XML."
resource: "https://laws-lois.justice.gc.ca/"
tags: ["federal", "jurisdiction"]
jurisdiction: "federal"
acts_en: 971
acts_fr: 971
regulations_en: 4897
regulations_fr: 4897
status: "stable"
generated: { by: process:canada-laws-federal-converter }
sources:
  - id: "justice-xml"
    resource: "https://github.com/justicecanada/laws-lois-xml"
    title: "Justice Canada consolidated XML (laws-lois-xml)"
    author: "org:justice-canada"
  - id: "reproduction-order"
    resource: "https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/"
    title: "Reproduction of Federal Law Order (SI/97-5)"
    author: "org:justice-canada"
---

# Canada (federal)

The consolidated Acts and regulations of Canada, as published by the Department of Justice on the
[Justice Laws Website](https://laws-lois.justice.gc.ca/). Each concept is converted from the official
XML in [justicecanada/laws-lois-xml](https://github.com/justicecanada/laws-lois-xml).[^justice-xml]

| | English | Français |
|---|---|---|
| Acts / Lois | [971](acts/en/) | [971](acts/fr/) |
| Regulations / Règlements | [4897](regulations/en/) | [4897](regulations/fr/) |

# Concepts

Every law is one concept (`type: Act` or `type: Regulation`) with its official URL in `resource`,
its consolidation date in `current_to`, and a `translation` link to the other-language version.
File names follow the official identifiers (`C-46` is the Criminal Code; `SOR-98-106` the Federal
Courts Rules; `C.R.C., c. 870` becomes `CRC-c-870`); the original identifier is kept in `source_id`.

# Terms of use

© His Majesty the King in Right of Canada. Reproduced under the Reproduction of Federal Law
Order,[^reproduction-order] which allows anyone to reproduce federal law without charge or
permission, provided it is reproduced accurately and not represented as an official version.
These are unofficial copies; only the Justice Laws Website versions are official.

[^justice-xml]: Justice Canada consolidated XML (laws-lois-xml)
[^reproduction-order]: Reproduction of Federal Law Order (SI/97-5)
