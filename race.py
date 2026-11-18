"""The Current Race: Driver Finnley's swim race around the Undersea town (town.py).
- Tap Driver Finnley (townsfolk.py) > "Let's race!": the kid is switched to Adventure (no flying, no breaking hoops),
  put in front of the START gate by the bus stop and counted in: 3, 2, 1, GO. The clock starts when they swim through
  the gate and stops when they swim back through it after the last checkpoint.
- 11 checkpoints in order: 10 red-and-white rings (5-block opening, floating number) and the welcome arch (10).
  Only the next one counts, and it sparkles for that kid only. 5-minute limit.
- Checkpoint 5 is the Bubble Lift: 3x3 soul sand in the seabed makes an upward bubble column through a flat ring. An
  invisible, non-solid light block ends the column 16 up (instead of at the surface), so riders float out of the top
  and swim on. A glass cap pinned them: the bubbles held them against it (play-test, 2026-11-17). No down columns:
  those need magma, which burns whoever touches the bottom.
- Best times: a sidebar shown only to the team family.undersea, which everyone in the Undersea is put on (their names
  show aqua there). The score is race points, 3000 minus the time in tenths of a second, so the fastest is on top on
  PC and iPad. PCs show the time instead of the number (fixed number format); iPads show "name time" and the points
  (Geyser adds the fixed text to the name and Bedrock always shows the score).
- Leaderboard: floating BEST TIMES text in front of the bus stop, beside Driver Finnley, shows the top 5 best times
  with names. It turns to face you (on iPad it's a name tag anyway) and nothing solid is behind it, so kids swim right
  through. A datapack can't read names off the scoreboard, so each finish puts the racer's name (from a player head's
  profile, in a hidden item display) and best time into a sorted top-10 list in storage family:race board.
- Leaving the Undersea, leaving the game, "Stop racing" or the limit ends a race and gives back the kid's game mode.
- A ring block that gets broken (it turns to water) comes back within 5 s while someone is near the hub.
Coordinates are relative to the hub centre, like town.py; y=0 is the street.
  python3 race.py -> previews/race.png
  build.py        -> family:undersea/race/*  (admin runs family:undersea/build_race; safe to re-run)"""
import json, math, os
import town, undersea, townsfolk as tf
from town import M
from townsfolk import F, snbt, say, dialog

T = town.build()
GATE = (0, 4, 18)                       # START/FINISH arch across the south street, just south of the bus stop
START = (0, 3, 14)                      # a racer is put here, facing south through the gate
ARCH_Z = -12                            # town.py's welcome arch: opening x -3..3, y 1..7
CHECKPOINTS = [                         # (ring centre, travel axis); None = the welcome arch. Corners are split
    ((0, 4, 23), "z"),                  # 1  just after the gate             across two rings placed diagonally,
    ((15, 5, 38), "x"),                 # 2  past the street's end, east     so no turn is sharper than ~55 deg
    ((28, 5, 38), "x"),                 # 3  south of the submarine          (play-test: a 103 deg turn after
    ((42, 5, 26), "z"),                 # 4  turning north                   ring 1 left people lost)
    ((44, 13, 0), "y"),                 # 5  the Bubble Lift past the east street's end (flat ring, ridden up)
    ((42, 7, -26), "z"),                # 6  east of the Coconut house
    ((30, 7, -38), "x"),                # 7  meadow, turning west
    ((12, 8, -38), "x"),                # 8  under a jelly (the first course's ring 7)
    ((0, 6, -21), "z"),                 # 9  down the north street
    (None, "z"),                        # 10 through the welcome arch
    ((6, 8, 0), "z")]                   # 11 over the hub's east side, clear of its bubble column (the way home)
RETIRED = [((0, 4, 34), "z"), ((26, 5, 28), "x"), ((42, 5, 14), "z"), ((42, 5, -1), "z"),   # the first course's rings
           ((42, 7, -17), "z"), ((31, 7, -36), "x"), ((-10, 6, -36), "z"),                    # (build takes them out)
           ((42, 5, 0), "z")]                                                                 # ring 5 before the lift
LIFT_CAP = 16                           # where a lift's column ends; the column is x/z +-1 around the ring centre, y 1..15
LIFT_END = M + "light[level=15,waterlogged=true]"   # not water, so the bubbles stop; no collision, so nobody is pinned
BOARD_AT, BOARD_SHOWN = (4.5, 1.7, 13.5), 5       # leaderboard text: over the sidewalk between the BUS STOP sign and
                                                   # Finnley (his name tag is 2 blocks south), bottom at 1.7 up
OLD_BOARD = {(-4, y, z): M + ("horn_coral_block" if y == 4 else "dark_prismarine")    # the first leaderboard, a wall
             for y in range(1, 5) for z in range(12, 17)}   # across the street on a lamp's spot: build puts the lamp back
# Found in the world but not in town.py (probes, 2026-11-17): the course keeps clear of them.
SEEN = {**{(x, y, z): M + "wet_sponge" for x, y in ((-2, 1), (-2, 2), (-2, 3), (-1, 3), (0, 3), (1, 1), (1, 2), (1, 3))
           for z in (29, 30)},                                              # a kids' sponge arch on the south street
        **{p: M + "light[level=15]" for p in ((0, 5, 25), (0, 5, 32), (0, 5, 39), (0, 5, 18), (0, 5, -17), (14, 5, -38))}}   # an older hidden-light grid
