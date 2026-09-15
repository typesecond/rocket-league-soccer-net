# Rocket League Soccer Net

A procedural soccer-style goal asset for a Rocket League custom-map workflow.

This is a source prototype; game integration and collision validation are pending.

See [the design brief](docs/design.md) for the project scope.

## Browser study

Run `python3 -m http.server 4173 --directory prototype` and open http://localhost:4173 to study net deformation.

## Generate a mesh

Run `python3 tools/generate_goal_net.py` to produce OBJ and material files in `assets/`.

The default generated mesh and materials are committed under `assets/`.

## Blender and UDK

The FBX export script and proposed import workflow are described in [docs/udk-integration.md](docs/udk-integration.md).
