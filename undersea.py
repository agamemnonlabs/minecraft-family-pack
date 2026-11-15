"""The Undersea: an ocean-only dimension, whirlpool portals, the Bubble Shell and the Shark costume.
build.py calls java(), bedrock(), datapack() and mappings(); art lives in undersea_art.py.

Bedrock players (via Geyser) only see vanilla biomes, so the Undersea uses vanilla ocean biomes
(warm, lukewarm, ocean, lush caves) and gets its look from terrain + a raised sea level."""
import json, os
from undersea_art import bubble_shell, shark_layers, shark_icon

HERE = os.path.dirname(os.path.abspath(__file__))
SEA_LEVEL = 100          # vanilla is 63: land up to y=100 is flooded, hills above it become islands
HUB_Y = 86               # top of the hub platform at x=0 z=0, 14 blocks below the surface
DIM = "family:undersea"

SHELL = {
    "minecraft:item_model": "family:bubble_shell",
    "minecraft:custom_name": {"text": "Bubble Shell", "color": "#7FE3F0", "italic": False},
    "minecraft:lore": [{"text": "Hold to swim to the Undersea and back", "color": "gray", "italic": False}],
    "minecraft:consumable": {"consume_seconds": 1.0, "animation": "toot_horn", "has_consume_particles": False,
                             "sound": "minecraft:block.bubble_column.upwards_inside"},
    "minecraft:use_cooldown": {"seconds": 3.0, "cooldown_group": "family:bubble_shell"},
    "minecraft:max_stack_size": 1,
    "minecraft:custom_data": {"family_shell": True}}

# piece -> (diamond base item, equipment slot, Bedrock armour geometry/visibility name, name)
SHARK = {"hood": ("diamond_helmet", "head", "helmet", "Shark Hood"),
         "suit": ("diamond_chestplate", "chest", "chestplate", "Shark Suit"),
         "pants": ("diamond_leggings", "legs", "leggings", "Shark Pants"),
         "flippers": ("diamond_boots", "feet", "boots", "Shark Flippers")}
LAYER_VISIBLE = {"helmet": "helmet", "chestplate": "chest", "leggings": "leg", "boots": "boot"}

def shark_components(piece):
    _, slot, _, name = SHARK[piece]
    return {"minecraft:item_model": f"family:shark_{piece}",
            "minecraft:custom_name": {"text": name, "color": "#9CC3DA", "italic": False},
            "minecraft:equippable": {"slot": slot, "asset_id": "family:shark",
                                     "equip_sound": "minecraft:item.armor.equip_diamond"},
            "minecraft:unbreakable": {},
            "minecraft:custom_data": {"family_costume": "shark"}}

# ------------------------------------------------------------------ Java resource pack
def java(a, put):
    flat = lambda n: {"parent": "minecraft:item/generated", "textures": {"layer0": f"family:item/{n}"}}
    for n, img in [("bubble_shell", bubble_shell())] + [(f"shark_{p}", shark_icon(p)) for p in SHARK]:
        put(f"{a}/family/items/{n}.json", {"model": {"type": "minecraft:model", "model": f"family:item/{n}"}})
        put(f"{a}/family/models/item/{n}.json", flat(n))
        img.save(f"{a}/family/textures/item/{n}.png")
    put(f"{a}/family/equipment/shark.json", {"layers": {"humanoid": [{"texture": "family:shark"}],
                                                        "humanoid_leggings": [{"texture": "family:shark"}]}})
    layer1, layer2 = shark_layers()
    for layer, img in (("humanoid", layer1), ("humanoid_leggings", layer2)):
        os.makedirs(f"{a}/family/textures/entity/equipment/{layer}", exist_ok=True)
        img.save(f"{a}/family/textures/entity/equipment/{layer}/shark.png")

# ------------------------------------------------------------------ Bedrock pack
def bedrock(b, put):
    """Writes armour textures + attachables; returns item icons for item_texture.json."""
    os.makedirs(f"{b}/textures/models/armor", exist_ok=True)
    layer1, layer2 = shark_layers()
    layer1.save(f"{b}/textures/models/armor/family_shark_1.png")
    layer2.save(f"{b}/textures/models/armor/family_shark_2.png")
    for piece, (_, _, geo, _) in SHARK.items():   # same setup as Mojang's diamond armour attachables
        put(f"{b}/attachables/shark_{piece}.json", {"format_version": "1.8.0", "minecraft:attachable": {
            "description": {
                "identifier": f"family:shark_{piece}",
                "materials": {"default": "armor", "enchanted": "armor_enchanted"},
                "textures": {"default": f"textures/models/armor/family_shark_{2 if geo == 'leggings' else 1}",
                             "enchanted": "textures/misc/enchanted_actor_glint"},
                "geometry": {"default": f"geometry.humanoid.armor.{geo}"},
                "scripts": {"parent_setup": f"variable.{LAYER_VISIBLE[geo]}_layer_visible = 0.0;"},
                "render_controllers": ["controller.render.armor"]}}})
    return {"family_bubble_shell": bubble_shell(), **{f"family_shark_{p}": shark_icon(p) for p in SHARK}}

