"""Original pixel art for the Undersea: Bubble Shell icon + the costumes (armour layers and icons).
Grids use one letter per pixel ('.' = transparent); rows given as a left half are mirrored."""
import os, random, copy
from PIL import Image, ImageDraw, ImageFont
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
    (16, 29, ["GGGG"] * 3), (20, 29, ["GGGGGGGG"] * 3),                 # waistband: bottom rows of the torso
    (28, 29, ["GGGG"] * 3), (32, 29, ["GGGGGGGG"] * 3),
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


# ------------------------------------------------------------------ Costumes from face specs
# Where each face sits in the 64x32 armour layers: (x, y, width, height). Boots are the bottom 5 rows of
# the legs (layer 1); pants are the legs plus a waistband on the torso's bottom 3 rows (layer 2).
FACES_1 = {("head", "top"): (8, 0, 8, 8), ("head", "bottom"): (16, 0, 8, 8), ("head", "right"): (0, 8, 8, 8),
           ("head", "front"): (8, 8, 8, 8), ("head", "left"): (16, 8, 8, 8), ("head", "back"): (24, 8, 8, 8),
           ("body", "top"): (20, 16, 8, 4), ("body", "bottom"): (28, 16, 8, 4), ("body", "right"): (16, 20, 4, 12),
           ("body", "front"): (20, 20, 8, 12), ("body", "left"): (28, 20, 4, 12), ("body", "back"): (32, 20, 8, 12),
           ("arm", "top"): (44, 16, 4, 4), ("arm", "out"): (40, 20, 4, 12), ("arm", "front"): (44, 20, 4, 12),
           ("arm", "inside"): (48, 20, 4, 12), ("arm", "back"): (52, 20, 4, 12),
           ("boot", "sole"): (8, 16, 4, 4), ("boot", "out"): (0, 27, 4, 5), ("boot", "front"): (4, 27, 4, 5),
           ("boot", "inside"): (8, 27, 4, 5), ("boot", "back"): (12, 27, 4, 5)}
FACES_2 = {("waist", "right"): (16, 29, 4, 3), ("waist", "front"): (20, 29, 8, 3), ("waist", "left"): (28, 29, 4, 3),
           ("waist", "back"): (32, 29, 8, 3), ("leg", "top"): (4, 16, 4, 4), ("leg", "bottom"): (8, 16, 4, 4),
           ("leg", "out"): (0, 20, 4, 12), ("leg", "front"): (4, 20, 4, 12), ("leg", "inside"): (8, 20, 4, 12),
           ("leg", "back"): (12, 20, 4, 12)}
OPEN_HANDS = ["....", "...."]          # sleeves stop short of the hands, like the shark's

def spec_layers(spec):
    """A face left out of the spec stays transparent; 'left' faces default to the mirrored 'right'."""
    out = []
    for faces in (FACES_1, FACES_2):
        img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
        for (part, face), (x, y, w, h) in faces.items():
            rows = spec.get(part, {}).get(face)
            if rows is None and face == "left" and "right" in spec.get(part, {}):
                rows = [r[::-1] for r in spec[part]["right"]]
            if rows is None:
                continue
            img.alpha_composite(grid([rows * w] * h if len(rows) == 1 else rows, spec["pal"]), (x, y))
        out.append(img)
    return tuple(out)

# 16x16 icon silhouettes (left halves, mirrored): O outline, M main, N second colour, D detail, E eyes,
# x inside the hood. Each costume colours them per piece.
ICON_SHAPES = {
    "head": ["........", "........", ".......D", ".....OOD", "...OOMMM", "..OMMMMM", "..OMEMMM", ".OMMMMMM",
             ".OMMNNNN", ".OMNxxxx", ".OMNxxxx", ".OMNxxxx", ".OMMNNNN", "..OMMMMM", "...OOOOO", "........"],
    "chest": ["........", "..OOOO..", ".OMMMMOO", "OMMMMMMN", "OMMMMMMN", "OMMOMMNN", "OMMOMMNN", "OMMOMMNN",
              "OOOOMMNN", "...OMMNN", "...ODDDD", "...OMMNN", "...OMMMN", "...OOOOO", "........", "........"],
    "legs": ["........", "........", "...OOOOO", "...ODDDD", "...OMMMM", "...OMMMM", "...OMMMO", "...OMMMO",
             "...OMMNO", "...OMMNO", "...OMMMO", "...OMMMO", "...ONNNO", "...OOOOO", "........", "........"],
    "feet": ["........", "........", "........", "........", "...OOOO.", "...OMMO.", "...OMMO.", "...ODDO.",
             "...OMMO.", "..OMMMO.", ".OMMMMO.", "OMMMMMO.", "ONNNNNO.", "OOOOOOO.", "........", "........"]}

def spec_icon(spec, slot):
    pal = {"O": "#222222", "E": spec["icons"][slot].get("M", "#888888"), **spec["icons"][slot]}
    return grid(ICON_SHAPES[slot], pal, mirror=True)

