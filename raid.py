"""Undersea raids: sea raiders attack the whole town (town.py). Datapack only.
- Start: a kid taps the alarm bell on the hub (where everyone arrives) > "Ring it!" (10 s warning; the bell rests 15 minutes after a
  raid), or a surprise raid at Undersea dusk (the chef going to bed, alive.py): only when a kid has been in town 10+
  minutes and the last raid was 60+ minutes ago, 1-in-2 chance, 30 s warning. Admin: raid/start, raid/stop,
  raid/surprises_on, raid/surprises_off.
- Warning: "ENEMY ATTACK!" title, raid horns and bells, a red countdown bar, the town's 43 lamps blinking red, whirlpools
  at the 4 breach points, a banner over the welcome arch.
- In the fight: everyone in the town's zone (not spectators, racers or players tagged family.raid.exempt) switches to
  Adventure (mobs never target Creative players), heals 1 heart every 20 s, and gets their own game mode back when they leave
  the zone or the Undersea, or the raid ends (also after a restart or rejoining later). A racer is left to the race; if
  the raid ends mid-race, the race gives the mode back (race.py's tags).
- Bubble rescue: at 3 hearts or less in a raid, a kid is healed, shielded for 5 s and sent to the hub.
- Waves (N = kids in the fight): 1 Scouts, 4+2N Barnacle Pirates. 2 Crew: N+2 Pirates, N+2 Seabed Shamblers, 2 Bone
  Divers, 1-2 Spike Eyes. 3 Captain Grimtide with N+2 Shell Riders. The next wave comes when 2 or fewer are left or
  after 90 s; at most 24 alive. Beat the Captain and the rest swim off: TOWN SAVED, 3 Sand Dollars per defender.
- Town Spirit (green bar) drops 1 a second for each raider within 8 blocks of the hub; at 0, or after 8 minutes, the
  raiders swim off with the cafe's cookies (no bonus, nothing really lost).
- Raiders: vanilla mobs (so iPads see them) with low hits on Easy, no drops but a 1-in-3 Sand Dollar (5 from the Captain)
  when a kid beats them, no item pickup, never despawning by themselves (vanilla drops monsters 32+ blocks from players). A raider with no kid near drifts towards the square; one that swims high above
  the town or wanders off is pulled back to a whirlpool. Every raider goes when the raid ends; leftovers (a restart,
  unloaded chunks) go as soon as they load.
Coordinates are relative to the hub centre like town.py (y=0 is the ground).
  python3 raid.py -> checks the spots and prints the layout
  build.py        -> family:undersea/raid/*  (admin runs family:undersea/build_raid once for the alarm bell; safe to re-run)"""
import json
import town, undersea, alive, houses, townsfolk as tf
from town import M
from townsfolk import F, snbt, say

DIM = undersea.DIM
ZONE, ZONE_Y, MARGIN = (-62, -68, 56, 56), (-20, 70), 20   # x1 z1 x2 z2: inside = in the fight; out past MARGIN more
HIGH = 25                                                  # raiders this far above the street are pulled back
BREACH = {"n": (0, -66), "e": (56, -6), "s": (-6, 54), "w": (-62, 6)}   # whirlpools, on the seabed
ALARM = (0, -4)                                            # post (y 1-2) and bell (y 3): the hub's north side, facing
OLD_ALARM = (-6, -12)                                      # the arch; the first spot (beside the arch) was hard to find
POST, BELL = town.wl(town.LAMP_POST), M + "bell[attachment=floor,facing=south]"
BANNER = (0.5, 12.5, -11.5)                                # over the welcome arch (its golden pearl is at y 10)
RESCUE = (0.5, 1, 4.5)                                     # on the hub platform, clear of its bubble column
LAMPS = sorted(p for p, b in tf.T.v.items() if b == town.LAMP) + [(x, 4, z) for x in (-2, 2) for z in (-2, 2)]
ALERT = M + "red_concrete"                                 # a lamp during the raid
HUB_NEAR, KID_NEAR, RESCUE_HP, REGEN_EVERY = 8, 16, 6, 10    # REGEN_EVERY s: half a heart (a short Regeneration I)
WARN, SURPRISE_WARN, WAVE_TIME, LIMIT, QUIET = 10, 30, 90, 480, 30                 # seconds
COOLDOWN, SURPRISE_GAP, SURPRISE_TOWN = 900, 3600, 600
CAP, WIN_PAY, CAPTAIN_PAY, DROP = 24, 3, 5, 0.333
TEAM = "family.raiders"
NIGHT = tf.NIGHT
# kind: (mob, name, name colour, health, attributes, more NBT). Hits on Easy: attack_damage 1 = half a heart, 2 = a heart.
RAIDERS = {
    "pirate": ("drowned", "Barnacle Pirate", "dark_aqua", 16, {"attack_damage": 1}, {}),
    "shambler": ("zombie_villager", "Seabed Shambler", "dark_green", 16,   # walks the seabed; a zombie villager never
                 {"attack_damage": 1, "water_movement_efficiency": 0.6, "spawn_reinforcements": 0}, {}),  # turns drowned
                                                                   # (a zombie does in 26.3, whatever its InWaterTime)
    "diver": ("skeleton", "Bone Diver", "gray", 14, {"water_movement_efficiency": 0.6},
              {"equipment": {"mainhand": {"id": M + "bow", "count": 1}}}),
    "eye": ("guardian", "Spike Eye", "gold", 16, {"attack_damage": 2, "follow_range": 16}, {}),   # 30 normally: they dart
                                                    # about. Its beam reaches as far as it targets: 64 sniped unseen
    "rider": ("drowned", "Shell Rider", "aqua", 16, {"attack_damage": 1}, {}),           # rides a zombie nautilus
    "captain": ("drowned", "Captain Grimtide", "light_purple", 60, {"attack_damage": 2, "scale": 1.8,
                                                                     "knockback_resistance": 0.6},
                {"equipment": {"mainhand": {"id": M + "spyglass", "count": 1}, "head": {"id": M + "golden_helmet", "count": 1}},
                 "CustomNameVisible": True}),
}
# wave: [(kind, how many, whirlpools)]; how many: "2n+4", "n+2", a number, or "eyes" (1, 2 with 2+ kids)
WAVES = {1: [("pirate", "2n+4", "we")],
         2: [("pirate", "n+2", "nsw"), ("shambler", "n+2", "nsw"), ("diver", "2", "nsw"), ("eye", "eyes", "e")],
         3: [("rider", "n+2", "n")]}
