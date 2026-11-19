"""Parachute: worn on the back (chest slot, like an elytra). It opens by itself after a 4-block fall, or early with
jump in mid-air; crouch folds it (then it stays folded until you land, unless you jump again); it packs itself up
on landing, in water or when flying. build.py calls java(), bedrock(), mappings(), datapack() and gives();
`python3 parachute.py` writes previews/parachute.png and previews/parachute-open.m4a.

- Floating: slow falling (iPads follow it themselves), plus a levitation "brake" whenever the kid falls faster than
  5 blocks/s, until they're under 3 b/s again (about one short tug every 2 s). Slow falling alone settles near
  10 b/s on a long drop. The server sees the kid's real speed, so the brake also suits the iPad's own physics.
- Canopy on PC: an item display riding the kid. /ride can't mount anything on a player, so the Skript script
  skript/family-parachute.sk does it; a canopy left without a rider (no Skript, a death, a log-out) is removed.
- Canopy on iPad: item displays are invisible on Bedrock, so the worn item's attachable draws it (custom geometry
  bound to the body bone). The datapack swaps the worn item's item_model between family:parachute and
  family:parachute_open, which Geyser maps to two Bedrock items with their own attachables.
- No glider component: Geyser shows a chest glider to Bedrock as a plain elytra."""
import math, os, subprocess, tempfile
from PIL import Image, ImageDraw
from art import hexc
from undersea_art import grid, fill, armour_layer
import katana_sounds as snd

BASE_ITEM = "minecraft:leather_chestplate"
NAME_COLOUR = "#FF9A3C"
OPEN_SOUND = "family.parachute_open"
CANOPY_SCALE, CANOPY_Y = 2.0, 1.075       # display scale; lift above the rider point (1.8 blocks up) in blocks
JAVA_Y0 = 46                              # px above the feet that sits at the Java model's centre (y = 8)

# ------------------------------------------------------------------ the shape (px: 16 = 1 block, from the feet)
# Canopy colours: palette cells (4x4 swatches). Java uses a 16x16 palette; Bedrock the same cells under the pack.
PALETTE = ["#FF8A2B", "#F6F2EA", "#CFCAC2"]       # orange, white, line grey
ORANGE, WHITE, LINE = range(3)
RIM = 52                                          # canopy rim height (the head's top is at 32)
RINGS = [(0, 12, 13, 15, ORANGE, ORANGE),         # (inner, outer half-width, y0, y1 above the rim, N/S, E/W colour)
         (12, 18, 10, 14, WHITE, ORANGE),         # inner 0 = a solid cap; the rest are hollow frames, so
         (18, 22, 5, 11, ORANGE, WHITE),          # the canopy is hollow underneath and stepped like a dome
         (22, 24, 0, 6, WHITE, ORANGE)]           # 3 blocks across
LINE_TOP, LINE_END, SHOULDER = 23, 4, 24          # lines: rim radius -> radius near the neck, at shoulder height

def boxes():
    """(x0, y0, z0, x1, y1, z1, colour) for the canopy and its 4 lines (staircases of 1 px steps: no rotations,
    so Java and Bedrock draw them the same)."""
    out = []
    for r0, r1, y0, y1, ns, ew in RINGS:
        y0, y1 = RIM + y0, RIM + y1
        if r0 == 0:
            out.append((-r1, y0, -r1, r1, y1, r1, ns)); continue
        out += [(-r1, y0, -r1, r1, y1, -r0, ns), (-r1, y0, r0, r1, y1, r1, ns),
                (-r1, y0, -r0, -r0, y1, r0, ew), (r0, y0, -r0, r1, y1, r0, ew)]
    steps = LINE_TOP - LINE_END
    h = (RIM - SHOULDER) / steps
    for i in range(steps):
        r = LINE_TOP - i
        y1, y0 = RIM - i * h + 0.3, RIM - (i + 1) * h
        for sx, sz in ((1, 0), (-1, 0), (0, 1), (0, -1)):      # E, W, S, N
            cx, cz = sx * (r - 0.5), sz * (r - 0.5)
            out.append((cx - 0.5, y0, cz - 0.5, cx + 0.5, y1, cz + 0.5, LINE))
    return out