# ---- Deep-Sea Diver: brass helmet with a porthole for your face, canvas suit, lead-weight belt and boots
DIVER = {"pal": {"Y": "#C9922E", "y": "#8C5F1C", "l": "#F0CF6A", "R": "#5A3A12", "G": "#7FC4D6", "g": "#3E8299",
                 "C": "#B49A6E", "c": "#8F7650", "B": "#4A3826", "W": "#6E6E76", "w": "#4C4C52", "K": "#1E1A16"},
    "head": {"top": ["yYYYYYYy", "YYYYYYYY", "YYYRRYYY", "YYRKKRYY", "YYRKKRYY", "YYYRRYYY", "YYYYYYYY", "yYYYYYYy"],
             "bottom": ["y"],
             "right": ["yYYYYYYy", "YYYYYlYY", "YYyyyyYY", "YyGGGgyY", "YyGGggyY", "YyGgggyY", "YYyyyyYY", "yRyyyyRy"],
             "front": ["yYYllYYy", "YRYYYYRY", "YYyyyyYY", "Yy....yY", "Yy....yY", "Yy....yY", "Yy....yY", "yRyyyyRy"],
             "back": ["yYYYYYYy", "YYYYYYYY", "YYYRRYYY", "YYRKKRYY", "YYRKKRYY", "YYYRRYYY", "YYYYYYYY", "yRyyyyRy"]},
    "body": {"top": ["Y"], "bottom": ["C"],
             "front": ["yRYYYYRy", "YYYlYYYY", "yYYYYYYy", "cCCCCCCc", "CCCCCCCC", "CCCcCCCC", "CCCCCCCC", "CCCCCcCC",
                       "WWBWWBWW", "CCCCCCCC", "CCcCCCCC", "CCCCCCCC"],
             "back": ["yRYYYYRy", "YYYYYYYY", "yYYYYYYy", "CCCCCCCC", "CCCcCCCC", "CCCCCCCC", "CCCCCCcC", "CCCCCCCC",
                      "WWBWWBWW", "CCCCCCCC", "CCCCcCCC", "CCCCCCCC"],
             "right": ["yYYy", "YYYY", "yYYy", "CCCC", "CCcC", "CCCC", "CCCC", "CcCC", "WBWW", "CCCC", "CCCC", "CCCC"]},
    "arm": {"top": ["Y"],
            "out": ["yYYy", "CCCC", "CCCC", "CCcC", "CCCC", "CCCC", "CcCC", "CCCC", "CCCC", "cccc"] + OPEN_HANDS,
            "front": ["YYYY", "CCCC", "CCCC", "CCCC", "CcCC", "CCCC", "CCCC", "CCcC", "CCCC", "cccc"] + OPEN_HANDS,
            "inside": ["CCCC"] * 9 + ["cccc"] + OPEN_HANDS,
            "back": ["YYYY", "CCCC", "CCcC", "CCCC", "CCCC", "CCCC", "CcCC", "CCCC", "CCCC", "cccc"] + OPEN_HANDS},
    "boot": {"sole": ["w"], "out": ["BBBB", "BYYB", "BBBB", "WWWW", "wwww"], "front": ["BBBB", "BYYB", "BBBB", "WWWW", "wwww"],
             "inside": ["BBBB", "BBBB", "BBBB", "WWWW", "wwww"], "back": ["BBBB", "BYYB", "BBBB", "WWWW", "wwww"]},
    "waist": {"right": ["CCCC", "CcCC", "CCCC"], "front": ["CCCCCCCC", "CCCcCCCC", "CCCCCCCC"],
              "back": ["CCCCCCCC", "CCCCCcCC", "CCCCCCCC"]},
    "leg": {"top": ["C"], "bottom": ["c"],
            "out": ["CCCC", "CCCC", "CcCC", "CCCC", "CCCC", "CCCC", "CCcC", "CCCC", "CCCC", "CcCC", "CCCC", "CCCC"],
            "front": ["CCCC", "CCCC", "CCCC", "CCCC", "CBBC", "CBBC", "CCCC", "CCCC", "CCcC", "CCCC", "CCCC", "CCCC"],
            "inside": ["CCCC"] * 12,
            "back": ["CCCC", "CCcC", "CCCC", "CCCC", "CCCC", "CCCC", "CcCC", "CCCC", "CCCC", "CCCC", "CCcC", "CCCC"]},
    "icons": {"head": {"O": "#4A3315", "M": "#C9922E", "N": "#8C5F1C", "x": "#7FC4D6", "D": "#5A3A12", "E": "#F0CF6A"},
              "chest": {"O": "#3A2E20", "M": "#B49A6E", "N": "#8F7650", "D": "#6E6E76"},
              "legs": {"O": "#3A2E20", "M": "#B49A6E", "N": "#4A3826", "D": "#8F7650"},
              "feet": {"O": "#1E1A16", "M": "#4A3826", "N": "#6E6E76", "D": "#C9922E"}}}