WAVE_TEXT = {1: ("WAVE 1", "Barnacle Pirates!", None),
             2: ("WAVE 2", "Pirates, Shamblers, Bone Divers and Spike Eyes!",
                 "Here comes their crew! Watch out for the Spike Eyes' lasers!"),
             3: ("CAPTAIN GRIMTIDE!", "Beat the Captain to save the town!",
                 "That's Captain Grimtide! Beat him and the rest will swim away!")}

def world():
    """Every known block in town: town, course, cafe, pearls, and the houses' work."""
    w = dict(alive.world())
    w.update(houses.SIGNS); w.update(houses.club_seal()); w.update(houses.club_roof())
    w.update({p: "shelf" for p in houses.SHELVES + [houses.LECTERN]})
    return w

def check():
    w = world()
    x, z = ALARM
    for p in [(x, 1, z), (x, 2, z), (x, 3, z), (x, 4, z)]:
        assert p not in w, f"the alarm bell's spot {p} is taken: {w[p]}"
    for p in [(0, 12, -12), (0, 11, -12), (0, 1, 4), (0, 2, 4)]:
        assert p not in w, f"{p} is taken: {w[p]}"
    assert len(LAMPS) == 43, len(LAMPS)
    for k, (bx, bz) in BREACH.items():
        assert not any(z1 - 6 <= bz <= z2 + 6 and x1 - 6 <= bx <= x2 + 6 for x1, z1, x2, z2, _ in tf.T.zones), k

def nbt(kind, tags):
    mob, name, colour, hp, attrs, extra = RAIDERS[kind]
    return {"Tags": tags, "Team": TEAM, "CustomName": {"text": name, "color": colour}, "Health": F(hp),
            "CanPickUpLoot": False, "PersistenceRequired": True,
            "DeathLootTable": f"family:raid/{'captain' if kind == 'captain' else 'raider'}",
            "drop_chances": {"mainhand": F(0), "head": F(0)},
            "attributes": [{"id": M + "max_health", "base": float(hp)},
                           {"id": M + "follow_range", "base": float(attrs.get("follow_range", 64))},
                           *[{"id": M + k, "base": float(v)} for k, v in attrs.items() if k != "follow_range"]], **extra}

def summon(kind, tags):
    """Summon command (relative position ~ ~ ~) for one raider; a Shell Rider comes on its zombie nautilus."""
    if kind == "rider":
        mount = {"Tags": tags + ["family.raid.mount"], "Team": TEAM, "PersistenceRequired": True,
                 "DeathLootTable": "minecraft:empty",
                 "attributes": [{"id": M + "follow_range", "base": 64.0}],
                 "Passengers": [{"id": M + "drowned", **nbt("rider", [t for t in tags if t != "family.raid.new"]
                                                            + ["family.raid.rider"])}]}
        return f"summon minecraft:zombie_nautilus ~ ~ ~ {snbt(mount)}"
    return f"summon minecraft:{RAIDERS[kind][0]} ~ ~ ~ {snbt(nbt(kind, tags + [f'family.raid.{kind}']))}"

