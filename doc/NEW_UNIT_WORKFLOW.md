# Creating a custom unit (experimental workflow)

The **Units DEF editor** (View > Units DEF editor) now includes **New unit...**
(Ctrl+N, the button under the units list, or right-click on the list).

## Create a unit definition

1. Open your working `JEDNOTKY.DEF` via **File > Open units DEF file(s)**.
   The editor now preserves the entire selected path (DEF files outside the
   working directory load correctly).
2. Choose **New unit...**, enter a unique name and select an existing unit as a
   template. Cloning carries over combat stats, movement, animation references,
   graphics references and sounds. An empty definition can also be created,
   but it must be filled before use.
3. On **Sprite PNG**, optionally choose a single PNG and set its *three-character
   sprite code* (A-Z, 0-9 and underscore only, e.g. `A00`).
4. Confirm. The new unit is selected in the list. Use the existing **Basic**,
   **Graphics**, **Sounds** and **Special actions** pages to configure it.
5. Save the working `JEDNOTKY.DEF` to your **mod directory**, not the original
   game installation. Confirm before overwriting any destination.

## PNG encoding and palette

If a PNG was selected, the wizard creates two metadata files **beside the PNG**:

- `<image-stem>.info` describes the PNG as an `UNITS.FSU` sprite, with its
  three-character code, dimensions and alpha transparency.
- `spellcross_units.palinfo` is exported from the original loaded
  `UNITS.PAL` and makes the graphics encoder quantize to the actual game's
  units palette (indexes 128–223).

Existing PNG files and metadata are never overwritten automatically.
If `<image-stem>.info` exists, it must describe the same PNG and sprite code.
If `spellcross_units.palinfo` exists, it must match the loaded palette.

The **Graphics Resource Encoder** opens the newly prepared resource directly.
Inspect the encoded preview, transparency and offsets; choose **Save resource**
and select an export directory to produce the encoded three-character sprite
file.

**Important limitation:** one PNG produces **one FSU sprite**, not an entire
unit. Complete unit graphics require the correct directions, poses and frames.
The encoded three-character sprite files need to be assembled into a named FSU
resource (resource folder name at most **five characters**) and packed into
`UNITS.FSU` with the FSU tools. The new `JEDNOTKY.DEF` must then point to that
resource name, and that resource must be present in the loaded game assets.

The wizard deliberately **does not assign an unbuilt FSU graphic** to the
definition. A cloned unit retains the template's graphics and can be configured
while the new assets are being prepared.

## Map placement and game testing

The DEF editor manipulates **external files**, not the unit catalog already
loaded into the running map editor. Saving a DEF does not hot-reload units.

To test a complete unit: deploy both the modded `JEDNOTKY.DEF` in the
appropriate game archive and its compatible `UNITS.FSU` (using the existing
mod/build workflow), **reload the editor's game configuration/assets**, open a
map, then use the existing unit placement tool to select and place the new unit.
The game can load custom missions through **File > Load custom map...**, as
described in the main README.

## Scope of this change

**Implemented:** template-based creation, prominent UI actions, input
validation, automatic `.info` creation, palette generation, direct entry to
the existing graphics encoder, full-path DEF loading and save-path tracking.

**Not yet implemented:** sprite-sheet slicing, automatic generation of
directional/animated FSU sets, automatic archive assembly/installation,
in-session unit hot-reload, and one-click launch of a playable test map.

These are real technical constraints: a standalone PNG cannot be represented
as a fully animated Spellcross unit, and a DEF change alone does not register
new graphics or change the currently loaded map catalog.
