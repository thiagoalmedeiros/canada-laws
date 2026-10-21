---
type: "Regulation"
title: "Regulation respecting the digital official signature of a notary"
description: "Quebec regulation, CQLR c N-3, r 13.1."
resource: "https://www.legisquebec.gouv.qc.ca/en/document/cr/N-3,%20r.%2013.1"
tags: ["qc", "regulation", "en"]
jurisdiction: "qc"
language: "en"
citation: "CQLR c N-3, r 13.1"
document_date: "2019-10-01"
translation: "../fr/CQLR-c-N-3-r-13.1.md"
upstream_license: "See upstream license: https://perma.cc/4LUK-B5SK Source is Lois et règlements codifiés du Québec, Ministère de l'Emploi et de la Solidarité sociale, via Données Québec, https://www.donneesquebec.ca/recherche/dataset/https-donneesquebec-ca-recherche-dataset-edit-lois-et-reglements-quebec (archived at https://perma.cc/9TQE-JWBV). © Gouvernement du Québec. Licensed under CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode). Terms include non-commercial use only; no derivatives (adapted material) may be shared. Provided as-is without warranties; the distributors do not guarantee accuracy, precision, or completeness. Modifications from source are technical / mechanical, effecting a format change: converted from source XML to text, no textual alteration, visual content in source PDFs not included. Unofficial reproduction, without endorsement or affiliation by the Gouvernement du Québec. Official versions available at: https://www.legisquebec.gouv.qc.ca/fr."
status: "stable"
generated: { by: process:canada-laws-provincial-converter, at: 2026-10-09T00:00:00Z }
sources:
  - id: "official"
    resource: "https://www.legisquebec.gouv.qc.ca/en/document/cr/N-3,%20r.%2013.1"
    title: "Gouvernement du Québec: official text"
    author: "org:qc-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws/blob/main/REGULATIONS-QC/train.parquet"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
    last_modified: "2026-10-09T00:00:00Z"
---

# Regulation respecting the digital official signature of a notary

> **Unofficial version, for personal and non-commercial use only.** © Gouvernement du Québec. Not endorsed by or affiliated with the Government of Quebec. Text obtained from the [official source](https://www.legisquebec.gouv.qc.ca/en/document/cr/N-3,%20r.%2013.1) via the [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws). Always check the official version before relying on it.

*CQLR c N-3, r 13.1*

*Enabling statute: Notaries Act (chapter N-3, s. 98, 1st par., subpar. 1)*

*Updated to 2019-10-01*

## I — PURPOSE

**1** The purpose of this Regulation is to determine, in addition to the provisions in the Act to establish a legal framework for information technology (chapter C-1.1), the technological process to be used by a notary to affix his or her official signature using such means, the conditions and procedure for authorizing the use of an official signature affixed by means of such a technological process, those for revoking such authorization, and the minimal conditions a certification service provider must meet.

## II — TECHNOLOGICAL PROCESS

**2** The technological process by means of which a notary may affix his or her official signature is an asymmetric cryptographic system supported by a public-key infrastructure.

The signature affixed by a notary using that process constitutes the notary’s digital official signature.

## III — AUTHORIZATION TO USE AND REVOCATION

### 1 — Authorization to use

**3** The secretary of the Order authorizes the notary who makes an application to that effect, using the document established by the Order, to use a digital official signature using the process described in section 2.

To obtain the authorization, the notary must have his or her identity verified by another notary and must attach the attestation of the verification to the application.

In the application, the notary must undertake

(1) to use his or her digital official signature only in the practice of the profession;

(2) not to allow the use of the signature by a third person;

(3) to ensure the security and the confidentiality of every password or secret element related to his or her digital official signature.

In addition, if the notary becomes aware that the security or the confidentiality of any password or secret element related to the digital official signature has been compromised or if the notary has reasonable grounds to believe so, the notary undertakes to immediately notify

(1) the secretary of the Oder;

(2) the certification service provider;

(3) any person who may have received a document bearing the notary’s digital official signature while, in fact, it was affixed by a third person.

The notary must pay the fees relating to the application for an authorization.

### 2 — Revocation of the authorization

**4** The secretary of the Order must revoke the authorization given to a notary in any of the following cases:

(1) on the written application of the notary;

(2) the notary has been removed from the roll of the Order;

(3) the notary fails to fulfil one of the undertakings provided for in section 3;

(4) any situation where the notary is informed that the confidentiality or the security of the password or of the secret elements related to the digital official signature has been compromised;

(5) on the written application of the certification service provider, where the notary fails to pay the fees relating to the use of the digital official signature.

The secretary of the Order must inform the notary and the certification service provider of the revocation.

## IV — CERTIFICATION SERVICE PROVIDER

**5** Only a certification service provider that has been authorized by the Order may issue the keys and certificates allowing a notary to affix his or her digital official signature using the process described in section 2.

**6** The Order authorizes a certification service provider that enters into an agreement with the Order determining the administrative procedures necessary for the application of this Regulation and that meets the following minimal conditions:

(1) it has a certification policy that complies with documents RFC 3647 and RFC 3280 developed by the Internet Engineering Task Force and that includes a procedure for identity verification;

(2) it issues keys and certificates by means of a public-key infrastructure;

(3) it has a certificate directory that complies with the International Telecommunication Union (ITU) Recommendation X.500;

(4) it issues certificates that comply with the ITU Recommendation X.509;

(5) it issues keys that consist of a unique and indissociable pair of keys, one public and the other private, which allow the signing of technology-based documents and the identification of the signatory;

(6) it issues certificates that include, in particular, the following elements:

(a) the distinguishing name of the notary combined with a unique code;

(b) a mention to the effect that he or she is a notary;

(7) it enters the certificates into a directory held on a medium based on information technology and keeps it up-to-date. The directory must include, in particular, the serial numbers of the certificates that are valid, suspended, cancelled, or archived.

The reference to a standard provided for in subparagraphs 1, 3 and 4 of the first paragraph includes any subsequent amendments made thereto.

**7** The certification service provider must make sure that the notary has the authorization of the secretary of the Order before it issues the keys and certificates allowing the notary to affix his or her digital official signature.

**8** The certification service provider who has knowledge of one of the cases of revocation of the authorization provided for in section 4 notifies the secretary of the Order and the notary.

**9** The certification service provider revokes the keys and certificates allowing the notary to affix his or her digital official signature in particular where the secretary of the Order informs the provider of the revocation of the authorization made in accordance with section 4.

If the certification service provider revokes them for a reason other than a case referred to in section 4, the certification service provider so informs the secretary of the Order and the notary.

## V — TRANSITIONAL AND FINAL

**10** The personal code or mark assigned to a notary by the secretary of the Order before 1 October 2019 is the notary’s digital official signature.

The notary is authorized to use the signature if

(1) the notary undertakes in writing in accordance with section 3; and

(2) the certification service provider that issued the keys and certificates allowing to affix the signature meets the conditions provided for in sections 5 and 6.

**11** (Omitted).
