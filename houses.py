"""Something to do in the Undersea town's houses (town.py). Datapack only.
- Coconut house: Clam Bop, an arcade game. Tap Coach Cockle > Play Clam Bop!, 3-2-1-GO, 30 seconds: 8 clams (bone
  blocks) on the coconut's floor pop open one at a time (glowing pink, bubbles, a pop) and shut again a second or so
  later, faster towards the end. Tap an open one (iPad) or click it with either button (PC): 1 bop. Everyone in the
  coconut plays at once. Best per kid, a TOP BOPPERS board (top 5), 10+ bops pays 2 Sand Dollars once a day.
  Each clam has an interaction box: a tap or right-click fires an advancement; a left-click is read from the box's
  `attack` data every tick of a game.
- Seashell house: Professor Periwinkle among bookshelves: a joke, a true sea fact, or the riddle of the day (3 answer
  buttons; right pays 2 Sand Dollars once a day, wrong gives a hint). A kid hears every joke (and fact) once before any
  comes round again.
- Watermelon house: the kids' clubhouse, dried out like the Bubble Cafe (a wooden door holds the sea back), with a second
  rind layer wherever the sea sits on a 1-thick ceiling (no drips) and a sign the kids can name. Empty, to furnish.
- A sign over each door.
Coach Cockle and Professor Periwinkle are townsfolk (townsfolk.FOLK): their greetings, turning to face kids, coming back
when missing and Order Up! lunches come from townsfolk.py. Their menus and the activities are here.
Coordinates are relative to the hub centre like town.py (y=0 is the ground).
  python3 houses.py -> previews/houses.png
  build.py          -> family:undersea/houses/*  (admin runs family:undersea/build_houses; safe to re-run)"""
import math
import town, undersea, race, alive, townsfolk as tf
from town import M
from townsfolk import F, snbt, say, dialog

T = tf.T
DIM = undersea.DIM
WORLD = alive.world()                                   # every known block: town, course, cafe, pearls
COCO, SHELL, MELON = (31, -17), (16, -17), (-16, -10)   # house centres, as town.build() places them
CLAM_SHUT, CLAM_OPEN = M + "bone_block[axis=y]", M + "pearlescent_froglight[axis=y]"
COUNT, PLAY = 60, 600                                   # ticks: 3-2-1, then 30 s of bopping
PHASES = [(401, PLAY, 28, 12, 20), (201, 400, 22, 9, 15), (1, 200, 16, 6, 11)]   # ticks left: open for, next pop a..b
PRIZE_AT, PRIZE, RIDDLE_PAY = 10, 2, 2
COCO_BOX = (COCO[0] - 6, 1, COCO[1] - 6, COCO[0] + 6, 12, COCO[1] + 7)   # inside the coconut and its doorway
BOARD_AT = (COCO[0] + 0.5, 6.6, COCO[1] + 0.5)          # TOP BOPPERS, floating in the middle of the coconut
NAMER_AT = (COCO[0] + 0.5, -0.5, COCO[1] + 0.5)         # the board's hidden name helper, in the ground under it
SHELVES = [(13, 1, -21), (14, 1, -21), (18, 1, -21), (19, 1, -21), (14, 2, -21), (18, 2, -21), (16, 1, -22)]
LECTERN = (14, 1, -20)
BTN = {name.split("houses/")[1]: n for n, name in tf.BUTTONS.items() if "houses/" in name}
ANSWER = [n for n, name in sorted(tf.BUTTONS.items()) if name.endswith("prof/answer")]

