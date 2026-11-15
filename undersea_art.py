"""Original pixel art for the Undersea: Bubble Shell icon + Shark costume (armour layers and icons).
Grids use one letter per pixel ('.' = transparent); rows given as a left half are mirrored."""
from PIL import Image, ImageDraw
from art import hexc

def grid(rows, pal, mirror=False):
    rows = [r + r[::-1] if mirror else r for r in rows]
    img = Image.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0)); p = img.load()
    for y, row in enumerate(rows):
        assert len(row) == img.width, row
        for x, ch in enumerate(row):
            if ch != ".":
                p[x, y] = hexc(pal[ch])
    return img

# ------------------------------------------------------------------ Shark costume
SHARK = {"G": "#6F8FA6", "D": "#4F6B80", "B": "#DCE6EC", "W": "#FFFFFF", "K": "#15191C", "R": "#C0485A",
         "x": "#3A2A30", "O": "#2E3D4A", "F": "#4D6A80", "L": "#86A7BC"}

def fill(c, w, h):
    return [c * w] * h

# Faces of the classic 64x32 armour layout: (x, y, rows). Head 8x8x8, body 8x12x4, arm/leg 4x12x4.
# Side faces run back -> front on the right side and front -> back on the left side.
SHARK_LAYER1 = [                                            # hood + suit + flippers
    (8, 0, fill("GGGDDGGG", 1, 8)),                                     # hood top (ridge)
    (16, 0, fill("B", 8, 8)),                                           # hood bottom
    (0, 8, ["GGGGGGGG", "GGGGGGGG", "GGGGWKGG", "GGGGKKGG", "GGGGGGGG", "GGGGGGGG", "BBBBBBBB", "BBBBBBBB"]),
    (8, 8, ["GKGGGGKG", "RWRWWRWR", "R......R", "R......R", "R......R", "R......R", "R......R", "RWRWWRWR"]),
    (16, 8, ["GGGGGGGG", "GGGGGGGG", "GGKWGGGG", "GGKKGGGG", "GGGGGGGG", "GGGGGGGG", "BBBBBBBB", "BBBBBBBB"]),
    (24, 8, fill("GGGDDGGG", 1, 8)),                                    # hood back
    (20, 16, fill("G", 8, 4)), (28, 16, fill("B", 8, 4)),               # suit top / bottom
    (16, 20, ["GGGG"] + ["GDGD"] * 3 + ["GGGG"] * 8),                   # suit right side (gills)
    (20, 20, ["GGGGGGGG", "GGGBBGGG"] + ["GGBBBBGG"] * 7 + ["GGGBBGGG"] + ["GGGGGGGG"] * 2),  # suit front (belly)
    (28, 20, ["GGGG"] + ["DGDG"] * 3 + ["GGGG"] * 8),                   # suit left side (gills)
    (32, 20, ["GGGGGGGG", "GGGDGGGG", "GGGDDGGG", "GGGDDDGG", "GGDDDDGG", "GGDDDDDG"] + ["GGGGGGGG"] * 6),  # dorsal fin
    (44, 16, fill("G", 4, 4)),                                          # sleeve top (bottom left open: hands)
    (40, 20, ["GGGG"] * 4 + ["GGDG", "GDDG", "DDDG"] + ["GGGG"] * 3 + ["...."] * 2),  # sleeve outside (fin)
    (44, 20, ["GGGG"] * 9 + ["DDDD"] + ["...."] * 2),                   # sleeve front
    (48, 20, ["BBBB"] * 10 + ["...."] * 2),                             # sleeve inside
    (52, 20, ["GGGG"] * 10 + ["...."] * 2),                             # sleeve back
    (8, 16, fill("F", 4, 4)),                                           # flipper soles
    (0, 20, ["...."] * 7 + ["FFFF"] * 5), (8, 20, ["...."] * 7 + ["FFFF"] * 5),
    (12, 20, ["...."] * 7 + ["FFFF"] * 5),
    (4, 20, ["...."] * 7 + ["FFFF", "FFFF", "FLFL", "FLFL", "FLFL"]),   # flipper front (webbing)
]
SHARK_LAYER2 = [                                            # pants
    (16, 20, ["GGGG"] * 3 + ["...."] * 9), (20, 20, ["GGGGGGGG"] * 3 + ["........"] * 9),
    (28, 20, ["GGGG"] * 3 + ["...."] * 9), (32, 20, ["GGGGGGGG"] * 3 + ["........"] * 9),
    (4, 16, fill("G", 4, 4)), (8, 16, fill("G", 4, 4)),
    (0, 20, fill("G", 4, 12)),                                          # leg outside
    (4, 20, fill("GGGB", 1, 12)),                                       # leg front (white inner edge)
    (8, 20, fill("B", 4, 12)),                                          # leg inside
    (12, 20, ["GGGG", "GGGG", "GGGD", "GGDD", "GDDG", "DDGG", "DGGG"] + ["GGGG"] * 5),  # tail fluke (a V across both legs)
]