# ------------------------------------------------------------------ pictures
PACK = {"K": "#26262C", "D": "#1F4466", "B": "#2E6A9E", "O": PALETTE[ORANGE], "R": "#D8343C", "S": "#C8C8D0"}
PACK_LAYER = [                                        # body faces of the 64x32 armour layer; arms stay bare
    (20, 16, fill("K..KK..K", 1, 4)),                                  # top: shoulder straps
    (20, 20, [".K....K."] * 4 + [".KKSSKK."] + [".K....K."] * 5 + [".KKKKKK.", "........"]),  # front: harness
    (32, 20, [".K....K.", "DDDDDDDD", "DBBBBBBD", "DBOOOOBD", "DBBBBBBD", "DBBBBBBD", "DBBBBBBD", "DBBBBRBD",
              "DBBBBBBD", "DBBBBBBD", "DDDDDDDD", ".K....K."]),        # back: the pack, ripcord handle
    (16, 20, ["...."] + ["D..."] * 10 + ["...."]),                    # sides: the pack's thickness at the back
    (28, 20, ["...."] + ["...D"] * 10 + ["...."]),
    (28, 16, ["........", "........", "........", "DDDDDDDD"]),       # bottom: the pack's underside
]
ICON = ["........", ".....OOW", "...OOOOW", "..WOOOOW", ".WWWOOOW", ".WWWOOOW", "WWWWOOOW", "L..L...L",
        ".L..L..L", "..L..L.L", "...L.L.L", "....LL.L", ".....LBB", "......BB", "......BR", "......DD"]

def pack_layer():
    return armour_layer(PACK_LAYER, PACK)

def icon():
    return grid(ICON, {**PACK, "W": PALETTE[WHITE], "L": "#3A3733"}, mirror=True)   # dark: inventory slots are grey

def palette_cells(img, x0, y0):
    for i, c in enumerate(PALETTE):
        ImageDraw.Draw(img).rectangle([x0 + i * 4, y0, x0 + i * 4 + 3, y0 + 3], fill=hexc(c))
    return img

# ------------------------------------------------------------------ items
def components(state="closed"):
    model = "family:parachute" if state == "closed" else "family:parachute_open"
    sound = "minecraft:item.armor.equip_leather" if state == "closed" else "minecraft:intentionally_empty"
    return {"minecraft:item_model": model,
            "minecraft:custom_name": {"text": "Parachute", "color": NAME_COLOUR, "italic": False},
            "minecraft:lore": [{"text": "Wear it on your back. Opens when you fall,", "color": "gray", "italic": False},
                               {"text": "or jump in the air. Crouch to fold it.", "color": "gray", "italic": False}],
            "minecraft:equippable": {"slot": "chest", "asset_id": "family:parachute", "equip_sound": sound},
            "minecraft:unbreakable": {},
            "minecraft:custom_data": {"family_parachute": True}}

def gives(give_string):
    return give_string(BASE_ITEM, components())

def open_sound(path, seed=7):
    """Canopy catching air: a noise burst through a falling band-pass, a low thump, a short cloth flutter."""
    def fn(rnd, n):
        bp, out = snd.BandPass(0.7), []
        for i in range(n):
            t = i / snd.RATE
            env = min(1.0, t / 0.012) * math.exp(-t / 0.16)
            flutter = 1 + 0.6 * math.sin(2 * math.pi * 23 * t) * math.exp(-t / 0.25)
            noise = bp(rnd.uniform(-1, 1), 2600 * math.exp(-t / 0.09) + 300)
            thump = math.sin(2 * math.pi * (70 - 30 * t) * t) * math.exp(-t / 0.07) * min(1.0, t / 0.005)
            out.append(env * flutter * noise * 1.2 + 0.8 * thump)
        return out
    snd.render(path, 0.7, fn, seed)

