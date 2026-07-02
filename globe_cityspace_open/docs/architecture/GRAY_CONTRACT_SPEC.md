# Globe-CitySpace
# Gray Contract Specification

## Purpose

The Gray Contract is the final logical representation consumed by:

- BMP Generator
- Physical Table
- Projection Mapping

---

## Coordinate System

Origin:
(0,0,0)

Location:
Upper Left Corner

x':
Right

y':
Down

z':
Up

North:
Always Up

---

## Physical Layout

Grid:
16 x 8

Cell Size:
1 cm x 1 cm
or
2 cm x 2 cm

---

## Spatial Layout

P001 = Upper Left

P008 = Lower Left

P121 = Lower Right

P128 = Upper Right

---

## Scan Pattern

Column ZigZag IPT

Column 1:
Top → Bottom

Column 2:
Bottom → Top

...

Column 16:
Bottom → Top

---

## Value Range

Gray:
0 → 255

Pin Height:
0 → 10 cm

