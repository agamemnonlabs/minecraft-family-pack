"""Undersea townsfolk: villagers who live and work in the town (town.py), shops paid in Sand Dollars,
tap-to-talk menus and two activities.
- Chef Clamuel works the Bubble Cafe. The cafe is dried out (a wooden door holds the sea back; doors never let
  water through) and gets a counter across the room with a 2-deep kitchen behind it: smoker, bed, pantry, order
  bell. The chef keeps full villager AI (works by day, sleeps at night) but can't get over the 1.5-high counter.
- Mayor Marina (welcome arch), Farmer Kelpsey (Jelly Meadow) and Driver Finnley (bus stop) stand at fixed posts in
  the water: NoAI (they'd swim to the surface otherwise), Invulnerable (no drowning). They turn to face a kid.
- Everyone greets a kid once per visit. While a kid is at the hub, a missing townsperson, tap box or pearl comes back.
- Shops are vanilla trade screens. Talking uses Java dialogs, which Geyser shows as Bedrock forms; their buttons
  run /trigger, which runs on iPads without a confirm screen. Dialogs are inline, so minecraft:reload is enough.
- Taps are caught by invisible interaction boxes (Geyser supports them) and player_interacted_with_entity advancements.
- Lost Pearls: 10 golden pearls hidden around town, progress per kid; Mayor Marina pays out once.
- Order Up!: once a Minecraft day (20 min of game time) the chef's bell hands out a lunch for another townsperson.
- Driver Finnley runs the Current Race (race.py); tapping him opens its menu.
- Professor Periwinkle (Seashell house) and Coach Cockle (Coconut house) are posts too; their menus are in houses.py.
Coordinates are relative to the hub centre, like town.py; y=0 is the ground.
  python3 townsfolk.py -> previews/townsfolk-cafe.png + previews/townsfolk-map.png
  build.py             -> family:undersea/folk/*  (admin runs family:undersea/build_townsfolk; safe to re-run)"""
import json, math, os
import town, undersea
from town import M

T = town.build()
CX, CZ = next((x, z) for x, z, s in T.labels if s.startswith("Bubble Cafe"))
R, L, CY = 4.5, 8, 4.0                       # the submarine hull, same numbers as town.submarine()

class F(float):
    """Written as an SNBT float (rotations, box sizes, price multipliers)."""

