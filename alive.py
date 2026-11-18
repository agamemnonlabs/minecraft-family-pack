"""Small touches that make the Undersea town (town.py) feel alive. Datapack only.
- Sea pets, named (names always show, PC and iPad), Invulnerable, never despawn:
  - axolotls Noodle, Sprinkles and Puddle in the square and Blueberry (the rare blue one) in the Jelly Meadow. Vanilla
    AI; one that strays past its range pops back home. Their bite does 0 damage, so they can't kill fish (the Lost
    Pearls pet fish) or the glow squid. A kid can bucket one: the bucket keeps the name but not our tags, so it's the
    kid's pet now, and a new one turns up in town.
  - turtles Grandpa Mossback and Pebble (a baby, kept little) in the Jelly Meadow. A vanilla turtle swims off towards a
    random spot up to 512 blocks away, so these are NoAI and paddle a slow loop instead (moved a little every tick).
- Bubble chimney: a vent in the Bubble Cafe's tower top with soul sand under it makes a real bubble column, ended
  9 blocks up by an invisible light block (the Bubble Lift trick, race.LIFT_END), so kids can ride it.
- Night = while Chef Clamuel is asleep in his bed (his vanilla routine, about half of each Minecraft day; a sleeping
  villager doesn't trade). Then a CLOSED sign floats over the cafe door, the chef's hello is a sleepy one
  (townsfolk.py), and three named glow squid drift among the jellies; they leave at sunrise.
- A missing pet, sign, glow squid or chimney block comes back once a kid has been near that part of town for 5 s
  (so everything there has loaded: no doubles).
Coordinates are relative to the hub centre like town.py (y=0 is the ground); floats are block positions (x.5 = mid-block).
  build.py -> family:undersea/alive/*  (admin runs family:undersea/build_alive; safe to re-run)"""
import json, math
import town, undersea, race, townsfolk as tf
from town import M
from townsfolk import F, snbt

T = tf.T
DIM = undersea.DIM
SQUARE, MEADOW, NEAR = (0.5, 2, 0.5), (0.5, 4, -38.5), 32      # a kid within NEAR of these "settles" that part
# key: (mob, name, name colour, spawn, range, area, extra NBT)
AXOLOTL = {"lucy": 0, "wild": 1, "gold": 2, "cyan": 3, "blue": 4}
NO_BITE = {"attributes": [{"id": "minecraft:attack_damage", "base": 0.0}]}
PETS = {
    "noodle": ("axolotl", "Noodle", "light_purple", (-5.5, 2, 6.5), 10, "square", {"Variant": AXOLOTL["lucy"], **NO_BITE}),
    "sprinkles": ("axolotl", "Sprinkles", "yellow", (6.5, 2, -5.5), 10, "square", {"Variant": AXOLOTL["gold"], **NO_BITE}),
    "puddle": ("axolotl", "Puddle", "aqua", (-5.5, 2, -5.5), 10, "square", {"Variant": AXOLOTL["cyan"], **NO_BITE}),
    "blueberry": ("axolotl", "Blueberry", "blue", (20.5, 4, -30.5), 8, "meadow", {"Variant": AXOLOTL["blue"], **NO_BITE}),
}
GLOW = {"glimmer": ("Glimmer", (-5.5, 8, -45.5)), "twinkle": ("Twinkle", (8.5, 8, -39.5)), "lumo": ("Lumo", (12.5, 9, -46.5))}
GLOW_RANGE = 8
# turtles paddle a loop: (name, colour, loop centre, radius, blocks per tick, baby)
TURTLES = {"mossback": ("Grandpa Mossback", "dark_green", (-16.5, 7.0, -35.5), 4.5, 0.04, False),
           "pebble": ("Pebble", "green", (-4.5, 6.0, -31.5), 3.0, 0.05, True)}
VENT = tf.cafe(0, 11, 1)                     # tower top, beside the periscope: becomes water (the column's bottom)
SOUL = (VENT[0], VENT[1] - 1, VENT[2])       # under it, inside the tower: soul sand
CAP = (VENT[0], VENT[1] + 9, VENT[2])        # column = 9 bubble cells, then the light block
SIGN_AT = (tf.CX + 0.5, 5.1, tf.CZ - 4.5)     # over the cafe's north door, just above the wall sign
NIGHT = tf.NIGHT                             # 1 while the chef sleeps, 0 while he's awake (kept while he's unloaded)
CHEF = "@e[type=minecraft:villager,tag=family.folk.chef]"

