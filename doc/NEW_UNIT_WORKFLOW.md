# Create a new custom Spellcross Reloaded unit

**Recommended workflow: import a 3D model.** The editor supports `.glb` and
`.gltf` (preferred), with optional `.fbx` import through Blender. Unlike
single-image PNG rotation, this produces **eight geometrically real camera
views** of the source model. Install Blender 4.x/5.x for the renderer; the
first import prompts you to locate `blender.exe`, or set the environment
variable `SPELLCROSS_BLENDER_EXE` to its full path.

The editor launches Blender headlessly with its bundled
`render_unit_model.py` script. This file is copied beside the editor EXE
during the Windows build; if copying the editor to another folder, copy the
script with it. No 3D runtime, Python package, or 3D rendering library is
embedded into the editor.

## Model-to-sprite pipeline

1. Open the editor and load the game archives.
2. Open **View > Units DEF editor**, load your working `JEDNOTKY.DEF`, and
   select **New unit...**, or select an existing custom unit and click
   **Create game sprites from artwork...**.
3. Choose a `.glb`, `.gltf` or `.fbx` model. For `.gltf`, keep external
   textures and `.bin` buffers in their original relative locations.
4. Pick a unique FSU graphics group (1–5 uppercase letters/digits).
   Choose **Air** for aircraft that may extend beyond one map tile,
   **Ground** to constrain the resulting sprites to one 80×48 game tile.
5. Set **3D camera elevation**, initially 65° for aircraft or 35° for
   ground units. Select the model's forward direction with **Source image
   points toward**. The default assumes forward is negative Y in the
   imported scene; each subsequent camera direction steps by 45 degrees.
   Set **Facing directions** to *8 real 3D camera viewpoints*.
6. Blender renders transparent 512×512 PNGs with consistent orthographic
   magnification. The editor computes a **shared crop/scale across all
   angles**, produces 8 game-scale images, and previews each angle.
   Neither model nor textures are modified.
7. Select **Build game graphics**, choose a fresh output folder, and the
   editor encodes the directions as `A00–A07` and `F00–F07` using the
   original `UNITS.PAL` and merges them into a modded `UNITS.FSU`.
8. The editor automatically generates a dedicated `I_<group>.LZ` unit
   icon for `COMMON.FS`, plus separate `N<group>.LZ` info artwork and a
   192-color `N<group>.PAL` for `INFO.FS`. These no longer come from
   the template.
9. Use **Place / test on map...** to preview and place the unit; then
   **Export mod COMMON.FS...** to write the updated unit definitions, icon
   and INFO resources into mod archive copies.

The renderer uses actual Blender camera rotation and fixed camera scale.
It does not use one PNG rotated eight times. If the model includes animations,
the current version renders a single chosen frame for all headings;
walking/firing/dying sequences are not automatically imported yet.
Material support is subject to Blender's glTF/FBX importers.

## Legacy PNG import (optional)

The old transparent-background/crop/rotation importer is still available
through the PNG file filter. Its eight directions remain approximate
2D transformations, so it is not recommended for new directional units.
Ground units use the same one-tile limit and Spellcross-native FSU anchors.
The separate **Build PNG graphics / UNITS.FSU...** button still accepts
artist-prepared PNG sprite folders.

## Safety and current verification

Always work against a separate editor/game test installation. Mod builds
create `UNITS.FSU`, `COMMON.FS`, and `INFO.FS` as copies and never modify
the original game archives. Select an empty export folder rather than
overwriting previous exports.

**Status:** This GLB/glTF/FBX implementation is experimental and has not yet
passed a Windows compilation and real Blender/game-data runtime test.
The associated PR is draft and has not been merged into main.