def ogg(dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        open_sound(f"{tmp}/o.wav")
        subprocess.run(["oggenc", "-Q", "-q", "5", "-s", "3001", "-o", dest, f"{tmp}/o.wav"], check=True)

# ------------------------------------------------------------------ Java resource pack
def java(a, put):
    """Returns sounds.json entries (minecraft namespace, so Geyser passes the name to Bedrock unchanged)."""
    for n in ("parachute", "parachute_open"):                 # same picture closed and open
        put(f"{a}/family/items/{n}.json", {"model": {"type": "minecraft:model", "model": "family:item/parachute"}})
    put(f"{a}/family/models/item/parachute.json",
        {"parent": "minecraft:item/generated", "textures": {"layer0": "family:item/parachute"}})
    icon().save(f"{a}/family/textures/item/parachute.png")
    put(f"{a}/family/equipment/parachute.json", {"layers": {"humanoid": [{"texture": "family:parachute"}]}})
    os.makedirs(f"{a}/family/textures/entity/equipment/humanoid", exist_ok=True)
    pack_layer().save(f"{a}/family/textures/entity/equipment/humanoid/parachute.png")
    # canopy (on the item display): 0.5 model units per px, shown at scale 2
    to_model = lambda x, y, z: [8 + x / 2, 8 + (y - JAVA_Y0) / 2, 8 + z / 2]
    els = []
    for x0, y0, z0, x1, y1, z1, c in boxes():
        uv = [c * 4 + 1, 1, c * 4 + 3, 3]
        els.append({"from": to_model(x0, y0, z0), "to": to_model(x1, y1, z1),
                    "faces": {f: {"uv": uv, "texture": "#palette"} for f in ("north", "south", "east", "west", "up", "down")}})
    put(f"{a}/family/items/parachute_canopy.json", {"model": {"type": "minecraft:model", "model": "family:item/parachute_canopy"}})
    put(f"{a}/family/models/item/parachute_canopy.json", {
        "textures": {"palette": "family:item/parachute_palette", "particle": "family:item/parachute_palette"},
        "elements": els})
    palette_cells(Image.new("RGBA", (16, 16), (0, 0, 0, 0)), 0, 0).save(f"{a}/family/textures/item/parachute_palette.png")
    ogg(f"{a}/family/sounds/parachute/open.ogg")
    return {OPEN_SOUND: {"sounds": ["family:parachute/open"]}}

# ------------------------------------------------------------------ Bedrock pack
def bedrock(b, put):
    """Writes the attachables, armour textures, canopy geometry and sound; returns (item icons, sound definitions).
    Closed: Mojang's chestplate geometry, the same setup as the costumes. Open: the chestplate's body cube plus the
    canopy in a child bone of `body` (Bedrock wiki "Method 1": bones named like the player's follow them).
    Neither hides the player's jacket layer (the pack covers only the back)."""
    os.makedirs(f"{b}/textures/models/armor", exist_ok=True)
    pack_layer().save(f"{b}/textures/models/armor/family_parachute.png")
    tex = Image.new("RGBA", (64, 64), (0, 0, 0, 0)); tex.paste(pack_layer(), (0, 0))
    palette_cells(tex, 0, 32).save(f"{b}/textures/models/armor/family_parachute_open.png")
    for name, texture, geometry in (("parachute", "family_parachute", "geometry.humanoid.armor.chestplate"),
                                    ("parachute_open", "family_parachute_open", "geometry.family_parachute_open")):
        put(f"{b}/attachables/{name}.json", {"format_version": "1.8.0", "minecraft:attachable": {"description": {
            "identifier": f"family:{name}",
            "materials": {"default": "armor", "enchanted": "armor_enchanted"},
            "textures": {"default": f"textures/models/armor/{texture}", "enchanted": "textures/misc/enchanted_actor_glint"},
            "geometry": {"default": geometry},
            "render_controllers": ["controller.render.armor"]}}})
    face = lambda c: {f: {"uv": [c * 4 + 1, 33], "uv_size": [2, 2]} for f in ("north", "south", "east", "west", "up", "down")}
    canopy = [{"origin": [x0, y0, z0], "size": [x1 - x0, y1 - y0, z1 - z0], "uv": face(c)}
              for x0, y0, z0, x1, y1, z1, c in boxes()]
    put(f"{b}/models/entity/family_parachute.geo.json", {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.family_parachute_open", "texture_width": 64, "texture_height": 64,
                        "visible_bounds_width": 5, "visible_bounds_height": 6, "visible_bounds_offset": [0, 2.5, 0]},
        "bones": [{"name": "body", "pivot": [0, 24, 0],
                   "cubes": [{"origin": [-4, 12, -2], "size": [8, 12, 4], "uv": [16, 16], "inflate": 1.01}]},
                  {"name": "parachute", "parent": "body", "pivot": [0, 24, 0], "cubes": canopy}]}]})
    ogg(f"{b}/sounds/family/parachute/open.ogg")
    return ({"family_parachute": icon()},
            {OPEN_SOUND: {"category": "player", "max_distance": 24.0, "sounds": ["sounds/family/parachute/open"]}})

