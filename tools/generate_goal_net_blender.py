"""Run inside Blender to generate the UDK-ready soccer goal FBX.

Example:
  blender --background --python tools/generate_goal_net_blender.py -- \
    --output assets/goal_net.fbx
"""

import argparse
import sys

import bpy


def box(name, center, size, material):
    bpy.ops.mesh.primitive_cube_add(location=center)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    return obj


def make_material(name, color, roughness):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1.0)
    material.roughness = roughness
    return material


def build(width, height, depth, columns, rows):
    frame = max(width, height) * 0.035
    rope = max(width, height) * 0.009
    frame_material = make_material('GoalFrame', (0.82, 0.86, 0.84), 0.35)
    net_material = make_material('NetRope', (0.72, 0.94, 0.68), 0.6)
    objects = []

    def add(material, center, size):
        objects.append(box('SoccerNetPart', center, size, material))

    add(frame_material, (-width / 2, 0, height / 2), (frame, frame, height))
    add(frame_material, (width / 2, 0, height / 2), (frame, frame, height))
    add(frame_material, (0, 0, height), (width + frame, frame, frame))
    add(frame_material, (0, 0, frame / 2), (width, frame, frame))
    add(frame_material, (0, depth / 2, height), (width, frame, frame))
    add(frame_material, (-width / 2, depth / 2, height / 2), (frame, depth, frame))
    add(frame_material, (width / 2, depth / 2, height / 2), (frame, depth, frame))
    add(frame_material, (0, depth, height / 2), (width, frame, height))

    for column in range(columns + 1):
        x = -width / 2 + width * column / columns
        add(net_material, (x, depth - frame, height / 2), (rope, rope, height))
        add(net_material, (x, depth / 2, height - frame * 2), (rope, depth, rope))
        add(net_material, (x, depth / 2, frame * 2), (rope, depth, rope))
    for row in range(rows + 1):
        z = height * row / rows
        add(net_material, (0, depth - frame, z), (width, rope, rope))
        add(net_material, (-width / 2 + frame * 2, depth / 2, z), (rope, depth, rope))
        add(net_material, (width / 2 - frame * 2, depth / 2, z), (rope, depth, rope))

    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    objects[0].name = 'SoccerGoalNet'
    return objects[0]


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--width', type=float, default=7.32)
    parser.add_argument('--height', type=float, default=2.44)
    parser.add_argument('--depth', type=float, default=2.0)
    parser.add_argument('--columns', type=int, default=18)
    parser.add_argument('--rows', type=int, default=8)
    args = parser.parse_args(argv)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    build(args.width, args.height, args.depth, args.columns, args.rows)
    bpy.ops.export_scene.fbx(
        filepath=args.output,
        use_selection=True,
        apply_unit_scale=True,
        axis_forward='-Y',
        axis_up='Z',
        object_types={'MESH'},
        use_mesh_modifiers=True,
    )
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()