def loop(key):
    """A turtle's loop: (start point, turn per tick in degrees, points). It starts facing south (yaw 0) and each tick
    moves `speed` blocks ahead and turns, so it goes round a circle of the given radius about the centre."""
    _, _, (cx, cy, cz), r, speed, _ = TURTLES[key]
    n = round(2 * math.pi * r / speed)
    turn = 360 / n
    pts, x, z, yaw = [], 0.0, 0.0, 0.0
    for _ in range(n):
        pts.append((x, z))
        x -= speed * math.sin(math.radians(yaw)); z += speed * math.cos(math.radians(yaw))
        yaw += turn
    mx, mz = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    pts = [(cx + x - mx, cy, cz + z - mz) for x, z in pts]
    return pts[0], turn, pts

PLANTS = {M + "seagrass", M + "tall_seagrass[half=lower]", M + "tall_seagrass[half=upper]", M + "sea_pickle[pickles=3]"}

def world():
    """Every known block: the town, the course, the race's probe finds, the townsfolk's cafe work and pearls."""
    w = {**T.v, **race.SEEN, **race.blocks(), **tf.cafe_blocks(), **{p: tf.PEARL for p in tf.PEARLS}}
    w.update(race.lifts()[1])
    return w

def cells(x, y, z, half, height):
    """Block cells a box centred on (x, z), from y up `height`, overlaps."""
    return {(i, j, k) for i in range(math.floor(x - half), math.floor(x + half) + 1)
            for j in range(math.floor(y), math.floor(y + height) + 1) for k in range(math.floor(z - half), math.floor(z + half) + 1)}

def check():
    """Spawn spots, turtle loops, the sign and the chimney column must be in open water (plants are fine)."""
    w = world()
    blocked = lambda cs: sorted((p, w[p]) for p in cs if p in w and w[p] not in PLANTS and "light[" not in w[p])
    for key, (_, _, _, (x, y, z), *_) in PETS.items():
        assert not blocked(cells(x, y, z, 0.4, 0.5)), f"{key} spawns in {blocked(cells(x, y, z, 0.4, 0.5))}"
    for key, (_, (x, y, z)) in GLOW.items():
        assert not blocked(cells(x, y, z, 0.5, 0.9)), f"{key} spawns in {blocked(cells(x, y, z, 0.5, 0.9))}"
    for key in TURTLES:
        half, height = (0.3, 0.2) if TURTLES[key][5] else (0.8, 0.5)
        hit = blocked(set().union(*(cells(x, y, z, half, height) for x, y, z in loop(key)[2])))
        assert not hit, f"turtle {key}'s loop runs into {hit[:4]}"
    assert not blocked(cells(SIGN_AT[0], SIGN_AT[1], SIGN_AT[2], 0.3, 1.0)), "the CLOSED sign's spot is taken"
    assert T.v.get(VENT) == T.v.get(SOUL) == M + "orange_concrete", "the vent isn't in the tower top"
    col = [(VENT[0], y, VENT[2]) for y in range(VENT[1] + 1, CAP[1] + 1)]
    assert not [p for p in col if p in w], f"the chimney column is blocked: {[(p, w[p]) for p in col if p in w]}"
    assert all(abs(p[0] - VENT[0]) + abs(p[2] - VENT[2]) >= 2 for p in tf.PEARLS), "a pearl's tap box is in the column"

def name(text, colour):
    return {"text": text, "color": colour}

def common(key, text, colour):
    return {"Tags": ["family.alive", f"family.alive.{key}"], "CustomName": name(text, colour), "CustomNameVisible": True,
            "PersistenceRequired": True, "Invulnerable": True}

