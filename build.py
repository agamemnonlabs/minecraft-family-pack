"""Builds the family pack from art.py / sounds.py.
  dist/family-pack-java.zip         -> PC players (server.properties resource-pack)
  dist/family-pack-bedrock.mcpack   -> iPads (Geyser packs/ folder)
  dist/family-datapack.zip          -> server world/datapacks: recipes, hit sound, blaster main-hand lock
  dist/lightsabers.json             -> /give item strings, used by ../give-lightsaber.sh
  dist/foam-blaster.item            -> /give item string, used by ../give-blaster.sh
  dist/undersea.json                -> /give item strings: Bubble Shell + Shark costume
  dist/katanas.json                 -> /give item strings for the elemental katanas, used by ../give-katana.sh
  geyser/custom_mappings/family.json -> Geyser: our items -> custom Bedrock items
Run: python3 build.py   (needs Pillow and oggenc)"""
from PIL import Image
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import (draw_blaster, saber_hilt, saber_blade, draw_glow_saber, mix, hexc, blaster_3d_elements,
                 palette_texture, LIGHTSABERS)
from katana_art import bedrock_held_frames, FRAMES
from sounds import swing, VARIANTS
import undersea, town, wardrobe, katana, townsfolk, race, alive, houses

ROOT = os.path.dirname(os.path.abspath(__file__))
JAVA, BEDROCK, DATA, DIST = (os.path.join(ROOT, d) for d in ("java", "bedrock", "datapack", "dist"))
VERSION = [1, 0, 22]                      # bump for every change shipped to Bedrock (iPads cache by version)
JAVA_FORMAT, DATA_FORMAT = 97, 121        # resource / data pack formats of Minecraft 26.3
BEDROCK_HEADER_UUID = "6f1d2b8e-3c47-4a8e-9d2f-5b1a7c0e4f21"
BEDROCK_MODULE_UUID = "a3c9e5d7-81f2-4b6a-b0e4-2d8f6c1a9e53"
HIT_SOUND = "family.lightsaber_hit"
# vanilla item/generated + item/handheld display transforms (26.3), for the element-based blade model
HANDHELD_DISPLAY = {
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "scale": [1, 1, 1]},
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]}}       # lives in minecraft: so Geyser passes it to Bedrock unchanged

def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, (dict, list)):
        data = json.dumps(data, indent=2) + "\n"
    with open(path, "w") as f:
        f.write(data)

def saber_components(colour):
    blade = LIGHTSABERS[colour][0]
    return {"minecraft:item_model": f"family:lightsaber_{colour}",
            "minecraft:custom_name": {"text": f"{colour.title()} Lightsaber", "color": blade, "italic": False},
            "minecraft:custom_data": {"family_lightsaber": True}}

# Pewpew recognises its gun by the custom_data tag; the rest matches what Pewpew itself puts on the item.
BLASTER_COMPONENTS = {
    "minecraft:item_model": "family:foam_blaster",
    "minecraft:custom_name": {"text": "Foam Blaster", "color": "gold", "italic": False},
    "minecraft:lore": [{"text": "Foam darts only. Pew pew!", "color": "gray", "italic": False}],
    "minecraft:use_cooldown": {"seconds": 0.4, "cooldown_group": "pewpew:gun_foam_blaster"},
    "minecraft:custom_data": {"PublicBukkitValues": {"pewpew:item_id": "foam_blaster"}},
    "minecraft:charged_projectiles": [{"id": "minecraft:arrow"}]}     # holdPose CROSSBOW look

def give_string(item, components):
    """/give syntax for the same components the recipes use (JSON is valid SNBT)."""
    return f"{item}[" + ",".join(f"{k.removeprefix('minecraft:')}={json.dumps(v)}"
                                 for k, v in components.items()) + "]"