N = len(CHECKPOINTS)
FINISH = N + 1                          # family.race_cp: 0 = start gate next, 1..N = that checkpoint, N+1 = finish
LIMIT, WAIT, BASE = 6000, 1200, 3000    # ticks: 5 min to finish, 60 s to cross the start; points = BASE - tenths
PITCH = [2 ** (s / 12 - 5 / 12) for s in (0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17)]   # chime per checkpoint: a scale up
PLANTS = {M + "seagrass", M + "tall_seagrass[half=lower]", M + "tall_seagrass[half=upper]", M + "sea_pickle[pickles=3]"}

def ring(c, axis):
    """A round hoop ~7 across across the travel axis: ring cells -> block (8 red and white segments, like a life ring),
    and the 5-wide opening's cells."""
    cx, cy, cz = c
    cells, hole = {}, set()
    for i in range(-3, 4):
        for j in range(-3, 4):
            d = math.hypot(i, j)
            p = {"z": (cx + i, cy + j, cz), "x": (cx, cy + j, cz + i), "y": (cx + i, cy, cz + j)}[axis]
            if 2.5 <= d < 3.5:
                seg = int(((math.degrees(math.atan2(j, i)) + 22.5) % 360) // 45)
                cells[p] = M + ("red_concrete" if seg % 2 else "white_concrete")
            elif d < 2.5:
                hole.add(p)
    return cells, hole

def gate():
    """Checkered black and white arch across the street: pillars at x = +-4 (y 1-7) and a 2-high beam on top."""
    cx, _, cz = GATE
    cells = {}
    for y in range(1, 10):
        for x in range(-4, 5):
            if abs(x) == 4 or y >= 8:
                cells[(cx + x, y, cz)] = M + ("black_concrete" if (x + y) % 2 else "white_concrete")
    return cells

def box(i):
    """Checkpoint i's opening as an inclusive cell box (x1, y1, z1, x2, y2, z2); 0 and FINISH are the gate."""
    if i in (0, FINISH):
        return (GATE[0] - 3, 1, GATE[2], GATE[0] + 3, 7, GATE[2])
    c, axis = CHECKPOINTS[i - 1]
    if c is None:
        return (-3, 1, ARCH_Z, 3, 7, ARCH_Z)
    (cx, cy, cz), r = c, 2
    return {"z": (cx - r, cy - r, cz, cx + r, cy + r, cz), "x": (cx, cy - r, cz - r, cx, cy + r, cz + r),
            "y": (cx - r, cy, cz - r, cx + r, cy, cz + r)}[axis]

def centre(i):
    x1, y1, z1, x2, y2, z2 = box(i)
    return ((x1 + x2 + 1) / 2, (y1 + y2 + 1) / 2, (z1 + z2 + 1) / 2)

def label(i):
    """(position, text) of the floating number over checkpoint i (inside the arch's opening for 10)."""
    if i == 0:
        return (GATE[0] + 0.5, 10.3, GATE[2] + 0.5), "CURRENT RACE\nStart / Finish"
    c, axis = CHECKPOINTS[i - 1]
    if c is None:
        return (0.5, 6.2, ARCH_Z + 0.5), str(i)
    if axis == "y":                                     # over the top of a lift
        return (c[0] + 0.5, LIFT_CAP + 1.4, c[2] + 0.5), str(i)
    return (c[0] + 0.5, c[1] + 4.3, c[2] + 0.5), str(i)

def lifts():
    """(column ends, soul sand in the seabed, bubble column cells) of every lift."""
    caps, seabed, column = {}, {}, set()
    for c, axis in CHECKPOINTS:
        if axis == "y":
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    caps[(c[0] + i, LIFT_CAP, c[2] + j)] = LIFT_END
                    seabed[(c[0] + i, 0, c[2] + j)] = M + "soul_sand"
                    column.update((c[0] + i, y, c[2] + j) for y in range(1, LIFT_CAP))
    return caps, seabed, column

def blocks():
    """Everything the course places into water: the gate, rings and lift ends (not the lifts' soul sand)."""
    out = gate()
    for c, axis in CHECKPOINTS:
        if c:
            out.update(ring(c, axis)[0])
    out.update(lifts()[0])
    return out

def check():
    """The course must fit the town: rings and gate only in water, openings clear, and a 3x3 tube along the straight
    line between checkpoints free of town blocks and away from the hub's bubble column. Returns the route length."""
    placed, world = blocks(), {**T.v, **SEEN}
    taken = [(p, world[p]) for p in placed if p in world]
    assert not taken, f"course blocks on town blocks: {taken[:5]}"
    _, seabed, column = lifts()
    blocked = [(p, world[p]) for p in [*seabed, *column] if p in world or p in placed]
    assert not blocked, f"a lift's column or soul sand spot is taken: {blocked[:5]}"
    for i in range(1, N + 1):
        x1, y1, z1, x2, y2, z2 = box(i)
        for p in [(x, y, z) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1) for z in range(z1, z2 + 1)]:
            assert p not in world or world[p] in PLANTS or "light[" in world[p] or p in placed, \
                f"checkpoint {i} opening blocked at {p}: {world[p]}"
    pts = [centre(i) for i in range(0, FINISH + 1)]
    length = 0.0
    for a, b in zip(pts, pts[1:]):
        length += math.dist(a, b)
        n = int(math.dist(a, b) * 3) + 1
        for k in range(n + 1):
            x, y, z = (a[i] + (b[i] - a[i]) * k / n for i in range(3))
            assert math.hypot(x - 0.5, z - 0.5) >= 3, f"route passes the hub's bubble column at {(x, y, z)}"
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        p = (math.floor(x) + dx, math.floor(y) + dy, math.floor(z) + dz)
                        assert p not in world or world[p] in PLANTS or "light[" in world[p] or p in placed, \
                            f"route {a} -> {b} hits {world[p]} at {p}"
    return length

