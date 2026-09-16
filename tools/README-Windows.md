# Windows integration checklist

This is the final game-facing workflow. The Mac is only being used to author
and version the source asset.

## One-time setup

1. Install **UDK 2015-02** on Windows.
2. Run the Rocket League mapmaking setup from
   <https://github.com/RocketLeagueMapmaking/UDK_RL_Setup>.
3. Install Rocket League on Steam or Epic on the same Windows machine.
4. Keep an untouched backup of the game's `TAGame/CookedPCConsole` directory.
5. Install a current custom-map loader or use the Steam Workshop route.

## Stage the asset

From PowerShell in the repository root:

```powershell
py -3 tools/generate_goal_net.py
blender.exe --background --python tools/generate_goal_net_blender.py -- --output assets/goal_net.fbx
Set-ExecutionPolicy -Scope Process Bypass
.\tools\Prepare-SoccerNet.ps1 -UdkRoot 'C:\UDK\UDK-2015-02'
```

Use `-OpenEditor` to launch UDK after staging:

```powershell
.\tools\Prepare-SoccerNet.ps1 -UdkRoot 'C:\UDK\UDK-2015-02' -OpenEditor
```

## Build the map

1. Create/open a custom Rocket League map in UDK.
2. Import `goal_net.fbx` into `SoccerNetAssets`.
3. Place one mesh at each goal and mirror the second instance.
4. Preserve the stock goal-scoring trigger and goal collision volumes.
5. Set the decorative `NetRope` geometry to no collision.
6. Save and cook/export the map as `.udk`/`.upk`.
7. Load the map in an offline/non-EAC Rocket League session.
8. Confirm scoring, ball exit behavior, car clearance, and both mirrored goals.

The first game build is intentionally static. Net deformation is the second
UDK milestone after the map loads and scores correctly.

