"""Elemental katanas: Flame, Water, Thunder and Wind (original designs, diamond-sword strength).
build.py calls java(), bedrock(), mappings(), datapack() and gives(); art in katana_art.py, sounds in katana_sounds.py.

- Swing (left-click): the Skript script skript/family-katana.sk tags the player on every left-click at air or
  a block (a datapack can't see those); our tick function then draws that katana's arc. Hitting a mob or
  player draws the arc too, via a player_hurt_entity advancement.
- Special move (hold use): the item is "eaten" forever (consumable, 1000 s, no animation, silent), so a
  using_item advancement fires; the move animates over a few ticks, hurts hostile mobs only and pushes
  players (0.01 damage, no armour wear). A scoreboard cooldown stops spamming: use_cooldown would only
  start when a use finishes, and finishing would use the sword up.
Particles in arcs are drawn in the player's view: ^left ^up ^forward from the eyes, level (yaw only),
except the Wind spiral, which follows where you look."""
import functools, math, os, shutil, subprocess, tempfile
import katana_art as art, katana_sounds as snd

# element -> name, colour, recipe item, special move, swing (Java type, ticks), special-move swing
KATANAS = {
    "flame":   dict(name="Flame Katana", colour="#FF7A1A", ingredient="blaze_powder", move="Ember Crescent",
                    swing=("whack", 8), special=("whack", 10)),
    "water":   dict(name="Water Katana", colour="#3FA9FF", ingredient="prismarine_crystals", move="Tide Ribbon",
                    swing=("whack", 9), special=("whack", 12)),
    "thunder": dict(name="Thunder Katana", colour="#FFD23A", ingredient="copper_ingot", move="Storm Strike",
                    swing=("stab", 5), special=("whack", 7)),
    "wind":    dict(name="Wind Katana", colour="#6FF2C0", ingredient="feather", move="Gale Spiral",
                    swing=("whack", 5), special=("stab", 6)),
}
COOLDOWN, SWING_COOLDOWN = 60, 4          # ticks
SPECIAL_DAMAGE, PUSH_DAMAGE = 6, 0.01     # hostile mobs / players (just enough for a knockback)
# Special moves only ever hurt these (26.3 ids). Never pets, villagers, animals, armour stands,
# item frames, boats or minecarts. Neutral mobs (endermen, piglins) are left alone too.
HOSTILE = ["blaze", "bogged", "breeze", "cave_spider", "creaking", "creeper", "drowned", "elder_guardian",
           "ender_dragon", "endermite", "evoker", "ghast", "guardian", "hoglin", "husk", "illusioner",
           "magma_cube", "parched", "phantom", "piglin_brute", "pillager", "ravager", "shulker", "silverfish",
           "skeleton", "slime", "spider", "stray", "vex", "vindicator", "warden", "witch", "wither",
           "wither_skeleton", "zoglin", "zombie", "zombie_nautilus", "zombie_villager"]

def components(el):
    k = KATANAS[el]; kind, ticks = k["swing"]
    return {"minecraft:item_model": f"family:katana_{el}",
            "minecraft:custom_name": {"text": k["name"], "color": k["colour"], "italic": False},
            "minecraft:lore": [{"text": f"Special move: {k['move']}", "color": "gray", "italic": False},
                               {"text": "Hold use to unleash it", "color": "dark_gray", "italic": False}],
            "minecraft:attack_animation": {"type": kind, "duration": ticks},
            "minecraft:consumable": {"consume_seconds": 1000, "animation": "none", "has_consume_particles": False,
                                     "sound": "minecraft:intentionally_empty"},
            "minecraft:use_effects": {"can_sprint": True, "speed_multiplier": 1.0},
            "minecraft:custom_data": {"family_katana": el}}

def sound_names(el):
    return f"family.katana_{el}_swing", f"family.katana_{el}_special"

