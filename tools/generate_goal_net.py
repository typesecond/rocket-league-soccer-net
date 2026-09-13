#!/usr/bin/env python3
"""Generate a simple Rocket League goal/net mesh as Wavefront OBJ.

The output is intentionally made from separate rectangular bars. It imports
cleanly as a static mesh in UDK and keeps the decorative net separate from
gameplay collision. Units are meters; Rocket League/UDK scale can be adjusted
at import time.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path


class Obj:
    def __init__(self) -> None:
        self.vertices: list[tuple[float, float, float]] = []
        self.faces: list[tuple[str, list[int]]] = []

    def box(self, name: str, center: tuple[float, float, float], size: tuple[float, float, float]) -> None:
        cx, cy, cz = center
        sx, sy, sz = (value / 2 for value in size)
        x0, x1 = cx - sx, cx + sx
        y0, y1 = cy - sy, cy + sy
        z0, z1 = cz - sz, cz + sz
        base = len(self.vertices) + 1
        self.vertices += [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
        ]
        self.faces += [
            (name, [base + 0, base + 1, base + 2, base + 3]),
            (name, [base + 4, base + 7, base + 6, base + 5]),
            (name, [base + 0, base + 4, base + 5, base + 1]),
            (name, [base + 1, base + 5, base + 6, base + 2]),
            (name, [base + 2, base + 6, base + 7, base + 3]),
            (name, [base + 4, base + 0, base + 3, base + 7]),
        ]

    def write(self, path: Path) -> None:
        lines = ["# Rocket League soccer-net prototype", "mtllib goal_net.mtl", "o GoalNet"]
        lines += [f"v {x:.5f} {y:.5f} {z:.5f}" for x, y, z in self.vertices]
        last_material = None
        for material, indices in self.faces:
            if material != last_material:
                lines += [f"usemtl {material}"]
                last_material = material
            lines.append("f " + " ".join(str(index) for index in indices))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build(width: float, height: float, depth: float, columns: int, rows: int) -> Obj:
    mesh = Obj()
    frame = max(width, height) * 0.035
    post_y = 0.0
    back_y = depth
    material_frame = "GoalFrame"
    material_net = "NetRope"

    # Front frame: two posts, crossbar, and a lower rail.
    mesh.box(material_frame, (-width / 2, post_y, height / 2), (frame, frame, height))
    mesh.box(material_frame, (width / 2, post_y, height / 2), (frame, frame, height))
    mesh.box(material_frame, (0, post_y, height), (width + frame, frame, frame))
    mesh.box(material_frame, (0, post_y, frame / 2), (width, frame, frame))

    # Roof and side supports give the net a real volume instead of a flat plane.
    mesh.box(material_frame, (0, depth / 2, height), (width, frame, frame))
    mesh.box(material_frame, (-width / 2, depth / 2, height / 2), (frame, depth, frame))
    mesh.box(material_frame, (width / 2, depth / 2, height / 2), (frame, depth, frame))
    mesh.box(material_frame, (0, back_y, height / 2), (width, frame, height))

    rope = max(width, height) * 0.009
    # Net on the back wall.
    for column in range(columns + 1):
        x = -width / 2 + width * column / columns
        mesh.box(material_net, (x, back_y - frame, height / 2), (rope, rope, height))
    for row in range(rows + 1):
        z = height * row / rows
        mesh.box(material_net, (0, back_y - frame, z), (width, rope, rope))

    # Roof and side net panels, slightly inset from the frame.
    for column in range(columns + 1):
        x = -width / 2 + width * column / columns
        mesh.box(material_net, (x, depth / 2, height - frame * 2), (rope, depth, rope))
    for column in range(columns + 1):
        x = -width / 2 + width * column / columns
        mesh.box(material_net, (x, depth / 2, frame * 2), (rope, depth, rope))
    for row in range(rows + 1):
        z = height * row / rows
        mesh.box(material_net, (-width / 2 + frame * 2, depth / 2, z), (rope, depth, rope))
        mesh.box(material_net, (width / 2 - frame * 2, depth / 2, z), (rope, depth, rope))

    return mesh


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("assets"))
    parser.add_argument("--width", type=float, default=7.32)
    parser.add_argument("--height", type=float, default=2.44)
    parser.add_argument("--depth", type=float, default=2.0)
    parser.add_argument("--columns", type=int, default=18)
    parser.add_argument("--rows", type=int, default=8)
    args = parser.parse_args()
    if min(args.width, args.height, args.depth, args.columns, args.rows) <= 0:
        parser.error("all dimensions and subdivisions must be positive")

    args.output.mkdir(parents=True, exist_ok=True)
    mesh = build(args.width, args.height, args.depth, args.columns, args.rows)
    mesh.write(args.output / "goal_net.obj")
    (args.output / "goal_net.mtl").write_text(
        "newmtl GoalFrame\nKd 0.82 0.86 0.84\n\n"
        "newmtl NetRope\nKd 0.72 0.94 0.68\n\n",
        encoding="utf-8",
    )
    print(f"wrote {len(mesh.vertices)} vertices and {len(mesh.faces)} faces to {args.output}")


if __name__ == "__main__":
    main()

