"""The Undersea: an ocean-only dimension, whirlpool portals, the Bubble Shell and the sea costumes.
build.py calls java(), bedrock(), datapack() and mappings(); art lives in undersea_art.py.

Bedrock players (via Geyser) only see vanilla biomes, so the Undersea uses vanilla ocean biomes
(warm, lukewarm, ocean, lush caves) and gets its look from terrain + a raised sea level."""
import json, os
from undersea_art import bubble_shell, costume_layers, costume_icon

HERE = os.path.dirname(os.path.abspath(__file__))
SEA_LEVEL = 100          # vanilla is 63: land up to y=100 is flooded, hills above it become islands
HUB_X, HUB_Y, HUB_Z = -168, 38, -144   # hub platform on the seabed of a warm (coral) ocean, measured
                                       # on the server: arriving mid-water showed nothing but fog
DIM = "family:undersea"
BEAM_GLASS = "minecraft:light_blue_stained_glass"   # tints the beacon beams that mark both portal ends

def disc_rows(r, hole=0):
    """(dz, x1, x2) row segments of a disc of radius r around 0,0, minus the square |dx|,|dz| <= hole."""
    rows = []
    for dz in range(-int(r), int(r) + 1):
        w = int((r * r - dz * dz) ** 0.5)
        rows += [(dz, -w, -hole - 1), (dz, hole + 1, w)] if hole and abs(dz) <= hole else [(dz, -w, w)]
    return [row for row in rows if row[1] <= row[2]]

def disc_fill(prefix, r, hole, y1, y2, block, replace=""):
    """fill commands for a disc (relative to the executing position), one per row segment."""
    return [f"{prefix}fill ~{x1} ~{y1} ~{dz} ~{x2} ~{y2} ~{dz} {block}{' replace ' + replace if replace else ''}"
            for dz, x1, x2 in disc_rows(r, hole)]

def beacon(prefix, dx, dy, dz):
    """A beacon on a hidden 3x3 iron base with blue glass on top (it gives no effect unless activated)."""
    return [f"{prefix}fill ~{dx - 1} ~{dy - 1} ~{dz - 1} ~{dx + 1} ~{dy - 1} ~{dz + 1} minecraft:iron_block",
            f"{prefix}setblock ~{dx} ~{dy} ~{dz} minecraft:beacon",
            f"{prefix}setblock ~{dx} ~{dy + 1} ~{dz} {BEAM_GLASS}"]

SHELL = {
    "minecraft:item_model": "family:bubble_shell",
    "minecraft:custom_name": {"text": "Bubble Shell", "color": "#7FE3F0", "italic": False},
    "minecraft:lore": [{"text": "Hold to swim to the Undersea and back", "color": "gray", "italic": False}],
    "minecraft:consumable": {"consume_seconds": 1.0, "animation": "toot_horn", "has_consume_particles": False,
                             "sound": "minecraft:block.bubble_column.upwards_inside"},
    "minecraft:use_cooldown": {"seconds": 3.0, "cooldown_group": "family:bubble_shell"},
    "minecraft:max_stack_size": 1,
    "minecraft:custom_data": {"family_shell": True}}