def mappings():
    """Geyser custom item definitions (format 2). Protection and the wearable slot come from the
    diamond base items; the shell is a 1-second 'use' like food."""
    out = {"minecraft:nautilus_shell": [{
        "bedrock_identifier": "family:bubble_shell", "model": "family:bubble_shell",
        "bedrock_options": {"icons": {"default": "family_bubble_shell"}},
        "components": {"minecraft:consumable": {"consume_seconds": 1.0, "animation": "toot_horn"},
                       "minecraft:use_cooldown": {"seconds": 3.0, "cooldown_group": "family:bubble_shell"},
                       "minecraft:max_stack_size": 1}}]}
    for piece, (base, *_rest) in SHARK.items():
        out[f"minecraft:{base}"] = [{"bedrock_identifier": f"family:shark_{piece}", "model": f"family:shark_{piece}",
                                     "bedrock_options": {"icons": {"default": f"family_shark_{piece}"}}}]
    return out

def gives(give_string):
    return {"bubble_shell": give_string("minecraft:nautilus_shell", SHELL),
            **{f"shark_{p}": give_string(f"minecraft:{SHARK[p][0]}", shark_components(p)) for p in SHARK}}

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
    # Run ONCE by an admin, after checking gamerules are per-dimension on this server
    # (otherwise these would switch monsters off in the Overworld too).
    put(f"{f}/gamerules.mcfunction", mcf(*[f"{in_sea} gamerule {r}" for r in (
        "keep_inventory true", "spawn_monsters false", "spawner_blocks_work false", "spawn_phantoms false",
        "spawn_patrols false", "spawn_wandering_traders false", "drowning_damage false")]))

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

    # Hub at x=0 z=0: a lit platform 14 blocks down with an upward bubble column (soul sand) as the
    # way home. Run ONCE by an admin: family:undersea/build_hub (it loads the area first).
    put(f"{f}/build_hub.mcfunction", mcf(
        f"{in_sea} forceload add -16 -16 15 15",
        "schedule function family:undersea/build_hub_2 3s replace"))
    y = HUB_Y
    pillars = [(px, pz) for px in (-2, 2) for pz in (-2, 2)]
    lanterns = [(lx, lz) for lx in (-5, 0, 5) for lz in (-5, 0, 5) if (lx, lz) != (0, 0)]
    put(f"{f}/build_hub_2.mcfunction", mcf(
        f"execute in {DIM} unless loaded 0 {y} 0 run return run schedule function family:undersea/build_hub_2 2s replace",
        f"{in_sea} fill -6 {y + 1} -6 6 {y + 8} 6 minecraft:water",
        f"{in_sea} fill -6 {y - 1} -6 6 {y - 1} 6 minecraft:prismarine",
        f"{in_sea} fill -5 {y} -5 5 {y} 5 minecraft:prismarine_bricks",
        *[f"{in_sea} setblock {lx} {y} {lz} minecraft:sea_lantern" for lx, lz in lanterns],
        f"{in_sea} setblock 0 {y} 0 minecraft:soul_sand",
        *[f"{in_sea} fill {px} {y + 1} {pz} {px} {y + 3} {pz} minecraft:dark_prismarine" for px, pz in pillars],
        *[f"{in_sea} setblock {px} {y + 4} {pz} minecraft:sea_lantern" for px, pz in pillars],
        f"{in_sea} kill @e[type=minecraft:marker,tag=family.portal_up,distance=0..]",
        f'{in_sea} summon minecraft:marker 0.5 {y + 1.5} 0.5 {{Tags: ["family.portal", "family.portal_up"]}}',
        f"data modify storage family:undersea hub set value {{x: 0.5d, y: {y + 1}.0d, z: 3.5d}}",
        f"{in_sea} forceload remove -16 -16 15 15"))

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
    for piece, (base, *_rest) in SHARK.items():      # diamond piece + grey dye + white dye
        put(f"{d}/recipe/shark_{piece}.json", {
            "type": "minecraft:crafting_shapeless", "category": "equipment",
            "ingredients": [f"minecraft:{base}", "minecraft:gray_dye", "minecraft:white_dye"],
            "result": {"id": f"minecraft:{base}", "components": shark_components(piece)}})
    put(f"{d}/advancement/unlock_shark.json", {
        "criteria": {"has_diamond_armour": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [
            {"items": [f"minecraft:{b}" for b, *_ in SHARK.values()]}]}}},
        "rewards": {"recipes": [f"family:shark_{p}" for p in SHARK]}})
