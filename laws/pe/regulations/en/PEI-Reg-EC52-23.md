---
type: "Regulation"
title: "Spatial Referencing Regulations"
description: "Prince Edward Island regulation, PEI Reg EC52/23."
resource: "https://www.princeedwardisland.ca/sites/default/files/legislation/l02-2-1-land_survey_act_spatial_referencing_regulations.pdf"
tags: ["pe", "regulation", "en"]
jurisdiction: "pe"
language: "en"
citation: "PEI Reg EC52/23"
document_date: "2023-02-04"
upstream_license: "See upstream license: https://perma.cc/V9XJ-HTR4 © Government of Prince Edward Island. The consolidated statutes and regulations and the annual statutes from Prince Edward Island were updated by the A2AJ (Access to Algorithmic Justice project) on August 15, 2026 from the Legislative Counsel Office website (https://www.princeedwardisland.ca/en/legislation), maintained by the Government of Prince Edward Island. Copyright: Reproduction of Acts and regulations available in the A2AJ Canadian Laws dataset is governed by the Prince Edward Island's government copyright policy: https://www.princeedwardisland.ca/en/information/executive-council-office/website-disclaimer-and-copyright-policy. NOTE: This is an unofficial reproduction of Prince Edward Island regulations, made without endorsement or affiliation by the Government of Prince Edward Island. The official versions should be consulted for all purposes of interpreting and applying the law. Reproduced with the permission of the Legislative Counsel Office of Prince Edward Island (granted by email on July 20, 2026)."
status: "stable"
generated: { by: process:canada-laws-provincial-converter, at: 2026-08-15T00:00:00Z }
sources:
  - id: "official"
    resource: "https://www.princeedwardisland.ca/sites/default/files/legislation/l02-2-1-land_survey_act_spatial_referencing_regulations.pdf"
    title: "Government of Prince Edward Island: official text"
    author: "org:pe-government"
  - id: "a2aj"
    resource: "https://huggingface.co/datasets/a2aj/canadian-laws/blob/main/REGULATIONS-PE/train.parquet"
    title: "A2AJ Canadian Laws dataset"
    author: "org:a2aj"
    last_modified: "2026-08-15T00:00:00Z"
---

# Spatial Referencing Regulations

> **Unofficial version, for personal and non-commercial use only.** © Government of Prince Edward Island. Not endorsed by or affiliated with the Government of Prince Edward Island. Text obtained from the [official source](https://www.princeedwardisland.ca/sites/default/files/legislation/l02-2-1-land_survey_act_spatial_referencing_regulations.pdf) via the [A2AJ Canadian Laws dataset](https://huggingface.co/datasets/a2aj/canadian-laws). Always check the official version before relying on it.

PEI Reg EC52/23

*Made under the Land Survey Act*

Pursuant to section 15 of the Land Survey Act R.S.P.E.I. 1988, Cap. L-2.2, Council made the following

regulations:

### Definitions

1. In these regulations,

(a) “NAD83” means North American Datum of 1983;

(b) “CSRS” means the Canadian Spatial Reference System;

(c) “CBN” means the Canadian Base Network;

(d) “CGVD” means the Canadian Geodetic Vertical Datum.

### Schedule adopted

2. The Schedule to these regulations is adopted and forms part of these regulations.

### PEI Coordinate System

3. The Prince Edward Island Coordinate System shall be that set out in Part I of the Schedule.

### Vertical Reference System

4. The Vertical Reference System for the purposes of the Prince Edward Island Coordinate

System shall be that set out in Part II of the Schedule.

## SCHEDULE

### PART I - PRINCE EDWARD ISLAND COORDINATE SYSTEM

Coordinate system defined

1. The Prince Edward Island Plane Rectangular Coordinate Projection is a stereographic double

projection of the NAD83 (CSRS) geocentric ellipsoid, on a secant plane. The North American Datum

of 1983 has been redefined through the Canadian Spatial Reference System (CSRS). It will be

identified as NAD83 (CSRS). The dimensions of the NAD83 (CSRS) ellipsoid are as follows:

Semi-major axis (Equatorial Radius) = 6,378,137.0000 metres

Semi-minor axis (Polar Semi-diameter) = 6,356,752.3141 metres

2. The datum in Prince Edward Island is defined in terms of the values of the Canadian Base Network

(CBN) stations determined from version 6.0 (2010) of the Canadian adjustment prepared by the

Geodetic Survey Division of Natural Resources Canada. The values for the two Prince Edward Island

CBN stations are listed as follows:

Monument Name Number Geodetic Latitude Geodetic Longitude

Bloomfield PE05804 N46º45’04.43056” W64º11’26.34846”

Carl-Val-Archie PE05803 N46º22’37.02703” W62º08’08.76854”

3. The true origin of the Prince Edward Island Coordinate System is a point at

Latitude: 47º15’ North Longitude: 63º00’ West

as defined by the NAD83 (CSRS) ellipsoid. The Y axis (North Axis) is the Geodetic Meridian through

the origin, and the X axis (East Axis) is the straight line through the origin perpendicular to the Y axis.

The scale factor at the origin is 0.999912 and the Gaussian mean radius of the projection sphere at the

origin is 6,379,782.0995 metres. Coordinates are considered positive to the East and to the North. To

avoid negative values, the origin has been given the coordinates

Y (North Axis) = 800,000 metres X (East Axis) = 400,000 metres

4. The position of a point shall be defined by two expressions, each given in metres and decimals of a

metre. The first expression, to be known as the X coordinate minus 400,000 metres, shall indicate the

perpendicular distance from the Y axis. When the distance is positive, the point is east of the origin;

and when the distance is negative, the point is west of the origin. The second expression, to be known

as the Y coordinate minus 800,000 metres, shall indicate the perpendicular distance from the X axis.

When the distance is positive, the point is north of the origin; and when the distance is negative, the

point is south of the origin.

5. The coordinates shall be made to depend upon

(a) the values of the two Prince Edward Island CBN stations set out in this Part; or

(b) the values of the densification of the CBN carried out by the Department of Transportation and

Infrastructure for the purpose of establishing the Prince Edward Island Active Control Network.

6. The values referred to in clause 5(b) for the active control stations are listed as follows:

Station Name Location Geodetic Latitude Geodetic Longitude

PEAL Alliston 46º03’39.95752” 62º36’02.84052”

PESO Souris 46º21’29.04194” 62º15’03.27472”

PEMO Morell 46º24’42.07632” 62º42’28.85081”

PETI Charlottetown 46º13’57.85837” 63º08’00.30847”

PEAM Borden-Carleton 46º15’05.90485” 63º41’08.51465”

PEGS North Rustico 46º27’26.04582” 63º19’40.92219”

PEEL Ellerslie 46º36’21.11208” 63º56’03.32053”

PEWI Rosebank 46º48’24.00787” 64º08’50.96877”

PART II - VERTICAL REFERENCE SYSTEM

Canadian Geodetic Vertical Datum of 2013

1. The Canadian Geodetic Vertical Datum of 2013 (CGVD2013) is the official datum of Prince Edward

Island and replaces the Canadian Geodetic Vertical Datum of 1928 (CGVD28).

CGVD2013 defined

2. CGVD2013 is a gravimetric datum defined by the equipotential surface w = 62,636,856.0 m2s-2,

o

representing the average potential of coastal mean sea level at tide gauges across North America. The

definition and geopotential value come from an agreement between Canada and USA. Heights in terms

of CGVD2013 are in the orthometric height system.
