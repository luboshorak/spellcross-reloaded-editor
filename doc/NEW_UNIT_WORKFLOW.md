# Custom units: import, build, place and test (experimental)

The Units DEF editor now combines the existing DEF editor, graphics encoder,
FSU archive builder and map unit placement tool.

## Step 1: Create a unit

1. Open the editor's **View > Units DEF editor**.
2. Choose **File > Open units DEF file(s)** and open the game's (or a mod's)
   `JEDNOTKY.DEF`. Keep a backup; work on a copy.
3. Choose **New unit...** (Ctrl+N, button or list context menu).
4. Type a name and preferably select a similar existing unit as template.
   This copies its movement, combat parameters, sounds, animations and
   references. The new record gets the next unit ID.
5. The PNG selection on page 2 is optional. It prepares `.info` metadata
   from a PNG and opens the existing Graphics Resource Encoder directly.
   For a complete unit, prepare multiple PNG sprites covering the directions
   and animations required by your model.

Edit parameters in the existing **Basic**, **Graphics**, **Sounds** and
**Special actions** pages. A unit name can be up to 27 characters.

## Step 2: Build unit graphics from PNGs

1. Put the unit's PNG frames in **one folder**. Each file must have a
   three-character sprite name such as `A00.png`, `A01.png`, `F00.png`.
   Alternatively, a PNG can be accompanied by an `.info` file whose
   `name` specifies its three-character sprite code; the New unit wizard
   can create one of these automatically.
2. Select the newly created unit and click
   **Build PNG graphics / UNITS.FSU...**.
3. Enter a **unique 1–5 character FSU resource group name**, for example
   `NEW01`. Choose the PNG folder and an **empty mod output folder**.
4. The editor quantizes all PNGs against the game's original `UNITS.PAL`
   (indexes 128–223), encodes each sprite with existing
   `FSU_sprite::SaveSprite`, builds a standalone `NEW_<group>.FSU` and
   merges that group's compressed sprites into a **copy** of the currently
   loaded `UNITS.FSU`.
5. The new resource is added to the running editor without replacing any
   existing FSU resource; the selected unit's main `gra` reference is
   changed to the new group. You can see it under the **Graphics** tab.

All generated files are written to the chosen mod folder, never to the
original game archives. Existing output names are rejected instead of
overwritten. The encoded intermediate sprites are retained under
`spellcross_fsu_<group>/<group>/`, for inspection.

**Sprite naming matters:** one PNG is only a single pose/direction and does
not magically provide every movement frame and viewing direction. The FSU
resource parser interprets the naming/order of all provided frames. Complete
your directional/animation set to match the gameplay behavior of the cloned
template. The tool does not synthesize unseen camera angles from one image.

## Step 3: Place and preview the unit on a map

1. Open a tactical map in the main map editor.
2. In the Units DEF editor, select the new unit and click
   **Place / test on map...**.
3. The editor serializes that unit's DEF record, resolves its graphics,
   icons, sounds and animation links against the live Spellcross data, and
   appends it to the live catalog **without moving/replacing existing
   unit records** that may already be referenced from a map.
4. The existing **Add unit** window opens with your new unit selected.
   Position and place it as usual; inspect its sprites and parameters.

For safety this imports **new, sequential unit IDs only**. If several
new units precede the selected unit, the editor registers the pending units
in order. Overwriting an in-use unit ID could corrupt pointers held by map
units, so the editor refuses it. To re-test after changing an already
registered record, reload the editor's data and repeat the procedure.

If the unit refers to an FSU group not loaded (or to missing icon/animation/
sound resources), registration fails with a descriptive error instead of
placing a broken unit.

## Step 4: Export a mod for the Reloaded game

1. Click **Export mod COMMON.FS...** in the Units DEF editor.
2. Choose the **same mod output folder** as for your `UNITS.FSU`.
   The editor copies the loaded `COMMON.FS`, replaces `JEDNOTKY.DEF`
   with the edited data, and writes a **new** `COMMON.FS` there.
3. The folder now contains the updated `COMMON.FS` and (when you built
   new graphics) a matching `UNITS.FSU`. Configure Reloaded to load
   these mod assets through the supported mod/data-path workflow, then
   open the custom mission through **File > Load custom map...**.
4. Keep any other mission assets (e.g. referenced `.DTA`) accessible.

The export preserves the commercial game's original files and refuses to
overwrite an existing `COMMON.FS`. The editor and game each need to load
the **same mod archives** when evaluating new units.

## Limitations and test status

- This implementation uses **PNG folders containing already rendered
  angles/frames**; it does not create novel angles or animation frames from a
  single PNG or slice sprite sheets automatically.
- It assembles FSU resources, links live graphics, registers live DEF records,
  opens map placement and exports standalone mod archives; it does not
  automatically launch the Reloaded game executable or install files into
  its configuration.
- Working `JEDNOTKY.DEF` edits are separate from the live catalog until
  **Place / test on map** is clicked; registration is append-only to avoid
  invalidating pointers on existing maps.
- **Windows C++/wxWidgets build and real asset-based integration tests have
  not been run in this environment.** Check the compiled editor against a
  backed-up Spellcross installation before deploying the mod.