# ---------------------------------------------------------------- datapack
def leaderboard(put, f, fn, store, tmp, score, title, line, namer_tag, sign_tag, extra=(), shown=BOARD_SHOWN, keep=10):
    """A top-`keep` list in storage `store` board ([{u: UUID, n: name, p: points, ...}], best first) and the top `shown`
    on the text display tagged `sign_tag`. `{fn}/leaderboard/add` runs as a player after a new score: points are their
    `score` (bigger is better); `extra` are commands that store more fields in `store` new for `line` (a row: $(n), $(p)
    and those fields). A name can't be read off the scoreboard, so a player head in the hidden item display tagged
    `namer_tag` is filled with the player's profile and the name is read from it. (26.3 loot functions are keyed "type",
    not "function".) `tmp` holds #np, #bp and #i."""
    mcf, lb = undersea.mcf, f"{fn}/leaderboard"
    namer = f"@e[type=minecraft:item_display,tag={namer_tag},limit=1]"
    sign = f"@e[type=minecraft:text_display,tag={sign_tag},limit=1]"
    put(f"{f}/leaderboard/add.mcfunction", mcf(
        f"execute unless score @s {score} matches 0.. run return fail",
        f"data remove storage {store} new",
        f"item replace entity {namer} contents with minecraft:player_head",
        f'item modify entity {namer} contents {{type:"minecraft:fill_player_head",entity:"this"}}',
        f'data modify storage {store} new.n set from entity {namer} item.components."minecraft:profile".name',
        f'execute unless data storage {store} new.n run data modify storage {store} new.n set value "?"',
        f"data modify storage {store} new.u set from entity @s UUID",
        f"execute store result storage {store} new.p int 1 run scoreboard players get @s {score}",
        *extra,
        f"function {lb}/drop with storage {store} new",
        f"scoreboard players operation #np {tmp} = @s {score}",
        f"data modify storage {store} at.i set value 0",
        f"function {lb}/insert with storage {store} at",
        f"data remove storage {store} board[{keep}]",
        f"function {lb}/show"))
    put(f"{f}/leaderboard/drop.mcfunction", f"$data remove storage {store} board[{{u:$(u)}}]\n")
    put(f"{f}/leaderboard/insert.mcfunction", mcf(               # walk down the list; go in before the first lower one
        f"$execute unless data storage {store} board[$(i)] run return run "
        f"data modify storage {store} board append from storage {store} new",
        f"$execute store result score #bp {tmp} run data get storage {store} board[$(i)].p",
        f"$execute if score #np {tmp} > #bp {tmp} run return run "
        f"data modify storage {store} board insert $(i) from storage {store} new",
        f"$scoreboard players set #i {tmp} $(i)", f"scoreboard players add #i {tmp} 1",
        f"execute store result storage {store} at.i int 1 run scoreboard players get #i {tmp}",
        f"function {lb}/insert with storage {store} at"))
    put(f"{f}/leaderboard/show.mcfunction", mcf(
        f"data modify storage {store} view set value {{" + ",".join(f'l{k}:"-"' for k in range(shown)) + "}",
        *[l for k in range(shown) for l in (
            f"data modify storage {store} row set from storage {store} board[{k}]",
            f"data modify storage {store} row.k set value {k}",
            f"execute if data storage {store} board[{k}] run function {lb}/line with storage {store} row")],
        f"function {lb}/render with storage {store} view"))
    put(f"{f}/leaderboard/line.mcfunction", f'$data modify storage {store} view.l$(k) set value "{line}"\n')
    put(f"{f}/leaderboard/render.mcfunction", f"$data modify entity {sign} text set value " + json.dumps(
        [{"text": f"{title}\n", "color": "gold", "bold": True},
         {"text": "\n".join(f"{k + 1}. $(l{k})" for k in range(shown)), "color": "white", "bold": False}]) + "\n")

