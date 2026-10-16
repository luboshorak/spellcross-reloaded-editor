# Create a new custom Spellcross Reloaded unit

This experimental editor branch adds direct high-resolution artwork conversion,
DEF editing, FSU archive building, map placement and mod export.

## Start with a unit and an ordinary image

1. Open the editor and load the original game archives.
2. Open **View > Units DEF editor** and **File > Open units DEF file(s)**.
   Load a **working copy** of your `JEDNOTKY.DEF`, not a retail original.
3. Click **New unit...** and choose a compatible template unit. Set the new
   unit's name. On **2. Source artwork**, pick any PNG artwork, including a
   high-resolution illustration or top-down photo (e.g. 1800×1500).
4. Click **Create unit**. The source image goes straight to
   **Create game sprites from artwork...**. You can also open this converter
   at any time by selecting a unit in the DEF list and clicking that button.
5. In the converter, choose a **unique 1–5 character** graphics name
   (A–Z, 0–9), select a game-scale object size (default **96 pixels**) and:
   - **8 rotated views** for a plane, top-down vehicle or object represented
     from above; the image is rotated by 45 degrees per direction.
   - **One fixed view** for perspective artwork where turning the flat image
     would look incorrect.
   - **Remove plain background** for pictures with a uniform border color.
     Adjust tolerance for near-white/colored backgrounds. Transparent PNG
     alpha is preserved.
6. Check the preview. If satisfied, click **Build game graphics** and choose
   a writable mod export folder.

The converter flood-removes uniform border background, crops around the
visible subject, scales it while preserving aspect ratio and generates
centered sprites. It writes `A00...A07` as one-frame movement sprites and
`F00...F07` as static direction sprites (for one-view mode only `A00` and
`F00`). The game cannot infer unseen details of an aircraft or vehicle:
this is **2D rotation**, not actual 3D camera-view synthesis.

It then uses the existing graphics encoder and **UNITS.PAL indices 128–223**
to quantize the new images, produces a named FSU resource and merges it with
a copy of the loaded `UNITS.FSU`. The new group is linked to your unit in
the currently running editor; the original commercial archives are unchanged.

Export results include:
- `spellcross_source_<group>/` — generated small PNGs and their .info files
- `spellcross_fsu_<group>/<group>/` — encoded 3-character FSU sprites
- `NEW_<group>.FSU` — standalone new resource for inspection
- `UNITS.FSU` — merged mod archive

The editor refuses to overwrite existing generated archives and metadata.

## Existing artist-prepared direction frames

**Build PNG graphics / UNITS.FSU...** remains available for artists who
already have a complete set of individual `A00.png`, `F00.png`, etc.
and matching optional `.info` files. Choose a new group name, the input
folder and an empty output folder. All sprites share the original
`UNITS.PAL`. You can inspect individual PNGs and metadata in the
**Graphics Resource Encoder**. It now scales large source images to fit its
preview instead of leaving the panel blank.

## Place and test the unit

1. Keep a tactical map loaded in the main map editor.
2. In the Units DEF editor select the new unit and click
   **Place / test on map...**.
3. The editor serializes new DEF records, resolves graphics, icon, sounds and
   metadata against the live game data and appends new IDs without moving or
   overwriting existing map unit records. Several pending new IDs are
   registered in order.
4. The normal **Add unit** tool opens with your new unit selected. Place it
   and check orientation, size, rendering and stats.
5. To export the definition to Reloaded, click **Export mod COMMON.FS...**
   and choose the folder containing the generated `UNITS.FSU`. The export
   replaces `JEDNOTKY.DEF` inside a **copy** of the original `COMMON.FS`.
   The original archives are never overwritten.

To test in the Reloaded game executable, configure your game's mod/data
path to use this mod folder and load a custom tactical mission. The editor
does not yet automatically install the mod or launch the game process.

## Important limits

- Removing a complex photographic background is **not** AI segmentation.
  Plain/near-plain edge-connected backgrounds are supported. For a complex
  environment, provide a transparent PNG of the aircraft/object instead.
- Eight-view rotation assumes top-down artwork; perspective sprites require
  artist-provided viewpoints. A single source image does not create real
  walking/fire/dying animations. Generated movement frames are repeated
  one-frame poses to support moving units at different headings.
- Editor preview registration is **append-only**: to change a unit already
  registered in memory, reload game data with the updated mod and start again.
- **Build/runtime status:** the new converter and pipeline are not yet
  verified by a Windows C++ build or a real game-data integration test.
  Test only in a separate editor/game installation.