@functools.cache
def sound_files():
    """Renders every katana sound once per build: {name without extension: .ogg path}.
    The temporary folder lives as long as this cached result (removed when the build exits)."""
    global _sound_dir
    _sound_dir = tempfile.TemporaryDirectory(prefix="katana-sounds-")
    tmp = _sound_dir.name; out = {}
    for i, el in enumerate(KATANAS):
        jobs = [(f"{el}_swing{v}", "swing", 10 * i + v) for v in range(1, snd.SWING_VARIANTS + 1)]
        for name, kind, seed in jobs + [(f"{el}_special", "special", 10 * i + 9)]:
            snd.make(el, kind, f"{tmp}/{name}.wav", seed)
            subprocess.run(["oggenc", "-Q", "-q", "5", "-s", str(2000 + seed), "-o", f"{tmp}/{name}.ogg",
                            f"{tmp}/{name}.wav"], check=True)
            out[name] = f"{tmp}/{name}.ogg"
    return out

def copy_sounds(dest):
    os.makedirs(dest, exist_ok=True)
    for name, path in sound_files().items():
        shutil.copyfile(path, f"{dest}/{name}.ogg")

# ------------------------------------------------------------------ Java resource pack
def java(a, put, display):
    """Hilt = normal handheld item; blade = full-bright panel with an animated texture (like the lightsabers).
    Returns sounds.json entries (minecraft namespace, so Geyser passes the names to Bedrock unchanged)."""
    for el in KATANAS:
        n = f"katana_{el}"
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
            "display": display})
        art.draw(el, "hilt").save(f"{a}/family/textures/item/{n}_hilt.png")
        art.blade_strip(el).save(f"{a}/family/textures/item/{n}_blade.png")
        put(f"{a}/family/textures/item/{n}_blade.png.mcmeta", {"animation": {"frametime": 2}})
    copy_sounds(f"{a}/family/sounds/katana")
    entries = {}
    for el in KATANAS:
        swing, special = sound_names(el)
        entries[swing] = {"sounds": [f"family:katana/{el}_swing{v}" for v in range(1, snd.SWING_VARIANTS + 1)]}
        entries[special] = {"sounds": [f"family:katana/{el}_special"]}
    return entries

# ------------------------------------------------------------------ Bedrock pack
def bedrock(b, put):
    """Copies sounds; returns (item icons, sound definitions). The in-hand models are in build.py."""
    copy_sounds(f"{b}/sounds/family/katana")
    defs = {}
    for el in KATANAS:
        swing, special = sound_names(el)
        defs[swing] = {"category": "player", "max_distance": 24.0,
                       "sounds": [f"sounds/family/katana/{el}_swing{v}" for v in range(1, snd.SWING_VARIANTS + 1)]}
        defs[special] = {"category": "player", "max_distance": 32.0, "sounds": [f"sounds/family/katana/{el}_special"]}
    return {f"family_katana_{el}": art.bedrock_icon(el) for el in KATANAS}, defs

def mappings():
    """Geyser (format 2) entries for minecraft:diamond_sword. Bedrock only gets the swing's length
    (Geyser drops whack/stab), and needs the item to be usable to send a use when you tap/hold."""
    return [{"bedrock_identifier": f"family:katana_{el}", "model": f"family:katana_{el}",
             "bedrock_options": {"icons": {"default": f"family_katana_{el}"}, "display_handheld": True},
             "components": {"minecraft:consumable": {"consume_seconds": 1000, "animation": "none"},
                            "minecraft:use_effects": {"speed_multiplier": 1.0},
                            "minecraft:attack_animation": {"duration": KATANAS[el]["swing"][1]}}}
            for el in KATANAS]

def gives(give_string):
    return {el: give_string("minecraft:diamond_sword", components(el)) for el in KATANAS}