# Costumes are diamond armour underneath (same protection, unbreakable), crafted from the diamond piece
# + two dyes. costume -> (name colour, (dye, dye), [(piece, item name)] for head, chest, legs, feet)
COSTUMES = {
    "shark": ("#9CC3DA", ("gray_dye", "white_dye"),
              [("hood", "Shark Hood"), ("suit", "Shark Suit"), ("pants", "Shark Pants"), ("flippers", "Shark Flippers")]),
    "diver": ("#E0B25A", ("orange_dye", "brown_dye"),
              [("helmet", "Diver Helmet"), ("suit", "Diver Suit"), ("pants", "Diver Pants"), ("boots", "Diver Boots")]),
    "angler": ("#B9A8E8", ("black_dye", "yellow_dye"),
               [("hood", "Angler Hood"), ("suit", "Angler Suit"), ("pants", "Angler Pants"), ("fins", "Angler Fins")]),
    "turtle": ("#8CCB72", ("green_dye", "lime_dye"),
               [("hood", "Turtle Hood"), ("shell", "Turtle Shell"), ("pants", "Turtle Pants"), ("flippers", "Turtle Flippers")]),
    "coral": ("#F59CC8", ("pink_dye", "blue_dye"),
              [("helm", "Coral Helm"), ("breastplate", "Coral Breastplate"), ("greaves", "Coral Greaves"), ("boots", "Coral Boots")]),
    "axolotl": ("#F7B6CF", ("pink_dye", "magenta_dye"),
                [("hood", "Axolotl Hood"), ("suit", "Axolotl Suit"), ("pants", "Axolotl Pants"), ("feet", "Axolotl Feet")]),
    "sponge": ("#F4E888", ("yellow_dye", "white_dye"),
               [("hood", "Sponge Hood"), ("top", "Sponge Top"), ("legs", "Sponge Legs"), ("feet", "Sponge Feet")]),
    "spongebuddy": ("#FFE14D", ("yellow_dye", "brown_dye"),
                  [("hood", "Sponge Buddy Hood"), ("shirt", "Sponge Buddy Shirt"), ("shorts", "Sponge Buddy Shorts"), ("shoes", "Sponge Buddy Shoes")]),
}
# slot -> (diamond base item, Bedrock armour geometry, Bedrock layer-visibility variable)
SLOTS = {"head": ("diamond_helmet", "helmet", "helmet"), "chest": ("diamond_chestplate", "chestplate", "chest"),
         "legs": ("diamond_leggings", "leggings", "leg"), "feet": ("diamond_boots", "boots", "boot")}

def pieces():
    """(costume, slot, piece, item name) for every costume piece."""
    for costume, (_, _, names) in COSTUMES.items():
        for slot, (piece, name) in zip(SLOTS, names):
            yield costume, slot, piece, name

def costume_components(costume, slot, piece, name):
    return {"minecraft:item_model": f"family:{costume}_{piece}",
            "minecraft:custom_name": {"text": name, "color": COSTUMES[costume][0], "italic": False},
            "minecraft:equippable": {"slot": slot, "asset_id": f"family:{costume}",
                                     "equip_sound": "minecraft:item.armor.equip_diamond"},
            "minecraft:unbreakable": {},
            "minecraft:custom_data": {"family_costume": costume}}

# ------------------------------------------------------------------ Java resource pack
def java(a, put):
    flat = lambda n: {"parent": "minecraft:item/generated", "textures": {"layer0": f"family:item/{n}"}}
    icons = [("bubble_shell", bubble_shell())] + [(f"{c}_{p}", costume_icon(c, s)) for c, s, p, _ in pieces()]
    for n, img in icons:
        put(f"{a}/family/items/{n}.json", {"model": {"type": "minecraft:model", "model": f"family:item/{n}"}})
        put(f"{a}/family/models/item/{n}.json", flat(n))
        img.save(f"{a}/family/textures/item/{n}.png")
    for c in COSTUMES:
        put(f"{a}/family/equipment/{c}.json", {"layers": {"humanoid": [{"texture": f"family:{c}"}],
                                                          "humanoid_leggings": [{"texture": f"family:{c}"}]}})
        for layer, img in zip(("humanoid", "humanoid_leggings"), costume_layers(c)):
            os.makedirs(f"{a}/family/textures/entity/equipment/{layer}", exist_ok=True)
            img.save(f"{a}/family/textures/entity/equipment/{layer}/{c}.png")

