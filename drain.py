"""Drain command for underwater rooms. An op stands in the water inside a finished room and runs
/function family:drain_here (from the console: execute as NAME at NAME run function family:drain_here).
It spreads out through the water from there, and through anything else holding water (waterlogged chests,
stairs, slabs, glass panes, kelp, seagrass). If that reaches more than R blocks away, the room has a gap to the sea;
more than CAP blocks, it's too big. Either way everything is put back and nothing changes.
Otherwise the water becomes air, and a sponge is set and removed next to each waterlogged block, which dries it.
All in one tick, so the sea never flows in halfway.
Its own datapack beside the main one: python3 drain.py -> dist/family-drain.zip (goes in world/datapacks/)."""
import json, os, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
R, CAP = 15, 1500                      # keeps the undo fill (31^3) under max_block_modifications 32768, and the
DATA_FORMAT = 121                      # flood fill (about 30 commands a cell) under max_command_sequence_length 65536
FN = "family:drain"
SCORE = "family.drain"
MARK = "minecraft:marker"
SIDES = ("~1 ~ ~", "~-1 ~ ~", "~ ~1 ~", "~ ~-1 ~", "~ ~ ~1", "~ ~ ~-1")
BOX = f"~-{R} ~-{R} ~-{R} ~{R} ~{R} ~{R}"

def mcf(*lines):
    return "\n".join(lines) + "\n"

def tell(text, colour, *extra):
    return "tellraw @s " + json.dumps([{"text": text, "color": colour}, *extra])

def files():
    f = "data/family/function"
    return {
        "pack.mcmeta": json.dumps({"pack": {"description": "Family server: drain command for underwater rooms",
                                            "min_format": DATA_FORMAT, "max_format": 999}}, indent=2) + "\n",
        # anything whose fluid is water: water itself, waterlogged blocks, kelp, seagrass, bubble columns
        "data/family/predicate/drain/wet.json": json.dumps(
            {"type": "minecraft:location_check", "predicate": {"fluid": {"fluids": "#minecraft:water"}}}, indent=2) + "\n",
        f"{f}/drain_here.mcfunction": mcf(
            "execute unless entity @s[type=minecraft:player] run return fail",
            *[f"execute at @s align xyz positioned ~0.5 ~{y} ~0.5 if block ~ ~ ~ minecraft:water run return run function {FN}/start"
              for y in (0.5, 1.5)],                                     # feet, then head
            tell("Stand in the water inside the room you want to drain, then run this again.", "yellow")),
        f"{f}/drain/start.mcfunction": mcf(
            f"scoreboard objectives add {SCORE} dummy",
            f"scoreboard players set #cells {SCORE} 0",
            f"scoreboard players set #leak {SCORE} 0",
            f"kill @e[type={MARK},tag=family.drain]",
            f'summon {MARK} ~ ~ ~ {{Tags:["family.drain","family.drain_o"]}}',
            f"schedule function {FN}/rescue 1t replace",                # puts things back if this run gets cut off
            f"function {FN}/visit",
            f"execute if score #leak {SCORE} matches 0 run function {FN}/commit",
            f"execute unless score #leak {SCORE} matches 0 run function {FN}/undo",
            f"execute if score #leak {SCORE} matches 0 run " + tell(
                "Drained ", "green", {"score": {"name": "#cells", "objective": SCORE}, "color": "green"},
                {"text": " blocks of water.", "color": "green"}),
            f"execute if score #leak {SCORE} matches 1 run " + tell(
                "Can't drain: this water reaches the sea, so there's a gap somewhere. Nothing changed. Look for a missing "
                "block, or a glass pane, fence, stairs, slab or trapdoor in the outer walls, roof or floor.", "red"),
            f"execute if score #leak {SCORE} matches 2 run " + tell(
                f"Can't drain: this room holds more than {CAP} blocks of water, too much for one go. Nothing changed.", "red"),
            f"kill @e[type={MARK},tag=family.drain]"),
        # one cell: water becomes a structure void (marks it visited); other wet blocks get a marker entity
        f"{f}/drain/visit.mcfunction": mcf(
            f"execute unless entity @e[type={MARK},tag=family.drain_o,distance=..{R}] run return run scoreboard players set #leak {SCORE} 1",
            f"scoreboard players add #cells {SCORE} 1",
            f"execute if score #cells {SCORE} matches {CAP + 1}.. run return run scoreboard players set #leak {SCORE} 2",
            "execute if block ~ ~ ~ minecraft:water run setblock ~ ~ ~ minecraft:structure_void",
            f'execute unless block ~ ~ ~ minecraft:structure_void run summon {MARK} ~ ~ ~ {{Tags:["family.drain","family.drain_wet"]}}',
            *[f"execute if score #leak {SCORE} matches 0 positioned {s} run function {FN}/try" for s in SIDES]),
        f"{f}/drain/try.mcfunction": mcf(
            f"execute if block ~ ~ ~ minecraft:water run return run function {FN}/visit",
            f"execute if predicate family:drain/wet unless entity @e[type={MARK},tag=family.drain_wet,distance=..0.5] "
            f"run function {FN}/visit"),
        f"{f}/drain/commit.mcfunction": mcf(
            f"fill {BOX} minecraft:air replace minecraft:structure_void",
            f"execute as @e[type={MARK},tag=family.drain_wet] at @s run function {FN}/dry"),
        f"{f}/drain/undo.mcfunction": mcf(f"fill {BOX} minecraft:water replace minecraft:structure_void"),
        # a sponge in a drained cell next to the wet block soaks it up (and any wet blocks touching it)
        f"{f}/drain/dry.mcfunction": mcf(
            *[f"execute positioned {s} if block ~ ~ ~ minecraft:air run return run function {FN}/sponge" for s in SIDES]),
        f"{f}/drain/sponge.mcfunction": mcf("setblock ~ ~ ~ minecraft:sponge", "setblock ~ ~ ~ minecraft:air"),
        f"{f}/drain/rescue.mcfunction": mcf(
            f"execute as @e[type={MARK},tag=family.drain_o] at @s run function {FN}/undo",
            f"kill @e[type={MARK},tag=family.drain]"),
    }

def build(dest=os.path.join(HERE, "dist", "family-drain.zip")):
    """Deterministic zip (fixed timestamps, sorted), like build.py's."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in sorted(files().items()):
            z.writestr(zipfile.ZipInfo(path, date_time=(2026, 1, 1, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)
    return dest

if __name__ == "__main__":
    print(build())