# ------------------------------------------------------------------ arcs (particle commands)
def dust(hex_colour, scale):
    r, g, b = (int(hex_colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return f"minecraft:dust{{color:[{r:.2f},{g:.2f},{b:.2f}],scale:{scale}}}"

def pt(particle, x, y, z, spread=0.03, speed=0.0, count=1):
    return f"particle {particle} ^{x:.2f} ^{y:.2f} ^{z:.2f} {spread} {spread} {spread} {speed} {count}"

def sweep(r, a0, a1, n, y=lambda f: 0.0):
    """Points on a level arc around the player: a in degrees, -90 = right, +90 = left; f = 0..1 along it."""
    out = []
    for i in range(n):
        f = i / (n - 1); a = math.radians(a0 + (a1 - a0) * f)
        out.append((r * math.sin(a), y(f), r * math.cos(a)))
    return out

def split(points, frames):
    k = math.ceil(len(points) / frames)
    return [points[i * k:(i + 1) * k] for i in range(frames)]

def hurt(cx, cy, cz, radius):
    """Hostile mobs near ^cx ^cy ^cz take damage from the caster; other players are only pushed."""
    at = f"execute positioned ^{cx} ^{cy} ^{cz}"
    return [f"{at} as @e[type=#family:katana_targets,distance=..{radius}] run damage @s {SPECIAL_DAMAGE} "
            "minecraft:player_attack by @p[tag=family.caster]",
            f"{at} as @a[distance=..{radius},tag=!family.caster,gamemode=!spectator] run damage @s {PUSH_DAMAGE} "
            "family:katana_push by @p[tag=family.caster]"]

def special_frames(el):
    """Lists of commands, one list per tick; the caster is tagged family.caster during them."""
    if el == "flame":      # Ember Crescent: a thick fiery crescent rising from low right to high left
        core = sweep(2.0, -75, 75, 18, lambda f: -0.7 + 1.3 * f)
        outer = sweep(2.3, -75, 75, 18, lambda f: -0.6 + 1.3 * f)
        frames = [[pt("minecraft:flame", *p, 0.04, 0.01) for p in c] + [pt(dust("#FF5A1F", 1.6), *p) for p in o]
                  for c, o in zip(split(core, 3), split(outer, 3))]
        frames[1] += hurt(0, -1, 1.8, 2.5)
        frames[2] += [pt("minecraft:lava", *core[-1], 0.15, 0, 3)]
    elif el == "water":    # Tide Ribbon: two strands of a rolling wave sweeping right to left
        a = sweep(2.0, -85, 85, 24, lambda f: -0.4 + 0.25 * math.sin(f * 3 * math.pi))
        b = sweep(2.35, -85, 85, 24, lambda f: -0.4 - 0.25 * math.sin(f * 3 * math.pi))
        frames = [[pt(dust("#3FA9FF", 1.4), *p) for p in pa] + [pt(dust("#C8F4FF", 1.0), *p) for p in pb]
                  + [pt("minecraft:splash", *p, 0.1, 0, 2) for p in pa[::2]]
                  for pa, pb in zip(split(a, 4), split(b, 4))]
        frames[2] += hurt(0, -1, 1.8, 2.6)
    elif el == "thunder":  # Storm Strike: an overhead cut, then a crackling bolt along the ground
        cut = [(0.0, -0.1 + 1.9 * math.cos(math.radians(t)), 0.3 + 1.9 * math.sin(math.radians(t)))
               for t in range(20, 161, 10)]
        bolt = [((0.35 if i % 2 else -0.35), -1.5, 1.5 + 0.4 * i) for i in range(9)]
        frames = [[pt("minecraft:electric_spark", *p, 0.05, 0, 2) for p in half]
                  + [pt(dust("#FFE14D", 1.3), *p) for p in half] + [pt("minecraft:end_rod", *p) for p in half[::3]]
                  for half in split(cut, 2)]
        frames.append([pt("minecraft:electric_spark", *p, 0.1, 0.05, 3) for p in bolt]
                      + [pt(dust("#FFF59A", 1.5), *p) for p in bolt]
                      + [pt("minecraft:firework", *bolt[-1], 0.2, 0.05, 6)] + hurt(0, -1.1, 2.6, 2.4))
    else:                  # Gale Spiral: two strands corkscrewing forward where you look
        def strand(off):
            pts = []
            for i in range(32):
                z = 0.8 + 4.8 * i / 31; ang = 6 * math.pi * i / 31 + off; r = 0.35 + 0.1 * z
                pts.append((r * math.cos(ang), r * math.sin(ang) - 0.25, z))
            return pts
        a, b = strand(0), strand(math.pi)
        frames = [[pt(dust("#EAFFF6", 1.2), *p) for p in pa] + [pt(dust("#6FF2C0", 1.0), *p) for p in pb]
                  for pa, pb in zip(split(a, 4), split(b, 4))]
        frames[1] += [pt("minecraft:sweep_attack", 0, -0.25, 2.0)]
        frames[2] += hurt(0, -1, 2.0, 1.7) + hurt(0, -1, 4.0, 1.9)
        frames[3] += [pt("minecraft:small_gust", 0, -0.25, 5.6)]
    return frames

def swing_arc(el):
    """One tick of particles for an ordinary swing."""
    if el == "flame":
        pts = sweep(1.5, -60, 60, 9, lambda f: -0.6 + 0.8 * f)
        return [pt("minecraft:flame", *p, 0.03, 0.005) for p in pts] + [pt(dust("#FF5A1F", 1.2), *p) for p in pts[1::2]]
    if el == "water":
        pts = sweep(1.6, -65, 65, 10, lambda f: -0.4 + 0.12 * math.sin(f * 3 * math.pi))
        return [pt(dust("#3FA9FF", 1.2), *p) for p in pts] + [pt("minecraft:splash", *p, 0.08, 0, 2) for p in pts[::2]]
    if el == "thunder":
        pts = [(0.0, -0.3, 0.8 + 0.35 * i) for i in range(6)]
        return [pt("minecraft:electric_spark", *p, 0.06, 0.02, 2) for p in pts] + [pt("minecraft:end_rod", *pts[-1])]
    pts = sweep(1.6, -70, 70, 10, lambda f: -0.3)
    return [pt(dust("#EAFFF6" if i % 2 else "#6FF2C0", 1.1), *p) for i, p in enumerate(pts)]

BURSTS = {   # where a hit lands: ^ ^-0.4 ^2 from the eyes
    "flame": ["particle minecraft:flame ~ ~ ~ 0.25 0.25 0.25 0.03 10", "particle minecraft:lava ~ ~ ~ 0.1 0.1 0.1 0 2"],
    "water": ["particle minecraft:splash ~ ~ ~ 0.3 0.3 0.3 0.1 15", f"particle {dust('#3FA9FF', 1.3)} ~ ~ ~ 0.3 0.3 0.3 0 8"],
    "thunder": ["particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.2 12", "particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.3 6"],
    "wind": ["particle minecraft:poof ~ ~ ~ 0.2 0.2 0.2 0.02 5", f"particle {dust('#EAFFF6', 1.2)} ~ ~ ~ 0.3 0.3 0.3 0 8"],
}

# ------------------------------------------------------------------ Datapack
def mcf(*lines):
    return "\n".join(lines) + "\n"

def datapack(data, put, give_string):
    d = f"{data}/data/family"; f = f"{d}/function/katana"
    for el, item in gives(give_string).items():        # console: execute as <player> run function family:give/flame_katana
        put(f"{d}/function/give/{el}_katana.mcfunction", f"give @s {item}\n")
    put(f"{d}/tags/entity_type/katana_targets.json", {"values": [f"minecraft:{m}" for m in HOSTILE]})
    # Push for players: the smallest damage that still knocks back; no armour wear, no difficulty scaling.
    put(f"{d}/damage_type/katana_push.json", {"message_id": "player", "exhaustion": 0.0, "scaling": "never"})
    put(f"{data}/data/minecraft/tags/damage_type/bypasses_armor.json", {"values": ["family:katana_push"]})
    for el, k in KATANAS.items():                      # diamond sword + amethyst shard + element item
        put(f"{d}/recipe/katana_{el}.json", {
            "type": "minecraft:crafting_shapeless", "category": "equipment",
            "ingredients": ["minecraft:diamond_sword", "minecraft:amethyst_shard", f"minecraft:{k['ingredient']}"],
            "result": {"id": "minecraft:diamond_sword", "components": components(el)}})
    put(f"{d}/advancement/unlock_katanas.json", {
        "criteria": {"has_amethyst": {"trigger": "minecraft:inventory_changed",
                                      "conditions": {"items": [{"items": "minecraft:amethyst_shard"}]}}},
        "rewards": {"recipes": [f"family:katana_{el}" for el in KATANAS]}})

    put(f"{f}/load.mcfunction", mcf(*[f"scoreboard objectives add family.{s} dummy" for s in ("kcd", "kswcd", "kfr", "kel")]))
    put(f"{f}/tick.mcfunction", mcf(
        'execute as @a[scores={family.kcd=1}] run title @s actionbar {"text": "Special move ready!", "color": "gray"}',
        "scoreboard players remove @a[scores={family.kcd=1..}] family.kcd 1",
        "scoreboard players remove @a[scores={family.kswcd=1..}] family.kswcd 1",
        "execute as @a[tag=family.swing] at @s run function family:katana/swing",
        "execute as @a[scores={family.kfr=1..}] at @s run function family:katana/frame"))
    holding = lambda el: f'execute if items entity @s weapon.mainhand minecraft:diamond_sword[minecraft:custom_data~{{family_katana:"{el}"}}]'
    put(f"{f}/swing.mcfunction", mcf(                  # tagged by the Skript script on a left-click
        "tag @s remove family.swing",
        "execute if score @s family.kswcd matches 1.. run return 0",
        *[f"{holding(el)} run return run function family:katana/{el}/swing" for el in KATANAS]))
    put(f"{f}/frame.mcfunction", mcf(
        *[f"execute if score @s family.kel matches {i} run function family:katana/{el}/frame" for i, el in enumerate(KATANAS, 1)],
        "scoreboard players remove @s family.kfr 1"))

    for i, (el, k) in enumerate(KATANAS.items(), 1):
        e = f"{f}/{el}"; swing_snd, special_snd = sound_names(el)
        view = "rotated ~ ~" if el == "wind" else "rotated ~ 0"
        here = f"{view} anchored eyes positioned ^ ^ ^"
        item = {"items": "minecraft:diamond_sword", "predicates": {"minecraft:custom_data": f'{{family_katana:"{el}"}}'}}
        put(f"{d}/advancement/katana_use_{el}.json", {
            "criteria": {"use": {"trigger": "minecraft:using_item", "conditions": {"item": item}}},
            "rewards": {"function": f"family:katana/{el}/use"}})
        put(f"{d}/advancement/katana_hit_{el}.json", {
            "criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {"damage": {"type": {
                "direct_entity": {"minecraft:equipment": {"mainhand": item}}}}}}},
            "rewards": {"function": f"family:katana/{el}/hit"}})
        kind, ticks = k["special"]
        frames = special_frames(el)
        put(f"{e}/use.mcfunction", mcf(               # every tick while use is held; cooldown gates it
            f"advancement revoke @s only family:katana_use_{el}",
            "execute if score @s family.kcd matches 1.. run return 0",
            f"scoreboard players set @s family.kcd {COOLDOWN}",
            f"scoreboard players set @s family.kel {i}",
            f"scoreboard players set @s family.kfr {len(frames)}",
            f"swing @s mainhand {kind} {ticks}t",
            f"playsound minecraft:{special_snd} player @a ~ ~ ~ 1 1",
            f'title @s actionbar {{"text": "{k["move"]}!", "color": "{k["colour"]}"}}'))
        put(f"{e}/frame.mcfunction", mcf(
            *[f"execute if score @s family.kfr matches {len(frames) - n} {here} run function family:katana/{el}/f{n + 1}"
              for n in range(len(frames))]))
        for n, cmds in enumerate(frames, 1):
            if any(c.startswith("execute positioned") for c in cmds):
                cmds = ["tag @s add family.caster", *cmds, "tag @s remove family.caster"]
            put(f"{e}/f{n}.mcfunction", mcf(*cmds))
        put(f"{e}/swing.mcfunction", mcf(
            f"scoreboard players set @s family.kswcd {SWING_COOLDOWN}",
            f"playsound minecraft:{swing_snd} player @a ~ ~ ~ 0.8 1",
            f"execute {here} run function family:katana/{el}/arc"))
        put(f"{e}/arc.mcfunction", mcf(*swing_arc(el)))
        put(f"{e}/hit.mcfunction", mcf(               # a melee hit: the swing arc plus a burst where it lands
            f"advancement revoke @s only family:katana_hit_{el}",
            "execute if entity @s[tag=family.caster] run return 0",   # our own special move's damage
            f"function family:katana/{el}/swing",
            f"execute rotated ~ 0 anchored eyes positioned ^ ^-0.4 ^2 run function family:katana/{el}/burst"))
        put(f"{e}/burst.mcfunction", mcf(*BURSTS[el]))

