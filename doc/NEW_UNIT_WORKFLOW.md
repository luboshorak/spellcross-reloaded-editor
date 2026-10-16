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
   **Ground** for vehicles or infantry occupying one 80-pixel-wide map
   tile. Ground mode now offers **Vehicle (208 sprites)**, using 16 azimuths
   across all 13 original terrain slopes, and **Walker (96 sprites)**,
   using 16 standing directions plus 10 movement poses across 8 headings.
   Upright sprites may extend above the 48px terrain diamond.
   **Ground size relative to template (%)** now defaults to **125%**
   and can be adjusted from 50% to 200%. The former fixed width/height
   clamps have been removed: the imported 3D silhouette starts with the
   reference unit's actual occupied dimensions. **Reference size limit at
   100%** (default 144px for ground units) bounds the unscaled reference;
   the **percentage is applied afterwards**, up to a final 320px limit.
   Importantly, original FSU sprite row offsets are **signed 16-bit values
   when decoded**, so units can extend left and right beyond an 80px tile.
   We removed the incorrect 80px artwork cap and expand the transparent
   canvas in both dimensions as needed. The 3D preview shows the **visible
   object width/height in pixels**, not just the transparent canvas size:
   that lets you verify that changing 100% to 200% has an actual effect.
   Large sprites may overlap neighboring map tiles, as intended.
5. Set **3D camera elevation**, initially 65° for aircraft or 35° for
   ground units. Select the model's forward direction with **Source image
   points toward**. The default assumes forward is negative Y in the
   imported scene; each subsequent camera direction steps by 45 degrees.
   Set **Facing directions** to *8 real 3D camera viewpoints*.
6. Blender renders transparent 1024×1024 PNGs with consistent orthographic
   magnification. The editor computes a **shared crop/scale across all
   angles**, produces 8 game-scale images, and previews each angle.
   Neither model nor textures are modified.
   Ground rendering matches the **template unit's visible FSU size and
   slope-specific vertical offsets** instead of cropping against an 80×48
   canvas. The original map draws vehicles relative to the terrain
   sprite's own vertical offset; ground-plane contact is typically about
   32px below the FSU origin, not at pixel 128. The converter matches
   the reference sprite's last occupied row, with an optional **Ground
   contact adjustment (px)** for unusual models (+ moves down).
   For vehicles it also generates incline-dependent body skew variants.
   This is an approximation of suspension pitch/roll, not fully
   physics-driven articulation.

   When Ground is selected on an aircraft template, game class switches
   to Armored Ground and Flight is cleared. Walker mode uses Light/Walk;
   Vehicle mode clears Walk. A full-model render contains the turret in
   the main image, so the obsolete separate Turret flag is cleared.

   The **Enhance fine details** checkbox is enabled by default. It now
   applies only restrained shadow correction and mild alpha-safe edge
   sharpening **after downscaling and before** the fixed `UNITS.PAL`
   quantization; no global exposure boost is applied. Blender lighting
   is intentionally restrained to avoid bleaching model textures.
   **3D lighting intensity (%)** controls the light rig between 25% and
   200% without editing source code; start at 100%, lower if too bright.
7. Select **Build game graphics**, choose a fresh output folder, and
   the editor encodes the original `UNITS.PAL` and exports a modded
   `UNITS.FSU`. Aircraft retain the proven `A00–A07` / `F00–F07`
   layout. Ground vehicles use `000–C0F` (208 unique slope/heading
   slots). Walkers use `000,002,…,09E` (80 movement slots) and
   `F00–F0F` (16 standing slots). On an animated glTF/FBX model,
   Blender renders ten actual movement poses at eight camera angles;
   static models safely reuse the standing pose for movement until an
   animated asset is supplied. The editor verifies these frame tables
   when decoding the temporary FSU before mod archive export.
8. The editor automatically generates a dedicated `I_<group>.LZ` unit
   icon for `COMMON.FS`, plus separate `N<group>.LZ` info artwork and a
   192-color `N<group>.PAL` for `INFO.FS`. These no longer come from
   the template.
9. Use **Place / test on map...** to preview and place the unit; then
   **Export mod COMMON.FS...** to write the updated unit definitions, icon
   and INFO resources into mod archive copies.

The renderer uses actual Blender camera rotation and fixed camera scale.
It does not rotate one PNG into eight faked 3D perspectives. For Walker
units, any model with Blender-imported Actions is additionally sampled
for ten movement poses; otherwise its movement slots use static frames.
Separate firing, death and vehicle suspension animations are not
imported yet. Material and rig support are subject to Blender's
glTF/FBX importers.

## Legacy PNG import (optional)

The old transparent-background/crop/rotation importer is still available
through the PNG file filter. Its eight directions remain approximate
2D transformations, so it is not recommended for new directional units.
Ground units share the same template-based scale and opaque-pixel
ground anchoring as 3D input.
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
