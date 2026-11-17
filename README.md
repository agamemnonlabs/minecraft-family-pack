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
  The foam blaster's third person is turned the same way (muzzle ahead, top up); it sits a little above the fist.
- **Elemental katanas** (`katana.py`, art in `katana_art.py`, sounds in `katana_sounds.py`): Flame, Water, Thunder and
  Wind, separate items on top of a diamond sword (item model `family:katana_<element>`). Crafted from diamond sword +
  amethyst shard + blaze powder / prismarine crystals / copper ingot / feather, or `../give-katana.sh ELEMENT PLAYER`.
  From the server console (or in game as an op): `execute as PLAYER run function family:give/flame_katana`
  (also `water_katana`, `thunder_katana`, `wind_katana`; `@a` gives one to everyone online).
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
    that costume you don't already have. A knocked-over mannequin or broken pad comes back on its own within
    about 10 s while someone is near the hub. Admin: `/function family:undersea/build_wardrobe` (safe to re-run:
    it replaces the stands and pads).
  - **Townsfolk** (`townsfolk.py`, previews `previews/townsfolk-map.png` and `townsfolk-cafe.png`): four villagers
    with original names, paid in **Sand Dollars** (a gold nugget named so; renamed nuggets don't count).
    - **Chef Clamuel** lives in the Bubble Cafe, now dry inside behind a wooden door (a second roof layer stops drip
      particles), with a kitchen behind a 1.5-high counter (customers stand on a half-block step to see over it). The
      chef keeps full villager life (smoker by day, bed at night). Tap the chef to buy Coral Cookies, Kelp Shakes,
      Sea Pies and Party Cakes. Tap the bell on the counter for **Order Up!**: one lunch a Minecraft day (20 min) to
      deliver to another townsperson for 3 Sand Dollars.
    - **Mayor Marina** (welcome arch) runs **Lost Pearls**: 10 golden pearls (ochre froglights) hidden around town.
      Tap one to find it (progress per kid); all 10 pay 10 Sand Dollars and a pet fish, once.
    - **Farmer Kelpsey** (Jelly Meadow) buys kelp, sea pickles and seagrass for Sand Dollars.
    - **Driver Finnley** (bus stop) runs the **Current Race** (below).
    - The three outside are frozen posts (NoAI + Invulnerable, so they don't float up or drown); they turn to
      face a nearby kid. Everyone greets a kid once per visit. Talking uses dialog menus (iPad: forms).
    - Admin: `/function family:undersea/build_townsfolk` (re-run replaces the townsfolk and boxes and re-does the
      cafe rework). Missing townsfolk, tap boxes or pearls come back on their own while a kid is at the hub.
      `/function family:undersea/folk/give_coins` gives you 10 Sand Dollars for testing.
  - **Current Race** (`race.py`, preview `previews/race.png`): a swim race around town. Tap Driver Finnley at the bus
    stop > Let's race! > 3, 2, 1, GO. The clock runs from the checkered START gate across the south street, through 11
    checkpoints in order (10 red-and-white rings with floating numbers, and the welcome arch as number 10), and back
    through the gate. Your next checkpoint sparkles, and a short trail of sparkles in front of you points at it (only
    you see them); 5-minute limit. Corners are split across two rings so no turn is sharper than about 55 degrees.
    - Checkpoint 5 is the **Bubble Lift** past the east street's end: 3x3 soul sand makes an upward bubble column,
      and racers ride it up through a flat ring. An invisible light block ends the bubbles 16 up (so nobody is carried to
      the surface) without a ceiling to get pinned against: you float out of the top and swim on. No down columns (they
      need magma, which burns).
    - Racers are in Adventure mode (no flying, no breaking hoops) and get their own game mode back at the finish, on
      Stop racing (tap Finnley again), on leaving the Undersea or on rejoining the game.
    - Best times are on the sidebar, shown only in the Undersea (everyone there is on the aqua team `family.undersea`,
      so names show aqua). The score is race points (3000 minus the time in tenths of a second) so the fastest is on
      top: PCs show the time, iPads show the time after the name and the points on the right.
    - A broken ring block comes back within 5 s while someone is near the hub.
    - Admin: `/function family:undersea/build_race` (places the gate and rings only into water, so never over
      anything built; re-run replaces the floating numbers). `/function family:undersea/race/reset_times` clears the
      board.

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