# ------------------------------------------------------------------ previews (python3 katana.py)
def preview():
    """previews/katanas.png (art + move shapes) and previews/katana-sounds-<element>.m4a
    (three swings, then the special move; converted with macOS afconvert, like lightsaber-swings.m4a)."""
    import re, struct, wave
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs("previews", exist_ok=True)
    font, big = ImageFont.load_default(size=15), ImageFont.load_default(size=20)
    W, RH = 1660, 300
    sheet = Image.new("RGBA", (W, 40 + RH * len(KATANAS)), "#26262E"); dr = ImageDraw.Draw(sheet)
    heads = [(20, "Katana"), (250, "PC (Java): in the inventory, 4 of 8 animation frames"), (930, "iPad (Bedrock)"),
             (1150, "Special move from above"), (1410, "from the side (you = dot)")]
    for x, t in heads:
        dr.text((x, 12), t, fill="#BBBBC8", font=font)
    num = re.compile(r"\^(-?[\d.]+) \^(-?[\d.]+) \^(-?[\d.]+)")
    for row, (el, k) in enumerate(KATANAS.items()):
        y0 = 40 + row * RH
        dr.text((20, y0 + 20), k["name"], fill=k["colour"], font=big)
        kind, ticks = k["swing"]
        for i, line in enumerate([f"Special: {k['move']}", f"Craft: diamond sword + amethyst", f"   + {k['ingredient'].replace('_', ' ')}",
                                  f"PC swing: {kind}, {ticks} ticks", f"iPad swing: {ticks} ticks"]):
            dr.text((20, y0 + 60 + 22 * i), line, fill="#DDDDE6", font=font)
        for i, frame in enumerate((0, 2, 4, 6)):
            img = Image.new("RGBA", (32, 32), (139, 139, 139, 255))
            img.alpha_composite(art.draw(el, "hilt")); img.alpha_composite(art.draw(el, "blade", frame))
            sheet.paste(img.resize((160, 160), Image.NEAREST), (250 + i * 168, y0 + 20))
        bed = Image.new("RGBA", (32, 32), (49, 49, 58, 255)); bed.alpha_composite(art.bedrock_icon(el))
        sheet.paste(bed.resize((200, 200), Image.NEAREST), (930, y0 + 20))
        frames = special_frames(el)
        for view, x0 in (("top", 1150), ("side", 1410)):
            box = (x0, y0 + 20, x0 + 240, y0 + 260)
            dr.rectangle(box, outline="#55556A")
            scale = 34
            cx, cy = (x0 + 120, y0 + 230) if view == "top" else (x0 + 30, y0 + 120)
            dr.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill="#FFFFFF")
            for n, cmds in enumerate(frames):
                shadeit = 0.45 + 0.55 * n / max(1, len(frames) - 1)       # later ticks drawn brighter
                col = tuple(round(c * shadeit) for c in (int(k["colour"][1:3], 16), int(k["colour"][3:5], 16), int(k["colour"][5:7], 16)))
                for c in cmds:
                    m = num.search(c)
                    if not m or not c.startswith("particle"):
                        continue
                    x, yy, z = map(float, m.groups())
                    px, py = (cx - x * scale, cy - z * scale) if view == "top" else (cx + z * scale, cy - yy * scale)
                    dr.ellipse((px - 3, py - 3, px + 3, py + 3), fill=col)
        dr.text((1150, y0 + 266), "dim = first tick, bright = last tick", fill="#888896", font=font)
    sheet.save("previews/katanas.png")
    for el in KATANAS:                      # sound preview: swing, swing, swing, special
        rnd = __import__("random").Random(7)
        gap = [0.0] * int(0.35 * snd.RATE)
        parts = []
        for v in range(3):
            parts += snd.swing(el, __import__("random").Random(v + 1), int(snd.SWING_SECONDS * snd.RATE)) + gap
        parts += gap + snd.special(el, rnd, int(snd.special_seconds(el) * snd.RATE))
        m = max(abs(x) for x in parts) or 1
        with tempfile.TemporaryDirectory() as tmp:
            with wave.open(f"{tmp}/p.wav", "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(snd.RATE)
                w.writeframes(b"".join(struct.pack("<h", int(x / m * 0.89 * 32767)) for x in parts))
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", f"{tmp}/p.wav",
                            f"previews/katana-sounds-{el}.m4a"], check=True)

if __name__ == "__main__":
    preview()