def datapack(data, put):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    f, fn, mcf = f"{data}/data/family/function/undersea/alive", "family:undersea/alive", undersea.mcf
    check()
    num = lambda v: f"{round(v, 3):g}"
    a = lambda x, y, z: f"{num(hx + x)} {num(hy + y)} {num(hz + z)}"   # absolute
    sea = f"execute in {DIM} "
    sel = lambda mob, key, extra="": f"@e[type=minecraft:{mob},tag=family.alive.{key}{extra}]"

    def summon_pet(key):
        mob, text, colour, spot, *_, nbt = PETS[key]
        return f"{sea}run summon minecraft:{mob} {a(*spot)} {snbt({**common(key, text, colour), **nbt})}"
    def summon_turtle(key):
        text, colour, *_, baby = TURTLES[key]
        nbt = {**common(key, text, colour), "NoAI": True, "Rotation": [F(0), F(0)]}
        if baby:
            nbt["Age"] = -2147483648                    # counts up by 1 a tick: a baby for 3 years
        return f"{sea}run summon minecraft:turtle {a(*loop(key)[0])} {snbt(nbt)}"
    def summon_glow(key):
        text, spot = GLOW[key]
        return [f"{sea}run summon minecraft:glow_squid {a(*spot)} {snbt(common(key, text, 'aqua'))}",
                f"{sea}run particle minecraft:bubble {a(*spot)} 0.6 0.6 0.6 0.05 25"]
    def summon_sign():
        nbt = {"Tags": ["family.alive", "family.alive.closed"], "billboard": "center", "brightness": {"sky": 15, "block": 15},
               "text": [{"text": "CLOSED\n", "color": "red", "bold": True},
                        {"text": "Chef Clamuel is asleep. Zzz\nOpen again at sunrise!", "color": "white", "bold": False}],
               "transformation": {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                                  "translation": [F(0), F(0), F(0)], "scale": [F(1.2)] * 3}}
        return f"{sea}run summon minecraft:text_display {a(*SIGN_AT)} {snbt(nbt)}"
    area_of = lambda key: PETS[key][5]

    put(f"{f}/load.mcfunction", mcf("scoreboard objectives add family.alive dummy",
                                    f"schedule function {fn}/loop 1s replace"))
    # every tick: the turtles paddle (rotated ~ 0: always level, whatever a push did to their pitch)
    put(f"{f}/tick.mcfunction", mcf(*[
        f"execute as {sel('turtle', k)} at @s rotated ~ 0 run tp @s ^ ^ ^{TURTLES[k][4]} ~{loop(k)[1]:.4f} 0" for k in TURTLES]))

    # every second: who's near, strays home, repairs once settled, night or day
    loop_cmds = [f"schedule function {fn}/loop 1s replace"]
    for area, c in (("square", SQUARE), ("meadow", MEADOW)):
        loop_cmds += [f"{sea}positioned {a(*c)} if entity @a[distance=..{NEAR}] run scoreboard players add #{area} family.alive 1",
                      f"{sea}positioned {a(*c)} unless entity @a[distance=..{NEAR}] run scoreboard players set #{area} family.alive 0",
                      f"execute if score #{area} family.alive matches 5.. run function {fn}/repair_{area}"]
    for key, (mob, _, _, spot, rng, *_) in PETS.items():
        loop_cmds.append(f"{sea}positioned {a(*spot)} as {sel(mob, key, f',distance={rng}..')} run tp @s {a(*spot)}")
    for key, (_, spot) in GLOW.items():
        loop_cmds.append(f"{sea}positioned {a(*spot)} as {sel('glow_squid', key, f',distance={GLOW_RANGE}..')} run tp @s {a(*spot)}")
    for key, (*_, (cx, cy, cz), r, _, _) in TURTLES.items():     # pushed off its loop: back to the start
        loop_cmds.append(f"{sea}positioned {a(cx, cy, cz)} as {sel('turtle', key, f',distance={r + 2}..')} "
                         f"run tp @s {a(*loop(key)[0])} 0 0")
    loop_cmds += [
        # night: the chef asleep (26.3 saves sleeping_pos; older versions SleepingX). Unknown while he isn't loaded.
        "scoreboard players set #now family.alive -1",
        f"execute as {CHEF} run scoreboard players set #now family.alive 0",
        f"execute as {CHEF} if data entity @s sleeping_pos run scoreboard players set #now family.alive 1",
        f"execute as {CHEF} if data entity @s SleepingX run scoreboard players set #now family.alive 1",
        f"execute unless score #now family.alive matches -1 run scoreboard players operation {NIGHT} = #now family.alive",
        f"execute if score {NIGHT} matches 0 run function {fn}/day",
        # the sign shares the chef's chunk: summon it only while he's loaded (then the sign is too, so no doubles)
        f"execute if score #now family.alive matches 1 unless entity @e[type=minecraft:text_display,tag=family.alive.closed] "
        f"run {summon_sign()}"]
    put(f"{f}/loop.mcfunction", mcf(*loop_cmds))
    put(f"{f}/day.mcfunction", mcf(
        f"execute as @e[type=minecraft:text_display,tag=family.alive.closed] at @s run function {fn}/remove",
        f"execute as @e[type=minecraft:glow_squid,tag=family.alive] at @s run function {fn}/swim_off"))
    put(f"{f}/swim_off.mcfunction", mcf("particle minecraft:bubble ~ ~0.4 ~ 0.6 0.6 0.6 0.05 25", f"function {fn}/remove"))
    # out of the world first: no death puff in town and the drops (glow ink) fall into the void
    put(f"{f}/remove.mcfunction", mcf("tp @s ~ -300 ~", "kill @s"))

    # repairs (each resets its counter, so they run every 5 s while kids stay)
    chimney = [f"{sea}if block {a(*CAP)} #family:race_free run setblock {a(*CAP)} {race.LIFT_END}",   # cap before soul sand
               f"{sea}if block {a(*SOUL)} #family:race_free run setblock {a(*SOUL)} minecraft:soul_sand"]   # mined: water
    for area in ("square", "meadow"):
        put(f"{f}/repair_{area}.mcfunction", mcf(
            f"scoreboard players set #{area} family.alive 0",
            *[f"execute unless entity {sel(PETS[k][0], k)} run {summon_pet(k)}" for k in PETS if area_of(k) == area],
            *([f"execute unless entity {sel('turtle', k)} run {summon_turtle(k)}" for k in TURTLES]
              + [f"execute if score {NIGHT} matches 1 unless entity {sel('glow_squid', k)} run function {fn}/glow/{k}"
                 for k in GLOW] if area == "meadow" else chimney)))
    for k in GLOW:
        put(f"{f}/glow/{k}.mcfunction", mcf(*summon_glow(k)))

    # build: load the square, meadow and cafe, wait for their entities, replace ours, cut the vent
    pts = [SQUARE, MEADOW, VENT] + [p[3] for p in PETS.values()] + [g[1] for g in GLOW.values()] + [t[2] for t in TURTLES.values()]
    x1, z1 = math.floor(min(p[0] for p in pts)) - 10, math.floor(min(p[2] for p in pts)) - 10
    x2, z2 = math.floor(max(p[0] for p in pts)) + 10, math.floor(max(p[2] for p in pts)) + 10
    area = f"{hx + x1} {hz + z1} {hx + x2} {hz + z2}"
    put(f"{data}/data/family/function/undersea/build_alive.mcfunction", mcf(
        f"{sea}run forceload add {area}", f"schedule function {fn}/build 3s replace"))
    put(f"{f}/build.mcfunction", mcf(
        *[f"{sea}unless loaded {hx + x} {hy} {hz + z} run return run schedule function {fn}/build 2s replace"
          for x, z in ((x1, z1), (x2, z2))],
        f"{sea}as @e[tag=family.alive] at @s run function {fn}/remove",
        *chimney[:1],
        f"{sea}if block {a(*VENT)} minecraft:orange_concrete run setblock {a(*VENT)} minecraft:water",
        f"{sea}if block {a(*SOUL)} minecraft:orange_concrete run setblock {a(*SOUL)} minecraft:soul_sand",
        *[summon_pet(k) for k in PETS], *[summon_turtle(k) for k in TURTLES],
        f"{sea}run forceload remove {area}"))

if __name__ == "__main__":
    check()
    for k in TURTLES:
        start, turn, pts = loop(k)
        print(k, "start", tuple(round(v, 2) for v in start), f"turn {turn:.4f} deg/tick, lap {len(pts) / 20:.1f} s")
