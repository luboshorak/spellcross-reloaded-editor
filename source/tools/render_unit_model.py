"""Render eight real 3D camera azimuths to transparent PNGs for Spellcross.
Requires Blender (4.x/5.x) and one glTF/GLB or FBX model.
Run in Blender background mode with args after --.
"""
import argparse
import math
import pathlib
import sys
import traceback
import bpy
from mathutils import Vector

def parse_args():
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--views', type=int, choices=[1,8,16], default=8)
    parser.add_argument('--resolution', type=int, default=1024)
    parser.add_argument('--elevation', type=float, default=40.0)
    parser.add_argument('--heading', type=float, default=0.0)
    parser.add_argument('--frame', type=int, default=1)
    parser.add_argument('--lighting', type=int, default=100,
                        help='Lighting intensity percentage, 25..200 (default 100)')
    return parser.parse_args(argv)

def load_model(path):
    ext = path.suffix.lower()
    if ext in ('.gltf', '.glb'):
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif ext == '.fbx':
        if hasattr(bpy.ops.wm, 'fbx_import'):
            try:
                bpy.ops.wm.fbx_import(filepath=str(path))
                return
            except (RuntimeError, TypeError):
                pass
        bpy.ops.import_scene.fbx(filepath=str(path))
    else:
        raise ValueError('Unsupported model extension: '+ext)

def bounds():
    depsgraph = bpy.context.evaluated_depsgraph_get()
    points = []
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH' or obj.hide_render:
            continue
        evaluated = obj.evaluated_get(depsgraph)
        points.extend([evaluated.matrix_world @ Vector(c) for c in evaluated.bound_box])
    if not points:
        raise ValueError('Model has no visible meshes')
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center = (lo + hi) / 2
    radius = (hi - lo).length / 2
    if radius <= 1e-7:
        raise ValueError('Model bounds are empty')
    return center, radius

def light(scene, name, center, offset, radius, power):
    data = bpy.data.lights.new(name, type='AREA')
    # World-space radius varies wildly between game models. Scale wattage
    # with radius squared to keep lighting consistent after importing them.
    data.energy = power * radius * radius
    data.shape = 'DISK'
    data.size = 3.0 * radius
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = center + Vector(offset)*radius
    obj.rotation_euler = (center-obj.location).to_track_quat('-Z','Y').to_euler()

def render_views(args):
    model = pathlib.Path(args.input).resolve(strict=True)
    output = pathlib.Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not 128 <= args.resolution <= 2048:
        raise ValueError('Resolution must be 128..2048')
    if not 0 <= args.elevation <= 90:
        raise ValueError('Elevation must be 0..90')
    if not 25 <= args.lighting <= 200:
        raise ValueError('Lighting must be between 25 and 200 percent')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    load_model(model)
    scene = bpy.context.scene
    scene.frame_set(args.frame)
    center, radius = bounds()

    # Engine identifiers changed around Blender 4.2 / 5.x.
    # Try available operators directly rather than introspecting enum items.
    chosen = None
    for candidate in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE', 'CYCLES'):
        try:
            scene.render.engine = candidate
            chosen = candidate
            break
        except (TypeError, ValueError):
            pass
    if chosen is None:
        raise RuntimeError('No usable render engine found in Blender')
    if chosen == 'CYCLES':
        scene.cycles.samples = 16

    scene.render.resolution_x = args.resolution
    scene.render.resolution_y = args.resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'Standard'
    world = bpy.data.worlds.new('Spellcross Ambient')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.65, 0.68, 0.74, 1.0)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.60
    # No exposure boost: preserve the materials' highlights and colors.
    scene.view_settings.exposure = 0.0
    scene.world = world

    cam_data = bpy.data.cameras.new('Spellcross Camera')
    cam = bpy.data.objects.new('Spellcross Camera', cam_data)
    scene.collection.objects.link(cam)
    cam_data.type = 'ORTHO'
    # Single fixed scale is critical: don't enlarge individual directions.
    cam_data.ortho_scale = radius * 2.4
    scene.camera = cam
    # Preserve model scale invariance, but use restrained radiometric power.
    # Previous 1150+850+700+450 watts * radius^2 flattened highlights.
    strength = args.lighting / 100.0
    light(scene,'Spellcross Key',center,(-1.4,-2.0,3.0),radius,150*strength)
    light(scene,'Spellcross Fill',center,(1.7,1.8,2.0),radius,90*strength)
    light(scene,'Spellcross Rim',center,(0.6,2.7,3.0),radius,45*strength)
    light(scene,'Spellcross Side',center,(-2.4,1.2,2.2),radius,35*strength)
    elevation = math.radians(args.elevation)
    for index in range(args.views):
        az = math.radians(args.heading + index * (360.0 / args.views if args.views > 1 else 0.0))
        direction = Vector((math.sin(az)*math.cos(elevation),
                            -math.cos(az)*math.cos(elevation),
                            math.sin(elevation)))
        cam.location = center + direction*(radius*3.5)
        cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath = str(output/('view_%02d.png' % index))
        bpy.ops.render.render(write_still=True)
        print('SPELLCROSS_RENDERED',index+1,args.views,scene.render.filepath,flush=True)

if __name__ == '__main__':
    try:
        render_views(parse_args())
    except Exception as exc:
        print('SPELLCROSS_RENDER_FAILED:',str(exc),file=sys.stderr,flush=True)
        traceback.print_exc()
        sys.exit(3)
