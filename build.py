"""Builds the family pack from art.py / sounds.py.
  dist/family-pack-java.zip         -> PC players (server.properties resource-pack)
  dist/family-pack-bedrock.mcpack   -> iPads (Geyser packs/ folder)
  dist/family-datapack.zip          -> server world/datapacks: lightsaber recipes + hit sound
  dist/lightsabers.json             -> /give item strings, used by ../give-lightsaber.sh
  geyser/custom_mappings/family.json -> Geyser: our items -> custom Bedrock items
Run: python3 build.py   (needs Pillow and oggenc)"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import draw_blaster, draw_glow_saber, saber_hilt, saber_blade, LIGHTSABERS
from sounds import swing, VARIANTS

ROOT = os.path.dirname(os.path.abspath(__file__))
JAVA, BEDROCK, DATA, DIST = (os.path.join(ROOT, d) for d in ("java", "bedrock", "datapack", "dist"))
VERSION = [1, 0, 3]                       # bump for every change shipped to Bedrock (iPads cache by version)
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
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]}}
# vanilla item/crossbow display transforms (26.3) + generated head, for the blaster's Bedrock hold
CROSSBOW_DISPLAY = {
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "thirdperson_righthand": {"rotation": [-90, 0, -60], "translation": [2, 0.1, -3], "scale": [0.9, 0.9, 0.9]},
    "thirdperson_lefthand": {"rotation": [-90, 0, 30], "translation": [2, 0.1, -3], "scale": [0.9, 0.9, 0.9]},
    "firstperson_righthand": {"rotation": [-90, 0, -55], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [-90, 0, 35], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]}}       # lives in minecraft: so Geyser passes it to Bedrock unchanged

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

def give_string(colour):
    c = saber_components(colour)
    return (f'minecraft:diamond_sword[item_model="{c["minecraft:item_model"]}",'
            f'custom_name={json.dumps(c["minecraft:custom_name"])},custom_data={{family_lightsaber:1b}}]')

def make_sounds(dest_dir, prefix):
    os.makedirs(dest_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for i, v in enumerate(VARIANTS, start=1):
            swing(f"{tmp}/s.wav", **v, seed=i)
            subprocess.run(["oggenc", "-Q", "-q", "5", "-s", str(1000 + i),   # fixed serial: reproducible files
                            "-o", f"{dest_dir}/{prefix}{i}.ogg", f"{tmp}/s.wav"], check=True)

def build_java():
    shutil.rmtree(JAVA, ignore_errors=True)
    put(f"{JAVA}/pack.mcmeta", {"pack": {"description": "Family server: foam blaster + lightsabers",
                                         "min_format": JAVA_FORMAT, "max_format": 999}})
    draw_blaster(32).resize((64, 64), 0).save(f"{JAVA}/pack.png")
    a = f"{JAVA}/assets"
    os.makedirs(f"{a}/family/textures/item", exist_ok=True)
    # blaster: parent = vanilla crossbow, so it is held exactly like the crossbow it replaces
    put(f"{a}/family/items/foam_blaster.json", {"model": {"type": "minecraft:model", "model": "family:item/foam_blaster"}})
    put(f"{a}/family/models/item/foam_blaster.json",
        {"parent": "minecraft:item/crossbow", "textures": {"layer0": "family:item/foam_blaster"}})
    draw_blaster(32, "left").save(f"{a}/family/textures/item/foam_blaster.png")
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
    put(f"{a}/minecraft/sounds.json",
        {HIT_SOUND: {"sounds": [f"family:lightsaber/swing{i}" for i in range(1, len(VARIANTS) + 1)]}})

def attachable(identifier, texture, material, anim):
    name = identifier.split(":")[1]
    slots = ["thirdperson_main_hand", "thirdperson_off_hand", "head", "firstperson_main_hand", "firstperson_off_hand"]
    put(f"{BEDROCK}/attachables/{name}.json", {"format_version": "1.10.0", "minecraft:attachable": {"description": {
        "identifier": identifier,
        "materials": {"default": material, "enchanted": material},
        "textures": {"default": texture, "enchanted": "textures/misc/enchanted_item_glint"},
        "geometry": {"default": "geometry.family_item"},
        "scripts": {
            "pre_animation": ["v.main_hand = c.item_slot == 'main_hand';", "v.off_hand = c.item_slot == 'off_hand';",
                              "v.head = c.item_slot == 'head';"],
            "animate": [{"thirdperson_main_hand": "v.main_hand && !c.is_first_person"},
                        {"thirdperson_off_hand": "v.off_hand && !c.is_first_person"},
                        {"head": "v.head && !c.is_first_person"},
                        {"firstperson_main_hand": "v.main_hand && c.is_first_person"},
                        {"firstperson_off_hand": "v.off_hand && c.is_first_person"},
                        {"firstperson_head": "c.is_first_person && v.head"}]},
        "animations": {**{k: f"animation.family.{anim}.{k}" for k in slots},
                       "firstperson_head": "animation.family.disable"},
        "render_controllers": ["controller.render.item_default"]}}})

def hold_animations(prefix, disp):
    """Java display transforms -> Bedrock bone animations (same mapping as java2bedrock)."""
    def parts(d, flip_x, flip_z, scale_mul=1.0):
        r, t, s = d.get("rotation"), d.get("translation"), d.get("scale")
        x = {}
        if r: x["rotation"] = [-r[0], 0, 0]
        if t: x["position"] = [(-t[0] if flip_x else t[0]) * scale_mul, t[1] * scale_mul, (-t[2] if flip_z else t[2]) * scale_mul]
        if s: x["scale"] = [v * scale_mul for v in s]
        bones = {"family_x": x}
        if r: bones["family_y"] = {"rotation": [0, -r[1], 0]}; bones["family_z"] = {"rotation": [0, 0, r[2]]}
        return bones
    fp_root = {"rotation": [90, 60, -40], "position": [4, 10, 4], "scale": 1.5}
    tp_root = {"rotation": [90, 0, 0], "position": [0, 13, -3]}
    head = parts(disp["head"], True, False, 0.625); head["family"] = {"position": [0, 19.9, 0]}
    fp_main = parts(disp["firstperson_righthand"], True, True); fp_main["family"] = fp_root
    fp_off = parts(disp["firstperson_lefthand"], False, True); fp_off["family"] = fp_root
    tp_main = parts(disp["thirdperson_righthand"], True, False); tp_main["family"] = tp_root
    tp_off = parts(disp["thirdperson_lefthand"], False, False); tp_off["family"] = tp_root
    return {f"animation.family.{prefix}.{k}": {"loop": True, "bones": v} for k, v in
            {"thirdperson_main_hand": tp_main, "thirdperson_off_hand": tp_off, "head": head,
             "firstperson_main_hand": fp_main, "firstperson_off_hand": fp_off}.items()}

def glow_saber_emissive(blade, hilt):
    """Bedrock entity_emissive_alpha: the more transparent a pixel, the more it glows (alpha 0 = hidden).
    Hilt stays opaque (normally lit); every blade/glow pixel gets a low alpha so it glows."""
    img = draw_glow_saber(blade, hilt, solid_halo=True)
    hilt_mask = saber_hilt(hilt).getchannel("A").load()
    px = img.load()
    for y in range(32):
        for x in range(32):
            r, g, b, a = px[x, y]
            if a and not hilt_mask[x, y]:
                px[x, y] = (r, g, b, 25)
    return img

def build_bedrock():
    shutil.rmtree(BEDROCK, ignore_errors=True)
    put(f"{BEDROCK}/manifest.json", {
        "format_version": 2,
        "header": {"name": "Family server pack", "description": "Foam blaster + lightsabers",
                   "uuid": BEDROCK_HEADER_UUID, "version": VERSION, "min_engine_version": [1, 21, 0]},
        "modules": [{"type": "resources", "uuid": BEDROCK_MODULE_UUID, "version": VERSION}]})
    draw_blaster(32).resize((128, 128), 0).save(f"{BEDROCK}/pack_icon.png")
    t = f"{BEDROCK}/textures/items"; os.makedirs(t, exist_ok=True)
    textures = {"family_foam_blaster": draw_blaster(32, "right")}
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        textures[f"family_lightsaber_{colour}"] = draw_glow_saber(blade, hilt, solid_halo=True)
    for name, img in textures.items():
        img.save(f"{t}/{name}.png")
    put(f"{BEDROCK}/textures/item_texture.json", {"resource_pack_name": "family", "texture_name": "atlas.items",
        "texture_data": {n: {"textures": f"textures/items/{n}"} for n in textures}})
    # In-hand models (attachables), built the way java2bedrock does for Geyser custom items:
    # a flat extruded sprite bound to the hand, positioned from the same Java display numbers
    # the PC pack uses (crossbow for the blaster, handheld for the lightsabers).
    draw_blaster(32, "left").save(f"{t}/family_foam_blaster_held.png")
    attachable("family:foam_blaster", "textures/items/family_foam_blaster_held", "entity_alphatest_one_sided", "blaster")
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        glow_saber_emissive(blade, hilt).save(f"{t}/family_lightsaber_{colour}_held.png")
        attachable(f"family:lightsaber_{colour}", f"textures/items/family_lightsaber_{colour}_held",
                   "entity_emissive_alpha", "saber")
    put(f"{BEDROCK}/models/entity/family_item.geo.json", {"format_version": "1.16.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.family_item", "texture_width": 16, "texture_height": 16,
                        "visible_bounds_width": 4, "visible_bounds_height": 4.5, "visible_bounds_offset": [0, 0.75, 0]},
        "bones": [
            {"name": "family", "binding": "c.item_slot == 'head' ? 'head' : q.item_slot_to_bone_name(c.item_slot)", "pivot": [0, 8, 0]},
            {"name": "family_x", "parent": "family", "pivot": [0, 8, 0]},
            {"name": "family_y", "parent": "family_x", "pivot": [0, 8, 0]},
            {"name": "family_z", "parent": "family_y", "pivot": [0, 8, 0], "texture_meshes": [
                {"texture": "default", "position": [0, 8, 0], "rotation": [90, 0, -180], "local_pivot": [8, 0.5, 8]}]}]}]})
    anims = {"animation.family.disable": {"loop": True, "override_previous_animation": True, "bones": {"family": {"scale": 0}}}}
    anims.update(hold_animations("blaster", CROSSBOW_DISPLAY))
    anims.update(hold_animations("saber", HANDHELD_DISPLAY))
    put(f"{BEDROCK}/animations/family_items.animation.json", {"format_version": "1.8.0", "animations": anims})
    make_sounds(f"{BEDROCK}/sounds/family/lightsaber", "swing")
    put(f"{BEDROCK}/sounds/sound_definitions.json", {"format_version": "1.14.0", "sound_definitions": {
        HIT_SOUND: {"category": "player", "max_distance": 16.0,
                    "sounds": [f"sounds/family/lightsaber/swing{i}" for i in range(1, len(VARIANTS) + 1)]}}})
    def item(model, icon, category):
        return {"bedrock_identifier": model, "model": model,   # model = the Java item_model on the item
                "bedrock_options": {"icons": {"default": icon}, "display_handheld": True, "creative_category": category}}
    put(f"{ROOT}/geyser/custom_mappings/family.json", {"format_version": 2, "items": {
        "minecraft:crossbow": [item("family:foam_blaster", "family_foam_blaster", "equipment")],
        "minecraft:diamond_sword": [item(f"family:lightsaber_{c}", f"family_lightsaber_{c}", "equipment")
                                    for c in LIGHTSABERS]}})

def build_datapack():
    shutil.rmtree(DATA, ignore_errors=True)
    put(f"{DATA}/pack.mcmeta", {"pack": {"description": "Family server: lightsaber recipes + hit sound",
                                         "min_format": DATA_FORMAT, "max_format": 999}})
    d = f"{DATA}/data/family"
    for colour, (_, _, dye) in LIGHTSABERS.items():           # diamond sword + amethyst shard + dye
        put(f"{d}/recipe/lightsaber_{colour}.json", {
            "type": "minecraft:crafting_shapeless", "category": "equipment",
            "ingredients": ["minecraft:diamond_sword", "minecraft:amethyst_shard", f"minecraft:{dye}"],
            "result": {"id": "minecraft:diamond_sword", "components": saber_components(colour)}})
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
    put(f"{d}/function/lightsaber_hit.mcfunction",
        f"advancement revoke @s only family:lightsaber_hit\nplaysound minecraft:{HIT_SOUND} player @a ~ ~ ~\n")

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
    put(f"{DIST}/lightsabers.json", {c: give_string(c) for c in LIGHTSABERS})
    for f in sorted(os.listdir(DIST)):
        b = open(f"{DIST}/{f}", "rb").read()
        print(f"{f}: {len(b)} bytes, sha1 {hashlib.sha1(b).hexdigest()}")
