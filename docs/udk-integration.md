# Direct Rocket League integration

This is the proposed game-facing workflow. Blender export, UDK import, and
in-game behavior have not yet been validated end to end.

## Toolchain

Rocket League custom maps are authored with Unreal Development Kit 2015 and
exported as Unreal packages. The Rocket League Mapmaking community maintains a
setup path and UDK-specific documentation:

- <https://github.com/RocketLeagueMapmaking/UDK_RL_Setup>
- <https://rocketleaguemapmaking.com/>

The repository includes a portable OBJ generator, but the game-facing asset is
generated as FBX through Blender because FBX is UDK's preferred import format.
No proprietary or encrypted Rocket League package is committed.

## Build the first game asset

From the repository root:

```sh
python3 tools/generate_goal_net.py
blender --background --python tools/generate_goal_net_blender.py -- --output assets/goal_net.fbx
```

In UDK:

1. Import `assets/goal_net.fbx` into a new package named `SoccerNetAssets`.
2. Assign `GoalFrame` and `NetRope` materials.
3. Set the imported mesh to use simple collision only on the frame; the net
   should be visual-only.
4. Open a copy of a standard training/custom map.
5. Place and mirror the goal actor at both ends of the field.
6. Preserve the map's existing goal trigger and scoring volumes.
7. Cook/export the map as `.udk`/`.upk` and test it locally before Workshop
   publishing.

## What “direct” means here

The intended result is a custom-map asset. The current repository provides
source generators and staging instructions; it does not contain a tested game
map. Consult the game's official support and the mapmaking tool documentation
for current compatibility and permitted use before testing an exported map.

## Next integration milestone

The static net is the first game-facing checkpoint. Once it loads correctly,
we can add a second set of recessed net panels and an authored animation or
Kismet-driven impulse. That animation should remain visual-only and leave the
stock scoring/collision actors untouched.

