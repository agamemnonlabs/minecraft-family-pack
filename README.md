# Family Minecraft server pack

Original art and sounds for our family Paper server (Minecraft 26.3, Java + Bedrock via Geyser):

- **Foam Blaster**: the Pewpew `foam_blaster` gun (item model `family:foam_blaster`).
  Crafted from crossbow + amethyst shard + orange dye.
  Main hand only: one put in the off-hand goes back to the inventory.
- **Lightsabers**: 7 colours, separate items on top of a diamond sword (item model `family:lightsaber_<colour>`).
  Crafted from diamond sword + amethyst shard + dye; hitting something plays a "vwoom".
  iPads see the soft see-through halo in hand; it doesn't glow in the dark (held items can't on Bedrock).
- **iPad in-hand models** (attachables in `build.py`): katanas and lightsabers use the bow's hold, adjusted so the
  hilt sits in the fist with a katana's edge underneath. In the off-hand they are invisible on iPad.
- **Elemental katanas** (`katana.py`, art in `katana_art.py`, sounds in `katana_sounds.py`): Flame, Water, Thunder and
  Wind, separate items on top of a diamond sword (item model `family:katana_<element>`). Crafted from diamond sword +
  amethyst shard + blaze powder / prismarine crystals / copper ingot / feather, or `../give-katana.sh ELEMENT PLAYER`.
  - Every swing draws that katana's own arc of particles. Swings at air need the Skript plugin with
    `skript/family-katana.sk` (a datapack can't see them); hits on mobs and players also add a burst.
  - Hold use for the special move (Ember Crescent, Tide Ribbon, Storm Strike, Gale Spiral): 6 damage to hostile
    mobs only (tag `family:katana_targets`), other players are only pushed back, 3 s cooldown.
  - PC players see glowing, animated blades and a whack or stab swing; iPads see the blade animate in hand
    (solid colours, no glow at night), a still hotbar picture and the swing speed.
  - Previews: `python3 katana.py` writes `previews/katanas.png` and `previews/katana-sounds-<element>.wav`.
- **The Undersea** (`undersea.py`, art in `undersea_art.py`): dimension `family:undersea`, vanilla overworld
  terrain with the sea level raised to 100 and only vanilla ocean biomes (Bedrock players can't see custom
  biomes). Everyone there gets conduit power (breathing + underwater sight).
  - Getting there: whirlpool portals, or the **Bubble Shell** (kelp + sand + glass bottle; hold use for 1 s,
    it takes you to the hub and back to where you left).
  - **Shark costume**: hood, suit, pants, flippers. Crafted from the diamond piece + grey dye + white dye.
    Same protection as diamond, unbreakable.
  - Admin, once after the first start: `/function family:undersea/build_hub` (builds the hub on the
    seabed at x -168, z -144, and sets keep-inventory on and monster spawning off in the Undersea).
  - Admin, where a portal should go: stand there and run `/function family:portal_here` (replaces a 5x5x3
    area under your feet). `/function family:portal_remove` next to one removes its trigger.
    `/function family:portal_plaza` next to one levels a grass plaza around it (radius 8) and adds a beacon beam.
  - **Town** (`town.py`, previews in `previews/town-*.png`): original cartoon town around the hub. Seashell,
    coconut and watermelon houses, the Bubble Cafe (a sunken submarine), 6 empty plots for the kids, a jelly
    meadow, streets, a welcome arch the kids can name, a bus stop and hidden light blocks.
    Admin, ONCE ever: `/function family:undersea/build_town` (it flattens the plots, so never again once kids build).
    `/function family:undersea/tidy_town` clears natural reef (coral, sand/stone lumps) between and 6 blocks
    around the town and refreshes the hidden lights; it leaves plots, buildings and anything built alone.
  - **Costume ring** (`wardrobe.py`, preview `previews/wardrobe.png`): free costumes at the hub. Eight armour
    stands wear the costumes around the hub, each with a pink pad in front. Stepping on a pad gives the pieces of
    that costume you don't already have. Admin: `/function family:undersea/build_wardrobe` (safe to re-run:
    it replaces the stands and pads).

### Paint your own costume
Any costume (`shark`, `diver`, `angler`, `turtle`, `coral`, `axolotl`, `sponge`, `spongebuddy`) can be hand-painted:
1. `python3 undersea_art.py <name>` writes the current art to `art/costumes/<name>_1.png` (hood, top, sleeves,
   feet) and `<name>_2.png` (legs + waistband), plus `guide_<name>_1.png` / `_2.png` showing which pixels are which.
2. Paint `<name>_1.png` / `<name>_2.png` in a pixel editor that keeps transparency (Piskel, Aseprite, Pixilart).
   Keep them 64x32. Pixels are either solid or fully see-through (half-transparent ones get rounded).
   Leave the hood's face hole and the bottom 2 rows of the sleeves empty if you want the face and hands to show.
3. `python3 build.py`: if both files exist they replace the drawn art, on PC and iPad alike (bump `VERSION`).
   Delete them to go back to the drawn art. The item icons stay as drawn.

| File | Goes to |
|---|---|
| `dist/family-pack-java.zip` | `server.properties` `resource-pack` (PC players) |
| `dist/family-pack-bedrock.mcpack` | `plugins/Geyser-Spigot/packs/` (iPads) |
| `geyser/custom_mappings/family.json` | `plugins/Geyser-Spigot/custom_mappings/` |
| `dist/family-datapack.zip` | `world/datapacks/` (recipes, hit sound, blaster main-hand lock) |
| `skript/family-katana.sk` | `plugins/Skript/scripts/` (katana swing arcs; needs the Skript plugin) |

Rebuild after editing `art.py` / `sounds.py`: `python3 build.py` (needs Pillow and `oggenc` from vorbis-tools).
The server links to a specific commit, so a rebuild only goes live once that link and its sha1 are updated.
