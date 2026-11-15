"""Builds the family pack from art.py / sounds.py.
  dist/family-pack-java.zip         -> PC players (server.properties resource-pack)
  dist/family-pack-bedrock.mcpack   -> iPads (Geyser packs/ folder)
  dist/family-datapack.zip          -> server world/datapacks: lightsaber recipes + hit sound
  dist/lightsabers.json             -> /give item strings, used by ../give-lightsaber.sh
  geyser/custom_mappings/family.json -> Geyser: our items -> custom Bedrock items
Run: python3 build.py   (needs Pillow and oggenc)"""
from PIL import Image
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import draw_blaster, draw_glow_saber, saber_hilt, saber_blade, mix, hexc, LIGHTSABERS
from sounds import swing, VARIANTS

ROOT = os.path.dirname(os.path.abspath(__file__))
JAVA, BEDROCK, DATA, DIST = (os.path.join(ROOT, d) for d in ("java", "bedrock", "datapack", "dist"))
VERSION = [1, 0, 6]                       # bump for every change shipped to Bedrock (iPads cache by version)
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

# Mojang's player bow: wield pose, plus the first-person pull pose added on top for "aim".
fp = lambda a, b: f"c.is_first_person ? {a} : {b}"
BOW_POSES = {
    "standby": ([fp(-5.5, 0.5), fp(-3.0, -2.5), fp(-3.0, 1.0)], [fp(38.0, 0.0), fp(-120.0, 0.0), fp(-63.0, 0.0)]),
    "aim": ([fp(-7.0, 0.5), fp(-0.5, -2.5), fp(-7.8, 1.0)], [fp(-15.0, 0.0), fp(-112.0, 0.0), fp(-28.0, 0.0)]),
}
def attachable(identifier, texture, material, pose):
    put(f"{BEDROCK}/attachables/{identifier.split(':')[1]}.json", {"format_version": "1.10.0", "minecraft:attachable": {
        "description": {
            "identifier": identifier,
            "materials": {"default": material, "enchanted": material},
            "textures": {"default": texture, "enchanted": "textures/misc/enchanted_item_glint"},
            "geometry": {"default": "geometry.family_item"},
            "animations": {"hold": f"animation.family.{pose}"},
            "scripts": {"animate": ["hold"]},
            "render_controllers": ["controller.render.item_default"]}}})

def held_saber_emissive(blade_hex, hilt_hex):
    """In-hand lightsaber for Bedrock (entity_emissive_alpha: the more transparent a pixel, the more it
    glows; alpha 0 = hidden). Bright tube: wide white core fading to the blade colour at the rim.
    Hilt stays opaque so it is lit normally."""
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
                p[x, y] = c[:3] + (25,)
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
    # In-hand models (attachables). Poses and mesh copied from Mojang's player bow attachable
    # (bedrock-samples attachables/bow.json): "standby" = holding it, "aim" = standby + the
    # first-person pull pose (Bedrock adds the two). Lightsaber sprite runs diagonally like the
    # bow string; blaster muzzle points top-left like the arrow, which points ahead when aiming.
    # Our 32px sprites come out about the size of vanilla Bedrock swords/crossbows with the bow's numbers.
    draw_blaster(32, "left").save(f"{t}/family_foam_blaster_held.png")
    attachable("family:foam_blaster", "textures/items/family_foam_blaster_held", "entity_alphatest", "aim")
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        held_saber_emissive(blade, hilt).save(f"{t}/family_lightsaber_{colour}_held.png")
        attachable(f"family:lightsaber_{colour}", f"textures/items/family_lightsaber_{colour}_held",
                   "entity_emissive_alpha", "standby")
    put(f"{BEDROCK}/models/entity/family_item.geo.json", {"format_version": "1.16.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.family_item", "texture_width": 16, "texture_height": 16},
        "bones": [{"name": "rightitem", "texture_meshes": [{"texture": "default", "position": [2.0, 1.0, -1.0],
                   "rotation": [0.0, -135.0, 90.0], "local_pivot": [6.0, 0.0, 6.0]}]}]}]})
    put(f"{BEDROCK}/animations/family_items.animation.json", {"format_version": "1.8.0", "animations": {
        f"animation.family.{pose}": {"loop": True, "bones": {"rightitem": {"position": pos, "rotation": rot}}}
        for pose, (pos, rot) in BOW_POSES.items()}})
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
