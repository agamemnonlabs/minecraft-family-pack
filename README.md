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
- **Parachute** (`parachute.py`, preview `previews/parachute.png`): worn on the back in the chest slot, like an
  elytra (so not together with a costume top). Crafted from 3 wool on top, string at both sides and leather in the
  bottom middle, or `../give-parachute.sh PLAYER`, or from the console: `execute as PLAYER run function family:give/parachute`.
  - It opens by itself after a 4-block fall, or early with jump in mid-air, if there are 3 blocks of air below.
    Crouch folds it (it then stays folded until you land, unless you jump again). It packs itself up on landing,
    in water and when flying (creative or elytra).
  - Floating: slow falling, plus a short levitation "brake" whenever you fall faster than 5 blocks/s, until you're
    under 3 b/s (about one tug every 2 s; the levitation icon blinks then). Slow falling alone settles near 10 b/s.
  - PC: the canopy is an item display riding the kid; it pops open over 5 ticks. It needs the Skript plugin with
    `skript/family-parachute.sk` (nothing can be put on a player by command). Without it, PC players see no canopy.
  - iPad: the worn item's attachable draws the canopy (the datapack swaps the item between `family:parachute` and
    `family:parachute_open`). Your own canopy shows only in third-person view; everyone else's always shows.
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
    `/function family:undersea/tidy_town` clears natural reef between and 6 blocks around the town and refreshes the
    hidden lights. Plots, buildings, streets and the meadow are never touched. Elsewhere it turns coral, sand,
    sandstone, stone (and granite, diorite, andesite, tuff, deepslate), dirt, gravel, clay and magma into water up to
    16 blocks above the seabed, including anything a kid built from them, so check for kids' builds outside the plots
    before running it.
  - **Dry houses** (`drain.py`, its own datapack `dist/family-drain.zip`): kids build the whole shell first from full
    blocks, with a door for the doorway. No stairs, slabs, fences, glass panes or trapdoors in the outer walls, roof
    or floor: water gets through them. Then an op stands in the water inside and runs `/function family:drain_here`
    (console: `execute as NAME at NAME run function family:drain_here`). The water turns to air, and waterlogged
    chests, stairs and the like inside are dried. If the water reaches the sea (a gap, or a room spreading more than
    15 blocks from where you stand) or holds more than 1500 blocks, nothing changes and the chat says why. Run it
    again for any pocket it missed. A roof one block thick shows drips underneath; a second layer or glass stops them.
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
    - **Leaderboard**: floating BEST TIMES text in front of the bus stop, beside Driver Finnley, with the top 5 names
      and times, updated at every finish. It turns to face you and you can swim through it. A racer appears after their next finish (names are picked up then: a player
      head filled with their profile, in a hidden item display). The sorted top 10 is in storage `family:race board`.
    - A broken ring block comes back within 5 s while someone is near the hub.
    - Admin: `/function family:undersea/build_race` (places the gate and rings only into water, so never over
      anything built; re-run replaces the floating numbers). `/function family:undersea/race/reset_times` clears the
      sidebar and the leaderboard.
  - **Town life** (`alive.py`):
    - Sea pets with their names always showing:
      - axolotls Noodle, Sprinkles and Puddle in the square, and Blueberry (blue) in the Jelly Meadow. One that strays
        too far pops back home. They don't bite (0 damage), so fish and glow squid are safe. A kid can bucket one and
        keep it; a new one turns up in town.
      - turtles Grandpa Mossback and baby Pebble, who paddle slow loops over the meadow. Vanilla turtles swim off
        towards spots hundreds of blocks away, so these two are moved by the datapack.
    - **Bubble chimney**: a vent in the Bubble Cafe's tower top (soul sand under it) sends up a bubble column that ends
      9 blocks up at an invisible light block, so kids can ride it and float out of the top.
    - **Night** is while Chef Clamuel sleeps in his bed (about half of each 20-minute day; sleeping villagers don't
      trade). During it:
      - a floating CLOSED sign hangs over the cafe door;
      - the chef's hello is a sleepy one;
      - glow squid Glimmer, Twinkle and Lumo drift among the jellies, and swim off at sunrise.
      - The Order Up! bell keeps working.
    - Missing pets, the sign, the glow squid and chimney blocks come back while a kid is nearby.
    - Admin: `/function family:undersea/build_alive` (re-run replaces the pets; it cuts the vent only where the tower is
      still as built).
  - **Houses** (`houses.py`, preview `previews/houses.png`): something to do in each house, with a sign over each door.
    - **Clam Bop** (Coconut house): tap Coach Cockle > Play Clam Bop!, then 3, 2, 1, GO: 30 seconds. 8 clams (bone
      blocks) in the coconut's floor pop open one at a time (glowing pink, bubbles, a pop) and shut again a second or so
      later, faster towards the end. Tap an open clam (iPad) or click it with either button (PC): 1 bop. Everyone in the
      coconut plays at once. Each kid's best is kept, the top 5 float on a TOP BOPPERS board in the coconut, and
      10 bops or more pays 2 Sand Dollars (once a Minecraft day). `/function family:undersea/houses/bop/reset_scores`
      clears the bests and the board.
    - **Professor Periwinkle** (Seashell house), among bookshelves: tap for a joke, a true sea fact, or the riddle of the
      day (3 answer buttons; right pays 2 Sand Dollars once a day, wrong gives a hint). Each kid hears all 24 jokes (and
      all 24 facts) once, in a scrambled order, before any comes round again. The texts are lists in `houses.py`.
    - **The clubhouse** (Watermelon house): dried out like the Bubble Cafe behind a wooden door, with a second rind layer
      where the sea would sit on a 1-thick ceiling (no drips). Empty for the kids to furnish; its sign says
      "(name me!)".
    - Coach Cockle and Professor Periwinkle are townsfolk posts like the mayor, and Order Up! lunches go to them too.
    - Missing clam tap boxes and the board come back while a kid is near the coconut; an open clam left over shuts.
    - Admin: `/function family:undersea/build_houses` (safe to re-run: it replaces the two townsfolk, the boxes and the
      board, and places blocks only into water).
  - **Raids** (`raid.py`): sea raiders attack the whole town.
    - Starting one: tap the **alarm bell** on the hub's north side > Ring it! (10 s warning; the bell rests 15 minutes
      after a raid). **Surprise raids** also come by themselves at Undersea dusk (when Chef Clamuel goes to bed), if a kid
      has been in town 10+ minutes and the last raid was 60+ minutes ago: a 1-in-2 chance, with a 30 s warning.
    - The warning: ENEMY ATTACK! title, raid horns and bells, the town's 43 lamps blinking red, whirlpools at four spots
      round the edge of town, a banner over the welcome arch and a red countdown bar.
    - Everyone in town switches to Adventure for the raid (monsters never go for Creative players), except spectators,
      racers and anyone tagged `family.raid.exempt`. They get their own game mode back on leaving town or the Undersea,
      when the raid ends, or on rejoining later. Healing is 1 heart every 20 s. **Bubble rescue**: at 3 hearts a kid is
      healed, shielded for 5 s and sent to the hub.
    - Waves (N = kids in the fight): 4+2N Barnacle Pirates (drowned); then Pirates, Seabed Shamblers (zombie villagers,
      they walk the seabed), 2 Bone Divers (skeletons) and 1-2 Spike Eyes (guardians); then Captain Grimtide (a big
      drowned with his own purple bar) and N+2 Shell Riders on zombie nautiluses. The next wave comes when 2 or fewer
      are left or after 90 s; at most 24 alive. Beat the Captain and the rest swim off: TOWN SAVED, 3 Sand Dollars per
      defender. Each raider a kid beats has a 1-in-3 chance of dropping a Sand Dollar; the Captain drops 5.
    - **Town Spirit** (green bar) drops 1 a second for each raider in the square. At 0, or after 8 minutes of fighting,
      the raiders swim off with the cafe's cookies (no bonus, nothing really lost).
    - Raiders hit softly (half a heart; the Captain a heart), pick nothing up and never despawn by themselves. One with
      no kid near drifts towards the square; one that swims high above town or wanders off goes back to a whirlpool.
      All of them go when the raid ends, and any left over (a restart, an unloaded chunk) goes as soon as it loads.
      Mob griefing is off in the Undersea (`execute in family:undersea run gamerule mob_griefing false`).
    - Admin: `/function family:undersea/build_raid` places the bell (safe to re-run). `/function family:undersea/raid/start`
      starts one (10 s warning, ignores the bell's rest), `raid/stop` calls it off, `raid/surprises_off` /
      `raid/surprises_on` switch surprise raids. To watch as an op without being attacked: `/tag NAME add
      family.raid.exempt` (`tag NAME remove family.raid.exempt` to fight). One raider to try out:
      `execute as NAME at NAME run function family:undersea/raid/trial/pirate` (also `shambler`, `diver`, `eye`,
      `rider`, `captain`); `/function family:undersea/raid/trial/clear` removes them.

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
| `dist/family-drain.zip` | `world/datapacks/` (drain command; rebuild with `python3 drain.py`) |
| `skript/family-katana.sk` | `plugins/Skript/scripts/` (katana swing arcs; needs the Skript plugin) |
| `skript/family-parachute.sk` | `plugins/Skript/scripts/` (parachute canopy on PC; needs the Skript plugin) |

Rebuild after editing `art.py` / `sounds.py`: `python3 build.py` (needs Pillow and `oggenc` from vorbis-tools).
The server links to a specific commit, so a rebuild only goes live once that link and its sha1 are updated.