# ------------------------------------------------------------------ Bedrock pack
def bedrock(b, put):
    """Writes armour textures + attachables; returns item icons for item_texture.json."""
    os.makedirs(f"{b}/textures/models/armor", exist_ok=True)
    for c in COSTUMES:
        for i, img in enumerate(costume_layers(c), 1):
            img.save(f"{b}/textures/models/armor/family_{c}_{i}.png")
    for c, slot, piece, _ in pieces():           # same setup as Mojang's diamond armour attachables
        _, geo, visible = SLOTS[slot]
        put(f"{b}/attachables/{c}_{piece}.json", {"format_version": "1.8.0", "minecraft:attachable": {
            "description": {
                "identifier": f"family:{c}_{piece}",
                "materials": {"default": "armor", "enchanted": "armor_enchanted"},
                "textures": {"default": f"textures/models/armor/family_{c}_{2 if slot == 'legs' else 1}",
                             "enchanted": "textures/misc/enchanted_actor_glint"},
                "geometry": {"default": f"geometry.humanoid.armor.{geo}"},
                "scripts": {"parent_setup": f"variable.{visible}_layer_visible = 0.0;"},
                "render_controllers": ["controller.render.armor"]}}})
    return {"family_bubble_shell": bubble_shell(),
            **{f"family_{c}_{p}": costume_icon(c, s) for c, s, p, _ in pieces()}}

def mappings():
    """Geyser custom item definitions (format 2). Protection and the wearable slot come from the
    diamond base items; the shell is a 1-second 'use' like food."""
    out = {"minecraft:nautilus_shell": [{
        "bedrock_identifier": "family:bubble_shell", "model": "family:bubble_shell",
        "bedrock_options": {"icons": {"default": "family_bubble_shell"}},
        # Geyser has no toot_horn on Bedrock (rejects the whole item); spyglass = held up to the face
        "components": {"minecraft:consumable": {"consume_seconds": 1.0, "animation": "spyglass"},
                       "minecraft:use_cooldown": {"seconds": 3.0, "cooldown_group": "family:bubble_shell"},
                       "minecraft:max_stack_size": 1}}]}
    for c, slot, piece, _ in pieces():
        out.setdefault(f"minecraft:{SLOTS[slot][0]}", []).append({
            "bedrock_identifier": f"family:{c}_{piece}", "model": f"family:{c}_{piece}",
            "bedrock_options": {"icons": {"default": f"family_{c}_{piece}"}}})
    return out

def gives(give_string):
    return {"bubble_shell": give_string("minecraft:nautilus_shell", SHELL),
            **{f"{c}_{p}": give_string(f"minecraft:{SLOTS[s][0]}", costume_components(c, s, p, n))
               for c, s, p, n in pieces()}}

# ------------------------------------------------------------------ Datapack
def mcf(*lines):
    return "\n".join(lines) + "\n"

