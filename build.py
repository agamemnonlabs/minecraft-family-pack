"""Builds the family pack from art.py / sounds.py.
  dist/family-pack-java.zip         -> PC players (server.properties resource-pack)
  dist/family-pack-bedrock.mcpack   -> iPads (Geyser packs/ folder)
  dist/family-datapack.zip          -> server world/datapacks: lightsaber recipes + hit sound
  dist/lightsabers.json             -> /give item strings, used by ../give-lightsaber.sh
  geyser/custom_mappings/family.json -> Geyser: our items -> custom Bedrock items
Run: python3 build.py   (needs Pillow and oggenc)"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import draw_blaster, draw_saber, LIGHTSABERS
from sounds import swing, VARIANTS

ROOT = os.path.dirname(os.path.abspath(__file__))
JAVA, BEDROCK, DATA, DIST = (os.path.join(ROOT, d) for d in ("java", "bedrock", "datapack", "dist"))
VERSION = [1, 0, 0]                       # bump for every change shipped to Bedrock
JAVA_FORMAT, DATA_FORMAT = 97, 121        # resource / data pack formats of Minecraft 26.3
BEDROCK_HEADER_UUID = "6f1d2b8e-3c47-4a8e-9d2f-5b1a7c0e4f21"
BEDROCK_MODULE_UUID = "a3c9e5d7-81f2-4b6a-b0e4-2d8f6c1a9e53"
HIT_SOUND = "family.lightsaber_hit"       # lives in minecraft: so Geyser passes it to Bedrock unchanged

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
            subprocess.run(["oggenc", "-Q", "-q", "5", "-o", f"{dest_dir}/{prefix}{i}.ogg", f"{tmp}/s.wav"], check=True)

def build_java():
    shutil.rmtree(JAVA, ignore_errors=True)
    put(f"{JAVA}/pack.mcmeta", {"pack": {"description": "Family server: foam blaster + lightsabers",
                                         "min_format": JAVA_FORMAT, "max_format": 999}})
    draw_blaster(32).resize((64, 64), 0).save(f"{JAVA}/pack.png")
    a = f"{JAVA}/assets"
    os.makedirs(f"{a}/family/textures/item", exist_ok=True)
    # parent = vanilla crossbow: same hand positions as the crossbow it replaces
    items = {"foam_blaster": ("minecraft:item/crossbow", draw_blaster(32, "left"))}
    for colour, (blade, hilt, _) in LIGHTSABERS.items():
        items[f"lightsaber_{colour}"] = ("minecraft:item/handheld", draw_saber(blade, hilt))
    for name, (parent, img) in items.items():
        put(f"{a}/family/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"family:item/{name}"}})
        put(f"{a}/family/models/item/{name}.json", {"parent": parent, "textures": {"layer0": f"family:item/{name}"}})
        img.save(f"{a}/family/textures/item/{name}.png")
    make_sounds(f"{a}/family/sounds/lightsaber", "swing")
    put(f"{a}/minecraft/sounds.json",
        {HIT_SOUND: {"sounds": [f"family:lightsaber/swing{i}" for i in range(1, len(VARIANTS) + 1)]}})

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
        textures[f"family_lightsaber_{colour}"] = draw_saber(blade, hilt)
    for name, img in textures.items():
        img.save(f"{t}/{name}.png")
    put(f"{BEDROCK}/textures/item_texture.json", {"resource_pack_name": "family", "texture_name": "atlas.items",
        "texture_data": {n: {"textures": f"textures/items/{n}"} for n in textures}})
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