def armour_layer(faces, pal):
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    for x, y, rows in faces:
        img.paste(grid(rows, pal), (x, y))
    return img

def shark_layers():
    return armour_layer(SHARK_LAYER1, SHARK), armour_layer(SHARK_LAYER2, SHARK)

SHARK_ICONS = {   # 16x16, left halves (mirrored)
    "hood": ["........", "....OOOO", "..OOGGGG", ".OGGGGGD", ".OGGGGGD", "OGGKGGGG", "OGGWWWWW", "OGGxWxWx",
             "OGGxxxxx", "OGGxxxxx", "OGGxxWxx", "OGBBBBBB", ".OBBBBBB", "..OOOOOO", "........", "........"],
    "suit": ["........", ".OOOO...", "OGGGGO..", "OGGGGGOO", "OGGOGGBB", "OGGOGGBB", "OGGOGBBB", "OGGOGBBB",
             "OOOOGBBB", "...OGBBB", "...OGGBB", "...OGGGG", "...OOOOO", "........", "........", "........"],
    "pants": ["........", "........", "..OOOOOO", "..OGGGGG", "..OGGGGG", "..OGGGBO", "..OGGGBO", "..OGGGBO",
              "..OGGGBO", "..OGGGBO", "..OGGGBO", "..OGGGBO", "..OOOOO.", "........", "........", "........"],
    "flippers": ["........", "........", "........", "........", "...OOOO.", "...OFFO.", "...OFFO.", "..OFFFO.",
                 ".OFFFFO.", "OFLFLFO.", "OFLFLFO.", "OFFFFFO.", ".OOOOOO.", "........", "........", "........"],
}

def shark_icon(piece):
    return grid(SHARK_ICONS[piece], SHARK, mirror=True)

# ------------------------------------------------------------------ Bubble Shell
SHELL = {"d": "#6B3A2E", "c": "#FFE6D2", "s": "#E3AE8C", "w": "#FFFFFF", "p": "#F58FA8", "P": "#D8607E",
         "b": "#C9F3FF", "o": "#5CC6EA"}

def bubble_shell():
    """16x16 conch (pink opening bottom-left, spire top-right) with two bubbles."""
    return grid(["................", ".ob.......dd....", "obbo.....dccd...", ".oo.....dcwsd...",
                 "...ob..ddddddd..", "...oo.dcccwccsd.", ".....dccwcccccsd", "....dddddddddsd.",
                 "...dpPcccwcccsd.", "..dpPPpcccccssd.", ".dpPPPPdddddsd..", ".dpPPPPpcccsd...",
                 ".dpPPPpccssd....", "..dpPPpcssd.....", "...ddddddd......", "................"], SHELL)

# ------------------------------------------------------------------ Preview
BASE_SKIN = {"S": "#E0AC8C", "H": "#4A3020", "E": "#FFFFFF", "I": "#3060C0", "M": "#9C5A4A",
             "T": "#2FA4A0", "N": "#2B3A67", "Q": "#555560"}