def mappings():
    """Geyser (format 2): closed and open are separate Bedrock items, one per item_model; both use the same icon."""
    return {BASE_ITEM: [{"bedrock_identifier": f"family:{n}", "model": f"family:{n}",
                         "bedrock_options": {"icons": {"default": "family_parachute"}}}
                        for n in ("parachute", "parachute_open")]}

# ------------------------------------------------------------------ Datapack
def mcf(*lines):
    return "\n".join(lines) + "\n"

def datapack(data, put, give_string):
    d = f"{data}/data/family"; f = f"{d}/function/parachute"; p = f"{d}/predicate/parachute"
    put(f"{d}/function/give/parachute.mcfunction", f"give @s {gives(give_string)}\n")
    put(f"{d}/recipe/parachute.json", {                       # wool canopy, string lines, leather pack
        "type": "minecraft:crafting_shaped", "category": "equipment", "pattern": ["WWW", "S S", " L "],
        "key": {"W": "#minecraft:wool", "S": "minecraft:string", "L": "minecraft:leather"},
        "result": {"id": BASE_ITEM, "components": components()}})
    put(f"{d}/advancement/unlock_parachute.json", {           # in every recipe book from the first join
        "criteria": {"joined": {"trigger": "minecraft:tick"}}, "rewards": {"recipes": ["family:parachute"]}})
    for state in ("open", "closed"):
        c = components(state)
        put(f"{d}/item_modifier/parachute/{'fold' if state == 'closed' else 'open'}.json", {
            "type": "minecraft:set_components",
            "components": {k: c[k] for k in ("minecraft:item_model", "minecraft:equippable")}})

    me = lambda pred: {"type": "minecraft:entity_properties", "entity": "this", "predicate": pred}
    player = lambda **kw: me({"minecraft:type_specific/player": kw})
    ref = lambda n: {"type": "minecraft:reference", "name": f"family:parachute/{n}"}
    fluid = {"type": "minecraft:any_of", "terms": [
        {"type": "minecraft:location_check", "predicate": {"fluid": {"fluids": f"#minecraft:{t}"}}} for t in ("water", "lava")]}
    put(f"{p}/in_fluid.json", fluid)                          # at the feet (functions run at @s)
    put(f"{p}/landed.json", {"type": "minecraft:any_of", "terms": [
        me({"minecraft:flags": {"is_on_ground": True}}), me({"minecraft:flags": {"is_flying": True}}),
        me({"minecraft:flags": {"is_swimming": True}}), me({"minecraft:vehicle": {}}), ref("in_fluid")]})
    put(f"{p}/can_open.json", {"type": "minecraft:all_of", "terms": [
        {"type": "minecraft:inverted", "term": ref("landed")}, player(gamemode=["survival", "adventure", "creative"])]})
    put(f"{p}/should_close.json", {"type": "minecraft:any_of", "terms": [
        ref("landed"), player(input={"sneak": True}), player(gamemode=["spectator"])]})
    put(f"{p}/sneak.json", player(input={"sneak": True}))
    put(f"{p}/jump.json", player(input={"jump": True}))
    put(f"{p}/fall_far.json", me({"minecraft:movement": {"fall_distance": {"min": 4}}}))
    put(f"{p}/falling.json", me({"minecraft:movement": {"fall_distance": {"min": 1}}}))
    put(f"{p}/too_fast.json", me({"minecraft:movement": {"y": {"max": -5}}}))       # blocks per second
    put(f"{p}/gentle.json", me({"minecraft:movement": {"y": {"min": -3}}}))
    put(f"{p}/drifting.json", me({"minecraft:effects": {"minecraft:slow_falling": {"duration": {"min": 15}}}}))
    # ours are short: a potion's slow falling or a shulker's levitation (minutes / 10 s) is never cleared
    put(f"{p}/our_slow_fall.json", me({"minecraft:effects": {"minecraft:slow_falling": {"duration": {"max": 40}}}}))
    put(f"{p}/braking.json", me({"minecraft:effects": {"minecraft:levitation": {"duration": {"max": 20}}}}))
    put(f"{p}/riding.json", me({"minecraft:vehicle": {}}))

    worn = "armor.chest *[minecraft:custom_data~{family_parachute:1b}]"
    canopy_item = '{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"family:parachute_canopy"}}'
    transform = lambda s, y: (f"transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],"
                              f"translation:[0f,{y}f,0f],scale:[{s}f,{s}f,{s}f]}}")
    put(f"{f}/tick.mcfunction", mcf(
        # Skript has had a tick to mount last tick's canopy; any canopy without a rider by now goes
        "execute as @e[type=minecraft:item_display,tag=family.canopy] unless predicate family:parachute/riding run kill @s",
        "execute as @e[type=minecraft:item_display,tag=family.canopy_grow] run function family:parachute/grow",
        "tag @a remove family.chute_mount",
        f"execute as @a[tag=family.chute_open] unless items entity @s {worn} at @s run function family:parachute/close",
        f"execute as @a if items entity @s {worn} at @s run function family:parachute/worn"))
    put(f"{f}/grow.mcfunction", mcf(                          # pops open over 5 ticks (PC)
        "tag @s remove family.canopy_grow",
        f"data merge entity @s {{start_interpolation:0,interpolation_duration:5,{transform(CANOPY_SCALE, CANOPY_Y)}}}"))
    put(f"{f}/worn.mcfunction", mcf(          # the jump tag remembers last tick's jump, so a press is a fresh one
        "execute if entity @s[tag=family.chute_open] run function family:parachute/drift",
        "execute if entity @s[tag=!family.chute_open] run function family:parachute/closed",
        "execute if predicate family:parachute/jump run return run tag @s add family.chute_jump",
        "tag @s remove family.chute_jump"))
    put(f"{f}/closed.mcfunction", mcf(        # an item that was taken off while open shows open: fold it
        "execute if items entity @s armor.chest *[minecraft:item_model=\"family:parachute_open\"] run item modify entity @s armor.chest family:parachute/fold",
        "execute if predicate family:parachute/landed run tag @s remove family.chute_folded",
        "execute if predicate family:parachute/can_open if block ~ ~-1 ~ #minecraft:air if block ~ ~-2 ~ #minecraft:air "
        "if block ~ ~-3 ~ #minecraft:air run function family:parachute/try_open"))
    put(f"{f}/try_open.mcfunction", mcf(                      # 3 blocks of air below: worth opening
        "execute if entity @s[tag=!family.chute_folded] if predicate family:parachute/fall_far run return run function family:parachute/open",
        "execute if entity @s[tag=!family.chute_jump] if predicate family:parachute/jump if predicate family:parachute/falling run function family:parachute/open"))
    put(f"{f}/open.mcfunction", mcf(
        "tag @s add family.chute_open",
        "tag @s remove family.chute_folded",
        "item modify entity @s armor.chest family:parachute/open",
        "effect give @s minecraft:slow_falling 2 0 true",
        f"playsound minecraft:{OPEN_SOUND} player @a ~ ~ ~ 1 1",
        f'summon minecraft:item_display ~ ~1.8 ~ {{Tags:["family.canopy","family.canopy_new","family.canopy_grow"],'
        f'item:{canopy_item},item_display:"none",{transform(0.3, -0.2)}}}',
        "tag @s add family.chute_mount",
        f'title @s actionbar {{"text": "Parachute open! Crouch to fold it.", "color": "{NAME_COLOUR}"}}'))
    put(f"{f}/drift.mcfunction", mcf(
        "execute if predicate family:parachute/should_close run return run function family:parachute/close",
        "execute unless predicate family:parachute/drifting run effect give @s minecraft:slow_falling 2 0 true",
        "execute if predicate family:parachute/too_fast run tag @s add family.chute_brake",
        "execute if predicate family:parachute/gentle run tag @s remove family.chute_brake",
        "execute if entity @s[tag=family.chute_brake] unless predicate family:parachute/braking run effect give @s minecraft:levitation 1 0 true",
        "execute if entity @s[tag=!family.chute_brake] if predicate family:parachute/braking run effect clear @s minecraft:levitation"))
    put(f"{f}/close.mcfunction", mcf(
        "tag @s remove family.chute_open",
        "tag @s remove family.chute_brake",
        "execute if predicate family:parachute/sneak unless predicate family:parachute/landed run tag @s add family.chute_folded",
        f"execute if items entity @s {worn} run item modify entity @s armor.chest family:parachute/fold",
        "execute if predicate family:parachute/braking run effect clear @s minecraft:levitation",
        "execute if predicate family:parachute/our_slow_fall run effect clear @s minecraft:slow_falling",
        "execute on passengers if entity @s[type=minecraft:item_display,tag=family.canopy] run kill @s"))