def make_sounds(dest_dir, prefix):
    os.makedirs(dest_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for i, v in enumerate(VARIANTS, start=1):
            swing(f"{tmp}/s.wav", **v, seed=i)
            subprocess.run(["oggenc", "-Q", "-q", "5", "-s", str(1000 + i),   # fixed serial: reproducible files
                            "-o", f"{dest_dir}/{prefix}{i}.ogg", f"{tmp}/s.wav"], check=True)

def build_java():
    shutil.rmtree(JAVA, ignore_errors=True)
    put(f"{JAVA}/pack.mcmeta", {"pack": {"description": "Family server: foam blaster, lightsabers, katanas, Undersea",
                                         "min_format": JAVA_FORMAT, "max_format": 999}})
    draw_blaster(32).resize((64, 64), 0).save(f"{JAVA}/pack.png")
    a = f"{JAVA}/assets"
    os.makedirs(f"{a}/family/textures/item", exist_ok=True)
    # blaster: flat picture in the inventory, on the ground and in frames; 3D model in hand
    # (a flat picture held straight ahead can only show its top or its edge).
    put(f"{a}/family/items/foam_blaster.json", {"model": {
        "type": "minecraft:select", "property": "minecraft:display_context",
        "cases": [{"when": ["gui", "ground", "fixed"], "model": {"type": "minecraft:model", "model": "family:item/foam_blaster"}}],
        "fallback": {"type": "minecraft:model", "model": "family:item/foam_blaster_3d"}}})
    put(f"{a}/family/models/item/foam_blaster.json",
        {"parent": "minecraft:item/crossbow", "textures": {"layer0": "family:item/foam_blaster"}})
    draw_blaster(32, "left").save(f"{a}/family/textures/item/foam_blaster.png")
    # 3D model is built barrel = +y, top = +z, so the crossbow's hand positions apply with 45 degrees
    # added to the z rotation (the crossbow picture points at 135 degrees, the model at 90).
    put(f"{a}/family/models/item/foam_blaster_3d.json", {
        "textures": {"palette": "family:item/foam_blaster_palette", "particle": "family:item/foam_blaster"},
        "elements": blaster_3d_elements(),
        "display": {
            "thirdperson_righthand": {"rotation": [-90, 0, -15], "translation": [2, 0.1, -3], "scale": [0.9, 0.9, 0.9]},
            "thirdperson_lefthand": {"rotation": [-90, 0, -15], "translation": [2, 0.1, -3], "scale": [0.9, 0.9, 0.9]},
            # main hand: also cancel the game's centring of a loaded crossbow (translate -0.641864, rotate y 10)
            # so it sits on the right like an unloaded crossbow
            "firstperson_righthand": {"rotation": [-90, 0, -20], "translation": [12.89, 3.2, 4.82], "scale": [0.68, 0.68, 0.68]},
            "firstperson_lefthand": {"rotation": [-90, 0, -10], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
            "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]}}})
    palette_texture().save(f"{a}/family/textures/item/foam_blaster_palette.png")
    # lightsabers: hilt = normal handheld item; blade = full-bright panel (light_emission 15) on top
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        n = f"lightsaber_{colour}"
        put(f"{a}/family/items/{n}.json", {"model": {"type": "minecraft:composite", "models": [
            {"type": "minecraft:model", "model": f"family:item/{n}"},
            {"type": "minecraft:model", "model": f"family:item/{n}_blade"}]}})
        put(f"{a}/family/models/item/{n}.json",
            {"parent": "minecraft:item/handheld", "textures": {"layer0": f"family:item/{n}_hilt"}})
        put(f"{a}/family/models/item/{n}_blade.json", {
            "gui_light": "front",
            "textures": {"blade": f"family:item/{n}_blade", "particle": f"family:item/{n}_hilt"},
            "elements": [{"from": [0, 0, 7.45], "to": [16, 16, 8.55], "shade": False, "light_emission": 15,
                          "faces": {"south": {"uv": [0, 0, 16, 16], "texture": "#blade"},
                                    "north": {"uv": [16, 0, 0, 16], "texture": "#blade"}}}],
            "display": HANDHELD_DISPLAY})
        saber_hilt(hilt).save(f"{a}/family/textures/item/{n}_hilt.png")
        saber_blade(blade, solid_halo=False).save(f"{a}/family/textures/item/{n}_blade.png")
    make_sounds(f"{a}/family/sounds/lightsaber", "swing")
    katana_sounds = katana.java(a, put, HANDHELD_DISPLAY)
    put(f"{a}/minecraft/sounds.json",
        {HIT_SOUND: {"sounds": [f"family:lightsaber/swing{i}" for i in range(1, len(VARIANTS) + 1)]}, **katana_sounds})
    undersea.java(a, put)

def bright_saber(blade_hex, hilt_hex):
    """Bedrock lightsaber picture: bright tube (wide white core fading to the blade colour at the rim).
    Fully opaque, because Bedrock item pictures can't blend."""
    img = saber_hilt(hilt_hex); p = img.load()
    blade = hexc(blade_hex); white = hexc("#FFFFFF")
    ax, ay, bx, by = 11.0, 21.0, 28.5, 3.5
    vx, vy = bx - ax, by - ay; L2 = vx * vx + vy * vy
    for y in range(32):
        for x in range(32):
            cx, cy = x + 0.5, y + 0.5
            t = ((cx - ax) * vx + (cy - ay) * vy) / L2
            if t < 0:
                continue
            t = min(t, 1.0)
            d = ((cx - ax - t * vx) ** 2 + (cy - ay - t * vy) ** 2) ** 0.5
            c = (white if d <= 1.4 else mix(blade, white, 0.6) if d <= 2.3
                 else mix(blade, white, 0.25) if d <= 3.1 else blade if d <= 3.6 else None)
            if c:
                p[x, y] = c
    return img

def build_bedrock():
    shutil.rmtree(BEDROCK, ignore_errors=True)
    put(f"{BEDROCK}/manifest.json", {
        "format_version": 2,
        "header": {"name": "Family server pack", "description": "Foam blaster, lightsabers, katanas, Undersea",
                   "uuid": BEDROCK_HEADER_UUID, "version": VERSION, "min_engine_version": [1, 21, 0]},
        "modules": [{"type": "resources", "uuid": BEDROCK_MODULE_UUID, "version": VERSION}]})
    draw_blaster(32).resize((128, 128), 0).save(f"{BEDROCK}/pack_icon.png")
    t = f"{BEDROCK}/textures/items"; os.makedirs(t, exist_ok=True)
    textures = {"family_foam_blaster": draw_blaster(32, "right")}
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        textures[f"family_lightsaber_{colour}"] = bright_saber(blade, hilt)
    textures.update(undersea.bedrock(BEDROCK, put))
    katana_icons, katana_sounds = katana.bedrock(BEDROCK, put)
    textures.update(katana_icons)
    for name, img in textures.items():
        img.save(f"{t}/{name}.png")
    put(f"{BEDROCK}/textures/item_texture.json", {"resource_pack_name": "family", "texture_name": "atlas.items",
        "texture_data": {n: {"textures": f"textures/items/{n}"} for n in textures}})
    # In-hand models (attachables). Mesh and poses copied from Mojang's player bow (bedrock-samples
    # attachables/bow.json): "wield" is its normal hold, "aim" adds its first-person pull pose (Bedrock adds
    # the two), which points the arrow ahead; the blaster's muzzle sits where the arrow tip is (top-left).
    # Katanas and lightsabers use "wield" (since pack 1.0.21): katana blades animate like on PC, lightsabers
    # get the PC see-through halo. (No held item glows at night on Bedrock: emissive materials,
    # ignore_lighting and light_color_multiplier were all tested.) The hand holds the picture at local_pivot
    # (texture units, 16 across, rows from the top): the bow's (6, 6) is mid-sword on ours, which looks right
    # in first person. The bow's third-person pose holds a sword blade back and down (and the blaster's barrel
    # straight down), so in third person "wield" and "aim" turn the item over around the hand, and the model
    # is drawn from a flipped picture. A sword's is mirrored across the blade (turning it over along its
    # length, or a katana's edge ends up on top), held at (1.6, 11.6): mid-hilt, moved toward the spine so the
    # hilt sits in the fist, not above it; and 1.5 px further out from the body (the bow's mesh sits 2 px
    # inward of the hand), centred in the fist. The blaster's is mirrored left to right (muzzle ahead, top
    # up), held mid-grip: the sword's grip point moved by (grip - hilt middle). One render controller picks
    # the first- or third-person picture and mesh (a second controller didn't draw in first person). In the
    # off-hand a sword is hidden instead of being drawn in the right hand over the main-hand item (the blaster
    # can't be in the off-hand).
    suffix = lambda slot: "" if slot == "default" else f"_{slot}"
    tp_slot = lambda slot: f"tp{suffix(slot)}"
    MAIN, OFF = "context.item_slot != 'off_hand'", "context.item_slot == 'off_hand'"   # as GeyserMC Rainbow
    SWORD = ("family_sword", {"hold": "animation.family.wield", "hide": "animation.family.hide"},
             [{"hold": MAIN}, {"hide": OFF}], Image.Transpose.TRANSVERSE)   # across the blade line
    GUN = ("family_item", {"hold": "animation.family.aim"}, ["hold"], Image.Transpose.FLIP_LEFT_RIGHT)
    TP_GRIP, GUN_TP_GRIP = (1.6, 11.6, 0.5), (6.1, 11.7, 0.5)   # local_pivot x, z; mesh position x
    def held(name, frames, materials, controllers, rig):
        """Several frames cycle at Java's frametime 2; each gets its own mesh (cut from its picture).
        materials: (normal, enchanted); rig: (geometry, animations, animate, third-person picture flip)."""
        geometry, animations, animate, tp_flip = rig
        slots = ["default"] + [f"f{i}" for i in range(1, len(frames))]
        pictures = dict(zip(slots, frames))
        pictures.update({tp_slot(s): img.transpose(tp_flip) for s, img in zip(slots, frames)})
        for s, img in pictures.items():
            img.save(f"{t}/family_{name}_held{suffix(s)}.png")
        put(f"{BEDROCK}/attachables/{name}.json", {"format_version": "1.10.0", "minecraft:attachable": {
            "description": {
                "identifier": f"family:{name}",
                "materials": dict(zip(("default", "enchanted"), materials)),
                "textures": {**{s: f"textures/items/family_{name}_held{suffix(s)}" for s in pictures},
                             "enchanted": "textures/misc/enchanted_item_glint"},
                "geometry": {s: f"geometry.{geometry}{suffix(s)}" for s in pictures},
                "animations": animations,
                "scripts": {"pre_animation": ["variable.family_tp = c.is_first_person ? 0.0 : 1.0;"],
                            "animate": animate},
                "render_controllers": controllers}}})
    held("foam_blaster", [draw_blaster(32, "left")], ("entity_alphatest", "entity_alphatest"),
         ["controller.render.family_held"], GUN)
    for el in katana.KATANAS:
        held(f"katana_{el}", bedrock_held_frames(el), ("entity_alphatest", "entity_alphatest_glint"),
             ["controller.render.family_flipbook"], SWORD)
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        held(f"lightsaber_{colour}", [draw_glow_saber(blade, hilt, solid_halo=False)],
             ("entity_alphablend", "entity_alphatest_glint"), ["controller.render.family_held"], SWORD)
    slots = ["default"] + [f"f{i}" for i in range(1, FRAMES)]
    mesh = lambda s, x=6.0, z=6.0, at=2.0: {"texture": s, "position": [at, 1.0, -1.0],
                                            "rotation": [0.0, -135.0, 90.0], "local_pivot": [x, 0.0, z]}
    geo = lambda name, bones: {"description": {"identifier": name, "texture_width": 16, "texture_height": 16},
                               "bones": bones}
    held_at = lambda name, s, *pivot: geo(name, [{"name": "rightitem", "texture_meshes": [mesh(s, *pivot)]}])
    put(f"{BEDROCK}/models/entity/family_item.geo.json", {"format_version": "1.16.0", "minecraft:geometry": [
        held_at("geometry.family_item", "default"), held_at("geometry.family_item_tp", "tp", *GUN_TP_GRIP)] +
        [held_at(f"geometry.family_sword{suffix(s)}", s) for s in slots] +
        [held_at(f"geometry.family_sword{suffix(tp_slot(s))}", tp_slot(s), *TP_GRIP) for s in slots]})
    fp = lambda a, b: f"c.is_first_person ? {a} : {b}"
    put(f"{BEDROCK}/animations/family_items.animation.json", {"format_version": "1.8.0", "animations": {
        "animation.family.aim": {"loop": True, "bones": {"rightitem": {      # third person as "wield"
            "position": [fp(-7.0, 0.5), fp(-0.5, -0.5), fp(-7.8, -1.0)],
            "rotation": [fp(-15.0, 180.0), fp(-112.0, 0.0), fp(-28.0, 0.0)]}}},
        "animation.family.wield": {"loop": True, "bones": {"rightitem": {   # third person: turned over,
            "position": [fp(-5.5, 0.5), fp(-3.0, -0.5), fp(-3.0, -1.0)],        # grip kept in place
            "rotation": [fp(38.0, 180.0), fp(-120.0, 0.0), fp(-63.0, 0.0)]}}},
        "animation.family.hide": {"loop": True, "bones": {"rightitem": {"scale": 0.0}}}}})
    frame = f"math.mod(math.floor(q.life_time * 10.0), {FRAMES})"      # 10 a second = Java frametime 2
    def sword_controller(keys):
        """First-person pictures + meshes, then the third-person ones; several frames cycle (Mojang's bow
        swaps texture + mesh the same way)."""
        keys = keys + [tp_slot(k) for k in keys]
        pick = f"{frame if len(keys) > 2 else 0} + variable.family_tp * {len(keys) // 2}"
        return {"arrays": {"textures": {"array.frames": [f"texture.{k}" for k in keys]},
                           "geometries": {"array.meshes": [f"geometry.{k}" for k in keys]}},
                "geometry": f"array.meshes[{pick}]",
                "materials": [{"*": "variable.is_enchanted ? material.enchanted : material.default"}],
                "textures": [f"array.frames[{pick}]", "texture.enchanted"]}
    put(f"{BEDROCK}/render_controllers/family_items.render_controllers.json", {"format_version": "1.10.0",
        "render_controllers": {"controller.render.family_flipbook": sword_controller(slots),
                               "controller.render.family_held": sword_controller(["default"])}})
    make_sounds(f"{BEDROCK}/sounds/family/lightsaber", "swing")
    put(f"{BEDROCK}/sounds/sound_definitions.json", {"format_version": "1.14.0", "sound_definitions": {
        HIT_SOUND: {"category": "player", "max_distance": 16.0,
                    "sounds": [f"sounds/family/lightsaber/swing{i}" for i in range(1, len(VARIANTS) + 1)]},
        **katana_sounds}})
    # No creative_category: Geyser can't turn a creative-menu pick of these back into a Java item,
    # so they'd vanish (and lack the tags that make them work). Kids get them by /give or crafting.
    def item(model, icon):
        return {"bedrock_identifier": model, "model": model,   # model = the Java item_model on the item
                "bedrock_options": {"icons": {"default": icon}, "display_handheld": True}}
    put(f"{ROOT}/geyser/custom_mappings/family.json", {"format_version": 2, "items": {
        "minecraft:crossbow": [{**item("family:foam_blaster", "family_foam_blaster"),
            # Bedrock treats it as a usable item (no swing on use): no animation, a use that never
            # completes (like Geyser's trident trick), and no slowdown while held down.
            "components": {"minecraft:consumable": {"consume_seconds": 1000, "animation": "none"},
                           "minecraft:use_effects": {"speed_multiplier": 1.0}}}],
        "minecraft:diamond_sword": [item(f"family:lightsaber_{c}", f"family_lightsaber_{c}")
                                    for c in LIGHTSABERS] + katana.mappings(),
        **undersea.mappings()}})

def build_datapack():
    shutil.rmtree(DATA, ignore_errors=True)
    put(f"{DATA}/pack.mcmeta", {"pack": {"description": "Family server: recipes, lightsaber hit sound, blaster main-hand lock, katanas, Undersea",
                                         "min_format": DATA_FORMAT, "max_format": 999}})
    d = f"{DATA}/data/family"
    for colour, (_, _, dye) in LIGHTSABERS.items():           # diamond sword + amethyst shard + dye
        put(f"{d}/recipe/lightsaber_{colour}.json", {
            "type": "minecraft:crafting_shapeless", "category": "equipment",
            "ingredients": ["minecraft:diamond_sword", "minecraft:amethyst_shard", f"minecraft:{dye}"],
            "result": {"id": "minecraft:diamond_sword", "components": saber_components(colour)}})
    put(f"{d}/recipe/foam_blaster.json", {                    # crossbow + amethyst shard + orange dye
        "type": "minecraft:crafting_shapeless", "category": "equipment",
        "ingredients": ["minecraft:crossbow", "minecraft:amethyst_shard", "minecraft:orange_dye"],
        "result": {"id": "minecraft:crossbow", "components": BLASTER_COMPONENTS}})
    put(f"{d}/advancement/unlock_foam_blaster.json", {         # separate, so players who already unlocked
        "criteria": {"has_amethyst": {"trigger": "minecraft:inventory_changed",   # the sabers get it too
                                      "conditions": {"items": [{"items": "minecraft:amethyst_shard"}]}}},
        "rewards": {"recipes": ["family:foam_blaster"]}})
    put(f"{d}/advancement/unlock_lightsabers.json", {          # show recipes once they hold an amethyst shard
        "criteria": {"has_amethyst": {"trigger": "minecraft:inventory_changed",
                                      "conditions": {"items": [{"items": "minecraft:amethyst_shard"}]}}},
        "rewards": {"recipes": [f"family:lightsaber_{c}" for c in LIGHTSABERS]}})
    put(f"{d}/advancement/lightsaber_hit.json", {              # melee hit while holding a lightsaber
        "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {"damage": {"type": {
            "direct_entity": {"minecraft:equipment": {"mainhand": {
                "items": "minecraft:diamond_sword",
                "predicates": {"minecraft:custom_data": "{family_lightsaber:1b}"}}}}}}}}},
        "rewards": {"function": "family:lightsaber_hit"}})
    # Pewpew only fires from the main hand, and on iPads an off-hand blaster is drawn over the
    # main-hand item. So a blaster that lands in the off-hand goes straight back to the inventory.
    put(f"{d}/advancement/blaster_offhand.json", {
        "criteria": {"offhand": {"trigger": "minecraft:inventory_changed", "conditions": {"player": {
            "type": "minecraft:entity_properties", "entity": "this", "predicate": {
            "equipment": {"offhand": {"items": "minecraft:crossbow", "predicates": {
                "minecraft:custom_data": '{PublicBukkitValues:{"pewpew:item_id":"foam_blaster"}}'}}}}}}}},
        "rewards": {"function": "family:blaster_offhand"}})
    put(f"{d}/function/blaster_offhand.mcfunction",       # clear before give: no re-trigger, no duplicates
        "advancement revoke @s only family:blaster_offhand\n"
        "item replace entity @s weapon.offhand with air\n"
        f"give @s {give_string('minecraft:crossbow', BLASTER_COMPONENTS)}\n")
    put(f"{d}/function/lightsaber_hit.mcfunction",
        f"advancement revoke @s only family:lightsaber_hit\nplaysound minecraft:{HIT_SOUND} player @a ~ ~ ~\n")
    undersea.datapack(DATA, put, give_string)
    town.datapack(DATA, put, undersea.DIM, (undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z))
    wardrobe.datapack(DATA, put, give_string)
    katana.datapack(DATA, put, give_string)
    townsfolk.datapack(DATA, put, give_string)
    race.datapack(DATA, put)
    alive.datapack(DATA, put)
    houses.datapack(DATA, put, give_string)
    tags = f"{DATA}/data/minecraft/tags/function"
    put(f"{tags}/load.json", {"values": ["family:undersea/load", "family:undersea/wardrobe/load", "family:katana/load",
                                        "family:undersea/folk/load", "family:undersea/race/load",
                                        "family:undersea/alive/load", "family:undersea/houses/load"]})
    put(f"{tags}/tick.json", {"values": ["family:undersea/tick", "family:undersea/wardrobe/tick", "family:katana/tick",
                                        "family:undersea/race/tick", "family:undersea/alive/tick",
                                        "family:undersea/houses/tick"]})