def datapack(data, put):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    dim, d = undersea.DIM, f"{data}/data/family"
    f, fn = f"{d}/function/undersea/race", "family:undersea/race"
    mcf = undersea.mcf
    check()
    a = lambda x, y, z: f"{hx + x} {hy + y} {hz + z}"          # absolute, for blocks and particles
    def inside(i):
        x1, y1, z1, x2, y2, z2 = box(i)
        return f"x={hx + x1},y={hy + y1},z={hz + z1},dx={x2 - x1},dy={y2 - y1},dz={z2 - z1}"
    def at_centre(i):
        x, y, z = centre(i)
        return f"{hx + x} {hy + y} {hz + z}"
    def spread(i):
        x1, y1, z1, x2, y2, z2 = box(i)
        return " ".join(str(round(max(0.2, (b - a_ + 1) / 4), 2)) for a_, b in ((x1, x2), (y1, y2), (z1, z2)))
    tmp = lambda name: {"score": {"name": "#" + name, "objective": "family.race_tmp"}}
    secs = lambda s, dd: [tmp(s), {"text": "."}, tmp(dd)]
    def tell(*parts):
        """Driver Finnley's chat line to the racer: strings (with {kid}) and score components."""
        out = [{"text": tf.FOLK["driver"]["name"], "color": tf.FOLK["driver"]["colour"]}, {"text": ": ", "color": "white"}]
        for p in parts:
            if isinstance(p, str):
                bits = p.split("{kid}")
                out.append({"text": bits[0], "color": "white"})
                for b in bits[1:]:
                    out += [{"selector": "@s", "color": "white"}, {"text": b, "color": "white"}]
            else:
                out += p if isinstance(p, list) else [p]
        return "tellraw @s " + json.dumps(out)
    split = lambda src, s, dd: [                                 # tenths in #src -> #s seconds and #dd tenths digit
        f"scoreboard players operation #{s} family.race_tmp = #{src} family.race_tmp",
        f"scoreboard players operation #{s} family.race_tmp /= #10 family.race_tmp",
        f"scoreboard players operation #{dd} family.race_tmp = #{src} family.race_tmp",
        f"scoreboard players operation #{dd} family.race_tmp %= #10 family.race_tmp"]
    tenths = ["scoreboard players operation #t family.race_tmp = @s family.race_t",
              "scoreboard players operation #t family.race_tmp /= #2 family.race_tmp", *split("t", "s", "d")]
    best = ["scoreboard players operation #b family.race_tmp = #base family.race_tmp",
            "scoreboard players operation #b family.race_tmp -= @s family.race", *split("b", "bs", "bd")]

    put(f"{f}/load.mcfunction", mcf(
        'scoreboard objectives add family.race dummy {"text":"Current Race","color":"aqua","bold":true}',
        *[f"scoreboard objectives add family.race_{s} dummy" for s in ("cp", "t", "cd", "tmp")],
        "scoreboard objectives add family.race_left minecraft.custom:minecraft.leave_game",
        *[f"scoreboard players set #{n} family.race_tmp {n}" for n in (2, 10)],
        f"scoreboard players set #base family.race_tmp {BASE}",
        'team add family.undersea {"text":"Undersea"}',
        "team modify family.undersea color aqua",
        "scoreboard objectives setdisplay sidebar.team.aqua family.race"))

    # --- every tick: who sees the board, rejoins, ring repair, then crossings and each racer's clock
    cross = [f"execute in {dim} as @a[tag=family.racing,scores={{family.race_cp=0,family.race_cd=0}},{inside(0)}] "
             f"at @s run function {fn}/started"]
    cross += [f"execute in {dim} as @a[tag=family.racing,scores={{family.race_cp={i}}},{inside(i)}] at @s run function {fn}/cp/{i}"
              for i in range(1, N + 1)]
    cross += [f"execute in {dim} as @a[tag=family.racing,scores={{family.race_cp={FINISH}}},{inside(FINISH)}] "
              f"at @s run function {fn}/finish"]
    put(f"{f}/tick.mcfunction", mcf(
        f"execute as @a[team=!family.undersea] at @s if dimension {dim} run team join family.undersea @s",
        f"execute as @a[team=family.undersea] at @s unless dimension {dim} run team leave @s",
        f"execute as @a[scores={{family.race_left=1..}}] run function {fn}/rejoined",
        "scoreboard players add #repair family.race_tmp 1",
        f"execute if score #repair family.race_tmp matches 100.. run function {fn}/repair",
        "execute unless entity @a[tag=family.racing] run return 0",
        "scoreboard players add #spark family.race_tmp 1",
        "execute if score #spark family.race_tmp matches 5.. run scoreboard players set #spark family.race_tmp 0",
        *cross,
        f"execute as @a[tag=family.racing] at @s run function {fn}/racer"))
    put(f"{f}/racer.mcfunction", mcf(
        f"execute unless dimension {dim} run return run function {fn}/away",
        f"execute if score @s family.race_cd matches 1.. run return run function {fn}/countdown",
        "scoreboard players add @s family.race_t 1",
        f"execute if score @s family.race_cp matches 0 run return run function {fn}/waiting",
        f"execute if score @s family.race_t matches {LIMIT}.. run return run function {fn}/timeout",
        *tenths,
        f"execute if score @s family.race_cp matches ..{N} run title @s actionbar " + json.dumps(
            [{"text": "Hoop ", "color": "aqua"}, {"score": {"name": "@s", "objective": "family.race_cp"}},
             {"text": f" of {N}   |   "}] + secs("s", "d") + [{"text": "s"}]),
        f"execute if score @s family.race_cp matches {FINISH} run title @s actionbar " + json.dumps(
            [{"text": "Back through the gate!   |   ", "color": "gold"}] + secs("s", "d") + [{"text": "s"}]),
        f"execute if score #spark family.race_tmp matches 0 run function {fn}/spark"))
    # The next checkpoint sparkles, and 3 sparkles 2-4 blocks in front of the racer's eyes point at it (racer only).
    put(f"{f}/spark.mcfunction", mcf(*[f"execute if score @s family.race_cp matches {i} run return run function {fn}/spark/{i}"
                                       for i in range(0, FINISH + 1)]))
    for i in range(0, FINISH + 1):
        put(f"{f}/spark/{i}.mcfunction", mcf(
            f"particle minecraft:end_rod {at_centre(i)} {spread(i)} 0.02 8 force @s",
            *[f"execute anchored eyes facing {at_centre(i)} run particle minecraft:end_rod ^ ^ ^{r} 0 0 0 0 1 force @s"
              for r in (2, 3, 4)]))

    # --- start: Adventure, to the start spot, then 3-2-1-GO (60 ticks), then the gate starts the clock
    put(f"{f}/go.mcfunction", mcf(
        "execute if entity @s[tag=family.racing] run return fail",
        f"execute at @s unless dimension {dim} run return fail",
        "execute at @s unless entity @e[type=minecraft:villager,tag=family.folk.driver,distance=..10] run return fail",
        "tag @s add family.racing",
        "execute if entity @s[gamemode=creative] run tag @s add family.race.creative",
        "execute if entity @s[gamemode=survival] run tag @s add family.race.survival",
        "gamemode adventure @s",
        "scoreboard players set @s family.race_cp 0", "scoreboard players set @s family.race_t 0",
        "scoreboard players set @s family.race_cd 61",
        f"execute in {dim} positioned {hx} {hy} {hz} run tp @s ~{START[0]} ~{START[1]} ~{START[2]} 0 0",
        "title @s times 0 20 5", 'title @s subtitle {"text":"Get ready...","color":"aqua"}',
        say("driver", "Ready, {kid}? Wait for GO, then swim through the START gate!")))
    count = [(60, "3"), (40, "2"), (20, "1")]
    put(f"{f}/countdown.mcfunction", mcf(
        "scoreboard players remove @s family.race_cd 1",
        *[l for t, n in count for l in (
            f"execute if score @s family.race_cd matches {t} run title @s title " + json.dumps({"text": n, "color": "yellow", "bold": True}),
            f"execute if score @s family.race_cd matches {t} run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1")],
        f"execute if score @s family.race_cd matches 0 run function {fn}/go_now"))
    put(f"{f}/go_now.mcfunction", mcf(
        'title @s subtitle {"text":"Swim through the gate!","color":"aqua"}',
        'title @s title {"text":"GO!","color":"green","bold":true}',
        "playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2",
        "scoreboard players set @s family.race_t 0"))
    put(f"{f}/waiting.mcfunction", mcf(
        f"execute if score @s family.race_t matches {WAIT}.. run return run function {fn}/no_start",
        'title @s actionbar {"text":"GO! Swim through the START gate!","color":"yellow"}',
        f"execute if score #spark family.race_tmp matches 0 run function {fn}/spark"))
    put(f"{f}/started.mcfunction", mcf(
        "scoreboard players set @s family.race_cp 1", "scoreboard players set @s family.race_t 0",
        "playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1"))
    for i in range(1, N + 1):
        put(f"{f}/cp/{i}.mcfunction", mcf(
            f"scoreboard players set @s family.race_cp {i + 1}",
            f"playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 {PITCH[i - 1]:.3f}",
            f"particle minecraft:happy_villager {at_centre(i)} {spread(i)} 0 20 force @s"))

    # --- finish: time in tenths, points, title, board (only if it's this kid's best)
    put(f"{f}/finish.mcfunction", mcf(
        *tenths,
        "scoreboard players operation #pts family.race_tmp = #base family.race_tmp",
        "scoreboard players operation #pts family.race_tmp -= #t family.race_tmp",
        f"function {fn}/end",
        "title @s times 5 60 20",
        "playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1",
        "particle minecraft:totem_of_undying ~ ~1 ~ 0.6 0.6 0.6 0.4 50",
        f"execute unless score @s family.race >= #pts family.race_tmp run return run function {fn}/new_best",
        "title @s subtitle " + json.dumps(secs("s", "d") + [{"text": " seconds", "color": "white"}]),
        'title @s title {"text":"FINISH!","color":"gold","bold":true}',
        *best,
        tell("Nice swim, {kid}! ", secs("s", "d"), " seconds. Your best is ", secs("bs", "bd"), " seconds. Try again?"),
        f"function {fn}/leaderboard/add"))
    put(f"{f}/new_best.mcfunction", mcf(
        "scoreboard players operation @s family.race = #pts family.race_tmp",
        "execute store result storage family:race t.s int 1 run scoreboard players get #s family.race_tmp",
        "execute store result storage family:race t.d int 1 run scoreboard players get #d family.race_tmp",
        f"function {fn}/board with storage family:race t",
        "title @s subtitle " + json.dumps(secs("s", "d") + [{"text": " seconds: your best!", "color": "white"}]),
        'title @s title {"text":"FINISH!","color":"gold","bold":true}',
        tell("Whoosh! ", secs("s", "d"), " seconds, {kid}! That's your best time yet. It's on the board!"),
        f"function {fn}/leaderboard/add"))
    put(f"{f}/board.mcfunction",
        '$scoreboard players display numberformat @s family.race fixed {"text":"$(s).$(d)s","color":"aqua"}\n')

    # --- ending a race any other way; every ending gives the kid's game mode back
    put(f"{f}/end.mcfunction", mcf(
        "tag @s remove family.racing",
        *[f"scoreboard players reset @s family.race_{s}" for s in ("cp", "t", "cd")],
        "execute if entity @s[tag=family.race.creative] run gamemode creative @s",
        "execute if entity @s[tag=family.race.survival] run gamemode survival @s",
        "tag @s remove family.race.creative", "tag @s remove family.race.survival",
        'title @s actionbar ""'))
    for name, text in (("away", "Race stopped: you left the Undersea. Tap me at the bus stop to race again!"),
                       ("timeout", f"Time's up, {{kid}}! {LIMIT // 1200} minutes is the limit. Tap me to try again!"),
                       ("no_start", "You didn't swim through the START gate, {kid}. Tap me to try again!")):
        put(f"{f}/{name}.mcfunction", mcf(f"function {fn}/end", tell(text)))
    put(f"{f}/rejoined.mcfunction", mcf(
        "scoreboard players reset @s family.race_left",
        "execute unless entity @s[tag=family.racing] run return 0",
        f"function {fn}/end", tell("Your race stopped when you left the game. Tap me to race again!")))

    # --- Driver Finnley's menu (from townsfolk tap/driver) and its buttons (townsfolk BUTTONS 5-7)
    arch = next(i for i, (c, _) in enumerate(CHECKPOINTS, 1) if c is None)
    lift = next(i for i, (_, axis) in enumerate(CHECKPOINTS, 1) if axis == "y")
    intro = (f"Beep beep! Want to race the Current Race? Swim through the START gate, then through all {N} hoops in "
             f"order (number {arch} is the welcome arch), and back through the gate. Follow the sparkles!")
    put(f"{f}/menu.mcfunction", mcf(
        "scoreboard players enable @s family.talk",
        "execute if entity @s[tag=family.racing] run return run " + dialog(
            "driver", "You're in the middle of a race! Do you want to stop?", [("Stop racing", 7)], "Keep racing"),
        "execute unless score @s family.race matches 0.. run return run " + dialog(
            "driver", intro, [("Let's race!", 5), ("How does it work?", 6)], "Not now"),
        *best,
        "execute store result storage family:race me.s int 1 run scoreboard players get #bs family.race_tmp",
        "execute store result storage family:race me.d int 1 run scoreboard players get #bd family.race_tmp",
        f"function {fn}/menu_best with storage family:race me"))
    put(f"{f}/menu_best.mcfunction", "$" + dialog(
        "driver", "Beep beep! Back for another race? Your best time is $(s).$(d) seconds. Can you beat it?",
        [("Let's race!", 5), ("How does it work?", 6)], "Not now") + "\n")
    put(f"{f}/rules.mcfunction", mcf(dialog(
        "driver", "1. Tap Let's race! and wait for GO.\n"
                  "2. Swim through the START gate: the clock starts.\n"
                  f"3. Swim through the hoops in order, 1 to {N}. Number {arch} is the welcome arch. Your next hoop "
                  "sparkles, and sparkles in front of you point the way.\n"
                  f"   Number {lift} is the Bubble Lift: swim into the bubbles and they carry you up through it!\n"
                  "4. Swim back through the gate to finish!\n\n"
                  f"No flying during a race. You have {LIMIT // 1200} minutes. Your best time goes on the board, "
                  "which you can see anywhere in the Undersea.", exit_label="Got it!")))
    put(f"{f}/stop.mcfunction", mcf(
        "execute unless entity @s[tag=family.racing] run return fail",
        f"function {fn}/end", say("driver", "OK, {kid}! Tap me any time to race again.")))

    # --- the leaderboard (the top 10 best times, each with its seconds and tenths for the board's line)
    lb = f"{fn}/leaderboard"
    leaderboard(put, f, fn, "family:race", "family.race_tmp", "family.race", "BEST TIMES", "$(n)   $(s).$(d)s",
                "family.race.namer", "family.race.board", extra=[
                    *best, "execute store result storage family:race new.s int 1 run scoreboard players get #bs family.race_tmp",
                    "execute store result storage family:race new.d int 1 run scoreboard players get #bd family.race_tmp"])

    # --- the course: rings, gate and lift ends placed only into water or bubbles (never over anything built), the
    # lifts' soul sand only into the sand floor (after the ends, so the column stops there), numbers as text displays.
    # A mined soul sand block fills with water: repair puts it back. The first lift's glass caps are swapped out.
    course, (_, seabed, _) = blocks(), lifts()
    put(f"{d}/tags/block/race_free.json", {"values": ["minecraft:water", "minecraft:bubble_column"]})
    put(f"{d}/tags/block/race_seabed.json", {"values": ["minecraft:sand", "minecraft:water"]})
    place = [f"execute in {dim} if block {a(*p)} #family:race_free run setblock {a(*p)} {b}" for p, b in sorted(course.items())]
    sink = lambda where: [f"execute in {dim} if block {a(*p)} {where} run setblock {a(*p)} {b}" for p, b in sorted(seabed.items())]
    put(f"{f}/repair.mcfunction", mcf(
        "scoreboard players set #repair family.race_tmp 0",
        f"execute in {dim} positioned {hx} {hy} {hz} unless entity @a[distance=..64] run return 0",
        *place, *sink("minecraft:water")))
    def summon_label(i):
        (x, y, z), text = label(i)
        nbt = {"Tags": ["family.race.label"], "billboard": "center", "brightness": {"sky": 15, "block": 15},
               "text": {"text": text, "color": "white" if i == 0 else "gold", "bold": True},
               "transformation": {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                                  "translation": [F(0), F(0), F(0)], "scale": [F(1.5 if i == 0 else 2.5)] * 3}}
        return f"execute in {dim} run summon minecraft:text_display {hx + x} {hy + y} {hz + z} {snbt(nbt)}"
    retired = {p: b for c, axis in RETIRED for p, b in ring(c, axis)[0].items() if p not in course and p not in seabed}
    xs = [p[0] for p in [*course, *retired, *OLD_BOARD]] + [-3]; zs = [p[2] for p in [*course, *retired, *OLD_BOARD]] + [ARCH_Z]
    def summon_board():
        """The leaderboard text (turns to face the viewer, like a name tag) and the hidden name helper in the ground
        under it (scale 0: invisible on PC; iPads can't see item displays anyway)."""
        x, y, z = BOARD_AT
        flat = lambda k: {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                          "translation": [F(0), F(0), F(0)], "scale": [F(k)] * 3}
        text = {"Tags": ["family.race.label", "family.race.board"], "billboard": "center",
                "brightness": {"sky": 15, "block": 15}, "line_width": 220, "transformation": flat(1.4),
                "text": {"text": "BEST TIMES", "color": "gold", "bold": True}}
        helper = {"Tags": ["family.race.label", "family.race.namer"], "transformation": flat(0)}
        return [f"execute in {dim} run summon minecraft:text_display {hx + x} {hy + y} {hz + z} {snbt(text)}",
                f"execute in {dim} run summon minecraft:item_display {hx + x} {hy - 0.5} {hz + z} {snbt(helper)}"]
    area = f"{hx + min(xs)} {hz + min(zs)} {hx + max(xs)} {hz + max(zs)}"
    put(f"{data}/data/family/function/undersea/build_race.mcfunction", mcf(
        f"execute in {dim} run forceload add {area}", f"schedule function {fn}/build 3s replace"))
    put(f"{f}/build.mcfunction", mcf(
        *[f"execute in {dim} unless loaded {hx + x} {hy} {hz + z} run return run schedule function {fn}/build 2s replace"
          for x, z in ((min(xs), min(zs)), (max(xs), max(zs)))],
        f"execute in {dim} run kill @e[type=minecraft:text_display,tag=family.race.label]",
        f"execute in {dim} run kill @e[type=minecraft:item_display,tag=family.race.namer]",
        *[f"execute in {dim} if block {a(*p)} {b} run setblock {a(*p)} minecraft:water" for p, b in sorted(retired.items())],
        *[f"execute in {dim} if block {a(*p)} minecraft:light_blue_stained_glass run setblock {a(*p)} {b}"
          for p, b in sorted(lifts()[0].items())],
        *[f"execute in {dim} if block {a(*p)} {b} run setblock {a(*p)} {town.wl(T.v[p]) if p in T.v else 'minecraft:water'}"
          for p, b in sorted(OLD_BOARD.items())],
        *place, *sink("#family:race_seabed"),
        *[summon_label(i) for i in range(0, N + 1)], *summon_board(), f"function {lb}/show",
        f"execute in {dim} run forceload remove {area}"))
    put(f"{f}/reset_times.mcfunction", mcf(                                           # admin: clear both boards
        "scoreboard players reset * family.race", "data remove storage family:race board", f"function {fn}/leaderboard/show"))