def snbt(v):
    if isinstance(v, F):
        return f"{float(v)}f"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dict):
        return "{" + ",".join(f"{json.dumps(k)}:{snbt(x)}" for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ",".join(snbt(x) for x in v) + "]"
    return json.dumps(v)

def cafe(x, y, z):
    """Cafe-relative (x along the hull, nose = +x; z = -north) to hub-relative."""
    return (CX + x, y, CZ + z)

# ---------------------------------------------------------------- who's who
FOLK = {
    "chef": dict(name="Chef Clamuel", colour="gold", job="butcher", look="plains", spot=cafe(8, 2, 0), yaw=90,
                 hello="Welcome to the Bubble Cafe, {kid}! Tap me for snacks, or tap my bell for a delivery job.",
                 night="Zzz... mmm, coral cookies... (Chef Clamuel is fast asleep. The cafe opens again at sunrise!)"),
    "mayor": dict(name="Mayor Marina", colour="light_purple", job="cleric", look="plains", spot=(-2, 1, -14), yaw=0,
                  hello="Hello, {kid}! Oh dear, have you seen my golden pearls? Tap me!", where="by the welcome arch"),
    "farmer": dict(name="Farmer Kelpsey", colour="green", job="farmer", look="swamp", spot=(2, 1, -26), yaw=0,
                   hello="Howdy, {kid}! I pay Sand Dollars for kelp, sea pickles and seagrass. Tap me to trade.",
                   where="at the Jelly Meadow"),
    "driver": dict(name="Driver Finnley", colour="aqua", job="cartographer", look="plains", spot=(4, 1, 15), yaw=90,
                   hello="Beep beep, {kid}! The bus is late again. Tap me to race the Current Race!",
                   where="at the bus stop", menu="family:undersea/race/menu"),
    # houses.py: their menus and activities live there
    "professor": dict(name="Professor Periwinkle", colour="dark_aqua", job="librarian", look="plains", spot=(16, 1, -21),
                      yaw=0, hello="Oh, hello {kid}! Tap me for a joke, a sea fact or the riddle of the day.",
                      where="in the Seashell house", menu="family:undersea/houses/prof/menu"),
    "coach": dict(name="Coach Cockle", colour="red", job="fisherman", look="jungle", spot=(31, 3, -21), yaw=0,
                  hello="Hey there, {kid}! Ready to bop some clams? Tap me to play Clam Bop!",
                  where="in the Coconut house", menu="family:undersea/houses/bop/menu"),
}
POSTS = ("mayor", "farmer", "driver", "professor", "coach")   # NoAI; the chef keeps its AI inside the dry cafe
TALKERS = ("mayor", "driver", "professor", "coach")          # tapped through a box (the farmer: his trade screen)
NIGHT = "#night family.alive"                  # 1 while the chef is asleep: set by alive.py, picks the "night" hello
LUNCH_TO = ("mayor", "farmer", "driver", "professor", "coach")   # Order Up! targets, picked at random
BELL = cafe(7, 4, 2)
PEARL = M + "ochre_froglight"                  # "golden pearl": glows, and nothing else in town uses it
MEADOW_FLOOR = 1 + max(y for (x, y, z), b in T.v.items() if (x, z) == (-6, -38) and b == M + "moss_block")
PEARL_SPOTS = [("on a Bubble Cafe table", cafe(-7, 3, -1)),
               ("inside the Seashell house", (16, 1, -17)),
               ("inside the Coconut house", (31, 1, -17)),
               ("inside the Watermelon house", (-16, 1, -14)),
               ("on the meadow floor under a jelly", (-6, MEADOW_FLOOR, -38)),
               ("on top of a jelly", (15, 16, -40)),
               ("on the bus stop roof", (6, 5, 14)),
               ("on top of the welcome arch", (0, 10, -12)),
               ("on the submarine's tower", cafe(-2, 12, 1)),
               ("on the Coconut house's umbrella", (29, 19, -19))]
PEARLS = [p for _, p in PEARL_SPOTS]
PLANTS = {M + "seagrass", M + "tall_seagrass[half=lower]", M + "sea_pickle[pickles=3]"}
assert all(p not in T.v or T.v[p] in PLANTS for p in PEARLS), "a pearl spot is taken"

COIN = "minecraft:gold_nugget"
COIN_DATA = {"family_coin": 1}
COIN_COMPONENTS = {"minecraft:item_name": {"text": "Sand Dollar", "color": "yellow"},
                   "minecraft:lore": [{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": False}],
                   "minecraft:custom_data": COIN_DATA}
CHEF_SELLS = [(1, "cookie", 4, "Coral Cookie"), (1, "honey_bottle", 1, "Kelp Shake"),
              (1, "pumpkin_pie", 2, "Sea Pie"), (4, "cake", 1, "Party Cake")]
FARMER_BUYS = [("kelp", 16), ("sea_pickle", 6), ("seagrass", 12)]
LUNCH_PAY, PEARL_PAY = 3, 10
FISH = {"minecraft:tropical_fish/pattern": "kob", "minecraft:tropical_fish/base_color": "orange",
        "minecraft:tropical_fish/pattern_color": "white"}

def offer(buy, sell):
    """Unlimited, no XP, and priceMultiplier 0 so neither demand nor reputation moves the price."""
    return {"buy": buy, "sell": sell, "maxUses": 999999, "uses": 0, "rewardExp": False, "xp": 0,
            "priceMultiplier": F(0), "specialPrice": 0, "demand": 0}

def coins(n):
    return {"id": COIN, "count": n, "components": {"minecraft:custom_data": COIN_DATA}}   # matches only Sand Dollars

OFFERS = {
    "chef": [offer(coins(price), {"id": M + item, "count": n, "components": {"minecraft:item_name": {"text": name}}})
             for price, item, n, name in CHEF_SELLS],
    "farmer": [offer({"id": M + item, "count": n}, {"id": COIN, "count": 1, "components": COIN_COMPONENTS})
               for item, n in FARMER_BUYS],
}

def villager(who):
    f = FOLK[who]
    nbt = {"Tags": ["family.folk", f"family.folk.{who}"] + (["family.tap.farmer"] if who == "farmer" else []),
           "CustomName": {"text": f["name"], "color": f["colour"]}, "CustomNameVisible": True,
           "Invulnerable": True, "PersistenceRequired": True, "Rotation": [F(f["yaw"]), F(0)],
           "VillagerData": {"profession": M + f["job"], "level": 5, "type": M + f["look"]}, "Xp": 250,
           "Offers": {"Recipes": OFFERS.get(who, [])}}
    if who in POSTS:
        nbt["NoAI"] = True
    x, y, z = f["spot"]
    return f"summon minecraft:villager ~{x} ~{y} ~{z} {snbt(nbt)}"   # the whole-number `positioned` origin is already
                                                                  # block-centred, so ~x lands mid-block

# Tap boxes: the talking townsfolk, the chef's bell and each pearl. Slightly bigger than what they cover,
# so taps hit the box first (on Bedrock too); a box over a pearl also stops it being mined.
def boxes():
    out = {f"{who}": (FOLK[who]["spot"], 1.0, 2.2, 0.0) for who in TALKERS}
    out["bell"] = (BELL, 1.1, 1.1, -0.05)
    out.update({f"pearl{i}": (p, 1.1, 1.1, -0.05) for i, p in enumerate(PEARLS, 1)})
    return out

def summon_box(key):
    (x, y, z), w, h, dy = boxes()[key]
    return (f"summon minecraft:interaction ~{x} ~{y + dy} ~{z} "
            f"{snbt({'Tags': ['family.folk.box', f'family.tap.{key}'], 'width': F(w), 'height': F(h)})}")

# ---------------------------------------------------------------- the Bubble Cafe rework
def hull_radius(x):
    e = abs(x) - L
    return R if e <= 0 else math.sqrt(R * R - e * e) if e < R else -1

def interior():
    """Cells inside the hull above the floor, hub-relative: the water that gets drained."""
    out = set()
    for x in range(-13, 14):
        r = hull_radius(x)
        for y in range(2, 10):
            for z in range(-5, 6):
                d = math.hypot(y + 0.5 - CY, z)
                if d <= r - 1.2 and abs(x) < L + R - 1:
                    out.add(cafe(x, y, z))
    return out

def cafe_seal():
    """The doorway's inner end becomes a wall with a door (placed first, before draining)."""
    b = {cafe(x, 1, -3): M + "spruce_planks" for x in (-1, 0, 1)}   # threshold: the door cut took this hull row out
    b.update({cafe(x, y, -3): M + "white_concrete" for y in (2, 3) for x in (-1, 1)})
    b[cafe(0, 2, -3)] = M + "spruce_door[half=lower,facing=south]"
    b[cafe(0, 3, -3)] = M + "spruce_door[half=upper,facing=south]"
    return b

def cafe_inside():
    """Kitchen and counter, plus every waterloggable block in or around the room re-placed dry."""
    b = {}
    for z in range(-2, 3):                               # counter across the room, 1.5 high
        b[cafe(7, 2, z)] = M + "smooth_quartz"
        b[cafe(7, 3, z)] = M + "smooth_quartz_slab[type=bottom,waterlogged=false]"
        b[cafe(6, 2, z)] = M + "spruce_slab[type=bottom,waterlogged=false]"   # customers' step: eyes at 1.62 barely clear 1.5
    for y in (3, 4):                                    # the hull ledges at z=+-3 would let the chef walk round
        for z in (-3, 3):
            b[cafe(7, y, z)] = M + "smooth_quartz"
    b[cafe(7, 3, 2)] = M + "smooth_quartz"               # bell stand
    b[BELL] = M + "bell[attachment=floor,facing=west]"
    b[cafe(9, 2, -2)] = M + "smoker[facing=west]"       # the chef's job site
    b[cafe(8, 2, 2)] = M + "red_bed[part=foot,facing=east]"
    b[cafe(9, 2, 2)] = M + "red_bed[part=head,facing=east]"
    for z in (-1, 0, 1):
        b[cafe(10, 2, z)] = M + "barrel[facing=up]"      # pantry against the nose window
    inside = interior()
    for p, blk in T.v.items():                           # lanterns, table stairs/slabs, hidden lights: dry
        near = any((p[0] + dx, p[1] + dy, p[2] + dz) in inside
                   for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
        if (p in inside or near) and town.wl(blk) != blk and p not in b:
            b[p] = town.wl(blk).replace("waterlogged=true", "waterlogged=false")
    return b

def cafe_roof():
    """A second roof layer wherever the sea sits right on a 1-thick ceiling (same block as below it). Water on top of
    a single block draws dripping particles under it on PC and iPad alike; two blocks thick, it doesn't."""
    room, b = interior(), {**cafe_seal(), **cafe_inside()}
    out = {}
    for (x, y, z) in room:
        ceil, over = (x, y + 1, z), (x, y + 2, z)
        blk = b.get(ceil) or T.v.get(ceil)
        if ceil not in room and blk and "glass" not in blk and over not in T.v and over not in room:
            out[over] = blk
    return out

def cafe_blocks():
    return {**cafe_seal(), **cafe_inside(), **cafe_roof()}

def check_sealed():
    """Every drained cell must be walled in by blocks, so no sea gets in (and nothing outside is drained)."""
    placed = cafe_blocks()
    dry = interior() - set(placed)
    for (x, y, z) in dry:
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if n in dry or n in placed:
                continue
            assert n in T.v, f"cafe leaks: {n} next to {(x, y, z)} is open water"
            assert town.wl(T.v[n]) == T.v[n], f"cafe leaks: waterlogged {T.v[n]} at {n}"
    return dry

def dry_fills(at, cells):
    """Kids' chests and light blocks in a drained room are waterlogged and would pour water back in. Dry them in the
    drain's tick: in open water a dried block soon refills. fill keeps a chest's contents when only its state changes."""
    (x1, y1, z1), (x2, y2, z2) = [[f(c[i] for c in cells) for i in range(3)] for f in (min, max)]
    box = f"~{x1} ~{y1} ~{z1} ~{x2} ~{y2} ~{z2}"
    return [f"{at}fill {box} minecraft:{s},waterlogged=false] replace minecraft:{s},waterlogged=true]"
            for s in [f"chest[facing={f},type={t}" for f in ("north", "south", "east", "west") for t in ("single", "left", "right")]
            + [f"light[level={n}" for n in range(16)]]

def cafe_commands(at):
    """Seal the doorway, take out the old counter, drain, then the kitchen and the dry re-placements."""
    put = lambda p, b: f"{at}setblock ~{p[0]} ~{p[1]} ~{p[2]} {b}"
    cmds = [put(p, b) for p, b in cafe_seal().items()]
    x1, _, z = cafe(1, 2, 2)                             # the old counter along the wall
    cmds.append(f"{at}fill ~{x1} ~2 ~{z} ~{x1 + 5} ~2 ~{z} minecraft:air replace minecraft:smooth_quartz")
    rows = {}
    for (x, y, z) in interior():
        rows.setdefault((y, z), []).append(x)
    for (y, z), xs in sorted(rows.items()):              # drain: one fill per straight run of cells
        xs.sort()
        start = xs[0]
        for a, b in zip(xs, xs[1:] + [None]):
            if b != a + 1:
                cmds.append(f"{at}fill ~{start} ~{y} ~{z} ~{a} ~{y} ~{z} minecraft:air replace minecraft:water")
                start = b
    cmds += dry_fills(at, interior())
    inside = sorted(cafe_inside().items(), key=lambda pb: (pb[0][1], "part=head" in pb[1]))  # stand before bell, bed foot before head
    return cmds + [put(p, b) for p, b in inside] + [put(p, b) for p, b in cafe_roof().items()]

# ---------------------------------------------------------------- talking
def say(who, text):
    """A townsperson's chat line to one kid; {kid} becomes the kid's name."""
    f, parts = FOLK[who], text.split("{kid}")
    comps = [{"text": f["name"], "color": f["colour"]}, {"text": ": " + parts[0], "color": "white"}]
    for p in parts[1:]:
        comps += [{"selector": "@s", "color": "white"}, {"text": p, "color": "white"}]
    return "tellraw @s " + json.dumps(comps)

def dialog(who, text, buttons=(), exit_label="Bye!"):
    """Inline dialog: one message and up to a few buttons that run /trigger family.talk set N."""
    body = [{"type": "minecraft:plain_message", "contents": {"text": text}}]
    title = {"text": FOLK[who]["name"], "color": FOLK[who]["colour"]}
    if not buttons:
        d = {"type": "minecraft:notice", "title": title, "body": body, "action": {"label": exit_label}}
    else:
        d = {"type": "minecraft:multi_action", "title": title, "body": body, "columns": 1,
             "actions": [{"label": lbl, "action": {"type": "minecraft:run_command", "command": f"/trigger family.talk set {n}"}}
                         for lbl, n in buttons],
             "exit_action": {"label": exit_label}}
    return "dialog show @s " + snbt(d)

BUTTONS = {1: "mayor_go", 2: "mayor_hints", 3: "pearl_reward", 4: "lunch_take",     # folk/<name>, or a full id
           5: "family:undersea/race/go", 6: "family:undersea/race/rules", 7: "family:undersea/race/stop",
           **{n: f"family:undersea/houses/{name}" for n, name in enumerate(
               ("prof/joke", "prof/punchline", "prof/fact", "prof/riddle", "prof/answer", "prof/answer", "prof/answer",
                "bop/start", "bop/rules"), 8)}}

# ---------------------------------------------------------------- datapack
def datapack(data, put, give_string):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    dim, d = undersea.DIM, f"{data}/data/family"
    f, fn = f"{d}/function/undersea/folk", "family:undersea/folk"
    at = f"execute in {dim} positioned {hx} {hy} {hz} run "
    absol = lambda x, y, z: f"{hx + x} {hy + y} {hz + z}"
    give_coins = lambda n: f"give @s {give_string(COIN, COIN_COMPONENTS)} {n}"
    def lunch(to):
        return give_string("minecraft:bowl", {
            "minecraft:item_name": {"text": f"Lunch for {FOLK[to]['name']}", "color": FOLK[to]["colour"]},
            "minecraft:lore": [{"text": "From the Bubble Cafe. Tap them to deliver it!", "color": "gray", "italic": False}],
            "minecraft:custom_data": {"family_lunch": 1, "family_to": to}})
    has_lunch = lambda to=None: (f'minecraft:bowl[minecraft:custom_data~{{family_to:"{to}"}}]' if to
                                 else "minecraft:bowl[minecraft:custom_data~{family_lunch:1}]")
    check_sealed()

    put(f"{f}/load.mcfunction", undersea.mcf(
        "scoreboard objectives add family.talk trigger",
        *[f"scoreboard objectives add family.{s} dummy" for s in ("pearls", "lunchday", "folk")],
        "scoreboard players set #day_ticks family.folk 24000",
        f"schedule function {fn}/loop 5t replace"))

    # Every 5 ticks: menu buttons, greetings, posts facing the nearest kid, the chef kept in the kitchen,
    # and self-repair once a kid has been at the hub for 5 s (so everything nearby has loaded: no doubles).
    loop = [f"schedule function {fn}/loop 5t replace",
            f"execute as @a[scores={{family.talk=1..}}] run function {fn}/button"]
    for who in FOLK:
        me = f"@e[type=minecraft:villager,tag=family.folk.{who}]"
        loop += [f"execute as {me} at @s as @a[distance=..5,tag=!family.met.{who}] run function {fn}/hello/{who}",
                 f"execute as {me} at @s run tag @a[distance=12..,tag=family.met.{who}] remove family.met.{who}"]
        put(f"{f}/hello/{who}.mcfunction", undersea.mcf(
            f"tag @s add family.met.{who}",
            *([f"execute if score {NIGHT} matches 1 run return run " + say(who, FOLK[who]["night"])] if "night" in FOLK[who] else []),
            say(who, FOLK[who]["hello"]),
            "playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~"))
    for who in POSTS:
        me = f"@e[type=minecraft:villager,tag=family.folk.{who}]"
        loop += [f"execute as {me} at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes",
                 f"execute as {me} at @s unless entity @a[distance=..8] run rotate @s {FOLK[who]['yaw']} 0"]
    kx, ky, kz = cafe(8, 2, -2)
    loop += [f"execute in {dim} as @e[type=minecraft:villager,tag=family.folk.chef] unless entity "
             f"@s[x={hx + kx},y={hy + ky},z={hz + kz},dx=1,dy=1,dz=4] run tp @s "
             f"{hx + FOLK['chef']['spot'][0] + 0.5} {hy + FOLK['chef']['spot'][1]} {hz + FOLK['chef']['spot'][2] + 0.5}",
             f"execute in {dim} positioned {hx} {hy} {hz} if entity @a[distance=..24] run scoreboard players add #near family.folk 5",
             f"execute in {dim} positioned {hx} {hy} {hz} unless entity @a[distance=..24] run scoreboard players set #near family.folk 0",
             f"execute if score #near family.folk matches 100.. run function {fn}/repair"]
    put(f"{f}/loop.mcfunction", undersea.mcf(*loop))
    put(f"{f}/button.mcfunction", undersea.mcf(
        *[f"execute if score @s family.talk matches {n} run function {name if ':' in name else fn + '/' + name}"
          for n, name in BUTTONS.items()],
        "scoreboard players set @s family.talk 0"))

    summons = {who: villager(who) for who in FOLK}
    put(f"{f}/repair.mcfunction", undersea.mcf(
        "scoreboard players set #near family.folk 0",
        *[f"execute unless entity @e[type=minecraft:villager,tag=family.folk.{who}] run {at}{s}" for who, s in summons.items()],
        *[f"execute unless entity @e[type=minecraft:interaction,tag=family.tap.{k}] run {at}{summon_box(k)}" for k in boxes()],
        *[f"execute in {dim} unless block {absol(*p)} {PEARL} run setblock {absol(*p)} {PEARL}" for p in PEARLS]))

    # --- taps (an advancement per tap box or shop villager; each revokes itself)
    for key in [*TALKERS, "farmer", "bell"] + [f"pearl{i}" for i in range(1, len(PEARLS) + 1)]:
        put(f"{d}/advancement/folk/tap_{key}.json", {
            "criteria": {"tap": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {"entity": {
                "type": "minecraft:entity_properties", "entity": "this",
                "predicate": {"nbt": '{Tags:["family.tap.%s"]}' % key}}}}},
            "rewards": {"function": f"{fn}/tap/{key}"}})
    revoke = lambda key: f"advancement revoke @s only family:folk/tap_{key}"
    deliver = lambda who: [f"execute if items entity @s {slot} {has_lunch(who)} run return run function {fn}/deliver/{who}"
                           for slot in ("container.*", "weapon.offhand")]
    for who in LUNCH_TO:
        put(f"{f}/deliver/{who}.mcfunction", undersea.mcf(
            f"clear @s {has_lunch(who)} 1", give_coins(LUNCH_PAY),
            say(who, f"Lunch from the Bubble Cafe? Yum! Thank you, {{kid}}! Here are {LUNCH_PAY} Sand Dollars."),
            "playsound minecraft:entity.villager.yes neutral @s ~ ~ ~"))

    # Mayor Marina: the Lost Pearls hunt. The macro fills in how many this kid has found.
    put(f"{f}/tap/mayor.mcfunction", undersea.mcf(
        revoke("mayor"), *deliver("mayor"),
        "scoreboard players enable @s family.talk",
        "execute if entity @s[tag=family.pearls_done] run return run " + dialog(
            "mayor", "Thank you again for finding my golden pearls! Our town is lucky to have you."),
        "execute if score @s family.pearls matches 10.. run return run " + dialog(
            "mayor", "You found all 10 of my golden pearls! Thank you so much! I have a reward for you.",
            [("Yay! Thank you!", 3)], "Later"),
        "execute store result storage family:folk pearls.n int 1 run scoreboard players get @s family.pearls",
        f"function {fn}/mayor_ask with storage family:folk pearls"))
    put(f"{f}/mayor_ask.mcfunction", "$" + dialog(
        "mayor", "Welcome to our town under the sea! Oh dear, I've lost my 10 golden pearls all over town. "
                 "Can you find them for me? When you see one, tap it.\n\nYou've found $(n) of 10.",
        [("I'll find them!", 1), ("Any hints?", 2)]) + "\n")
    put(f"{f}/mayor_go.mcfunction", undersea.mcf(say("mayor", "Thank you, {kid}! Tap each golden pearl you find.")))
    put(f"{f}/mayor_hints.mcfunction", undersea.mcf(dialog(
        "mayor", "Some pearls are inside houses. Some are up high: look on roofs and on top of things. "
                 "One is under a jelly, and one is somewhere you can get a snack!", exit_label="Thanks!")))
    put(f"{f}/pearl_reward.mcfunction", undersea.mcf(
        "execute unless score @s family.pearls matches 10.. run return fail",
        "execute if entity @s[tag=family.pearls_done] run return fail",
        "tag @s add family.pearls_done", give_coins(PEARL_PAY), f"give @s {give_string('minecraft:tropical_fish_bucket', FISH)}",
        say("mayor", f"Here are {PEARL_PAY} Sand Dollars, and a pet fish! Let it out somewhere nice."),
        "playsound minecraft:entity.player.levelup master @s ~ ~ ~"))
    for i, (x, y, z) in enumerate(PEARLS, 1):
        here = f"execute in {dim} positioned {hx + x + 0.5} {hy + y + 0.5} {hz + z + 0.5} run "
        count = [{"score": {"name": "@s", "objective": "family.pearls"}, "color": "gold"}, {"text": " of 10", "color": "gold"}]
        put(f"{f}/tap/pearl{i}.mcfunction", undersea.mcf(
            revoke(f"pearl{i}"),
            f"execute if entity @s[tag=family.found.pearl{i}] run return run title @s actionbar "
            + json.dumps([{"text": "You already found this pearl: ", "color": "gold"}] + count),
            f"tag @s add family.found.pearl{i}", "scoreboard players add @s family.pearls 1",
            here + "particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.05 25",
            here + "playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.2",
            "title @s actionbar " + json.dumps([{"text": "Golden pearl! ", "color": "gold"}] + count),
            "execute if score @s family.pearls matches 10 run " + say("mayor", "You found all 10?! Come and see me by the welcome arch!")))

    # Driver Finnley: the Current Race menu (race.py); Professor Periwinkle and Coach Cockle: houses.py.
    for who in [w for w in FOLK if "menu" in FOLK[w]]:
        put(f"{f}/tap/{who}.mcfunction", undersea.mcf(revoke(who), *deliver(who), f"function {FOLK[who]['menu']}"))
    # Farmer Kelpsey: tapping opens the trade screen; a lunch in the inventory is delivered at the same time.
    put(f"{f}/tap/farmer.mcfunction", undersea.mcf(revoke("farmer"), *deliver("farmer")))

    # Chef Clamuel's bell: Order Up!, one lunch per Minecraft day (24000 ticks of game time) per kid.
    today = [f"execute store result score #day family.folk run time query gametime",
             "scoreboard players operation #day family.folk /= #day_ticks family.folk"]
    put(f"{f}/tap/bell.mcfunction", undersea.mcf(
        revoke("bell"), f"execute in {dim} run playsound minecraft:block.bell.use block @a {absol(*BELL)}",
        "scoreboard players enable @s family.talk", *today,
        *[f"execute if items entity @s container.* {has_lunch(to)} run return run "
          + dialog("chef", f"You still have the lunch for {FOLK[to]['name']}! Tap them to deliver it.", exit_label="OK!")
          for to in LUNCH_TO],
        "execute if score @s family.lunchday = #day family.folk run return run "
        + dialog("chef", "That's all the deliveries for today. Come back later!", exit_label="OK!"),
        dialog("chef", f"Order up! I've got a lunch that needs delivering. Can you take it? It pays {LUNCH_PAY} Sand Dollars.",
               [("I'll take it!", 4)], "Not now")))
    put(f"{f}/lunch_take.mcfunction", undersea.mcf(
        f"execute if items entity @s container.* {has_lunch()} run return fail", *today,
        "execute if score @s family.lunchday = #day family.folk run return fail",
        "scoreboard players operation @s family.lunchday = #day family.folk",
        f"execute store result score #pick family.folk run random value 1..{len(LUNCH_TO)}",
        *[f"execute if score #pick family.folk matches {i} run return run function {fn}/lunch/{to}"
          for i, to in enumerate(LUNCH_TO, 1)]))
    for to in LUNCH_TO:
        put(f"{f}/lunch/{to}.mcfunction", undersea.mcf(
            f"give @s {lunch(to)}", say("chef", f"Thanks, {{kid}}! Take it to {FOLK[to]['name']} {FOLK[to]['where']}.")))

    # Build: load the area, wait for its entities, then the cafe, pearls and townsfolk (old ones replaced).
    pts = [FOLK[w]["spot"] for w in FOLK] + PEARLS + [cafe(-13, 0, -5), cafe(13, 0, 5)]
    x1, z1 = min(p[0] for p in pts), min(p[2] for p in pts)
    x2, z2 = max(p[0] for p in pts), max(p[2] for p in pts)
    area = f"{hx + x1} {hz + z1} {hx + x2} {hz + z2}"
    put(f"{data}/data/family/function/undersea/build_townsfolk.mcfunction", undersea.mcf(
        f"execute in {dim} run forceload add {area}", f"schedule function {fn}/build 3s replace"))
    put(f"{f}/build.mcfunction", undersea.mcf(
        *[f"execute in {dim} unless loaded {hx + x} {hy} {hz + z} run return run schedule function {fn}/build 2s replace"
          for x, z in ((x1, z1), (x2, z2))],
        "kill @e[type=minecraft:villager,tag=family.folk]", "kill @e[type=minecraft:interaction,tag=family.folk.box]",
        *cafe_commands(at),
        *[f"execute in {dim} run setblock {absol(*p)} {PEARL}" for p in PEARLS],
        *[at + s for s in summons.values()], *[at + summon_box(k) for k in boxes()],
        f"execute in {dim} run forceload remove {area}"))
    put(f"{f}/give_coins.mcfunction", undersea.mcf(give_coins(10)))     # admin/testing: 10 Sand Dollars

# ---------------------------------------------------------------- previews
def preview():
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(f"{town.HERE}/previews", exist_ok=True)
    town.COLOURS.update({"smoker": "#5A5A5A", "red_bed": "#B02E26", "spruce_door": "#6B4E2E", "bell": "#F0C64A",
                         "smooth_quartz_slab": "#ECE6DE", "ochre_froglight": "#F5D27A", "light": None})
    after = dict(T.v)
    for p in interior():
        after.pop(p, None)
    after.update(cafe_blocks())
    for x in range(1, 7):
        after.pop(cafe(x, 2, 2), None)
    f15, f17 = ImageFont.load_default(size=15), ImageFont.load_default(size=17)

    def label(d, cx, cy, tx, ty, text, font):
        w = d.textlength(text, font=font)
        d.line([cx, cy, tx, ty], fill=(255, 255, 255), width=2)
        d.rectangle([tx - w / 2 - 4, ty - 11, tx + w / 2 + 4, ty + 11], fill=(255, 255, 255))
        d.text((tx - w / 2, ty - 10), text, fill=(20, 20, 20), font=font)

    # cafe, top-down: floor and what stands on it
    k, X0, X1, Z0, Z1 = 34, CX - 14, CX + 19, CZ - 7, CZ + 6
    img = Image.new("RGB", ((X1 - X0 + 1) * k, (Z1 - Z0 + 1) * k + 50), (24, 70, 84)); d = ImageDraw.Draw(img)
    hull = (238, 122, 18)
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            col = None
            for y in (1, 2, 3, 4):
                b = after.get((x, y, z))
                if b and town.colour(b) and "lantern" not in b:
                    col = hull if y > 1 and b in (M + "orange_concrete", M + "white_concrete") else town.colour(b)
                    if "spruce_slab[type=bottom" in b:
                        col = town.shade(col, 1.35)          # the customers' step, a little lighter than the floor
            if col:
                d.rectangle([(x - X0) * k, (z - Z0) * k, (x - X0 + 1) * k - 1, (z - Z0 + 1) * k - 1], fill=col)
    for tx in (-3, -7):
        for x in (tx - 1, tx, tx + 1):
            p = cafe(x, 0, -1)
            d.rectangle([(p[0] - X0) * k, (p[2] - Z0) * k, (p[0] - X0 + 1) * k - 1, (p[2] - Z0 + 1) * k - 1], fill=(74, 53, 32))
    P = lambda p: ((p[0] - X0 + 0.5) * k, (p[2] - Z0 + 0.5) * k)
    cx, cy = P(FOLK["chef"]["spot"])
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 60, 60), outline=(255, 255, 255), width=3)
    for p, text, dx, dy in ((cafe(0, 0, -3), "wooden door (tap to open)", 0, -2.6), (cafe(-3, 0, -1), "table", 0, -2.6),
                            (PEARLS[0], "table (golden pearl on it)", 0, 3.4), (cafe(7, 0, 0), "counter, 1.5 high", -3, -3.9),
                            (cafe(6, 0, 1), "half-block step", -6.5, 3.6),
                            (BELL, "order bell", -3.5, 2.6), (FOLK["chef"]["spot"], "Chef Clamuel", 2.5, -3.9),
                            (cafe(9, 0, -2), "smoker (job)", 5, -1.2), (cafe(9, 0, 2), "bed", 3.5, 2.9),
                            (cafe(10, 0, 0), "pantry barrels", 5, 0.8)):
        px, py = P(p)
        label(d, px, py, px + dx * k, py + dy * k, text, f17)
    d.text((10, img.height - 36), "Bubble Cafe after the rework, top-down, north up. Orange = hull. Dry inside; "
           "the kitchen is the strip behind the counter.", fill=(255, 255, 255), font=f15)
    img.save(f"{town.HERE}/previews/townsfolk-cafe.png")

    # town map: townsfolk and pearls
    xs = [x for (x, _, _) in T.v]; zs = [z for (_, _, z) in T.v]
    x0, z0, x1, z1 = min(xs) - 3, min(zs) - 3, max(xs) + 3, max(zs) + 3
    k = 7
    img = Image.new("RGB", ((x1 - x0 + 1) * k, (z1 - z0 + 1) * k + 150), (24, 70, 84)); d = ImageDraw.Draw(img)
    top = {}
    for (x, y, z), b in T.v.items():
        c = town.colour(b)
        if c and ((x, z) not in top or y > top[(x, z)][0]):
            top[(x, z)] = (y, c)
    for a, b, c, e, _ in T.zones:
        for x in range(a, c + 1):
            for z in range(b, e + 1):
                top.setdefault((x, z), (0, town.colour(town.SAND)))
    for x in range(-10, 11):
        for z in range(-10, 11):
            if math.hypot(x, z) <= 10.5:
                top.setdefault((x, z), (0, town.colour(town.SAND)))
    for (x, z), (y, c) in top.items():
        d.rectangle([(x - x0) * k, (z - z0) * k, (x - x0 + 1) * k - 1, (z - z0 + 1) * k - 1], fill=town.shade(c, 0.85 + 0.03 * min(y, 5)))
    M2 = lambda x, z: ((x - x0 + 0.5) * k, (z - z0 + 0.5) * k)
    for x, z, s in [(0, 0, "Hub")] + [(x, z, s) for x, z, s in T.labels if s.startswith("Plot")]:
        w = d.textlength(s, font=f15); cx, cy = M2(x, z)
        d.rectangle([cx - w / 2 - 3, cy - 9, cx + w / 2 + 3, cy + 9], fill=(255, 255, 255)); d.text((cx - w / 2, cy - 8), s, fill=(20, 20, 20), font=f15)
    for i, (x, y, z) in enumerate(PEARLS, 1):
        cx, cy = M2(x, z)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(245, 200, 60), outline=(60, 40, 0), width=2)
        d.text((cx - d.textlength(str(i), font=f15) / 2, cy - 8), str(i), fill=(40, 20, 0), font=f15)
    for who, fdat in FOLK.items():
        x, _, z = fdat["spot"]; cx, cy = M2(x, z)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 60, 60), outline=(255, 255, 255), width=3)
        w = d.textlength(fdat["name"], font=f15); lx = cx + 12 if cx + 18 + w < img.width else cx - 18 - w
        d.rectangle([lx, cy - 10, lx + w + 6, cy + 10], fill=(255, 60, 60)); d.text((lx + 3, cy - 8), fdat["name"], fill=(255, 255, 255), font=f15)
    top_y = (z1 - z0 + 1) * k + 8
    d.text((10, top_y), "North is up. Red = townsfolk. Gold = the 10 golden pearls:", fill=(255, 255, 255), font=f15)
    for i, (where, (_, y, _)) in enumerate(PEARL_SPOTS):
        d.text((10 + (i // 5) * (img.width // 2), top_y + 24 + (i % 5) * 22), f"{i + 1}. {where} (y{y})",
               fill=(245, 200, 60), font=f15)
    img.save(f"{town.HERE}/previews/townsfolk-map.png")

if __name__ == "__main__":
    print("drained cells:", len(check_sealed()), "| pearls:", PEARLS)
    preview()
