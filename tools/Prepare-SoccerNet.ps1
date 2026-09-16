[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path $_ -PathType Container })]
    [string]$UdkRoot,

    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [switch]$OpenEditor
)

$ErrorActionPreference = 'Stop'

$udkEditor = Join-Path $UdkRoot 'Binaries\Win32\UDK.exe'
$contentRoot = Join-Path $UdkRoot 'UDKGame\Content'
$sourceRoot = Join-Path $contentRoot 'SoccerNet'
$assetRoot = Join-Path $ProjectRoot 'assets'

if (-not (Test-Path $udkEditor -PathType Leaf)) {
    throw "UDK.exe was not found at $udkEditor. Install UDK 2015-02 and pass its root folder."
}

if (-not (Test-Path (Join-Path $assetRoot 'goal_net.fbx') -PathType Leaf)) {
    throw "goal_net.fbx is missing. Run Blender with tools/generate_goal_net_blender.py first."
}

New-Item -ItemType Directory -Force -Path $sourceRoot | Out-Null
Copy-Item (Join-Path $assetRoot 'goal_net.fbx') (Join-Path $sourceRoot 'goal_net.fbx') -Force

$instructions = @"
SoccerNet source staged at:
  $sourceRoot

In UDK:
  1. Open the SoccerNet package or create one named SoccerNetAssets.
  2. Import goal_net.fbx into the package.
  3. Assign GoalFrame and NetRope materials manually if UDK does not preserve them.
  4. Set collision to frame-only; keep NetRope visual-only.
  5. Save the package before opening the target Rocket League map.
"@
Set-Content -Path (Join-Path $sourceRoot 'IMPORT.txt') -Value $instructions

Write-Host "Soccer-net assets staged for UDK 2015." -ForegroundColor Green
Write-Host "Next: import goal_net.fbx into a package named SoccerNetAssets, then place the mesh in the target map."

if ($OpenEditor) {
    Start-Process -FilePath $udkEditor -ArgumentList '-editor'
}

