# Design brief

## Scope

The implementation begins as an offline/custom-map asset. A
BakkesMod DLL or online injection path is intentionally out of scope.

## MVP definition

Build a replacement goal assembly with:

- a regulation-looking frame and net volume;
- a visible mesh net with controllable depth and grid spacing;
- collision that preserves the existing goal behavior;
- a goal event or test trigger that briefly animates the net backward;
- blue/orange material variants;
- an export path that can be loaded by current custom-map tooling.

The first version should use a deforming visual mesh plus simple collision
volumes. Simulating every rope intersection is unnecessary for the MVP.

## Implementation plan

1. **Standalone asset prototype** — create the goal frame, net mesh, materials,
   and a small animation/test scene outside Rocket League.
2. **Rocket League map integration** — import the asset into a custom map and
   preserve stock goal trigger/collision behavior.
3. **Goal-response animation** — drive a short net displacement from the goal
   event, with shot speed and impact position controlling amplitude.
4. **Packaging and compatibility** — document the supported map loader and keep
   the asset usable offline/custom-map only.

## Acceptance checks

- A ball entering the goal is still scored exactly once.
- The net visibly deforms and settles within a short, deterministic interval.
- The ball and cars cannot snag on decorative net strands.
- The asset works for both goal colors and mirrored field ends.
- The map loads in an offline/custom-map session using the documented loader.

## References

- [Rocket League Custom Maps](https://rl-custom-maps.github.io/)
- [Map Expansion Plugin](https://github.com/blaku-rl/MapExpansionPlugin)
- [Rocket League Map Designer](https://github.com/adamwinuk-lgtm/rl-map-designer)
- [Epic support: third-party software](https://www.epicgames.com/help/c-37599050/c-42869540/a22460826)