# ------------------------------------------------------------------ preview (python3 parachute.py)
def preview():
    """previews/parachute.png: icon, the pack on a kid (front/back), the open parachute in 3D;
    previews/parachute-open.m4a: the opening sound (macOS afconvert)."""
    from PIL import ImageFont
    from undersea_art import base_skin, doll
    os.makedirs("previews", exist_ok=True)
    font = ImageFont.load_default(size=16)
    kid = [(-4, 24, -4, 4, 32, 4, "#E0AC8C"), (-4, 12, -2, 4, 24, 2, "#2FA4A0"), (-8, 12, -2, -4, 24, 2, "#2FA4A0"),
           (4, 12, -2, 8, 24, 2, "#2FA4A0"), (-4, 0, -2, 0, 12, 2, "#2B3A67"), (0, 0, -2, 4, 12, 2, "#2B3A67"),
           (-3, 13, 2, 3, 22, 3.5, PACK["B"])]                # pack on the back (+z, toward the viewer)
    canopy = [(*b[:6], PALETTE[b[6]]) for b in boxes()]
    def iso(img, ox, oy, items, S, below=False):
        """Isometric boxes, painter's order. Camera at +x +z, above (or below: near parts drawn higher)."""
        dr = ImageDraw.Draw(img); k = -1 if below else 1
        P = lambda x, y, z: (ox + (x - z) * 0.866 * S, oy + (k * (x + z) * 0.5 - y) * S)
        for x0, y0, z0, x1, y1, z1, col in sorted(items, key=lambda b: b[0] + b[3] + b[2] + b[5] + k * (b[1] + b[4])):
            sh = lambda f: tuple(round(v * f) for v in hexc(col)[:3])
            yf = y0 if below else y1                          # the bottom or the top face
            dr.polygon([P(x0, yf, z0), P(x1, yf, z0), P(x1, yf, z1), P(x0, yf, z1)], fill=sh(0.55 if below else 1.0))
            dr.polygon([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], fill=sh(0.82))
            dr.polygon([P(x1, y0, z0), P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0)], fill=sh(0.66))
    W, H = 1520, 960
    sheet = Image.new("RGBA", (W, H), "#26262E"); dr = ImageDraw.Draw(sheet)
    titles = [(20, "Item (PC and iPad)"), (230, "Folded, worn on the back (front / back)"),
              (560, "Open: the canopy above the kid"), (1130, "Seen from below (hollow)")]
    for x, t in titles:
        dr.text((x, 14), t, fill="#BBBBC8", font=font)
    on_grey = lambda img: Image.alpha_composite(Image.new("RGBA", img.size, (139, 139, 139, 255)), img)
    sheet.paste(on_grey(icon()).resize((160, 160), Image.NEAREST), (20, 50))
    layer = pack_layer()
    for i, view in enumerate(("front", "back")):
        img = doll(base_skin(), view); img.alpha_composite(doll(layer, view))
        sheet.alpha_composite(img.resize((16 * 10, 32 * 10), Image.NEAREST), (230 + i * 190, 50))
    iso(sheet, 820, 650, kid + canopy, 6)
    iso(sheet, 1310, 450, canopy, 4, below=True)
    notes = ["Opens by itself after falling 4 blocks (needs 3 blocks of air below), or with jump in mid-air.",
             "Crouch folds it; it packs itself up on landing, in water or when flying.",
             "Floats down at about 3 blocks a second (one gentle tug every ~2 s holds the speed).",
             "PC: the canopy pops open over a quarter second. iPad: it appears at once; your own canopy",
             "only shows to you in third-person view, but you see everyone else's."]
    for i, t in enumerate(notes):
        dr.text((20, 830 + 24 * i), t, fill="#DDDDE6", font=font)
    sheet.save("previews/parachute.png")
    with tempfile.TemporaryDirectory() as tmp:
        open_sound(f"{tmp}/o.wav")
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", f"{tmp}/o.wav", "previews/parachute-open.m4a"], check=True)

if __name__ == "__main__":
    preview()
