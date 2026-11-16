"""Costume ring: a free wardrobe around the Undersea hub, where everyone arrives. Eight armour stands
wear the costumes on the edge of the hub's sand ring, two in each corner between the streets, facing
the hub. Stepping onto the glowing pad in front of one gives that costume's pieces you don't already
have (in your inventory or worn), so it never hands out duplicates.
The town square's four benches stood where the pads go, so the build removes them (spruce stairs only).
Coordinates are relative to the hub centre, like town.py.
  python3 wardrobe.py -> previews/wardrobe.png
  build.py            -> family:undersea/wardrobe/*  (admin runs family:undersea/build_wardrobe; safe to re-run)"""
import json, math, os
import town, undersea
from town import M

PAD = M + "pearlescent_froglight"        # not a sea lantern: the hub floor already has those
SPOTS = [(5, -9), (9, -5), (9, 5), (5, 9), (-5, 9), (-9, 5), (-9, -5), (-5, -9)]   # clockwise from north-east

def stands():
    """(x, z, pad (x, z), yaw towards the hub, costume, title, colour), in COSTUMES order around the ring."""
    out = []
    for (x, z), (c, (colour, _, names)) in zip(SPOTS, undersea.COSTUMES.items()):
        pad = (x - (x > 0) + (x < 0), z) if abs(x) == 9 else (x, z - (z > 0) + (z < 0))
        out.append((x, z, pad, round(math.degrees(math.atan2(x, -z)), 1), c, names[0][1].rsplit(" ", 1)[0], colour))
    return out

def stand_nbt(costume, title, colour, yaw):
    eq = {}
    for c, slot, piece, name in undersea.pieces():
        if c == costume:
            eq[slot] = {"id": f"minecraft:{undersea.SLOTS[slot][0]}", "count": 1,
                        "components": undersea.costume_components(c, slot, piece, name)}
    return json.dumps({"Tags": ["family.wardrobe"], "Rotation": "R", "NoGravity": True, "Invulnerable": True,
                       "DisabledSlots": 4144959, "ShowArms": True, "NoBasePlate": True,
                       "CustomName": {"text": title, "color": colour}, "CustomNameVisible": True, "equipment": eq}
                      ).replace('"Rotation": "R"', f"Rotation: [{yaw}f, 0f]")

def datapack(data, put, give_string):
    hx, hy, hz = undersea.HUB_X, undersea.HUB_Y, undersea.HUB_Z
    dim, f = undersea.DIM, f"{data}/data/family/function/undersea/wardrobe"
    in_sea = f"execute in {dim} run "
    put(f"{f}/load.mcfunction", "scoreboard objectives add family.pad dummy\nscoreboard objectives add family.lastpad dummy\n")
    # Every tick: which pad is each player on (0 = none)? Only a change of pad hands anything out,
    # so standing on a pad doesn't repeat; stepping back on only gives pieces that went missing.
    put(f"{f}/tick.mcfunction", "\n".join(
        ["scoreboard players set @a family.pad 0"]
        + [f"{in_sea}scoreboard players set @a[x={hx + px},y={hy + 1},z={hz + pz},dx=0,dy=1,dz=0] family.pad {i}"
           for i, (_, _, (px, pz), *_) in enumerate(stands(), 1)]
        + ["execute as @a unless score @s family.pad = @s family.lastpad run function family:undersea/wardrobe/step"]) + "\n")
    put(f"{f}/step.mcfunction", "\n".join(
        ["scoreboard players operation @s family.lastpad = @s family.pad"]
        + [f"execute if score @s family.pad matches {i} run return run function family:undersea/wardrobe/{s[4]}"
           for i, s in enumerate(stands(), 1)]) + "\n")
    for *_, costume, title, colour in stands():
        lines = []
        for c, slot, piece, name in undersea.pieces():
            if c == costume:
                item = f"minecraft:{undersea.SLOTS[slot][0]}"
                has = f'{item}[minecraft:custom_data~{{family_costume:"{c}"}}]'
                lines.append(f"execute unless items entity @s container.* {has} unless items entity @s armor.* {has} "
                             f"run give @s {give_string(item, undersea.costume_components(c, slot, piece, name))}")
        lines += [f'title @s actionbar {{"text": "{title} costume! It\'s in your inventory.", "color": "{colour}"}}',
                  "playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 0.8"]
        put(f"{f}/{costume}.mcfunction", "\n".join(lines) + "\n")
    # Build: load the hub area, then benches out (only spruce stairs), pads in, stands (re)placed.
    area = f"{hx - 10} {hz - 10} {hx + 10} {hz + 10}"
    put(f"{data}/data/family/function/undersea/build_wardrobe.mcfunction",
        f"{in_sea}forceload add {area}\nschedule function family:undersea/wardrobe/build 3s replace\n")
    put(f"{f}/build.mcfunction", "\n".join(
        [f"execute in {dim} unless loaded {hx - 10} {hy} {hz - 10} run return run schedule function family:undersea/wardrobe/build 2s replace",
         f"execute in {dim} unless loaded {hx + 10} {hy} {hz + 10} run return run schedule function family:undersea/wardrobe/build 2s replace",
         f"{in_sea}kill @e[type=minecraft:armor_stand,tag=family.wardrobe]"]
        + [f"{in_sea}fill {hx + x1} {hy + 1} {hz + z} {hx + x2} {hy + 1} {hz + z} minecraft:water replace minecraft:spruce_stairs"
           for z in (-8, 8) for x1, x2 in ((-6, -4), (4, 6))]
        + [f"{in_sea}setblock {hx + px} {hy} {hz + pz} {PAD}" for _, _, (px, pz), *_ in stands()]
        + [f"{in_sea}summon minecraft:armor_stand {hx + x + 0.5} {hy + 1} {hz + z + 0.5} {stand_nbt(c, t, col, yaw)}"
           for x, z, _, yaw, c, t, col in stands()]
        + [f"{in_sea}forceload remove {area}"]) + "\n")