JOKES = [
    ("What did the ocean say to the beach?", "Nothing. It just waved!"),
    ("Why are fish so smart?", "Because they live in schools!"),
    ("What do you call a fish with no eyes?", "A fsh!"),
    ("Why don't crabs ever share?", "Because they're shellfish!"),
    ("Where do fish keep their money?", "In the river bank!"),
    ("What's a shark's favourite game?", "Swallow the leader!"),
    ("What did one tide pool say to the other?", "Show me your mussels!"),
    ("How do you make an octopus laugh?", "With ten-tickles!"),
    ("What's the best way to talk to a fish?", "Drop it a line!"),
    ("Why did the dolphin cross the beach?", "To get to the other tide!"),
    ("What do sea monsters eat for lunch?", "Fish and ships!"),
    ("Why do seagulls fly over the sea?", "Because if they flew over the bay, they'd be bagels!"),
    ("What do you get when you cross a fish and an elephant?", "Swimming trunks!"),
    ("What do you call a fish wearing a bow tie?", "Sofishticated!"),
    ("Where do mermaids watch movies?", "At the dive-in!"),
    ("What does a turtle do on its birthday?", "It shell-ebrates!"),
    ("What did the boat say to the pier?", "What's up, dock?"),
    ("How do fish get to school?", "On the octo-bus!"),
    ("Why do axolotls love quiz shows?", "Because they axolotl questions!"),
    ("Why is a turtle never homesick?", "Because it always has its house with it!"),
    ("What do you call a fish that does operations?", "A sturgeon!"),
    ("What's the saddest creature in the ocean?", "The blue whale!"),
    ("Which fish only comes out at night?", "A starfish!"),
    ("What did the whale say after bumping into the boat?", "Sorry, it was just a fluke!"),
]
FACTS = [
    "An octopus has three hearts, and its blood is blue!",
    "Axolotls can grow back a lost leg, and even parts of their heart.",
    "Seahorse dads carry the babies until they hatch.",
    "The blue whale is the biggest animal that has ever lived, bigger than any dinosaur.",
    "Sea stars don't have a brain or blood. They can grow back a lost arm, too!",
    "Jellyfish have been around for more than 500 million years, long before the dinosaurs.",
    "Jellyfish have no brain, no heart and no bones.",
    "Dolphins sleep with half of their brain at a time, so they can keep swimming and breathing.",
    "Every dolphin has its own whistle, like a name, and its friends use it to call it.",
    "Coral looks like a plant or a rock, but it's made of lots of tiny animals.",
    "The ocean covers more than two thirds of the Earth.",
    "About half of the air we breathe is made by tiny ocean plants called phytoplankton.",
    "Sharks have been around for longer than trees!",
    "Sharks never run out of teeth: new ones keep growing all their lives.",
    "Lots of real sea animals glow in the dark. It's called bioluminescence.",
    "A group of jellyfish is called a smack.",
    "A pufferfish puffs up by gulping lots of water very fast.",
    "Giant kelp can grow more than half a metre in one day.",
    "The deepest part of the ocean is deeper than Mount Everest is tall.",
    "A sea cucumber breathes through its bottom!",
    "A narwhal's long tusk is really a giant tooth.",
    "An octopus can taste things with its arms.",
    "Parrotfish crunch up coral and poop out sand. Lots of white beach sand comes from parrotfish!",
    "Sea pickles are real animals! They're called pyrosomes, and they glow.",
]
RIDDLES = [   # (riddle, 3 answers, which one is right, hint)
    ("I have eight arms but no hands, and I squirt ink when I'm scared. What am I?",
     ("An octopus", "A shark", "A crab"), 0, "Count my arms!"),
    ("I carry my house on my back wherever I go. Grandpa Mossback is one of me. What am I?",
     ("A jellyfish", "A turtle", "A fish"), 1, "Look for me paddling over the Jelly Meadow."),
    ("I have a bed but never sleep, and a mouth but never eat. What am I?",
     ("A whale", "A clam", "A river"), 2, "I flow all the way to the sea."),
    ("The more of me you take, the more you leave behind. What am I?",
     ("Footsteps", "Sand Dollars", "Bubbles"), 0, "Walk along the beach, then look behind you."),
    ("What can fill a whole room but takes up no space?", ("Water", "Light", "Sand"), 1, "Switch me on!"),
    ("What gets wetter the more it dries?", ("A fish", "Seaweed", "A towel"), 2, "You use me after a swim."),
    ("I'm full of holes, but I can still hold water. What am I?",
     ("A sponge", "A bucket", "A boat"), 0, "Squeeze me!"),
    ("What has to be broken before you can use it?", ("A pearl", "An egg", "A drum"), 1, "Chickens make them."),
    ("What has a neck but no head, and wears a cap?",
     ("A turtle", "A crab", "A bottle"), 2, "Sometimes there's a message inside me."),
    ("I go up and down twice a day, but I never leave the sea. What am I?",
     ("The tide", "A whale", "A boat"), 0, "Watch the water at the beach."),
    ("What has hands but can't clap?", ("A crab", "A clock", "An octopus"), 1, "Tick tock!"),
    ("What kind of tree fits in your hand?", ("A coral tree", "A kelp tree", "A palm tree"), 2,
     "Look at the inside of your hand."),
    ("I'm tall when I'm young and short when I'm old. What am I?",
     ("A candle", "A turtle", "A jellyfish"), 0, "I glow on birthday cakes."),
    ("What has a head and a tail, but no body?", ("A fish", "A coin", "A snake"), 1, "Like a Sand Dollar!"),
    ("Which room has no doors and no windows?",
     ("A submarine", "The Bubble Cafe", "A mushroom"), 2, "It grows in the forest."),
]

