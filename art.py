"""Original pixel art for the family pack: foam blaster + lightsabers.
Shapes are drawn in the item's own coordinates (u = along the barrel, v = up)
and mapped onto a diagonal, like vanilla item sprites."""
from PIL import Image, ImageDraw

def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

def shade(c, f):
    return tuple(max(0, min(255, round(x * f))) for x in c[:3]) + (c[3],)

# ---------------------------------------------------------------- blaster
ORANGE, BLUE, YELLOW, GREY = hexc("#F57A1F"), hexc("#2F7BEA"), hexc("#FFD23A"), hexc("#43434F")

# (polygon in u,v) , colour ; drawn in order, later parts on top
BLASTER = [
    ([(0, -1), (9, -1), (9, 6), (1, 6), (0, 4)], ORANGE),                # stock
    ([(2, 1), (6, 1), (6, 4), (2, 4)], None),                            # stock hole
    ([(8, -2), (27, -2), (27, 7), (8, 7)], ORANGE),                      # body
    ([(10, 7), (25, 7), (25, 9), (10, 9)], BLUE),                        # priming slide
    ([(26, 0), (35, 0), (35, 6), (26, 6)], ORANGE),                      # barrel
    ([(34, -1), (38, -1), (38, 7), (34, 7)], BLUE),                      # muzzle
    ([(36.6, 2), (38, 2), (38, 4), (36.6, 4)], GREY),                    # bore
    ([(30, 6), (32, 6), (32, 8), (30, 8)], BLUE),                        # front sight
    ([(12, 1), (22, 1), (22, 4), (12, 4)], BLUE),                        # side panel
    ([(11, -2), (16, -2), (14, -11), (9, -11)], GREY),                   # grip
    ([(16, -2), (22, -2), (22, -7), (18, -7)], YELLOW),                  # trigger guard
    ([(18, -3), (20.5, -3), (20.5, -5.5), (19, -5.5)], None),            # guard hole
    ([(23, -2), (27, -2), (27, -8), (23, -8)], BLUE),                    # dart clip
]

def draw_blaster(size=32, muzzle="left"):
    """muzzle='left': points top-left like the vanilla crossbow (Java).
    muzzle='right': mirrored, points top-right like tools (Bedrock)."""
    s = size / 32
    ox, oy = 29 * s, 29 * s                       # rear of the blaster, bottom-right
    k = 0.7071 * s
    def px(u, v):                                 # U = up-left, V = up-right
        return (ox - u * k + v * k, oy - u * k - v * k)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    part = Image.new("I", (size, size), 0)       # which part owns each pixel
    for i, (poly, col) in enumerate(BLASTER, start=1):
        pts = [px(u, v) for u, v in poly]
        ImageDraw.Draw(img).polygon(pts, fill=col if col else (0, 0, 0, 0))
        ImageDraw.Draw(part).polygon(pts, fill=i if col else 0)
    bevel(img, part, up=(1, -1))
    return img.transpose(Image.FLIP_LEFT_RIGHT) if muzzle == "right" else img

def bevel(img, part, up):
    """Light the 'up' edge of each part, shadow the opposite edge, dark outline."""
    W, H = img.size
    src, ids = img.load(), part.load()
    out = img.copy(); o = out.load()
    for y in range(H):
        for x in range(W):
            if src[x, y][3] == 0:
                continue
            def pid(dx, dy):
                X, Y = x + dx, y + dy
                return ids[X, Y] if 0 <= X < W and 0 <= Y < H and src[X, Y][3] else 0
            me = ids[x, y]
            if any(pid(dx, dy) == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                o[x, y] = shade(src[x, y], 0.38)                      # outline
            elif pid(*up) != me:
                o[x, y] = shade(src[x, y], 1.22)                      # highlight
            elif pid(-up[0], -up[1]) != me:
                o[x, y] = shade(src[x, y], 0.78)                      # shadow
    img.paste(out)

# -------------------------------------------------------------- lightsabers
# colour -> (blade colour, hilt colour, dye used to craft it)
LIGHTSABERS = {
    "blue":   ("#3C8CFF", "#B4B4BE", "blue_dye"),
    "red":    ("#FF2E2E", "#4A4250", "red_dye"),
    "green":  ("#39E65A", "#B4B4BE", "green_dye"),
    "purple": ("#B04CFF", "#B4B4BE", "purple_dye"),
    "yellow": ("#FFE23C", "#D9A92B", "yellow_dye"),
    "cyan":   ("#36E8F5", "#B4B4BE", "cyan_dye"),
    "orange": ("#FF8A2A", "#B8743E", "orange_dye"),
}

def draw_saber(blade_hex, hilt_hex):
    """16x16, hilt bottom-left, tip top-right (same as vanilla swords)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); p = img.load()
    blade, hilt = hexc(blade_hex), hexc(hilt_hex)
    ring, white = hexc("#3A3A46"), hexc("#FFFFFF")
    def band(x, y, core, side):                    # 3-pixel diagonal cross-section
        p[x, y] = core; p[x + 1, y] = side; p[x, y - 1] = side
    for i in range(9):                             # blade (5,10) -> (13,2)
        band(5 + i, 10 - i, white, blade)
    p[14, 1] = blade                               # rounded tip
    for i in range(5):                             # hilt (0,15) -> (4,11)
        c = ring if i in (1, 3) else hilt
        band(i, 15 - i, shade(c, 1.15), shade(c, 0.8))
    p[0, 15] = shade(hilt, 0.6)                    # pommel
    p[4, 10] = p[5, 11] = hexc("#1E1E24")          # emitter shroud
    bevel_outline(img)
    return img

def bevel_outline(img):
    """Darken the outermost hilt pixels so it reads on light and dark slots."""
    W, H = img.size; src = img.copy().load(); p = img.load()
    for y in range(H):
        for x in range(W):
            if src[x, y][3] and x + y >= 15 and x < 6 and y > 9:
                if any(not (0 <= x + dx < W and 0 <= y + dy < H) or src[x + dx, y + dy][3] == 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    p[x, y] = shade(src[x, y], 0.7)
