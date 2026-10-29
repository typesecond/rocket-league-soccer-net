# Rocket League Soccer Net

Procedural goal and net geometry for a Rocket League custom-map project.
Python generates the mesh and materials, Blender exports FBX, and a PowerShell
script stages the asset for UDK. Width, height, depth, and net subdivisions are
configurable.

The exported asset is static. A separate browser study handles visual net
deformation from shot speed and impact position.

## Generate the asset

Requires Python 3. FBX export also requires Blender on the command line.

```sh
python3 tools/generate_goal_net.py
blender --background --python tools/generate_goal_net_blender.py -- --output assets/goal_net.fbx
```

The Python generator writes `assets/goal_net.obj` and `assets/goal_net.mtl`.
The Blender script builds the geometry directly and writes `assets/goal_net.fbx`.
Both use separate `GoalFrame` and `NetRope` materials.

Defaults are 7.32 m wide, 2.44 m high, and 2 m deep, with 18 columns and 8 rows.
The OBJ contains 736 vertices and 552 quad faces. Override the dimensions and
subdivisions with `--width`, `--height`, `--depth`, `--columns`, and `--rows`.
The OBJ generator also accepts `--output` to select an output directory.

## UDK workflow

On Windows, stage the FBX in an existing UDK installation:

```powershell
.\tools\Prepare-SoccerNet.ps1 -UdkRoot 'C:\UDK\UDK-2015-02' -OpenEditor
```

Import it into `SoccerNetAssets`, assign the materials, and keep decorative net
geometry separate from gameplay collision. The integration plan retains the
map's existing scoring triggers and collision volumes.

See the [UDK import guide](docs/udk-integration.md) and
[Windows setup](tools/README-Windows.md) for the full workflow.

## Deformation study

```sh
python3 -m http.server 4173 --directory prototype
```

Open http://localhost:4173 and select **Trigger goal**. The Canvas renderer
varies displacement with shot speed and distance from the impact, then returns
the net to its starting shape. Depth, grid spacing, and impact coordinates can
be adjusted in the browser.

## Source checks

CI checks Python and JavaScript syntax, regenerates the OBJ/MTL files, and
compares them against the committed assets.

[Design](docs/design.md) · [Workshop plan](docs/workshop.md)

Commit dates are reconstructed; see [repository history](docs/history.md).
