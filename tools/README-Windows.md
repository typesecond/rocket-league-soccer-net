# Windows UDK Setup

Stage the generated FBX for UDK 2015-02 and import it into a custom-map package.

## Requirements

- Windows with UDK 2015-02 installed.
- Blender available as `blender.exe` on the command line.
- An existing Rocket League custom-map workspace.

See [the integration guide](../docs/udk-integration.md) for mapmaking setup references.

## Generate and stage

From PowerShell in the repository root:

```powershell
blender.exe --background --python tools/generate_goal_net_blender.py -- --output assets/goal_net.fbx
.\tools\Prepare-SoccerNet.ps1 -UdkRoot 'C:\UDK\UDK-2015-02'
```

The staging script checks for `Binaries\Win32\UDK.exe` and `assets/goal_net.fbx`,
then copies the FBX and import instructions to `UDKGame\Content\SoccerNet`.
Add `-OpenEditor` to launch UDK after staging.

## Import into the map

1. Import `goal_net.fbx` into a package named `SoccerNetAssets`.
2. Assign the `GoalFrame` and `NetRope` materials.
3. Place a goal at each end of the field and mirror the second instance.
4. Keep decorative net geometry out of gameplay collision. Preserve the map's
   scoring triggers and collision volumes.
5. Save and cook/export the map, then test both goals in an offline session.
   Check scoring, ball clearance, and car movement around the frame.

The exported mesh is static. The browser deformation study is not exported as
an FBX animation.