def preview():
    """previews/wardrobe.png: the hub from above and in close-up, stands drawn as coloured figures."""
    from PIL import Image, ImageDraw, ImageFont
    t = town.build()
    R = 14
    v = {p: b for p, b in t.v.items() if abs(p[0]) <= R and abs(p[2]) <= R}
    for x in range(-R, R + 1):                       # ground: hub platform, sand ring and cleared town sand
        for z in range(-R, R + 1):
            v.setdefault((x, 0, z), town.SAND)
            v[(x, -1, z)] = town.SANDSTONE
    for x in range(-5, 6):
        for z in range(-5, 6):
            v[(x, 0, z)] = M + ("sea_lantern" if x in (-5, 0, 5) and z in (-5, 0, 5) else "prismarine_bricks")
    v[(0, 0, 0)] = M + "soul_sand"
    for px in (-2, 2):
        for pz in (-2, 2):
            for y in (1, 2, 3):
                v[(px, y, pz)] = M + "dark_prismarine"
            v[(px, 4, pz)] = M + "sea_lantern"
    v[(5, 0, 5)], v[(5, 1, 5)] = M + "beacon", M + "light_blue_stained_glass"
    town.COLOURS.update({"prismarine_bricks": "#63AB9F", "dark_prismarine": "#335B4C", "soul_sand": "#51402F",
                         "beacon": "#7FE8E0"})
    for x, z, (px, pz), _, c, _, col in stands():
        v[(px, 0, pz)] = PAD
        town.COLOURS[f"stand_{c}"] = col
        for y in (1, 2, 3):
            v[(x, y, z)] = M + f"stand_{c}"
    font, big = ImageFont.load_default(size=15), ImageFont.load_default(size=18)
    k = 22                                            # top-down, north up
    top = {}
    for (x, y, z), b in v.items():
        if town.colour(b) and ((x, z) not in top or y > top[(x, z)][0]):
            top[(x, z)] = (y, town.colour(b))
    m = Image.new("RGB", ((2 * R + 1) * k, (2 * R + 1) * k), (24, 70, 84)); d = ImageDraw.Draw(m)
    for (x, z), (y, c) in top.items():
        d.rectangle([(x + R) * k, (z + R) * k, (x + R + 1) * k - 1, (z + R + 1) * k - 1], fill=town.shade(c, 0.85 + 0.03 * min(y, 5)))
    for x, z, (px, pz), _, c, title, col in stands():
        w = d.textlength(title, font=font)
        cx, cy = (x + R + 0.5 + 1.6 * (x > 0) - 1.6 * (x < 0)) * k, (z + R + 0.5 + 1.2 * (z > 0) - 1.2 * (z < 0)) * k
        d.rectangle([cx - w / 2 - 3, cy - 9, cx + w / 2 + 3, cy + 9], fill=(255, 255, 255))
        d.text((cx - w / 2, cy - 8), title, fill=(20, 20, 20), font=font)
    for s, (x, z) in (("Hub (you arrive here)", (0, 3)), ("Welcome arch", (0, -12)), ("Bus stop", (6, 14))):
        w = d.textlength(s, font=font); cx, cy = (x + R + 0.5) * k, (z + R + 0.5) * k
        d.rectangle([cx - w / 2 - 3, cy - 9, cx + w / 2 + 3, cy + 9], fill=(255, 230, 120))
        d.text((cx - w / 2, cy - 8), s, fill=(20, 20, 20), font=font)
    iso = town.iso({p: b for p, b in v.items() if p[1] >= 0}, unit=9)
    W = max(m.width, iso.width, 820)
    sheet = Image.new("RGB", (W, m.height + iso.height + 60), (16, 40, 58)); sd = ImageDraw.Draw(sheet)
    sheet.paste(m, ((W - m.width) // 2, 0))
    sd.text((14, m.height + 8), "Top: from above, north up. Pink squares = pads; coloured squares = mannequins.",
            fill=(255, 255, 255), font=big)
    sd.text((14, m.height + 32), "Bottom: close-up from the south-east. The 4 benches are gone.", fill=(200, 230, 240), font=big)
    sheet.paste(iso, ((W - iso.width) // 2, m.height + 60))
    sheet.save(os.path.join(town.HERE, "previews", "wardrobe.png"))

if __name__ == "__main__":
    preview()