def zipdir(src, dest):
    """Deterministic zip (fixed timestamps, sorted) so rebuilding unchanged content keeps the same sha1."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, files in sorted(os.walk(src)):
            for f in sorted(files):
                full = os.path.join(dirpath, f)
                info = zipfile.ZipInfo(os.path.relpath(full, src), date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(full, "rb") as fh:
                    z.writestr(info, fh.read())

if __name__ == "__main__":
    if not shutil.which("oggenc"):
        sys.exit("oggenc missing: brew install vorbis-tools")
    build_java(); build_bedrock(); build_datapack()
    zipdir(JAVA, f"{DIST}/family-pack-java.zip")
    zipdir(BEDROCK, f"{DIST}/family-pack-bedrock.mcpack")
    zipdir(DATA, f"{DIST}/family-datapack.zip")
    put(f"{DIST}/lightsabers.json", {c: give_string("minecraft:diamond_sword", saber_components(c)) for c in LIGHTSABERS})
    put(f"{DIST}/foam-blaster.item", give_string("minecraft:crossbow", BLASTER_COMPONENTS) + "\n")
    put(f"{DIST}/undersea.json", undersea.gives(give_string))
    put(f"{DIST}/katanas.json", katana.gives(give_string))
    for f in sorted(os.listdir(DIST)):
        b = open(f"{DIST}/{f}", "rb").read()
        print(f"{f}: {len(b)} bytes, sha1 {hashlib.sha1(b).hexdigest()}")