# ---- Anglerfish: dark deep-sea fish, glowing lure over your face, toothy mouth, glow-dots down the sides
ANGLER = {"pal": {"A": "#3E3656", "a": "#28223B", "L": "#6F6590", "p": "#8A7FB0", "s": "#514A6E", "Y": "#FFE45C",
                  "y": "#FFF6B8", "W": "#F0EEDC", "m": "#170F22", "E": "#9BE36B", "D": "#E8D45A"},
    "head": {"top": ["aAAAAAAa", "AAAAAAAA", "AAAAAAAA", "AAAssAAA", "AAAssAAA", "AAAssAAA", "AAAssAAA", "aAAssAAa"],
             "bottom": ["L"],
             "right": ["aAAAAAAa", "AAAAAAAA", "AAaAAAEA", "AAAAAAAA", "AaAAAAAm", "AAAAAAWm", "LLLLLLLm", "LLLLLLWm"],
             "front": ["aAAYYAAa", "AEAyyAEA", "WmWmmWmW", "m......m", "m......m", "m......m", "W......W", "mWmWWmWm"],
             "back": ["aAAAAAAa", "AAAaaAAA", "AAAaaAAA", "AAaAAaAA", "AAAAAAAA", "AAAAAAAA", "AAAAAAAA", "aAAAAAAa"]},
    "body": {"top": ["A"], "bottom": ["L"],
             "front": ["AAAAAAAA", "AALLLLAA", "ALLLLLLA", "ALLpLLLA", "ALLLLpLA", "ALLLLLLA", "ALpLLLLA", "ALLLLLLA",
                       "AALLLLAA", "AAALLAAA", "AAAAAAAA", "aAAAAAAa"],
             "back": ["AAAaaAAA", "AAaAAaAA", "AAAaaAAA", "AAaAAaAA", "AAAaaAAA", "AAAAAAAA", "AAAAAAAA", "AAAaaAAA",
                      "AAAAAAAA", "AAAAAAAA", "AAAAAAAA", "aAAAAAAa"],
             "right": ["AAAA", "AAAA", "ADAA", "AAAA", "AADA", "AAAA", "ADAA", "AAAA", "AADA", "AAAA", "AAAA", "aAAa"]},
    "arm": {"top": ["A"],
            "out": ["AAAA", "AAAA", "AaaA", "aaaa", "AaaA", "AAAA", "AAAA", "AAAA", "AAAA", "aaaa"] + OPEN_HANDS,
            "front": ["AAAA"] * 9 + ["aaaa"] + OPEN_HANDS, "inside": ["LLLL"] * 9 + ["aaaa"] + OPEN_HANDS,
            "back": ["AAAA", "AAAA", "AaaA", "aaaa", "AaaA", "AAAA", "AAAA", "AAAA", "AAAA", "aaaa"] + OPEN_HANDS},
    "boot": {"sole": ["a"], "out": ["aaaa", "AAAA", "AsAs", "AAAA", "aaaa"], "front": ["aaaa", "AAAA", "AsAs", "AsAs", "aaaa"],
             "inside": ["aaaa", "AAAA", "AAAA", "AAAA", "aaaa"], "back": ["aaaa", "AAAA", "AAAA", "AAAA", "aaaa"]},
    "waist": {"right": ["AAAA"] * 3, "front": ["AAAAAAAA", "AAALLAAA", "AAAAAAAA"], "back": ["AAAAAAAA"] * 3},
    "leg": {"top": ["A"], "bottom": ["a"],
            "out": ["AAAA", "AAAA", "ADAA", "AAAA", "AAAA", "AADA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA"],
            "front": ["AAAA", "AAAL", "AAAL", "AAAL", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA"],
            "inside": ["LLLL"] * 12,
            "back": ["AAAA", "AAAA", "AAAa", "AAaa", "AaaA", "aaAA", "aAAA", "AAAA", "AAAA", "AAAA", "AAAA", "AAAA"]},
    "icons": {"head": {"O": "#120C1A", "M": "#3E3656", "N": "#F0EEDC", "x": "#170F22", "D": "#FFE45C", "E": "#9BE36B"},
              "chest": {"O": "#120C1A", "M": "#3E3656", "N": "#6F6590", "D": "#28223B"},
              "legs": {"O": "#120C1A", "M": "#3E3656", "N": "#6F6590", "D": "#28223B"},
              "feet": {"O": "#120C1A", "M": "#3E3656", "N": "#28223B", "D": "#514A6E"}}}

# ---- Sea Turtle: green head and limbs, patterned shell on the back, cream belly plate on the front
TURTLE = {"pal": {"G": "#6DAA58", "g": "#4E8542", "s": "#8CC870", "S": "#6E5B2C", "T": "#A08646", "e": "#3C3218",
                  "P": "#E8D79C", "p": "#C4B070", "K": "#141414", "W": "#FFFFFF", "m": "#2F4A27"},
    "head": {"top": ["gGGGGGGg", "GGsGGsGG", "GGGGGGGG", "GsGGGGsG", "GGGGGGGG", "GGsGGsGG", "GGGGGGGG", "gGGGGGGg"],
             "bottom": ["s"],
             "right": ["gGGGGGGg", "GGsGGGGG", "GGGGGKWG", "GGGGGGGG", "GsGGGGGm", "GGGGGGmm", "GGGsGGGG", "gGGGGGGg"],
             "front": ["gGGsGGGg", "GWKGGKWG", "GGmmmmGG", "G......G", "G......G", "G......G", "G......G", "gGGGGGGg"],
             "back": ["gGGGGGGg", "GGsGGsGG", "GGGGGGGG", "GsGGGGsG", "GGGGGGGG", "GGsGGsGG", "GGGGGGGG", "gGGGGGGg"]},
    "body": {"top": ["eSSSSSSe", "STTTTTTS", "STTTTTTS", "eSSSSSSe"], "bottom": ["P"],
             "front": ["eSSSSSSe", "SPPPPPPS", "SPPPPPPS", "SppppppS", "SPPPPPPS", "SPPPPPPS", "SppppppS", "SPPPPPPS",
                       "SPPPPPPS", "SppppppS", "SPPPPPPS", "eSSSSSSe"],
             "back": ["eSSSSSSe", "STTeeTTS", "STeSSeTS", "SeSTTSeS", "eSTTTTSe", "STTeeTTS", "STeSSeTS", "SeSTTSeS",
                      "eSTTTTSe", "STTeeTTS", "SSeSSeSS", "eSSSSSSe"],
             "right": ["eSSe", "STTS", "STTS", "eSSe", "STTS", "STTS", "eSSe", "STTS", "STTS", "eSSe", "STTS", "eSSe"]},
    "arm": {"top": ["G"],
            "out": ["gGGg", "GsGG", "GGGG", "GGsG", "GGGG", "GsGG", "GGGG", "GGsG", "GGGG", "gggg"] + OPEN_HANDS,
            "front": ["GGGG", "GGsG", "GGGG", "GsGG", "GGGG", "GGGG", "GGsG", "GGGG", "GGGG", "gggg"] + OPEN_HANDS,
            "inside": ["GGGG"] * 9 + ["gggg"] + OPEN_HANDS,
            "back": ["gGGg", "GGsG", "GGGG", "GsGG", "GGGG", "GGsG", "GGGG", "GsGG", "GGGG", "gggg"] + OPEN_HANDS},
    "boot": {"sole": ["g"], "out": ["gGGg", "GGGG", "GsGG", "GGGG", "gggg"], "front": ["GGGG", "GGGG", "GgGg", "GgGg", "gggg"],
             "inside": ["gGGg", "GGGG", "GGGG", "GGGG", "gggg"], "back": ["gGGg", "GGGG", "GGsG", "GGGG", "gggg"]},
    "waist": {"right": ["SSSS", "STTS", "eSSe"], "front": ["SPPPPPPS", "SppppppS", "eSSSSSSe"],
              "back": ["SSeSSeSS", "STTTTTTS", "eSSSSSSe"]},
    "leg": {"top": ["G"], "bottom": ["g"],
            "out": ["GGGG", "GsGG", "GGGG", "GGsG", "GGGG", "GsGG", "GGGG", "GGsG", "GGGG", "GGGG", "GsGG", "GGGG"],
            "front": ["GGGG", "GGsG", "GGGG", "GGGG", "GsGG", "GGGG", "GGGG", "GGsG", "GGGG", "GGGG", "GsGG", "GGGG"],
            "inside": ["GGGG"] * 12,
            "back": ["GGGG", "GGGG", "GGgg", "GGGG", "GsGG", "GGGG", "GGGG", "GGsG", "GGGG", "GGGG", "GsGG", "GGGG"]},
    "icons": {"head": {"O": "#22361C", "M": "#6DAA58", "N": "#4E8542", "x": "#2F4A27", "D": "#8CC870", "E": "#141414"},
              "chest": {"O": "#2A2412", "M": "#6E5B2C", "N": "#E8D79C", "D": "#3C3218"},
              "legs": {"O": "#22361C", "M": "#6DAA58", "N": "#4E8542", "D": "#E8D79C"},
              "feet": {"O": "#22361C", "M": "#6DAA58", "N": "#4E8542", "D": "#8CC870"}}}

# ---- Coral Knight: armour of pink coral plates, blue tube-coral trim, yellow crest; eyes show through the visor
CORAL = {"pal": {"P": "#E05FA0", "p": "#A83C76", "q": "#F59CC8", "B": "#3D6BE0", "b": "#2A49A6", "Y": "#F0D040",
                 "y": "#B89A20", "K": "#1A1020"},
    "head": {"top": ["pPPYYPPp", "PPPYYPPP", "PqPYYPqP", "PPPYYPPP", "PPPYYPPP", "PqPYYPqP", "PPPYYPPP", "pPPYYPPp"],
             "bottom": ["p"],
             "right": ["pPPPPPPp", "PqPPPPPP", "PPPBBPPP", "PPBYYBPP", "PPBYYBPP", "PPPBBPPP", "PPPPPPqP", "pPPPPPPp"],
             "front": ["pPPYYPPp", "PqPYYPqP", "PPPPPPPP", "PbBBBBbP", "P......P", "PbBBBBbP", "PPKPPKPP", "pPPPPPPp"],
             "back": ["pPPYYPPp", "PPPYYPPP", "PqPYYPqP", "PPPYYPPP", "PPPYYPPP", "PPPPPPPP", "PPPPPPPP", "pPPPPPPp"]},
    "body": {"top": ["P"], "bottom": ["p"],
             "front": ["pBBBBBBp", "PPPPPPPP", "PPYPPYPP", "PPYPPYPP", "PPPYYPPP", "PPPYYPPP", "PPPYYPPP", "PqPPPPqP",
                       "YYYyyYYY", "PPPPPPPP", "PqPPPPqP", "pPpPPpPp"],
             "back": ["pBBBBBBp", "PPPPPPPP", "PqPPPPqP", "PPPPPPPP", "PPPPPPPP", "PqPPPPqP", "PPPPPPPP", "PPPPPPPP",
                      "YYYYYYYY", "PPPPPPPP", "PqPPPPqP", "pPpPPpPp"],
             "right": ["pBBp", "PPPP", "PqPP", "PPPP", "PPPP", "PPqP", "PPPP", "PPPP", "YYYY", "PPPP", "PPPP", "pPpP"]},
    "arm": {"top": ["B"],
            "out": ["BBBB", "bBBb", "PPPP", "PqPP", "PPPP", "BBBB", "PPPP", "PPqP", "PPPP", "YYYY"] + OPEN_HANDS,
            "front": ["BBBB", "BBBB", "PPPP", "PPPP", "PqPP", "BBBB", "PPPP", "PPPP", "PPPP", "YYYY"] + OPEN_HANDS,
            "inside": ["PPPP"] * 9 + ["YYYY"] + OPEN_HANDS,
            "back": ["BBBB", "bBBb", "PPPP", "PPqP", "PPPP", "BBBB", "PPPP", "PqPP", "PPPP", "YYYY"] + OPEN_HANDS},
    "boot": {"sole": ["b"], "out": ["YYYY", "BBBB", "BbBB", "BBBB", "bbbb"], "front": ["YYYY", "BBBB", "BBbB", "BBBB", "bbbb"],
             "inside": ["YYYY", "BBBB", "BBBB", "BBBB", "bbbb"], "back": ["YYYY", "BBBB", "BbBB", "BBBB", "bbbb"]},
    "waist": {"right": ["YYYY", "PPPP", "pPpP"], "front": ["YYYyyYYY", "PPPPPPPP", "pPpPPpPp"],
              "back": ["YYYYYYYY", "PPPPPPPP", "pPpPPpPp"]},
    "leg": {"top": ["P"], "bottom": ["p"],
            "out": ["PPPP", "PqPP", "PPPP", "PPPP", "BBBB", "BbBB", "PPPP", "PPqP", "PPPP", "PPPP", "PPPP", "PPPP"],
            "front": ["PPPP", "PPPP", "PqPP", "PPPP", "BYYB", "BBBB", "PPPP", "PPPP", "PqPP", "PPPP", "PPPP", "PPPP"],
            "inside": ["PPPP"] * 12,
            "back": ["PPPP", "PPPP", "PPqP", "PPPP", "BBBB", "BBBB", "PPPP", "PPPP", "PPPP", "PqPP", "PPPP", "PPPP"]},
    "icons": {"head": {"O": "#5A1A3A", "M": "#E05FA0", "N": "#3D6BE0", "x": "#1A1020", "D": "#F0D040", "E": "#E05FA0"},
              "chest": {"O": "#5A1A3A", "M": "#E05FA0", "N": "#F59CC8", "D": "#F0D040"},
              "legs": {"O": "#5A1A3A", "M": "#E05FA0", "N": "#3D6BE0", "D": "#F0D040"},
              "feet": {"O": "#1A2450", "M": "#3D6BE0", "N": "#2A49A6", "D": "#F0D040"}}}

# ---- Axolotl: pink with frilly red gills on the sides of the head, a big smile, spots and a tail fin
AXOLOTL = {"pal": {"P": "#F4A9C6", "p": "#DC7FA6", "L": "#FCD6E5", "G": "#D43A72", "g": "#9E2050", "K": "#2A1622",
                   "m": "#8C3657"},
    "head": {"top": ["pPPPPPPp", "PPPpPPPP", "PPPPPPpP", "PpPPPPPP", "PPPPpPPP", "PPPPPPPP", "PPpPPPPP", "pPPPPPPp"],
             "bottom": ["L"],
             "right": ["GPGPPPPP", "gGgGPPPP", "GgGgPPPP", "gGgPPPPP", "PPPPPPPP", "PPPPPpPP", "PPpPPPPP", "LLLLLLLL"],
             "front": ["PKPPPPKP", "PmPPPPmP", "PPmmmmPP", "P......P", "P......P", "P......P", "P......P", "LLLLLLLL"],
             "back": ["GPPPPPPG", "gGPPPPGg", "GgPPPPgG", "gPPPPPPg", "PpPPPPPP", "PPPPpPPP", "PPPPPPPP", "PPPPPPPP"]},
    "body": {"top": ["P"], "bottom": ["L"],
             "front": ["PPPPPPPP", "PPLLLLPP", "PLLLLLLP", "PLLLLLLP", "PLLLLLLP", "PLLLLLLP", "PLLLLLLP", "PLLLLLLP",
                       "PLLLLLLP", "PPLLLLPP", "PPPPPPPP", "PPPPPPPP"],
             "back": ["PPPppPPP", "PpPppPPP", "PPPppPPP", "PPPppPpP", "PPPppPPP", "PPPppPPP", "PpPppPPP", "PPPppPPP",
                      "PPPppPPP", "PPPppPpP", "PPPppPPP", "PPPPPPPP"],
             "right": ["PPPP", "PpPP", "PPPP", "PPpP", "PPPP", "PPPP", "PpPP", "PPPP", "PPPP", "PPpP", "PPPP", "PPPP"]},
    "arm": {"top": ["P"],
            "out": ["PPPP", "PPpP", "PPPP", "PpPP", "PPPP", "PPPP", "PPpP", "PPPP", "PPPP", "pppp"] + OPEN_HANDS,
            "front": ["PPPP"] * 9 + ["pppp"] + OPEN_HANDS, "inside": ["LLLL"] * 9 + ["pppp"] + OPEN_HANDS,
            "back": ["PPPP", "PpPP", "PPPP", "PPPP", "PPpP", "PPPP", "PPPP", "PpPP", "PPPP", "pppp"] + OPEN_HANDS},
    "boot": {"sole": ["p"], "out": ["PPPP", "PPPP", "PpPP", "PPPP", "pppp"], "front": ["PPPP", "PPPP", "PPPP", "PpPp", "pppp"],
             "inside": ["LLLL", "LLLL", "LLLL", "LLLL", "pppp"], "back": ["PPPP", "PPPP", "PPpP", "PPPP", "pppp"]},
    "waist": {"right": ["PPPP"] * 3, "front": ["PPLLLLPP", "PPPPPPPP", "PPPPPPPP"], "back": ["PPPppPPP", "PPPppPPP", "PPPPPPPP"]},
    "leg": {"top": ["P"], "bottom": ["p"],
            "out": ["PPPP", "PpPP", "PPPP", "PPPP", "PPpP", "PPPP", "PPPP", "PpPP", "PPPP", "PPPP", "PPPP", "PPPP"],
            "front": ["PPPP"] * 12, "inside": ["LLLL"] * 12,
            "back": ["PPPP", "PPPP", "PPPp", "PPpp", "PppP", "ppPP", "pPPP", "PPPP", "PPPP", "PPPP", "PPPP", "PPPP"]},
    "icons": {"head": {"O": "#7A2A4A", "M": "#F4A9C6", "N": "#DC7FA6", "x": "#8C3657", "D": "#D43A72", "E": "#2A1622"},
              "chest": {"O": "#7A2A4A", "M": "#F4A9C6", "N": "#FCD6E5", "D": "#DC7FA6"},
              "legs": {"O": "#7A2A4A", "M": "#F4A9C6", "N": "#FCD6E5", "D": "#DC7FA6"},
              "feet": {"O": "#7A2A4A", "M": "#F4A9C6", "N": "#DC7FA6", "D": "#D43A72"}}}

# ---- Sponge: a walking sponge block. Porous yellow all over; the kid's own face shows through the hood.
def porous(w, h, seed):
    """Sponge texture: yellow with scattered pores (some two pixels wide), fixed per face by the seed."""
    rnd = random.Random(seed)
    g = [["Y"] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if g[y][x] == "Y" and rnd.random() < 0.15:
                g[y][x] = "h"
                if x + 1 < w and rnd.random() < 0.45:
                    g[y][x + 1] = "H"
    return ["".join(r) for r in g]

def _sponge():
    seed = iter(range(1, 100))
    P = lambda w, h: porous(w, h, next(seed))
    front = P(8, 8)
    front[3:7] = [r[0] + "......" + r[7] for r in front[3:7]]      # face opening, like the other hoods
    shade = lambda rows: rows[:-1] + ["y" * len(rows[0])]          # darker bottom edge
    return {"pal": {"Y": "#E6D44E", "y": "#C9B536", "h": "#A8922A", "H": "#CDB93E", "l": "#F4E888"},
        "head": {"top": P(8, 8), "bottom": ["y"], "right": P(8, 8), "front": front, "left": P(8, 8), "back": P(8, 8)},
        "body": {"top": P(8, 4), "bottom": ["y"], "right": P(4, 12), "front": P(8, 12), "left": P(4, 12),
                 "back": P(8, 12)},
        "arm": {"top": P(4, 4), **{f: P(4, 10) + OPEN_HANDS for f in ("out", "front", "inside", "back")}},
        "boot": {"sole": ["y"], **{f: shade(P(4, 5)) for f in ("out", "front", "inside", "back")}},
        "waist": {"right": P(4, 3), "front": P(8, 3), "left": P(4, 3), "back": P(8, 3)},
        "leg": {"top": P(4, 4), "bottom": ["y"], **{f: P(4, 12) for f in ("out", "front", "inside", "back")}},
        "icons": {slot: {"O": "#5C4E10", "M": "#E6D44E", "N": "#C4B030", "x": "#3A3008", "D": "#8C7A1A", "E": "#8C7A1A"}
                  for slot in ("head", "chest", "legs", "feet")}}
SPONGE = _sponge()

# ---- Sponge Buddy: the yellow sponge in a white shirt + red tie, brown square shorts, and
# black shoes over white socks. The hood keeps the sponge's face opening, so the kid's own
# face peeks through (they're wearing it). The yellow body, sleeves and lower legs reuse the
# sponge's pores.
def _spongebuddy():
    s = copy.deepcopy(SPONGE)
    s["pal"] = dict(SPONGE["pal"])
    s["pal"].update({
        "W": "#FFFFFF", "w": "#D9D9D9",   # shirt white + soft shadow
        "R": "#D62828", "r": "#9E1B1B",   # tie red + shadow
        "b": "#8A5A2B", "B": "#5E3D1E",   # shorts brown + dark hem
        "K": "#20202A",                   # shoe black
    })
    # --- white shirt (chest): a red tie down the front, plain white on the rest ---
    s["body"]["front"] = ["WWRRRRWW", "WWWRRWWW", "WWWRRWWW", "WWWRRWWW", "WWWRRWWW",
                          "WWWRRWWW", "WWWRRWWW", "WWWRRWWW", "WWWRRWWW", "WWWRrWWW",
                          "WWWWWWWW", "WWWWWWWW"]
    s["body"]["back"] = ["WWWWWWWW"] * 12
    for f in ("right", "left"):
        s["body"][f] = ["WWWW"] * 12
    s["body"]["top"] = ["WWWWWWWW"] * 4
    s["body"]["bottom"] = ["WWWWWWWW"] * 4
    # --- arms: short white sleeves, then yellow sponge forearms ---
    s["arm"]["top"] = ["WWWW"] * 4
    for f in ("out", "front", "inside", "back"):
        rows = list(s["arm"][f])
        rows[0], rows[1], rows[2] = "WWWW", "WWWW", "WWWW"
        s["arm"][f] = rows
    # --- legs: brown square shorts over the yellow sponge legs ---
    s["leg"]["top"] = ["bbbb"] * 4
    for f in ("out", "front", "inside", "back"):
        rows = list(s["leg"][f])
        for i in range(6):
            rows[i] = "bbbb"
        rows[5] = "BBBB"                    # a darker hem at the bottom of the shorts
        s["leg"][f] = rows
    # --- waistband: the white shirt hem (mostly hidden under the body) ---
    s["waist"]["front"] = ["WWWWWWWW"] * 3
    s["waist"]["back"] = ["WWWWWWWW"] * 3
    for f in ("right", "left"):
        s["waist"][f] = ["WWWW"] * 3
    # --- feet: a white sock band over a black shoe ---
    s["boot"]["sole"] = ["KKKK"] * 4
    for f in ("out", "front", "inside", "back"):
        s["boot"][f] = ["WWWW", "KKKK", "KKKK", "KKKK", "KKKK"]
    s["icons"] = {
        "head": {"O": "#5C4E10", "M": "#E6D44E", "N": "#C4B030", "x": "#3A3008", "D": "#8C7A1A", "E": "#8C7A1A"},
        "chest": {"O": "#8A8A8A", "M": "#FFFFFF", "N": "#D9D9D9", "D": "#D62828"},
        "legs": {"O": "#3E2810", "M": "#8A5A2B", "N": "#E6D44E", "D": "#5E3D1E"},
        "feet": {"O": "#141418", "M": "#20202A", "N": "#FFFFFF", "D": "#FFFFFF"}}
    return s

SPONGE_BUDDY = _spongebuddy()

SPECS = {"diver": DIVER, "angler": ANGLER, "turtle": TURTLE, "coral": CORAL, "axolotl": AXOLOTL, "sponge": SPONGE,
         "spongebuddy": SPONGE_BUDDY}
SHARK_PIECE = {"head": "hood", "chest": "suit", "legs": "pants", "feet": "flippers"}

PAINTED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art", "costumes")

def painted_layers(name):
    """Hand-painted override: art/costumes/<name>_1.png + <name>_2.png (64x32 each) replace the drawn art."""
    paths = [os.path.join(PAINTED, f"{name}_{i}.png") for i in (1, 2)]
    if not all(map(os.path.exists, paths)):
        return None
    imgs = tuple(Image.open(p).convert("RGBA") for p in paths)
    for p, im in zip(paths, imgs):
        assert im.size == (64, 32), f"{p} must be 64x32, is {im.size}"
        im.putdata([(r, g, b, 255 if a >= 128 else 0) for r, g, b, a in im.getdata()])   # armour is cut-out: no half-see-through
    return imgs

def costume_layers(name):
    return painted_layers(name) or (shark_layers() if name == "shark" else spec_layers(SPECS[name]))

def costume_icon(name, slot):
    return shark_icon(SHARK_PIECE[slot]) if name == "shark" else spec_icon(SPECS[name], slot)

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

def preview(path, costumes):
    """One row per costume: front / side / back on a plain kid, then the four item icons.
    costumes: [(name, title, [piece names in head/chest/legs/feet order])]"""
    S, pad, row_h = 7, 22, 32 * 7 + 60
    skin = base_skin()
    W = pad + 3 * (16 * S + pad) + 4 * (16 * 6 + 28) + pad
    out = Image.new("RGBA", (W, pad + len(costumes) * row_h), hexc("#EDE6D6"))
    d = ImageDraw.Draw(out)
    for r, (name, title, pieces) in enumerate(costumes):
        y = pad + r * row_h
        d.text((pad, y), title, fill=(30, 30, 30))
        layer1, layer2 = costume_layers(name)
        x = pad
        for v in ("front", "side", "back"):
            dl = doll(skin, v); dl.alpha_composite(doll(layer2, v)); dl.alpha_composite(doll(layer1, v))
            out.alpha_composite(dl.resize((dl.width * S, 32 * S), Image.NEAREST), (x + (16 - dl.width) * S // 2, y + 16))
            x += 16 * S + pad
        for slot, label in zip(("head", "chest", "legs", "feet"), pieces):
            d.rectangle([x - 3, y + 40, x + 16 * 6 + 2, y + 40 + 16 * 6 + 2], fill=(139, 139, 139))
            out.alpha_composite(costume_icon(name, slot).resize((96, 96), Image.NEAREST), (x, y + 40))
            d.text((x, y + 40 + 96 + 8), label, fill=(30, 30, 30))
            x += 16 * 6 + 28
    out.save(path)

# ------------------------------------------------------------------ Painting your own: layout guides
GUIDE_LABELS = {
    ("head", "top"): "hood top", ("head", "bottom"): "under", ("head", "right"): "hood right side",
    ("head", "front"): "hood FRONT", ("head", "left"): "hood left side", ("head", "back"): "hood back",
    ("body", "top"): "shoulders", ("body", "bottom"): "", ("body", "right"): "R side",
    ("body", "front"): "chest FRONT", ("body", "left"): "L side", ("body", "back"): "BACK",
    ("arm", "top"): "", ("arm", "out"): "out", ("arm", "front"): "front", ("arm", "inside"): "in",
    ("arm", "back"): "back", ("boot", "sole"): "sole", ("boot", "out"): "out", ("boot", "front"): "front",
    ("boot", "inside"): "in", ("boot", "back"): "back",
    ("waist", "right"): "R", ("waist", "front"): "waist FRONT", ("waist", "left"): "L", ("waist", "back"): "waist BACK",
    ("leg", "top"): "", ("leg", "bottom"): "", ("leg", "out"): "out", ("leg", "front"): "front",
    ("leg", "inside"): "in", ("leg", "back"): "back"}
GUIDE_GROUPS = {"head": "#E06666", "body": "#6FA8DC", "arm": "#93C47D", "boot": "#F6B26B", "waist": "#8E7CC3", "leg": "#C27BA0"}
GUIDE_TITLES = {1: "Layer 1: hood, top + sleeves (arms), feet.  Arms stop 2 rows short of the hands.",
                2: "Layer 2: legs + waistband (worn under the top)."}

def layout_guide(layer, tex, scale=12):
    """The 64x32 texture blown up, with every face outlined and named, plus the pixel grid."""
    faces = FACES_1 if layer == 1 else FACES_2
    W, H, top = 64 * scale, 32 * scale, 30
    out = Image.new("RGBA", (W, H + top), (255, 255, 255, 255))
    out.alpha_composite(tex.resize((W, H), Image.NEAREST), (0, top))
    d = ImageDraw.Draw(out); font = ImageFont.load_default(size=12)
    for x in range(0, W + 1, scale):
        d.line([(x, top), (x, top + H)], fill=(0, 0, 0, 40))
    for y in range(0, H + 1, scale):
        d.line([(0, top + y), (W, top + y)], fill=(0, 0, 0, 40))
    for (part, face), (x, y, w, h) in faces.items():
        box = [x * scale, top + y * scale, (x + w) * scale - 1, top + (y + h) * scale - 1]
        d.rectangle(box, outline=GUIDE_GROUPS[part], width=3)
        label = GUIDE_LABELS[(part, face)]
        if label:
            tw = d.textlength(label, font=font)
            d.rectangle([box[0] + 3, box[1] + 3, box[0] + tw + 7, box[1] + 17], fill=(255, 255, 255, 220))
            d.text((box[0] + 5, box[1] + 3), label, fill=(0, 0, 0), font=font)
    d.text((6, 8), GUIDE_TITLES[layer] + "  Each square = 1 pixel.", fill=(0, 0, 0), font=font)
    return out

if __name__ == "__main__":     # python3 undersea_art.py sponge -> starting images + guides in art/costumes/
    import sys
    os.makedirs(PAINTED, exist_ok=True)
    for name in sys.argv[1:]:
        layers = costume_layers(name)
        for i, im in enumerate(layers, 1):
            im.save(os.path.join(PAINTED, f"{name}_{i}.png"))
            layout_guide(i, im).save(os.path.join(PAINTED, f"guide_{name}_{i}.png"))
