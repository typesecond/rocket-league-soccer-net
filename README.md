# Rocket League Soccer Net

A custom-map-first prototype for a more realistic soccer-style goal net in
Rocket League.

## Current status

Includes a procedural OBJ generator, generated mesh and materials, a Blender
FBX export script, a Windows staging helper, and a browser deformation study.
The OBJ output is reproducible from source. Blender export, UDK import, game
collision, scoring, and in-game deformation still need end-to-end validation.
There is no finished Rocket League map or Workshop release in this repository.

## Project direction

The first version will be a standalone goal asset with a visible net mesh,
simple gameplay-safe collision, and a short net deformation animation when a
goal is scored. Integration will target offline/custom-map workflows rather
than online game injection.

## MVP

- regulation-style goal frame and net volume;
- blue/orange material variants;
- controllable net depth and grid spacing;
- visual deformation with deterministic settle time;
- collision that does not snag cars or balls;
- export/package instructions for a custom Rocket League map.

## Planned milestones

1. Procedural standalone mesh prototype.
2. Material and animation test scene.
3. Custom-map integration.
4. Goal-event-driven deformation.
5. Packaging, compatibility notes, and playtest checklist.

See [docs/design.md](docs/design.md) for the current implementation brief.

## Run the prototype

The first milestone is a dependency-free browser sandbox:

```sh
cd prototype
python3 -m http.server 4173
```

Open <http://localhost:4173> and use **Trigger goal** to preview the net
deformation. The controls change net depth, grid spacing, shot speed, and
impact position.

This prototype is intentionally separate from Rocket League. It gives us a
place to tune the deformation behavior before packaging a custom-map asset.

See [docs/workshop.md](docs/workshop.md) for the later Steam Workshop
publishing path and account requirements.

The game-facing workflow is documented in
[docs/udk-integration.md](docs/udk-integration.md). Generate the first
importable goal asset with:

```sh
python3 tools/generate_goal_net.py
```

For the Windows/UDK integration workflow, see
[tools/README-Windows.md](tools/README-Windows.md) and run
`tools/Prepare-SoccerNet.ps1` from PowerShell.

## Source checks

GitHub Actions checks Python and JavaScript syntax and regenerates the OBJ/MTL
files to compare them with the committed assets. It does not run Blender, UDK,
PowerShell, or Rocket League.

## Publication history

The September 11–17, 2026 commit dates are a reconstructed publication timeline,
not original development timestamps. See [docs/history.md](docs/history.md).