def base_skin():
    """A plain test kid (64x32 layout) so the preview shows what the costume covers."""
    return armour_layer([
        (0, 8, fill("H", 8, 2) + fill("S", 8, 6)), (16, 8, fill("H", 8, 2) + fill("S", 8, 6)),
        (8, 8, ["HHHHHHHH", "HHHHHHHH", "SSSSSSSS", "SSSSSSSS", "SEISSIES", "SSSSSSSS", "SSSMMSSS", "SSSSSSSS"]),
        (24, 8, fill("H", 8, 8)), (8, 0, fill("H", 8, 8)), (16, 0, fill("S", 8, 8)),
        (16, 20, fill("T", 4, 12)), (20, 20, fill("T", 8, 12)), (28, 20, fill("T", 4, 12)), (32, 20, fill("T", 8, 12)),
        (40, 20, fill("T", 4, 4) + fill("S", 4, 8)), (44, 20, fill("T", 4, 4) + fill("S", 4, 8)),
        (48, 20, fill("T", 4, 4) + fill("S", 4, 8)), (52, 20, fill("T", 4, 4) + fill("S", 4, 8)),
        (0, 20, fill("N", 4, 10) + fill("Q", 4, 2)), (4, 20, fill("N", 4, 10) + fill("Q", 4, 2)),
        (8, 20, fill("N", 4, 10) + fill("Q", 4, 2)), (12, 20, fill("N", 4, 10) + fill("Q", 4, 2)),
    ], BASE_SKIN)

def doll(tex, view):
    """Flat front / back / right-side view (16x32 or 8x32) of a 64x32 skin or armour layer."""
    crop = lambda x, y, w, h: tex.crop((x, y, x + w, y + h))
    flip = lambda im: im.transpose(Image.FLIP_LEFT_RIGHT)
    if view == "side":
        out = Image.new("RGBA", (8, 32), (0, 0, 0, 0))
        out.paste(crop(0, 8, 8, 8), (0, 0))
        out.alpha_composite(crop(16, 20, 4, 12), (2, 8)); out.alpha_composite(crop(0, 20, 4, 12), (2, 20))
        out.alpha_composite(crop(40, 20, 4, 12), (2, 8))
        return out
    out = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    if view == "front":
        head, body, arm, leg = crop(8, 8, 8, 8), crop(20, 20, 8, 12), crop(44, 20, 4, 12), crop(4, 20, 4, 12)
        right_arm, left_arm, right_leg, left_leg = (0, 8), (12, 8), (4, 20), (8, 20)
    else:
        head, body, arm, leg = crop(24, 8, 8, 8), crop(32, 20, 8, 12), crop(52, 20, 4, 12), crop(12, 20, 4, 12)
        right_arm, left_arm, right_leg, left_leg = (12, 8), (0, 8), (8, 20), (4, 20)
    out.alpha_composite(head, (4, 0)); out.alpha_composite(body, (4, 8))
    out.alpha_composite(arm, right_arm); out.alpha_composite(flip(arm), left_arm)
    out.alpha_composite(leg, right_leg); out.alpha_composite(flip(leg), left_leg)
    return out

def preview(path):
    layer1, layer2 = shark_layers()
    skin = base_skin()
    S, pad = 10, 24
    views = []
    for v in ("front", "side", "back"):
        d = doll(skin, v)
        d.alpha_composite(doll(layer2, v)); d.alpha_composite(doll(layer1, v))
        views.append(doll(skin, v)); views.append(d)
    icons = [shark_icon(k) for k in SHARK_ICONS] + [bubble_shell()]
    W = pad + sum(v.width * S + pad for v in views)
    H = pad * 3 + 32 * S + 16 * 8 + 20
    out = Image.new("RGBA", (W, H), hexc("#EDE6D6"))
    d = ImageDraw.Draw(out)
    x = pad
    for i, v in enumerate(views):
        out.alpha_composite(v.resize((v.width * S, 32 * S), Image.NEAREST), (x, pad + 14))
        d.text((x, 6), ("before" if i % 2 == 0 else "shark costume") + " / " + ("front", "side", "back")[i // 2], fill=(40, 40, 40))
        x += v.width * S + pad
    y = pad * 2 + 32 * S + 14
    labels = ["Shark Hood", "Shark Suit", "Shark Pants", "Shark Flippers", "Bubble Shell"]
    for i, (ic, label) in enumerate(zip(icons, labels)):
        bx = pad + i * (16 * 8 + 40)
        d.rectangle([bx - 4, y - 4, bx + 16 * 8 + 3, y + 16 * 8 + 3], fill=(139, 139, 139))
        out.alpha_composite(ic.resize((128, 128), Image.NEAREST), (bx, y))
        d.text((bx, y + 16 * 8 + 6), label, fill=(40, 40, 40))
    out.save(path)