# ---------------------------------------------------------------- preview
def preview():
    """previews/race.png: the route on the town map, close-ups of the gate and a hoop, and the screen on PC/iPad."""
    from PIL import Image, ImageDraw, ImageFont
    town.COLOURS.update({"red_concrete": "#C8312D", "black_concrete": "#141519", "soul_sand": "#51402F"})
    f13, f15, f17, f20 = (ImageFont.load_default(size=s) for s in (13, 15, 17, 20))
    course, length = blocks(), check()
    xs = [x for (x, _, _) in T.v]; zs = [z for (_, _, z) in T.v]
    x0, z0, x1, z1 = min(xs) - 3, min(zs) - 3, max(xs) + 14, max(zs) + 3
    k = 8
    mp = Image.new("RGB", ((x1 - x0 + 1) * k, (z1 - z0 + 1) * k), (24, 70, 84)); d = ImageDraw.Draw(mp)
    top = {}
    for (x, y, z), b in T.v.items():
        c = town.colour(b)
        if c and ((x, z) not in top or y > top[(x, z)][0]):
            top[(x, z)] = (y, c)
    for zx in T.zones:
        for x in range(zx[0], zx[2] + 1):
            for z in range(zx[1], zx[3] + 1):
                top.setdefault((x, z), (0, town.colour(town.SAND)))
    for x in range(-10, 11):
        for z in range(-10, 11):
            if math.hypot(x, z) <= 10.5:
                top.setdefault((x, z), (0, town.colour(town.SAND)))
    for (x, z), (y, c) in top.items():
        d.rectangle([(x - x0) * k, (z - z0) * k, (x - x0 + 1) * k - 1, (z - z0 + 1) * k - 1], fill=town.shade(c, 0.62 + 0.02 * min(y, 5)))
    P = lambda x, z: ((x - x0) * k, (z - z0) * k)
    for x, z, s in [(0, 0, "Hub")] + [(x, z, s) for x, z, s in T.labels if s.startswith("Plot")]:
        w = d.textlength(s, font=f13); cx, cy = P(x + 0.5, z + 0.5)
        d.rectangle([cx - w / 2 - 3, cy - 8, cx + w / 2 + 3, cy + 8], fill=(225, 225, 225)); d.text((cx - w / 2, cy - 7), s, fill=(40, 40, 40), font=f13)
    pts = [centre(i) for i in range(0, FINISH + 1)]
    for p, q in zip(pts, pts[1:]):                   # the way to swim: yellow line, arrowhead half-way
        (ax, az), (bx, bz) = P(p[0], p[2]), P(q[0], q[2])
        d.line([ax, az, bx, bz], fill=(255, 225, 60), width=4)
        mx, mz, ang = (ax + bx) / 2, (az + bz) / 2, math.atan2(bz - az, bx - ax)
        d.polygon([(mx + 11 * math.cos(ang + t), mz + 11 * math.sin(ang + t)) for t in (0, 2.5, -2.5)], fill=(255, 225, 60))
    for (x, _, z), b in course.items():
        d.rectangle([(x - x0) * k, (z - z0) * k, (x - x0 + 1) * k - 1, (z - z0 + 1) * k - 1], fill=town.colour(b))
    for i in range(0, N + 1):
        (cx, cy, cz), axis = centre(i), (CHECKPOINTS[i - 1][1] if i else "z")
        txt = "START / FINISH" if i == 0 else f"{i} (y{math.floor(cy)})"
        w = d.textlength(txt, font=f15); px, pz = P(cx, cz)
        tx, ty = (px - 6.2 * k, pz) if i == 0 else (px, pz - 2.6 * k) if axis == "x" else (px + 2.4 * k + w / 2, pz)
        d.rectangle([tx - w / 2 - 4, ty - 10, tx + w / 2 + 4, ty + 10], fill=(20, 20, 20))
        d.text((tx - w / 2, ty - 9), txt, fill=(255, 255, 255) if i == 0 else (255, 225, 60), font=f15)
    dx, _, dz = tf.FOLK["driver"]["spot"]; cx, cy = P(dx + 0.5, dz + 0.5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 60, 60), outline=(255, 255, 255), width=2)
    d.text((cx + 10, cy + 6), "Driver Finnley", fill=(255, 255, 255), font=f15)

    def scene(lo, hi, extra, unit):
        v = {p: b for p, b in T.v.items() if all(lo[i] <= p[i] <= hi[i] for i in range(3)) and "light[" not in b}
        v.update({p: b for p, b in extra.items() if all(lo[i] <= p[i] <= hi[i] for i in range(3))})
        for x in range(lo[0], hi[0] + 1):
            for z in range(lo[2], hi[2] + 1):
                v.setdefault((x, 0, z), town.SAND); v.setdefault((x, -1, z), town.SANDSTONE)
        return town.iso(v, unit=unit)
    gate_img = scene((-7, -1, 11), (9, 11, 22), course, 11)
    hoop_img = scene((-4, -1, -1), (4, 8, 1), ring((0, 4, 0), "z")[0], 15)
    def panel(lines, w, title=None):
        im = Image.new("RGB", (w, 26 * len(lines) + (34 if title else 10)), (30, 30, 34)); dd = ImageDraw.Draw(im); y = 6
        if title:
            dd.text(((w - dd.textlength(title, font=f17)) / 2, y), title, fill=(255, 255, 255), font=f17); y += 28
        for left, right, rc in lines:
            dd.text((10, y), left, fill=(235, 235, 235), font=f17)
            dd.text((w - dd.textlength(right, font=f17) - 10, y), right, fill=rc, font=f17); y += 26
        return im
    kids = [(".IpadSwimmer", "52.3"), ("PcSwimmer", "58.9"), (".IpadParent", "64.8")]   # placeholders
    pc = panel([(n, f"{t}s", (120, 220, 255)) for n, t in kids], 300, "Current Race")
    ipad = panel([(f"{n} {t}s", str(BASE - round(float(t) * 10)), (255, 85, 85)) for n, t in kids], 300, "Current Race")
    bar = panel([(f"Hoop 4 of {N}   |   23.4s", "", (0, 0, 0))], 300)
    W, rx = mp.width + 40 + 640, mp.width + 30
    sheet = Image.new("RGB", (W, mp.height + 150), (16, 40, 58)); sd = ImageDraw.Draw(sheet)
    sheet.paste(mp, (10, 50))
    sd.text((14, 12), "Current Race (north up). Yellow = the way to swim; numbers = checkpoints in order "
            "(y = height above the street)", fill=(255, 255, 255), font=f20)
    yy = 50
    for title, im, dx_ in (("Start/finish gate across the street, by the bus stop (from the south-east)", gate_img, 0),
                           ("A hoop: 7 across, 5-block opening, a floating number above it", hoop_img, 60)):
        sd.text((rx, yy), title, fill=(255, 255, 255), font=f17); sheet.paste(im, (rx + dx_, yy + 26)); yy += 26 + im.height + 16
    sd.text((rx, yy), "While racing (action bar, PC and iPad):", fill=(255, 255, 255), font=f17)
    sheet.paste(bar, (rx, yy + 26)); yy += 26 + bar.height + 18
    sd.text((rx, yy), "Board, PC:", fill=(255, 255, 255), font=f17)
    sd.text((rx + 320, yy), "Board, iPad (time + race points):", fill=(255, 255, 255), font=f17)
    sheet.paste(pc, (rx, yy + 26)); sheet.paste(ipad, (rx + 320, yy + 26))
    for i, n in enumerate([
            "Tap Driver Finnley > Let's race! > 3, 2, 1, GO! The clock runs from the START gate back to it after "
            f"checkpoint {N}. Adventure mode while racing.",
            f"Your next checkpoint sparkles and a trail in front of you points at it (only you see them). "
            f"{LIMIT // 1200}-minute limit. Board only in the Undersea.",
            f"Route: about {round(length)} blocks. Race points = {BASE} minus your time in tenths of a second."]):
        sd.text((14, mp.height + 66 + i * 26), n, fill=(255, 230, 140) if i == 0 else (220, 235, 245), font=f17)
    os.makedirs(f"{town.HERE}/previews", exist_ok=True)
    sheet.save(f"{town.HERE}/previews/race.png")
    return length

if __name__ == "__main__":
    print("route length:", round(preview()), "blocks |", len(blocks()), "course blocks")