def datapack(data, put, give_string):
    d = f"{data}/data/family"
    shell = give_string("minecraft:nautilus_shell", SHELL)
    in_sea = f"execute in {DIM} run"

    # --- the dimension: vanilla overworld terrain with a raised sea level, ocean biomes only
    with open(f"{HERE}/vanilla/noise_settings_overworld.json") as fh:
        noise = json.load(fh)                       # vanilla 26.3 (misode/mcmeta tag 26.3-data)
    noise["sea_level"] = SEA_LEVEL
    put(f"{d}/worldgen/noise_settings/undersea.json", noise)
    full = [-1.0, 1.0]
    def biome(name, temperature, depth):
        return {"biome": f"minecraft:{name}", "parameters": {
            "temperature": temperature, "humidity": full, "continentalness": [-1.2, 1.0], "erosion": full,
            "weirdness": full, "depth": depth, "offset": 0.0}}
    # No deep ocean biomes: they carry ocean monuments (guardians). Surface biomes are listed at
    # depth 0 and 1 like vanilla; lush caves fill the underground.
    surface = [("ocean", [-1.0, -0.15]), ("lukewarm_ocean", [-0.15, 0.2]), ("warm_ocean", [0.2, 1.0])]
    put(f"{d}/dimension/undersea.json", {"type": "minecraft:overworld", "generator": {
        "type": "minecraft:noise", "settings": DIM, "biome_source": {"type": "minecraft:multi_noise", "biomes":
            [biome(n, t, depth) for n, t in surface for depth in (0.0, 1.0)]
            + [biome("lush_caves", full, [0.2, 0.9])]}}})

    put(f"{data}/data/minecraft/tags/function/load.json", {"values": ["family:undersea/load"]})
    put(f"{data}/data/minecraft/tags/function/tick.json", {"values": ["family:undersea/tick"]})
    f = f"{d}/function/undersea"
    put(f"{f}/load.mcfunction", mcf(
        *[f"scoreboard objectives add family.{s} dummy" for s in ("rx", "ry", "rz", "ret")],
        "schedule function family:undersea/effects 2s replace"))
    # Breathing + underwater sight for everyone in the Undersea (conduit power covers both).
    put(f"{f}/effects.mcfunction", mcf(
        f"execute as @a at @s if dimension {DIM} run effect give @s minecraft:conduit_power 20 0 true",
        "schedule function family:undersea/effects 2s replace"))

    # --- portals: markers (server-only entities, invisible to all clients) mark each whirlpool.
    # A player is sent once per visit: the in_portal tag stops repeats until they leave it.
    put(f"{f}/tick.mcfunction", mcf(
        "execute as @e[type=minecraft:marker,tag=family.portal] at @s run tag @a[distance=..1.5] add family.near_portal",
        "execute as @a[tag=family.near_portal,tag=!family.in_portal] at @s run function family:undersea/portal",
        "tag @a[tag=family.near_portal] add family.in_portal",
        "tag @a[tag=!family.near_portal] remove family.in_portal",
        "tag @a remove family.near_portal"))
    put(f"{f}/portal.mcfunction", mcf(
        "execute if entity @e[type=minecraft:marker,tag=family.portal_down,distance=..2] run return run function family:undersea/portal_down",
        "execute if entity @e[type=minecraft:marker,tag=family.portal_up,distance=..2] run function family:undersea/go_up"))
    put(f"{f}/portal_down.mcfunction", mcf(       # step out onto the rim first: that's where they come back to
        "execute at @e[type=minecraft:marker,tag=family.portal_down,distance=..2,sort=nearest,limit=1] run tp @s ~ ~1.5 ~2",
        "function family:undersea/go_down"))
    put(f"{f}/go_down.mcfunction", mcf(
        *[f"execute store result score @s family.r{a} run data get entity @s Pos[{i}] 100" for i, a in enumerate("xyz")],
        "scoreboard players set @s family.ret 1",
        "effect give @s minecraft:conduit_power 20 0 true",
        "function family:undersea/to_hub with storage family:undersea hub",
        "execute at @s run playsound minecraft:block.bubble_column.whirlpool_inside player @s ~ ~ ~",
        'title @s actionbar {"text": "Welcome to the Undersea!", "color": "aqua"}'))
    put(f"{f}/to_hub.mcfunction", f"$execute in {DIM} run tp @s $(x) $(y) $(z)\n")
    put(f"{f}/go_up.mcfunction", mcf(
        "execute unless score @s family.ret matches 1 run return run function family:undersea/to_home",
        *[f"execute store result storage family:undersea ret.{a} double 0.01 run scoreboard players get @s family.r{a}" for a in "xyz"],
        "function family:undersea/to_overworld with storage family:undersea ret",
        "execute at @s run playsound minecraft:block.bubble_column.upwards_inside player @s ~ ~ ~"))
    put(f"{f}/to_overworld.mcfunction", "$execute in minecraft:overworld run tp @s $(x) $(y) $(z)\n")
    put(f"{f}/to_home.mcfunction", mcf(
        "execute if data storage family:undersea home run return run function family:undersea/to_overworld with storage family:undersea home",
        'tellraw @s {"text": "The way home is lost. Ask a grown-up for help!", "color": "yellow"}'))

    # Hub: a lit platform on the seabed with an upward bubble column (soul sand) as the way home.
    # Run ONCE by an admin: family:undersea/build_hub (it loads the area first).
    # Gamerules are per-dimension on this server and a new dimension starts with defaults:
    # keep_inventory as everywhere else; no monsters (drowned filled all the deep, dark water).
    hx, y, hz = HUB_X, HUB_Y, HUB_Z
    area = f"{hx - 16} {hz - 16} {hx + 15} {hz + 15}"
    put(f"{f}/build_hub.mcfunction", mcf(
        f"{in_sea} gamerule keep_inventory true",
        f"{in_sea} gamerule spawn_monsters false",
        f"{in_sea} forceload add {area}",
        "schedule function family:undersea/build_hub_2 3s replace"))
    at_hub = f"execute in {DIM} positioned {hx} {y} {hz}"
    pillars = [(px, pz) for px in (-2, 2) for pz in (-2, 2)]
    lanterns = [(lx, lz) for lx in (-5, 0, 5) for lz in (-5, 0, 5) if (lx, lz) != (0, 0)]
    put(f"{f}/build_hub_2.mcfunction", mcf(
        f"{at_hub} unless loaded ~ ~ ~ run return run schedule function family:undersea/build_hub_2 2s replace",
        f"{at_hub} run fill ~-6 ~1 ~-6 ~6 ~8 ~6 minecraft:water",
        f"{at_hub} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 minecraft:prismarine",
        f"{at_hub} run fill ~-5 ~ ~-5 ~5 ~ ~5 minecraft:prismarine_bricks",
        *[f"{at_hub} run setblock ~{lx} ~ ~{lz} minecraft:sea_lantern" for lx, lz in lanterns],
        f"{at_hub} run setblock ~ ~ ~ minecraft:soul_sand",
        *[f"{at_hub} run fill ~{px} ~1 ~{pz} ~{px} ~3 ~{pz} minecraft:dark_prismarine" for px, pz in pillars],
        *[f"{at_hub} run setblock ~{px} ~4 ~{pz} minecraft:sea_lantern" for px, pz in pillars],
        # flat sand ring out to 10 blocks so the hub stands out from the reef; beacon beam on one corner
        *disc_fill(f"{at_hub} run ", 10.5, 6, -4, -1, "minecraft:sandstone", "#minecraft:replaceable"),
        *disc_fill(f"{at_hub} run ", 10.5, 6, 0, 0, "minecraft:sand"),
        *disc_fill(f"{at_hub} run ", 10.5, 6, 1, 12, "minecraft:water"),
        *beacon(f"{at_hub} run ", 5, 0, 5),
        f"{in_sea} kill @e[type=minecraft:marker,tag=family.portal_up,distance=0..]",
        f'{at_hub} run summon minecraft:marker ~0.5 ~1.5 ~0.5 {{Tags: ["family.portal", "family.portal_up"]}}',
        f"data modify storage family:undersea hub set value {{x: {hx + 0.5}d, y: {y + 1}.0d, z: {hz + 3.5}d}}",
        f"{in_sea} forceload remove {area}"))

    # Overworld whirlpool, built by an admin where they stand: /function family:portal_here
    # (replaces a 5x5x3 area under their feet). /function family:portal_remove clears the trigger.
    put(f"{d}/function/portal_here.mcfunction",
        "execute align xyz positioned ~0.5 ~ ~0.5 run function family:undersea/place_portal\n")
    put(f"{f}/place_portal.mcfunction", mcf(
        "fill ~-2 ~-3 ~-2 ~2 ~-1 ~2 minecraft:prismarine_bricks",
        "fill ~-1 ~-2 ~-1 ~1 ~-1 ~1 minecraft:water",
        "setblock ~ ~-3 ~ minecraft:soul_sand",
        *[f"setblock ~{cx} ~-1 ~{cz} minecraft:sea_lantern" for cx in (-2, 2) for cz in (-2, 2)],
        'summon minecraft:marker ~ ~-1.5 ~ {Tags: ["family.portal", "family.portal_down"]}',
        'summon minecraft:marker ~ ~ ~2 {Tags: ["family.tmp"]}',
        *[f"execute store result storage family:undersea home.{a} double 0.01 run data get entity @n[type=minecraft:marker,tag=family.tmp] Pos[{i}] 100"
          for i, a in enumerate("xyz")],
        "kill @e[type=minecraft:marker,tag=family.tmp]",
        "tp @s ~ ~ ~2",                               # onto the rim, not into the pool just made
        'tellraw @s {"text": "Undersea whirlpool built. Jump in!", "color": "aqua"}'))
    put(f"{d}/function/portal_remove.mcfunction", mcf(
        "kill @e[type=minecraft:marker,tag=family.portal,distance=..4]",
        'tellraw @s {"text": "Whirlpool trigger removed (the blocks stay).", "color": "yellow"}'))
    # Admin, next to an overworld whirlpool: /function family:portal_plaza levels a grass plaza
    # (radius 8) at the rim's height and adds a beacon beam 6 blocks from the pool's centre.
    put(f"{d}/function/portal_plaza.mcfunction", mcf(
        "execute unless entity @e[type=minecraft:marker,tag=family.portal_down,distance=..8] run return run "
        'tellraw @s {"text": "Stand next to a whirlpool first.", "color": "yellow"}',
        "execute at @n[type=minecraft:marker,tag=family.portal_down,distance=..8] positioned ~ ~1.5 ~ align xyz "
        "run function family:undersea/plaza",
        'tellraw @s {"text": "Plaza and beacon built around the whirlpool.", "color": "aqua"}'))
    put(f"{f}/plaza.mcfunction", mcf(        # at the pool centre, standing height (rim top is ~-1)
        *disc_fill("", 8.5, 0, 0, 12, "minecraft:air"),
        *disc_fill("", 8.5, 2, -11, -2, "minecraft:dirt", "#minecraft:replaceable"),
        *disc_fill("", 8.5, 2, -1, -1, "minecraft:grass_block"),
        *beacon("", 0, -1, 6)))

    # --- Bubble Shell: hold use for 1 s. The shell is used up like food, so it's handed back a tick
    # later (by then the hand slot is empty): into the empty hand, else the inventory.
    put(f"{d}/advancement/bubble_shell.json", {
        "criteria": {"used": {"trigger": "minecraft:consume_item", "conditions": {"item": {
            "items": "minecraft:nautilus_shell", "predicates": {"minecraft:custom_data": "{family_shell:1b}"}}}}},
        "rewards": {"function": "family:undersea/shell"}})
    put(f"{f}/shell.mcfunction", mcf(
        "advancement revoke @s only family:bubble_shell",
        "tag @s add family.shell_back",
        "schedule function family:undersea/shell_back 1t append",
        "execute if dimension minecraft:overworld run return run function family:undersea/go_down",
        f"execute if dimension {DIM} run return run function family:undersea/go_up",
        'tellraw @s {"text": "The Bubble Shell only works in the Overworld and the Undersea.", "color": "yellow"}'))
    put(f"{f}/shell_back.mcfunction", "execute as @a[tag=family.shell_back] run function family:undersea/give_shell\n")
    put(f"{f}/give_shell.mcfunction", mcf(
        "tag @s remove family.shell_back",
        f"execute unless items entity @s weapon.mainhand * run return run item replace entity @s weapon.mainhand with {shell}",
        f"execute unless items entity @s weapon.offhand * run return run item replace entity @s weapon.offhand with {shell}",
        f"give @s {shell}"))

    # --- recipes (+ recipe-book unlocks)
    put(f"{d}/recipe/bubble_shell.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": ["minecraft:kelp", "minecraft:sand", "minecraft:glass_bottle"],
        "result": {"id": "minecraft:nautilus_shell", "components": SHELL}})
    put(f"{d}/advancement/unlock_bubble_shell.json", {
        "criteria": {"has_kelp": {"trigger": "minecraft:inventory_changed",
                                  "conditions": {"items": [{"items": "minecraft:kelp"}]}}},
        "rewards": {"recipes": ["family:bubble_shell"]}})
    for c, slot, piece, name in pieces():          # diamond piece + the costume's two dyes
        base = SLOTS[slot][0]
        put(f"{d}/recipe/{c}_{piece}.json", {
            "type": "minecraft:crafting_shapeless", "category": "equipment",
            "ingredients": [f"minecraft:{base}", *(f"minecraft:{dye}" for dye in COSTUMES[c][1])],
            "result": {"id": f"minecraft:{base}", "components": costume_components(c, slot, piece, name)}})
    put(f"{d}/advancement/unlock_costumes.json", {
        "criteria": {"has_diamond_armour": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [
            {"items": [f"minecraft:{b}" for b, *_ in SLOTS.values()]}]}}},
        "rewards": {"recipes": [f"family:{c}_{p}" for c, _, p, _ in pieces()]}})