def datapack(data, put, give_string):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    d = f"{data}/data/family"
    f, fn, mcf = f"{d}/function/undersea/raid", "family:undersea/raid", undersea.mcf
    check()
    num = lambda v: f"{round(v, 3):g}"
    a = lambda x, y, z: f"{num(hx + x)} {num(hy + y)} {num(hz + z)}"                # absolute
    sea = f"execute in {DIM} "
    S = lambda name: f"#{name} family.raid"
    score = lambda name: {"score": {"name": f"#{name}", "objective": "family.raid"}}
    def box(m=0, y1=ZONE_Y[0], y2=ZONE_Y[1]):
        x1, z1, x2, z2 = ZONE
        return f"x={hx + x1 - m},y={hy + y1},z={hz + z1 - m},dx={x2 - x1 + 2 * m},dy={y2 - y1},dz={z2 - z1 + 2 * m}"
    everyone = f"{sea}as @a[distance=0..] at @s run function"           # everyone in the Undersea
    raiders = "@e[tag=family.raider,tag=!family.raid.mount]"
    hub = a(0.5, 1, 0.5)
    def shout(text):
        """Mayor Marina to everyone in the Undersea; {kid} = the player running it."""
        parts, mayor = text.split("{kid}"), tf.FOLK["mayor"]
        comps = [{"text": mayor["name"], "color": mayor["colour"]}, {"text": ": " + parts[0], "color": "white"}]
        for p in parts[1:]:
            comps += [{"selector": "@s", "color": "white"}, {"text": p, "color": "white"}]
        return f"{sea}run tellraw @a[distance=0..] " + json.dumps(comps)
    def titles(title, colour, sub, times="5 50 15"):
        return [f"title @s times {times}", "title @s subtitle " + json.dumps({"text": sub, "color": "yellow"}),
                "title @s title " + json.dumps({"text": title, "color": colour, "bold": True})]
    sound = lambda s, pitch=1: f"playsound minecraft:{s} master @s ~ ~ ~ 1 {pitch}"
    bars = ("wave", "spirit", "captain")

    # --- loot: a Sand Dollar (the exact coin the shops take: custom_data as SNBT keeps it an int)
    coin = {"type": "minecraft:set_components", "components": {
        **{k: v for k, v in tf.COIN_COMPONENTS.items() if k != "minecraft:custom_data"},
        "minecraft:custom_data": "{family_coin:1}"}}
    def loot(n, chance):
        conds = [{"type": "minecraft:killed_by_player"}] + ([{"type": "minecraft:random_chance", "chance": chance}] if chance < 1 else [])
        mods = [coin] + ([{"type": "minecraft:set_count", "count": n}] if n > 1 else [])
        return {"type": "minecraft:entity", "pools": [{"rolls": 1, "condition": {"type": "minecraft:all_of", "terms": conds},
                                                       "entries": [{"type": "minecraft:item", "name": tf.COIN, "modifier": mods}]}]}
    put(f"{d}/loot_table/raid/raider.json", loot(1, DROP))
    put(f"{d}/loot_table/raid/captain.json", loot(CAPTAIN_PAY, 1))
    put(f"{d}/tags/block/raid_open.json", {"values": [M + b for b in (       # what a drifting raider may move into
        "water", "bubble_column", "seagrass", "tall_seagrass", "kelp", "kelp_plant", "light", "sea_pickle")]
        + ["#minecraft:corals", "#minecraft:wall_corals"]})

    put(f"{f}/load.mcfunction", mcf(
        "scoreboard objectives add family.raid dummy",
        "scoreboard objectives add family.raid_bell trigger",
        "scoreboard objectives add family.raid_hp health",
        f'team add {TEAM} {{"text":"Sea Raiders"}}',
        *[f"scoreboard players set {S(n)} {n}" for n in (2, 3, 60)],
        f"scoreboard players set {S('cap')} {CAP}",
        f"execute unless score {S('on')} matches 0..1 run scoreboard players set {S('on')} 0",
        f"execute unless score {S('surprise')} matches 0..1 run scoreboard players set {S('surprise')} 1",
        f"execute unless score {S('since')} matches 0.. run scoreboard players set {S('since')} {SURPRISE_GAP}",
        f"schedule function {fn}/loop 1s replace",
        f"execute if score {S('on')} matches 1 if score {S('wave')} matches 0 run schedule function {fn}/blink 10t replace"))
    # every tick: the alarm bell's dialog button, and bubble rescue (health 0 = dead: left alone)
    put(f"{f}/tick.mcfunction", mcf(
        f"execute as @a[scores={{family.raid_bell=1..}}] run function {fn}/bell_go",
        f"execute if score {S('on')} matches 1 {sea[8:]}as @a[distance=0..,scores={{family.raid_hp=1..{RESCUE_HP}}},"
        f"gamemode=!creative,gamemode=!spectator] at @s run function {fn}/rescue"))
    put(f"{f}/rescue.mcfunction", mcf(
        "effect give @s minecraft:instant_health 1 1 true", "effect give @s minecraft:resistance 5 4 true",
        "particle minecraft:bubble ~ ~1 ~ 0.4 0.8 0.4 0.1 40",
        f"{sea}run tp @s {a(*RESCUE)}",
        *titles("Bubble rescue!", "aqua", "Catch your breath, then jump back in!", "5 40 10"),
        sound("block.note_block.chime", 1.5)))

    # --- the 1-second loop
    put(f"{f}/loop.mcfunction", mcf(
        f"schedule function {fn}/loop 1s replace",
        f"execute if score {S('on')} matches 1 run return run function {fn}/fight_loop",
        f"function {fn}/idle"))
    put(f"{f}/idle.mcfunction", mcf(
        f"execute as @e[tag=family.raider] at @s run function {fn}/flee",            # leftovers
        "kill @e[type=minecraft:text_display,tag=family.raid.banner]",
        f"execute as @a[tag=family.raid.in] run function {fn}/leave",              # rejoined after the raid ended
        f"execute if score {S('cool')} matches 1.. run scoreboard players remove {S('cool')} 1",
        f"scoreboard players add {S('since')} 1",
        f"{sea}if entity @a[{box()},tag=!family.raid.exempt,gamemode=!spectator] run scoreboard players add {S('town')} 1",
        f"{sea}unless entity @a[{box()},tag=!family.raid.exempt,gamemode=!spectator] run scoreboard players set {S('town')} 0",
        f"execute if score {NIGHT} matches 0 run scoreboard players set {S('dusk')} 0",
        f"execute if score {NIGHT} matches 1 unless score {S('dusk')} matches 1 run function {fn}/dusk",
        f"{sea}positioned {hub} if entity @a[distance=..24] run scoreboard players add {S('near')} 1",
        f"{sea}positioned {hub} unless entity @a[distance=..24] run scoreboard players set {S('near')} 0",
        f"execute if score {S('built')} matches 1 if score {S('near')} matches 5.. run function {fn}/repair",
        f"scoreboard players add {S('heal')} 1",
        f"execute if score {S('heal')} matches 30.. run function {fn}/lamps_white"))
    put(f"{f}/dusk.mcfunction", mcf(
        f"scoreboard players set {S('dusk')} 1",
        f"execute unless score {S('surprise')} matches 1 run return 0",
        f"execute unless score {S('since')} matches {SURPRISE_GAP}.. run return 0",
        f"execute unless score {S('town')} matches {SURPRISE_TOWN}.. run return 0",
        f"execute store result score {S('r')} run random value 0..1",
        f"execute if score {S('r')} matches 1 run function {fn}/begin_surprise"))
    put(f"{f}/fight_loop.mcfunction", mcf(
        f"execute as @a[tag=family.raid.in] at @s unless dimension {DIM} run function {fn}/leave",
        f"{sea}as @a[tag=family.raid.in] unless entity @s[{box(MARGIN)}] run function {fn}/leave",
        f"{sea}as @a[{box()},tag=!family.raid.in,tag=!family.raid.exempt,tag=!family.racing,gamemode=!spectator] "
        f"run function {fn}/join",
        *[f"{sea}run bossbar set family:raid_{b} players @a[distance=0..]" for b in bars],
        f"{sea}if entity @a[{box()}] run scoreboard players set {S('quiet')} 0",
        f"{sea}unless entity @a[{box()}] run scoreboard players add {S('quiet')} 1",
        f"execute if score {S('quiet')} matches {QUIET}.. run return run function {fn}/finish",
        f"scoreboard players add {S('regen')} 1",
        f"execute if score {S('regen')} matches {REGEN_EVERY}.. run function {fn}/regen",
        f"execute if score {S('wave')} matches 0 run return run function {fn}/warning",
        f"function {fn}/fighting"))
    put(f"{f}/regen.mcfunction", mcf(f"scoreboard players set {S('regen')} 0",
                                     "effect give @a[tag=family.raid.in] minecraft:regeneration 3 0 true"))

    # --- joining and leaving the fight (a racer's saved mode goes to the race if the raid ends mid-race)
    put(f"{f}/join.mcfunction", mcf(
        "tag @s add family.raid.in",
        "execute if entity @s[gamemode=creative] run tag @s add family.raid.creative",
        "execute if entity @s[gamemode=survival] run tag @s add family.raid.survival",
        "gamemode adventure @s",
        'tellraw @s {"text":"You\'re in the fight! No flying until the raid is over. If you get hurt, a bubble carries '
        'you to safety.","color":"gold"}'))
    put(f"{f}/leave.mcfunction", mcf(
        "tag @s remove family.raid.in",
        "effect clear @s minecraft:regeneration",
        "execute if entity @s[tag=family.racing,tag=family.raid.creative] run tag @s add family.race.creative",
        "execute if entity @s[tag=family.racing,tag=family.raid.survival] run tag @s add family.race.survival",
        "execute if entity @s[tag=!family.racing,tag=family.raid.creative] run gamemode creative @s",
        "execute if entity @s[tag=!family.racing,tag=family.raid.survival] run gamemode survival @s",
        "tag @s remove family.raid.creative", "tag @s remove family.raid.survival"))

    # --- starting: the alarm bell (a kid), a surprise at dusk, or the admin
    put(f"{f}/begin.mcfunction", mcf(
        f"scoreboard players set {S('on')} 1", f"scoreboard players set {S('wave')} 0",
        f"scoreboard players operation {S('t')} = {S('warn')}",
        f"scoreboard players set {S('spirit')} 100", f"scoreboard players set {S('quiet')} 0",
        'bossbar add family:raid_wave {"text":"ENEMY ATTACK!","color":"red"}', "bossbar set family:raid_wave color red",
        f"execute store result bossbar family:raid_wave max run scoreboard players get {S('warn')}",
        f"execute store result bossbar family:raid_wave value run scoreboard players get {S('warn')}",
        'bossbar add family:raid_spirit {"text":"Town Spirit","color":"green"}', "bossbar set family:raid_spirit color green",
        "bossbar set family:raid_spirit max 100", "bossbar set family:raid_spirit value 100",
        *[f"{sea}run bossbar set family:raid_{b} players @a[distance=0..]" for b in bars[:2]],
        "kill @e[type=minecraft:text_display,tag=family.raid.banner]",
        f"{sea}run summon minecraft:text_display {a(*BANNER)} " + snbt({
            "Tags": ["family.raid.banner"], "billboard": "center", "brightness": {"sky": 15, "block": 15},
            "text": {"text": "ENEMY ATTACK!", "color": "red", "bold": True},
            "transformation": {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                               "translation": [F(0), F(0), F(0)], "scale": [F(2.5)] * 3}}),
        f"function {fn}/lamps_red", f"scoreboard players set {S('blink')} 0",
        f"schedule function {fn}/blink 10t replace"))
    starts = {"start": (WARN, "alarm", "Sea raiders are coming! Everyone, defend the town!"),
              "begin_bell": (WARN, "alarm", "{kid} rang the alarm bell! Sea raiders are coming! Everyone, defend the town!"),
              "begin_surprise": (SURPRISE_WARN, "surprise",
                                 f"Sea raiders spotted! They attack in {SURPRISE_WARN} seconds. Everyone, get ready!")}
    for name, (warn, fx, text) in starts.items():
        put(f"{f}/{name}.mcfunction", mcf(
            f"execute if score {S('on')} matches 1 run return fail",
            f"scoreboard players set {S('warn')} {warn}", f"function {fn}/begin",
            f"{everyone} {fn}/fx/{fx}", shout(text)))
    put(f"{f}/fx/alarm.mcfunction", mcf(*titles("ENEMY ATTACK!", "red", "Raiders are coming! Defend the town!"),
                                        sound("event.raid.horn"), sound("block.bell.use")))
    put(f"{f}/fx/surprise.mcfunction", mcf(*titles("ENEMY ATTACK!", "red", f"Surprise raid! {SURPRISE_WARN} seconds to get ready!"),
                                           sound("event.raid.horn"), sound("block.bell.use")))
    put(f"{f}/fx/horn.mcfunction", mcf(sound("event.raid.horn"), sound("block.bell.use", 0.8)))
    put(f"{f}/fx/count.mcfunction", mcf(sound("block.note_block.pling", 1.5)))
    # lamps blink every 0.5 s in the warning; red all through the fight; only our own two blocks are ever swapped
    put(f"{f}/lamps_red.mcfunction", mcf(*[f"{sea}if block {a(*p)} {town.LAMP} run setblock {a(*p)} {ALERT}" for p in LAMPS]))
    put(f"{f}/lamps_white.mcfunction", mcf(f"scoreboard players set {S('heal')} 0",
                                           *[f"{sea}if block {a(*p)} {ALERT} run setblock {a(*p)} {town.LAMP}" for p in LAMPS]))
    put(f"{f}/blink.mcfunction", mcf(
        f"execute unless score {S('on')} matches 1 run return 0",
        f"execute unless score {S('wave')} matches 0 run return 0",
        f"schedule function {fn}/blink 10t replace",
        f"scoreboard players add {S('blink')} 1",
        f"execute if score {S('blink')} matches 2.. run scoreboard players set {S('blink')} 0",
        f"execute if score {S('blink')} matches 0 run function {fn}/lamps_red",
        f"execute if score {S('blink')} matches 1 run function {fn}/lamps_white"))
    for k, (bx, bz) in BREACH.items():
        put(f"{f}/whirl/{k}.mcfunction", mcf(*[
            f"{sea}positioned {a(bx + 0.5, 0, bz + 0.5)} positioned over ocean_floor run particle {p}" for p in (
                "minecraft:trial_omen ~ ~1.5 ~ 1.2 1.5 1.2 0.02 40 force", "minecraft:bubble_column_up ~ ~1 ~ 1.5 2 1.5 0.2 40 force",
                "minecraft:soul ~ ~1 ~ 1 1 1 0.02 12 force")]))
    put(f"{f}/warning.mcfunction", mcf(
        f"scoreboard players remove {S('t')} 1",
        f"execute store result bossbar family:raid_wave value run scoreboard players get {S('t')}",
        "bossbar set family:raid_wave name " + json.dumps([{"text": "ENEMY ATTACK in ", "color": "red"}, score("t"), {"text": " s"}]),
        *[f"function {fn}/whirl/{k}" for k in BREACH],
        f"execute if score {S('t')} matches 20 run {everyone} {fn}/fx/horn",
        f"execute if score {S('t')} matches 5 run {everyone} {fn}/fx/horn",
        f"execute if score {S('t')} matches 1..3 run {everyone} {fn}/fx/count",
        f"execute if score {S('t')} matches ..0 run function {fn}/wave/1"))

    # --- waves: each raider comes out of one of the wave's whirlpools in turn, then spreads 2.5 blocks on the seabed
    def counts(how):
        if how == "eyes":
            return [f"scoreboard players set {S('k')} 1", f"execute if score {S('n')} matches 2.. run scoreboard players add {S('k')} 1"]
        if "n" in how:
            mult, add = how.split("n+")
            return [f"scoreboard players operation {S('k')} = {S('n')}"] + [f"scoreboard players operation {S('k')} += {S('n')}"] * (
                int(mult or 1) - 1) + [f"scoreboard players add {S('k')} {add}"]
        return [f"scoreboard players set {S('k')} {how}"]
    def spawn_fn(kind, k, tags=("family.raider", "family.raid.new")):
        bx, bz = BREACH[k]
        return mcf(f"{sea}positioned {a(bx + 0.5, 0, bz + 0.5)} positioned over ocean_floor run {summon(kind, list(tags))}",
                   f"function {fn}/settle")
    put(f"{f}/settle.mcfunction", mcf(
        "execute as @e[tag=family.raid.new] store result entity @s Rotation[0] float 1 run random value 0..359",
        "execute as @e[tag=family.raid.new] at @s positioned ^ ^ ^2.5 positioned over ocean_floor run tp @s ~ ~ ~",
        f"execute as @e[tag=family.raid.new] at @s run rotate @s facing {hub}",
        "tag @e[tag=family.raid.new] remove family.raid.new"))
    made = set()
    for w, groups in WAVES.items():
        for kind, how, where in groups:
            for k in where:
                if (kind, k) not in made:
                    made.add((kind, k)); put(f"{f}/s/{kind}/{k}.mcfunction", spawn_fn(kind, k))
            put(f"{f}/many/{kind}/{where}.mcfunction", mcf(
                f"execute if score {S('k')} matches ..0 run return 0",
                f"execute if score {S('alive')} >= {S('cap')} run return 0",
                f"scoreboard players remove {S('k')} 1", f"scoreboard players add {S('alive')} 1",
                *([f"function {fn}/s/{kind}/{where}"] if len(where) == 1 else [
                    f"scoreboard players operation {S('m')} = {S('k')}",
                    f"scoreboard players operation {S('m')} %= {S(len(where))}",
                    *[f"execute if score {S('m')} matches {i} run function {fn}/s/{kind}/{k}" for i, k in enumerate(where)]]),
                f"function {fn}/many/{kind}/{where}"))
        title, sub, line = WAVE_TEXT[w]
        put(f"{f}/fx/wave{w}.mcfunction", mcf(*titles(title, "light_purple" if w == 3 else "red", sub, "5 40 10"),
                                              sound("event.raid.horn")))
        put(f"{f}/wave/{w}.mcfunction", mcf(
            f"scoreboard players set {S('wave')} {w}", f"scoreboard players set {S('t')} 0",
            *([f"scoreboard players set {S('elapsed')} 0", f"function {fn}/lamps_red",
               "data modify entity @e[type=minecraft:text_display,tag=family.raid.banner,limit=1] text set value "
               + json.dumps({"text": "DEFEND THE TOWN!", "color": "gold", "bold": True})] if w == 1 else []),
            f"execute store result score {S('n')} if entity @a[tag=family.raid.in]",
            f"execute if score {S('n')} matches ..0 run scoreboard players set {S('n')} 1",
            f"execute store result score {S('alive')} if entity {raiders}",
            *([f"{sea}positioned {a(BREACH['n'][0] + 0.5, 0, BREACH['n'][1] + 0.5)} positioned over ocean_floor run {summon('captain', ['family.raider', 'family.raid.new'])}",
               f"function {fn}/settle",
               f"{sea}positioned {a(BREACH['n'][0] + 0.5, 0, BREACH['n'][1] + 0.5)} positioned over ocean_floor run "
               "particle minecraft:sonic_boom ~ ~2 ~ 1 1 1 0 3 force",
               f"{sea}positioned {a(BREACH['n'][0] + 0.5, 0, BREACH['n'][1] + 0.5)} positioned over ocean_floor run "
               "particle minecraft:explosion_emitter ~ ~2 ~ 0 0 0 0 1 force",
               'bossbar add family:raid_captain {"text":"Captain Grimtide","color":"light_purple"}',
               "bossbar set family:raid_captain color purple", f"bossbar set family:raid_captain max {RAIDERS['captain'][3]}",
               f"bossbar set family:raid_captain value {RAIDERS['captain'][3]}"] if w == 3 else []),
            *[l for kind, how, where in groups for l in (*counts(how), f"function {fn}/many/{kind}/{where}")],
            *[f"function {fn}/whirl/{k}" for k in sorted({k for _, _, where in groups for k in where})],
            f"execute store result score {S('left')} if entity {raiders}",
            f"execute store result bossbar family:raid_wave max run scoreboard players get {S('left')}",
            f"{everyone} {fn}/fx/wave{w}", *([shout(line)] if line else [])))
    put(f"{f}/next.mcfunction", mcf(f"execute if score {S('wave')} matches 1 run return run function {fn}/wave/2",
                                    f"function {fn}/wave/3"))

    # --- every second of the fight: count, Town Spirit, bars, strays, next wave / win / lose
    put(f"{f}/fighting.mcfunction", mcf(
        f"scoreboard players add {S('t')} 1", f"scoreboard players add {S('elapsed')} 1",
        f"execute store result score {S('left')} if entity {raiders}",
        f"{sea}positioned {hub} store result score {S('hub')} if entity {raiders[:-1]},distance=..{HUB_NEAR}]",
        f"scoreboard players operation {S('spirit')} -= {S('hub')}",
        f"execute if score {S('hub')} matches 1.. as @a[tag=family.raid.in] run title @s actionbar "
        + json.dumps({"text": "Raiders in the square! Town Spirit is dropping!", "color": "red"}),
        f"execute store result bossbar family:raid_spirit value run scoreboard players get {S('spirit')}",
        f"execute store result bossbar family:raid_wave value run scoreboard players get {S('left')}",
        "bossbar set family:raid_wave name " + json.dumps(
            [{"text": "Wave ", "color": "red"}, score("wave"), {"text": " of 3 - "}, score("left"), {"text": " raiders left"}]),
        f"execute if score {S('wave')} matches 3 store result bossbar family:raid_captain value run "
        "data get entity @e[tag=family.raid.captain,limit=1] Health",
        # a mount whose rider is gone swims off; strays high up or far out go back to the north whirlpool; a raider
        # with no kid near drifts a block towards the square through open water, or a block up and on (a rising seabed,
        # a wall), so walkers on the seabed don't stall at their whirlpool
        "tag @e[tag=family.raid.mount] add family.raid.lonely",
        "execute as @e[tag=family.raid.rider] on vehicle run tag @s remove family.raid.lonely",
        f"execute as @e[tag=family.raid.lonely] at @s run function {fn}/flee",
        f"{sea}as @e[tag=family.raider,tag=!family.raid.rider,{box(MARGIN, HIGH, 200)}] at @s run function {fn}/pull",
        f"{sea}as @e[tag=family.raider,tag=!family.raid.rider] unless entity @s[{box(MARGIN)}] at @s run function {fn}/pull",
        "tag @e[tag=family.raid.moved] remove family.raid.moved",
        *[f"{sea}as @e[tag=family.raider,tag=!family.raid.rider,tag=!family.raid.moved] at @s unless entity @a[distance=..{KID_NEAR},"
          f"gamemode=!creative,gamemode=!spectator] facing {num(hx + 0.5)} ~ {num(hz + 0.5)} positioned ^ ^{up} ^1 "
          f"if block ~ ~ ~ #family:raid_open if block ~ ~1 ~ #family:raid_open run function {fn}/step" for up in (0, 1)],
        f"execute if score {S('spirit')} matches ..0 run return run function {fn}/lose",
        f"execute if score {S('elapsed')} matches {LIMIT}.. run return run function {fn}/lose",
        f"execute if score {S('wave')} matches 3 unless entity @e[tag=family.raid.captain] run return run function {fn}/win",
        f"execute if score {S('wave')} matches 1..2 if score {S('left')} matches ..2 if score {S('t')} matches 5.. "
        f"run return run function {fn}/next",
        f"execute if score {S('wave')} matches 1..2 if score {S('t')} matches {WAVE_TIME}.. run function {fn}/next"))
    put(f"{f}/step.mcfunction", mcf("tp @s ~ ~ ~ ~ ~", "tag @s add family.raid.moved"))
    put(f"{f}/pull.mcfunction", mcf(
        "particle minecraft:bubble ~ ~1 ~ 0.4 0.6 0.4 0.1 15",
        f"{sea}positioned {a(BREACH['n'][0] + 0.5, 0, BREACH['n'][1] + 0.5)} positioned over ocean_floor run tp @s ~ ~ ~"))
    put(f"{f}/flee.mcfunction", mcf("particle minecraft:bubble ~ ~1 ~ 0.4 0.6 0.4 0.1 15", "function family:undersea/alive/remove"))

    # --- the end
    coins = f"give @s {give_string(tf.COIN, tf.COIN_COMPONENTS)} {WIN_PAY}"
    put(f"{f}/win.mcfunction", mcf(
        f"{everyone} {fn}/fx/win",
        f"{sea}run particle minecraft:totem_of_undying {a(0.5, 4, 0.5)} 4 3 4 0.6 100 force",
        shout(f"Hooray! You saved the town! Here are {WIN_PAY} Sand Dollars for every defender!"),
        f"execute as @a[tag=family.raid.in] run {coins}",
        f"function {fn}/finish"))
    put(f"{f}/fx/win.mcfunction", mcf(*titles("TOWN SAVED!", "gold", "The raiders swam away!", "5 70 20"),
                                      sound("entity.player.levelup"), sound("ui.toast.challenge_complete"),
                                      sound("entity.firework_rocket.twinkle")))
    put(f"{f}/lose.mcfunction", mcf(
        f"{everyone} {fn}/fx/lose",
        shout(f"Oh no! The raiders swam off with the cafe's cookies! Don't worry, the chef will bake more. "
              f"The alarm bell can ring again in {COOLDOWN // 60} minutes."),
        f"function {fn}/finish"))
    put(f"{f}/fx/lose.mcfunction", mcf(*titles("OH NO!", "red", "The raiders swam off with the cafe's cookies!", "5 70 20"),
                                       sound("entity.villager.no")))
    put(f"{f}/finish.mcfunction", mcf(
        f"scoreboard players set {S('on')} 0", f"scoreboard players set {S('wave')} 0",
        f"scoreboard players set {S('cool')} {COOLDOWN}", f"scoreboard players set {S('since')} 0",
        f"schedule clear {fn}/blink",
        f"execute as @e[tag=family.raider] at @s run function {fn}/flee",
        *[f"bossbar remove family:raid_{b}" for b in bars],
        "kill @e[type=minecraft:text_display,tag=family.raid.banner]",
        f"function {fn}/lamps_white",
        f"execute as @a[tag=family.raid.in] run function {fn}/leave"))
    put(f"{f}/stop.mcfunction", mcf(f"execute unless score {S('on')} matches 1 run return fail",
                                    shout("The raid is called off. Thanks for helping, everyone!"), f"function {fn}/finish"))
    put(f"{f}/surprises_on.mcfunction", mcf(f"scoreboard players set {S('surprise')} 1"))
    put(f"{f}/surprises_off.mcfunction", mcf(f"scoreboard players set {S('surprise')} 0"))

    # --- the alarm bell: a post with a bell, a tap box over both, a label
    x, z = ALARM
    post = [(x, 1, z, POST), (x, 2, z, POST), (x, 3, z, BELL)]
    place = [f"{sea}if block {a(px, py, pz)} #family:race_free run setblock {a(px, py, pz)} {b}" for px, py, pz, b in post]
    tap_box = f"{sea}run summon minecraft:interaction {a(x + 0.5, 0.95, z + 0.5)} " + snbt(
        {"Tags": ["family.raid.alarm", "family.tap.alarm"], "width": F(1.2), "height": F(3.3)})
    label = f"{sea}run summon minecraft:text_display {a(x + 0.5, 4.6, z + 0.5)} " + snbt({
        "Tags": ["family.raid.alarm", "family.raid.label"], "billboard": "center", "brightness": {"sky": 15, "block": 15},
        "transformation": {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                           "translation": [F(0), F(0), F(0)], "scale": [F(1.6)] * 3},
        "text": [{"text": "ALARM BELL\n", "color": "red", "bold": True},
                 {"text": "Tap to call the sea raiders!", "color": "white", "bold": False}]})
    put(f"{d}/advancement/raid/tap_alarm.json", {
        "criteria": {"tap": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {"entity": {
            "type": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": '{Tags:["family.tap.alarm"]}'}}}}},
        "rewards": {"function": f"{fn}/tap"}})
    put(f"{f}/tap.mcfunction", mcf(
        "advancement revoke @s only family:raid/tap_alarm",
        f"{sea}run playsound minecraft:block.bell.use block @a {a(x + 0.5, 3.5, z + 0.5)} 2 1",
        f"execute if score {S('on')} matches 1 run return run " + say("mayor", "The raid is on, {kid}! Chase those raiders out of town!"),
        f"execute if score {S('cool')} matches 1.. run return run function {fn}/rest",
        "scoreboard players enable @s family.raid_bell",
        "dialog show @s " + snbt({"type": "minecraft:multi_action", "title": {"text": "Alarm Bell", "color": "red"},
                                  "body": [{"type": "minecraft:plain_message", "contents": {"text":
                                      "Ring the alarm? Sea raiders will attack the whole town! Everyone in town switches to "
                                      "Adventure (no flying) until the raid is over."}}],
                                  "columns": 1, "actions": [{"label": "Ring it!", "action": {
                                      "type": "minecraft:run_command", "command": "/trigger family.raid_bell set 1"}}],
                                  "exit_action": {"label": "Not now"}})))
    put(f"{f}/rest.mcfunction", mcf(
        f"scoreboard players operation {S('min')} = {S('cool')}", f"scoreboard players add {S('min')} 59",
        f"scoreboard players operation {S('min')} /= {S(60)}",
        "tellraw @s " + json.dumps([{"text": "The alarm bell needs a rest. Ring it again in ", "color": "yellow"},
                                    score("min"), {"text": " min."}])))
    put(f"{f}/bell_go.mcfunction", mcf(
        "scoreboard players set @s family.raid_bell 0",
        f"execute if score {S('cool')} matches 1.. run return fail",
        f"function {fn}/begin_bell"))
    put(f"{f}/repair.mcfunction", mcf(
        f"scoreboard players set {S('near')} 0", *place,
        f"execute unless entity @e[type=minecraft:interaction,tag=family.tap.alarm] run {tap_box}",
        f"execute unless entity @e[type=minecraft:text_display,tag=family.raid.label] run {label}"))
    ox, oz = OLD_ALARM
    old = [f"{sea}if block {a(ox, y, oz)} {b.split('[')[0]} run setblock {a(ox, y, oz)} minecraft:water" for _, y, _, b in post]
    area = f"{hx + min(x, ox) - 1} {hz + min(z, oz) - 1} {hx + max(x, ox) + 1} {hz + max(z, oz) + 1}"
    put(f"{data}/data/family/function/undersea/build_raid.mcfunction", mcf(
        f"{sea}run forceload add {area}", f"schedule function {fn}/build 3s replace"))
    put(f"{f}/build.mcfunction", mcf(
        f"{sea}unless loaded {a(x, 0, z)} run return run schedule function {fn}/build 2s replace",
        f"{sea}unless loaded {a(ox, 0, oz)} run return run schedule function {fn}/build 2s replace",
        f"{sea}run kill @e[tag=family.raid.alarm]", *old, *place, tap_box, label,
        f"scoreboard players set {S('built')} 1", f"{sea}run forceload remove {area}"))

    # --- admin mob trial: one raider 6 blocks ahead of whoever runs it (not a raid: kept until trial/clear)
    for kind in RAIDERS:
        put(f"{f}/trial/{kind}.mcfunction", mcf(
            f"execute positioned ^ ^ ^6 positioned over ocean_floor run {summon(kind, ['family.raid.trial'])}"))
    put(f"{f}/trial/clear.mcfunction", mcf(f"execute as @e[tag=family.raid.trial] at @s run function {fn}/flee"))

if __name__ == "__main__":
    check()
    print(len(LAMPS), "lamps; alarm", ALARM, "; breaches", BREACH)