def clam_cells():
    """8 cells on the coconut's bowl floor (y 2, a block under each), spread round it, clear of the doorway (south) and
    of Coach Cockle's spot (north)."""
    cx, cz = COCO
    ring = sorted((math.atan2(z - cz, x - cx), (x, 2, z)) for x in range(cx - 4, cx + 5) for z in range(cz - 4, cz + 5)
                  if (x, 2, z) not in WORLD and (x, 1, z) in T.v and 2.6 <= math.hypot(x - cx, z - cz) <= 3.7
                  and not (abs(x - cx) <= 1 and abs(z - cz) >= 2))
    return [ring[len(ring) * i // 8][1] for i in range(8)]

CLAMS = clam_cells()

def door_sign(part, cx, *lines):
    """A wall sign (kids can edit it) on a house's front at y 5, over its south-facing door."""
    z = max(p[2] for p in T.parts[part] if p[0] == cx and p[1] == 5 and p in T.v)
    return (cx, 5, z + 1), town.wl(town.sign("oak_wall_sign", "facing=south", *lines))

SIGNS = dict([door_sign("seashell", SHELL[0], "Professor", "Periwinkle", "Jokes, facts", "and riddles!"),
              door_sign("coconut", COCO[0], "~ Clam Bop ~", "", "Tap the Coach", "to play!"),
              door_sign("watermelon", MELON[0], "~ Clubhouse ~", "", "(name me!)")])

# ---------------------------------------------------------------- the clubhouse (the watermelon, dried out)
def club_seal():
    """The 3x4 doorway in the cut face: red frame (the flesh's colour) round a wooden door."""
    cx, cz = MELON
    b = {(cx + dx, y, cz): M + "red_concrete" for dx in (-1, 1) for y in range(1, 5)}
    b.update({(cx, y, cz): M + "red_concrete" for y in (3, 4)})
    b[(cx, 1, cz)] = M + "spruce_door[half=lower,facing=north]"
    b[(cx, 2, cz)] = M + "spruce_door[half=upper,facing=north]"
    return b

def club_room():
    """(water cells to drain, waterlogged blocks to dry): everything reachable from inside without passing a block.
    Asserts the room is closed (nothing reaches outside the watermelon)."""
    walls = {**WORLD, **club_seal()}
    wet = lambda p: p in walls and town.wl(walls[p]) != walls[p]          # waterloggable: holds water, not a wall
    cx, cz = MELON
    water, dry, todo = set(), {}, [(cx, 1, cz - 3)]
    while todo:
        p = todo.pop()
        if p in water or p in dry or (p in walls and not wet(p)):
            continue
        assert cx - 9 <= p[0] <= cx + 9 and 1 <= p[1] <= 9 and cz - 9 <= p[2] < cz, f"the clubhouse leaks at {p}"
        if p in walls:
            dry[p] = town.wl(walls[p]).replace("waterlogged=true", "waterlogged=false")
        else:
            water.add(p)
        x, y, z = p
        todo += [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
    return water, dry

def club_roof():
    """A second rind layer wherever the sea sits right on a 1-thick ceiling (same block as below it): water on top of a
    single block draws drip particles under it (townsfolk.cafe_roof)."""
    water, dry = club_room()
    room = water | set(dry)
    out = {}
    for (x, y, z) in room:
        ceil, over = (x, y + 1, z), (x, y + 2, z)
        if ceil not in room and ceil in T.v and "glass" not in T.v[ceil] and over not in WORLD and over not in room:
            out[over] = T.v[ceil]
    return out

def check():
    """Everything placed goes into open water; the townsfolk stand on a block with room above."""
    taken = lambda ps: [(p, WORLD[p]) for p in ps if p in WORLD]
    assert len(set(CLAMS)) == 8 and not taken(CLAMS), taken(CLAMS)
    for who in ("professor", "coach"):
        x, y, z = tf.FOLK[who]["spot"]
        assert not taken([(x, y, z), (x, y + 1, z)]) and (x, y - 1, z) in T.v, f"{who}'s spot isn't free"
    assert not taken(SHELVES + [LECTERN] + list(SIGNS) + list(club_seal()) + list(club_roof())), "a spot is taken"

# ---------------------------------------------------------------- datapack
def datapack(data, put, give_string):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    d = f"{data}/data/family"
    f, fn, mcf = f"{d}/function/undersea/houses", "family:undersea/houses", undersea.mcf
    check()
    num = lambda v: f"{round(v, 3):g}"
    a = lambda x, y, z: f"{num(hx + x)} {num(hy + y)} {num(hz + z)}"            # absolute
    mid = lambda p: a(p[0] + 0.5, p[1] + 0.5, p[2] + 0.5)
    sea = f"execute in {DIM} "
    at = f"execute in {DIM} positioned {hx} {hy} {hz} run "     # block-centred origin, like townsfolk's summons
    S = "family.house"                                         # #game clock, #c<i> open clams, #next, #day, ...
    coins = lambda n: f"give @s {give_string(tf.COIN, tf.COIN_COMPONENTS)} {n}"
    x1, y1, z1, x2, y2, z2 = COCO_BOX
    inside = f"in {DIM} as @a[x={hx + x1},y={hy + y1},z={hz + z1},dx={x2 - x1},dy={y2 - y1},dz={z2 - z1}]"
    today = [f"execute store result score #day {S} run time query gametime", f"scoreboard players operation #day {S} /= #day_ticks {S}"]
    shut = M + "bone_block"
    opened = M + "pearlescent_froglight"

    put(f"{f}/load.mcfunction", mcf(
        *[f"scoreboard objectives add {o} dummy" for o in (S, "family.bops", "family.bop_best", "family.bop_day",
                                                          "family.riddle_day", "family.joke", "family.fact")],
        f"scoreboard players set #day_ticks {S} 24000", f"scoreboard players set #20 {S} 20",
        f"scoreboard players set #riddles {S} {len(RIDDLES)}",
        *[f"scoreboard players set #{kind}s {S} {len(lst)}" for kind, lst in (("joke", JOKES), ("fact", FACTS))],
        f"schedule function {fn}/loop 1s replace"))
    put(f"{f}/tick.mcfunction", mcf(f"execute if score #game {S} matches 1.. run function {fn}/bop/tick"))

    # --- Clam Bop: #game counts down from PLAY + COUNT (3-2-1), GO at PLAY, the end at 0
    b, bf = f"{fn}/bop", f"{f}/bop"
    clam_box = lambda i: at + f"summon minecraft:interaction ~{CLAMS[i][0]} ~{CLAMS[i][1] - 0.05} ~{CLAMS[i][2]} " + snbt(
        {"Tags": ["family.house", "family.house.clam", f"family.tap.clam{i}"], "width": F(1.1), "height": F(1.1)})
    put(f"{bf}/tick.mcfunction", mcf(
        f"scoreboard players remove #game {S} 1",
        f"execute if score #game {S} matches {PLAY + 1}.. run return run function {b}/countdown",
        f"execute if score #game {S} matches {PLAY} run function {b}/go",
        *[f"execute as @e[type=minecraft:interaction,tag=family.tap.clam{i}] if data entity @s attack run function {b}/hit/{i}"
          for i in range(8)],
        *[f"execute if score #c{i} {S} matches 1 run function {b}/shut/{i}" for i in range(8)],
        *[f"execute if score #c{i} {S} matches 1.. run scoreboard players remove #c{i} {S} 1" for i in range(8)],
        f"scoreboard players remove #next {S} 1",
        f"execute if score #next {S} matches ..0 run function {b}/pop",
        f"scoreboard players operation #s {S} = #game {S}", f"scoreboard players operation #s {S} /= #20 {S}",
        f"execute {inside} run function {b}/show",
        f"execute if score #game {S} matches 0 run function {b}/end"))
    put(f"{bf}/countdown.mcfunction", mcf(*[
        f"execute if score #game {S} matches {PLAY + t} {inside} at @s run " + cmd
        for t, n in ((60, "3"), (40, "2"), (20, "1")) for cmd in (
            'title @s title ' + snbt({"text": n, "color": "yellow", "bold": True}),
            "playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1")]))
    put(f"{bf}/go.mcfunction", mcf(
        "scoreboard players reset * family.bops", "tag @a remove family.bopper",
        f"execute as @e[type=minecraft:interaction,tag=family.house.clam] run data remove entity @s attack",
        f"scoreboard players set #next {S} 6",
        f"execute {inside} run title @s subtitle " + snbt({"text": "Bop the pink clams!", "color": "light_purple"}),
        f"execute {inside} run title @s title " + snbt({"text": "GO!", "color": "green", "bold": True}),
        f"execute {inside} at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2"))
    put(f"{bf}/show.mcfunction", mcf(
        f"scoreboard players add @s family.bops 0",
        "title @s actionbar " + snbt([
            {"text": "Clam Bop   ", "color": "light_purple"}, {"text": "Bops: ", "color": "white"},
            {"score": {"name": "@s", "objective": "family.bops"}, "color": "gold"}, {"text": "   Time: ", "color": "white"},
            {"score": {"name": "#s", "objective": S}, "color": "gold"}, {"text": "s", "color": "white"}])))
    put(f"{bf}/pop.mcfunction", mcf(
        f"execute store result score #pick {S} run random value 0..7",
        *[f"execute if score #pick {S} matches {i} run function {b}/open/{i}" for i in range(8)],
        *[f"execute if score #game {S} matches {lo}..{hi} store result score #next {S} run random value {g1}..{g2}"
          for lo, hi, _, g1, g2 in PHASES]))
    for i, c in enumerate(CLAMS):
        put(f"{bf}/open/{i}.mcfunction", mcf(
            f"execute if score #c{i} {S} matches 1.. run return fail",
            f"{sea}run setblock {a(*c)} {CLAM_OPEN}",
            *[f"execute if score #game {S} matches {lo}..{hi} run scoreboard players set #c{i} {S} {t}" for lo, hi, t, _, _ in PHASES],
            f"{sea}run particle minecraft:bubble {mid(c)} 0.3 0.4 0.3 0.05 12",
            f"{sea}run playsound minecraft:block.bubble_column.bubble_pop block @a {mid(c)} 1 1.4"))
        put(f"{bf}/shut/{i}.mcfunction", mcf(f"{sea}if block {a(*c)} {opened} run setblock {a(*c)} {CLAM_SHUT}"))
        put(f"{bf}/hit/{i}.mcfunction", mcf(f"execute on attacker at @s run function {b}/bop/{i}", "data remove entity @s attack"))
        put(f"{bf}/tap/{i}.mcfunction", mcf(f"advancement revoke @s only family:houses/clam{i}", f"function {b}/bop/{i}"))
        put(f"{d}/advancement/houses/clam{i}.json", {
            "criteria": {"tap": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {"entity": {
                "type": "minecraft:entity_properties", "entity": "this",
                "predicate": {"nbt": '{Tags:["family.tap.clam%d"]}' % i}}}}},
            "rewards": {"function": f"{b}/tap/{i}"}})
        put(f"{bf}/bop/{i}.mcfunction", mcf(                    # as the kid, at the kid
            f"execute unless score #game {S} matches 1..{PLAY} run return fail",
            f"execute unless score #c{i} {S} matches 1.. run return fail",
            f"scoreboard players set #c{i} {S} 0",
            f"function {b}/shut/{i}",
            "scoreboard players add @s family.bops 1", "tag @s add family.bopper",
            f"{sea}run particle minecraft:end_rod {mid(c)} 0.3 0.3 0.3 0.05 10",
            "playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.2"))
    put(f"{bf}/end.mcfunction", mcf(
        *[f"scoreboard players set #c{i} {S} 0" for i in range(8)], *[f"function {b}/shut/{i}" for i in range(8)],
        f"execute {inside} run tag @s add family.bopper",
        f"execute as @a[tag=family.bopper] at @s run function {b}/result"))
    put(f"{bf}/result.mcfunction", mcf(
        "tag @s remove family.bopper", "scoreboard players add @s family.bops 0",
        "title @s times 5 60 20",
        "title @s subtitle " + snbt([{"text": "You bopped ", "color": "white"},
                                     {"score": {"name": "@s", "objective": "family.bops"}, "color": "gold"},
                                     {"text": " clams!", "color": "white"}]),
        "title @s title " + snbt({"text": "Time's up!", "color": "light_purple", "bold": True}),
        "playsound minecraft:entity.player.levelup master @s ~ ~ ~",
        *today,
        f"execute if score @s family.bops matches {PRIZE_AT}.. unless score @s family.bop_day = #day {S} run function {b}/prize",
        f"execute if score @s family.bops matches 1.. unless score @s family.bop_best >= @s family.bops run function {b}/best"))
    put(f"{bf}/prize.mcfunction", mcf(
        f"scoreboard players operation @s family.bop_day = #day {S}", coins(PRIZE),
        say("coach", f"Great bopping, {{kid}}! {PRIZE_AT} or more! Here are {PRIZE} Sand Dollars.")))
    put(f"{bf}/best.mcfunction", mcf(
        "scoreboard players operation @s family.bop_best = @s family.bops",
        say("coach", "That's your best yet, {kid}!"), f"function {b}/leaderboard/add"))
    race.leaderboard(put, bf, b, "family:houses", S, "family.bop_best", "TOP BOPPERS", "$(n)   $(p)",
                     "family.house.namer", "family.house.board")
    put(f"{bf}/board.mcfunction", mcf(                          # the board and its name helper (summon, then fill in)
        f"{sea}run summon minecraft:text_display {a(*BOARD_AT)} " + snbt({
            "Tags": ["family.house", "family.house.board"], "billboard": "center", "brightness": {"sky": 15, "block": 15},
            "line_width": 220, "text": {"text": "TOP BOPPERS", "color": "gold", "bold": True}}),
        f"{sea}run summon minecraft:item_display {a(*NAMER_AT)} " + snbt({
            "Tags": ["family.house", "family.house.namer"],
            "transformation": {"left_rotation": [F(0), F(0), F(0), F(1)], "right_rotation": [F(0), F(0), F(0), F(1)],
                               "translation": [F(0), F(0), F(0)], "scale": [F(0)] * 3}}),
        f"function {b}/leaderboard/show"))

    # Coach Cockle's menu (townsfolk tap/coach) and its buttons
    intro = ("Hi! I'm Coach Cockle. Want to play Clam Bop? Clams in the floor pop open and glow pink. Bop them before "
             "they shut! You have 30 seconds.")
    play = [("Play Clam Bop!", BTN["bop/start"]), ("How to play", BTN["bop/rules"])]
    put(f"{bf}/menu.mcfunction", mcf(
        "scoreboard players enable @s family.talk",
        f"execute if score #game {S} matches 1.. run return run " + dialog(
            "coach", "A game is on right now! Jump in and bop the pink clams!", exit_label="OK!"),
        "execute unless score @s family.bop_best matches 0.. run return run " + dialog("coach", intro, play, "Not now"),
        "execute store result storage family:houses me.b int 1 run scoreboard players get @s family.bop_best",
        f"function {b}/menu_best with storage family:houses me"))
    put(f"{bf}/menu_best.mcfunction", "$" + dialog(
        "coach", "Back for more bopping? Your best is $(b) bops. Can you beat it?", play, "Not now") + "\n")
    put(f"{bf}/rules.mcfunction", mcf(dialog(
        "coach", "1. Tap Play Clam Bop! and wait for GO.\n"
                 "2. Clams in the floor pop open: they glow pink.\n"
                 "3. Tap an open clam before it shuts (on PC, click it): that's a bop!\n"
                 "4. You have 30 seconds, and it gets faster at the end.\n\n"
                 f"Everyone in the coconut can play at once. {PRIZE_AT} bops win {PRIZE} Sand Dollars (once a day). "
                 "Your best goes on the TOP BOPPERS board.", exit_label="Got it!")))
    put(f"{bf}/start.mcfunction", mcf(                          # button: as the kid (position not set)
        f"execute if score #game {S} matches 1.. run return fail",
        "execute at @s unless entity @e[type=minecraft:villager,tag=family.folk.coach,distance=..12] run return fail",
        f"scoreboard players set #game {S} {PLAY + COUNT + 1}",
        f"execute {inside} run title @s times 0 20 5",
        f"execute {inside} run title @s subtitle " + snbt({"text": "Get ready to bop!", "color": "light_purple"}),
        say("coach", "Here we go, {kid}! Bop the clams when they glow pink!")))
    put(f"{bf}/reset_scores.mcfunction", mcf(                   # admin: clear the bests and the board
        "scoreboard players reset * family.bop_best", "data remove storage family:houses board", f"function {b}/leaderboard/show"))

    # --- Professor Periwinkle (townsfolk tap/professor), and his buttons. Sounds need `at @s` (buttons have no position).
    p, pf = f"{fn}/prof", f"{f}/prof"
    enable = "scoreboard players enable @s family.talk"
    put(f"{pf}/menu.mcfunction", mcf(enable, dialog(
        "professor", "Oh, hello! I'm Professor Periwinkle. I study everything under the sea, and I collect jokes! "
                     "What would you like?",
        [("Tell me a joke!", BTN["prof/joke"]), ("A sea fact, please!", BTN["prof/fact"]),
         ("Riddle of the day", BTN["prof/riddle"])], "Bye!")))
    def next_one(kind, n):
        """No repeats: each kid steps through the list by a stride that shares no factor with its length, from a random
        start, so they hear all n before any comes round again (in a scrambled order)."""
        stride = next(k for k in range(n // 3, n) if math.gcd(k, n) == 1)
        return [f"execute unless score @s family.{kind} matches 0.. store result score @s family.{kind} run random value 0..{n - 1}",
                f"scoreboard players add @s family.{kind} {stride}", f"scoreboard players operation @s family.{kind} %= #{kind}s {S}"]
    put(f"{pf}/joke.mcfunction", mcf(
        enable, *next_one("joke", len(JOKES)),
        *[f"execute if score @s family.joke matches {i} run return run " + dialog("professor", q, [("Tell me!", BTN["prof/punchline"])])
          for i, (q, _) in enumerate(JOKES)]))
    put(f"{pf}/punchline.mcfunction", mcf(
        enable, "execute at @s run playsound minecraft:entity.villager.celebrate neutral @s ~ ~ ~",
        *[f"execute if score @s family.joke matches {i} run return run " + dialog("professor", ans, [("Another joke!", BTN["prof/joke"])])
          for i, (_, ans) in enumerate(JOKES)]))
    put(f"{pf}/fact.mcfunction", mcf(
        enable, *next_one("fact", len(FACTS)),
        *[f"execute if score @s family.fact matches {i} run return run " + dialog("professor", fact, [("Another fact!", BTN["prof/fact"])], "Thanks!")
          for i, fact in enumerate(FACTS)]))
    riddle_today = [*today, f"scoreboard players operation #r {S} = #day {S}", f"scoreboard players operation #r {S} %= #riddles {S}"]
    put(f"{pf}/riddle.mcfunction", mcf(
        enable, *riddle_today,
        f"execute if score @s family.riddle_day = #day {S} run return run " + dialog(
            "professor", "You already solved today's riddle. Well done! A new one comes tomorrow.", exit_label="OK!"),
        *[f"execute if score #r {S} matches {i} run return run " + dialog(
            "professor", f"Riddle of the day:\n\n{q}", list(zip(answers, ANSWER)), "Let me think")
          for i, (q, answers, _, _) in enumerate(RIDDLES)]))
    put(f"{pf}/answer.mcfunction", mcf(                          # buttons ANSWER: family.talk says which one
        enable, *riddle_today,
        f"execute if score @s family.riddle_day = #day {S} run return fail",
        *[f"execute if score #r {S} matches {i} if score @s family.talk matches {ANSWER[right]} run return run function {p}/right"
          for i, (_, _, right, _) in enumerate(RIDDLES)],
        *[f"execute if score #r {S} matches {i} run return run " + dialog(
            "professor", f"Not quite! Here's a hint: {hint}", [("Try again", BTN["prof/riddle"])], "Later")
          for i, (_, _, _, hint) in enumerate(RIDDLES)]))
    put(f"{pf}/right.mcfunction", mcf(
        f"scoreboard players operation @s family.riddle_day = #day {S}", coins(RIDDLE_PAY),
        "execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~",
        dialog("professor", f"That's right! Brilliant! Here are {RIDDLE_PAY} Sand Dollars. Come back tomorrow for a new riddle.",
               exit_label="Yay!")))

    # --- repairs, every 5 s while a kid stays near the coconut (after build_houses has run once)
    put(f"{f}/loop.mcfunction", mcf(
        f"schedule function {fn}/loop 1s replace",
        f"{sea}positioned {mid((COCO[0], 4, COCO[1]))} if entity @a[distance=..20] run scoreboard players add #near {S} 1",
        f"{sea}positioned {mid((COCO[0], 4, COCO[1]))} unless entity @a[distance=..20] run scoreboard players set #near {S} 0",
        f"execute if score #built {S} matches 1 if score #near {S} matches 5.. run function {fn}/repair"))
    put(f"{f}/repair.mcfunction", mcf(
        f"scoreboard players set #near {S} 0",
        *[f"execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam{i}] run {clam_box(i)}" for i in range(8)],
        f"execute unless entity @e[type=minecraft:text_display,tag=family.house.board] run function {b}/board",
        f"execute if score #game {S} matches 1.. run return 0",
        *[f"{sea}if block {a(*c)} {blk} run setblock {a(*c)} {CLAM_SHUT}" for c in CLAMS for blk in (opened, "minecraft:water")]))

    # --- build: load the three houses, wait for their entities, then everything (only ever into water)
    water, dry = club_room()
    assert all(blk.startswith(M + "light[") for blk in dry.values()), f"dry_fills only dries lights and chests: {dry}"
    rows = {}
    for (x, y, z) in water:
        rows.setdefault((y, z), []).append(x)
    drain = []
    for (y, z), xs in sorted(rows.items()):                    # one fill per straight run of cells
        xs.sort()
        start = xs[0]
        for c, n in zip(xs, xs[1:] + [None]):
            if n != c + 1:
                drain.append(f"{at}fill ~{start} ~{y} ~{z} ~{c} ~{y} ~{z} minecraft:air replace minecraft:water")
                start = n
    into_water = lambda cells: [f"{sea}if block {a(*q)} minecraft:water run setblock {a(*q)} {blk}" for q, blk in cells]
    seal = sorted(club_seal().items(), key=lambda qb: (qb[0][1], qb[0][0]))    # door: lower half before upper
    door = (MELON[0], 1, MELON[1])
    put(f"{f}/club.mcfunction", mcf(                            # the sea held back first, then drained in one tick
        *into_water(seal),
        f"{sea}unless block {a(*door)} minecraft:spruce_door run return fail",
        *drain, *tf.dry_fills(at, water | set(dry)),
        *into_water(sorted(club_roof().items()))))
    pts = [(COCO[0] + 7, MELON[1] + 2), (MELON[0] - 10, COCO[1] - 8)]   # all three houses and their signs
    area = f"{hx + pts[1][0]} {hz + pts[1][1]} {hx + pts[0][0]} {hz + pts[0][1]}"
    put(f"{d}/function/undersea/build_houses.mcfunction", mcf(
        f"{sea}run forceload add {area}", f"schedule function {fn}/build 3s replace"))
    put(f"{f}/build.mcfunction", mcf(
        *[f"{sea}unless loaded {hx + x} {hy} {hz + z} run return run schedule function {fn}/build 2s replace" for x, z in pts],
        f"kill @e[type=minecraft:villager,tag=family.folk.professor]", f"kill @e[type=minecraft:villager,tag=family.folk.coach]",
        f"kill @e[type=minecraft:interaction,tag=family.tap.professor]", f"kill @e[type=minecraft:interaction,tag=family.tap.coach]",
        "kill @e[tag=family.house]",
        *[at + tf.villager(who) for who in ("professor", "coach")], *[at + tf.summon_box(who) for who in ("professor", "coach")],
        *into_water([(c, CLAM_SHUT) for c in CLAMS]), *[f"{sea}if block {a(*c)} {opened} run setblock {a(*c)} {CLAM_SHUT}" for c in CLAMS],
        *[clam_box(i) for i in range(8)], f"function {b}/board",
        *into_water([(q, M + "bookshelf") for q in SHELVES] + [(LECTERN, M + "lectern[facing=south]")]),
        *into_water(sorted(SIGNS.items())),
        f"function {fn}/club",
        f"scoreboard players set #built {S} 1",
        f"{sea}run forceload remove {area}"))

# ---------------------------------------------------------------- preview
def preview():
    from PIL import Image, ImageDraw, ImageFont
    font, big = ImageFont.load_default(size=15), ImageFont.load_default(size=20)
    water, dry = club_room()
    k, pad, shots = 30, 8, []
    marks = {**{c: ("clam", (227, 221, 196)) for c in CLAMS}, **{q: ("shelf", (138, 106, 62)) for q in SHELVES},
             LECTERN: ("lectern", (164, 128, 75)), **{q: ("sign", (184, 148, 90)) for q in SIGNS},
             **{q: ("seal", (200, 49, 45)) for q in club_seal()}, **{q: ("pearl", (245, 200, 60)) for q in tf.PEARLS}}
    marks[(MELON[0], 1, MELON[1])] = ("door", (107, 78, 46))
    for title, (cx, cz), y, r, folk in (("Seashell: Professor Periwinkle (floor)", SHELL, 1, 8, "professor"),
                                         ("Coconut: Clam Bop (bowl floor, y 2)", COCO, 2, 8, "coach"),
                                         ("Watermelon: the clubhouse (floor)", MELON, 1, 9, None)):
        n = 2 * r + 1
        img = Image.new("RGB", (n * k + 2 * pad, n * k + 2 * pad + 34), (24, 70, 84)); dr = ImageDraw.Draw(img)
        dr.text((pad, 6), title, fill=(255, 255, 255), font=big)
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                X, Z = pad + (x - cx + r) * k, 34 + pad + (z - cz + r) * k
                cell = None
                for yy in (y, y + 1, 5):                           # shelves 2 high; signs hang at y 5
                    q = (x, yy, z)
                    if q in marks and (yy == y or marks[q][0] in ("shelf", "sign")):
                        cell = marks[q][1]; break
                if cell is None:
                    q = (x, y, z)
                    cell = (150, 205, 225) if q in water else town.colour(T.v[q]) if q in T.v and town.colour(T.v[q]) else \
                        (60, 120, 150) if (x, y - 1, z) in T.v else None
                if cell:
                    dr.rectangle([X, Z, X + k - 2, Z + k - 2], fill=cell)
        if folk:
            fx, _, fz = tf.FOLK[folk]["spot"]
            X, Z = pad + (fx - cx + r + 0.5) * k, 34 + pad + (fz - cz + r + 0.5) * k
            dr.ellipse([X - 11, Z - 11, X + 11, Z + 11], fill=(255, 60, 60), outline=(255, 255, 255), width=3)
        shots.append(img)
    legend = ("Top-down, north up; doors face south (bottom). Light blue = drained (clubhouse); pale = clams; gold = golden "
              "pearl; red dot = townsperson; brown = bookshelves, lectern; tan = signs; dark red + wood = door.")
    W = sum(i.width for i in shots) + 16 * (len(shots) + 1)
    sheet = Image.new("RGB", (W, max(i.height for i in shots) + 60), (16, 40, 58)); sd = ImageDraw.Draw(sheet)
    x = 16
    for im in shots:
        sheet.paste(im, (x, 16)); x += im.width + 16
    sd.text((16, sheet.height - 30), legend, fill=(255, 255, 255), font=font)
    sheet.save(f"{town.HERE}/previews/houses.png")

if __name__ == "__main__":
    check()
    w, dr = club_room()
    print("clams", CLAMS, "| signs", list(SIGNS), "| clubhouse: drain", len(w), "dry", dr, "roof", len(club_roof()))
    preview()
