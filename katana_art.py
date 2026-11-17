"""Original pixel art for the elemental katanas (32x32, pommel bottom-left, tip top-right like vanilla swords).
Each pixel is classified in the sword's own coordinates: u = along the sword from the pommel, v = across it
(+v = the cutting edge side). Java gets the hilt and an animated, see-through glowing blade as two layers;
Bedrock gets one opaque picture (its item pictures can't blend)."""
import math, random
from PIL import Image
from art import hexc, mix, shade

# element -> colours: edge glow core/rim, halo, handle wrap + diamonds, guard + its rim
PALETTES = {
    "flame":   dict(core="#FFD27A", edge="#FF5A1F", halo="#FF7A1A", wrap="#8B1A1A", ray="#F2E2C4",
                    guard="#2B2B33", rim="#E0A030"),
    "water":   dict(core="#C8F4FF", edge="#2F8BFF", halo="#3FA9FF", wrap="#1F3A8A", ray="#E6F2FF",
                    guard="#AEB8C6", rim="#3E6FD8"),
    "thunder": dict(core="#FFFBD0", edge="#FFC400", halo="#FFE14D", wrap="#1E1E24", ray="#F5D33A",
                    guard="#3A3A44", rim="#FFD23A"),
    "wind":    dict(core="#F0FFF8", edge="#2FCF8F", halo="#6FF2C0", wrap="#1E6B4F", ray="#EAF7F0",
                    guard="#5E8F7A", rim="#CFEFE2"),
}
STEEL, STEEL_DARK, GOLD = hexc("#D5DCE4"), hexc("#7E8894"), hexc("#E8B84A")
P0, P1 = (3.0, 29.0), (29.6, 2.4)               # pommel end -> tip, pixel coordinates
L = math.dist(P0, P1)
DX, DY = (P1[0] - P0[0]) / L, (P1[1] - P0[1]) / L
NX, NY = DY, -DX                                 # +v points up-left: the cutting edge side. Held items turn this
                                                 # side forward/down (where axe heads sit); down-right faced back.
POMMEL, HANDLE, GUARD, COLLAR = 1.6, 9.6, 12.0, 13.2   # where each part ends (u)
FRAMES = 8                                       # Java blade animation frames

def uv(x, y):
    cx, cy = x + 0.5 - P0[0], y + 0.5 - P0[1]
    return cx * DX + cy * DY, cx * NX + cy * NY

def spine(u):
    """Centre line of the blade: a gentle katana curve away from the edge towards the tip."""
    t = max(0.0, (u - COLLAR) / (L - COLLAR))
    return -1.5 * t ** 1.8

def widths(u):
    """(spine side, edge side) half-widths; the tip (kissaki) sweeps the edge up into the spine."""
    left = L - u
    return 1.05 * min(1.0, left / 1.0), 1.55 * min(1.0, left / 5.0) ** 1.1

def hamon(el, u, phase):
    """Where the glowing edge starts (offset from the spine line); each element has its own pattern.
    phase 0..1 shifts the pattern by exactly one wavelength, so the animation loops."""
    if el == "flame":     # tall, uneven peaks that rise towards the tip
        return 0.25 + 0.45 * abs(math.sin(0.9 * u - math.pi * phase)) ** 2
    if el == "water":     # smooth rolling waves
        return 0.35 + 0.3 * math.sin(0.7 * u - 2 * math.pi * phase)
    if el == "thunder":   # sharp sawtooth steps
        return 0.25 + 0.5 * ((0.55 * u - phase) % 1.0)
    return 0.45 + 0.2 * math.sin(0.45 * u - 2 * math.pi * phase)  # wind: long, low swells

def hilt_pixel(el, u, v):
    p = PALETTES[el]
    if u < 0:
        return None
    if u < POMMEL:
        return hexc(p["rim"]) if abs(v) <= 1.7 else None
    if u < HANDLE:                                # wrapped handle: diamonds of the ray-skin showing through
        if abs(v) > 1.5:
            return None
        if abs(v) > 1.05:
            return shade(hexc(p["wrap"]), 0.7)
        k = (u - POMMEL) % 2.8
        return hexc(p["ray"]) if abs(k - 1.4) < 0.7 - abs(v) * 0.6 else hexc(p["wrap"])
    if u < GUARD:                                 # the guard (tsuba): a disc seen edge-on
        if abs(v) > 3.0:
            return None
        return hexc(p["rim"]) if abs(v) > 2.2 else hexc(p["guard"])
    if u < COLLAR:                                # gold collar (habaki)
        return GOLD if abs(v) <= 1.4 else None
    return None

def blade_pixel(el, u, v, phase, solid):
    """Colour of a blade pixel (or its glow), None if empty. solid: opaque glow for Bedrock."""
    p = PALETTES[el]
    if u < COLLAR or u > L + 0.3:
        return None
    s = spine(u); back, front = widths(u)
    w = v - s                                     # across the blade, from the spine line
    if -back <= w <= front:
        h = hamon(el, u, phase) * front / 1.55
        if w < -back * 0.45:
            return STEEL_DARK                     # back of the spine
        if w < h:
            return STEEL
        t = (w - h) / max(0.01, front - h)        # 0 at the hamon line .. 1 at the very edge
        return mix(hexc(p["core"]), hexc(p["edge"]), t ** 1.5)
    if w > front and u > COLLAR + 0.5:            # glow on the edge side
        d = w - front
        if solid:
            return mix(hexc(p["halo"]), hexc("#FFFFFF"), 0.35) if d < 0.75 else None
        if d < 2.2:
            return hexc(p["halo"])[:3] + (round(190 * (1 - d / 2.2) ** 1.4),)
    return None

def sparkle(el, img, frame, solid):
    """Per-frame accents on the blade: sparks, shimmer bands, wind streaks (opaque when solid)."""
    p = PALETTES[el]; px = img.load(); rnd = random.Random(f"{el}{frame}")
    if el == "thunder":                            # a few sparks crackling around the edge
        for _ in range(4):
            u = rnd.uniform(COLLAR + 2, L - 1.5); v = spine(u) + widths(u)[1] + rnd.uniform(0.6, 2.4)
            x, y = P0[0] + u * DX + v * NX, P0[1] + u * DY + v * NY
            if 0 <= int(x) < 32 and 0 <= int(y) < 32:
                px[int(x), int(y)] = hexc("#FFFFFF") if rnd.random() < 0.5 else hexc(p["core"])
    if el in ("water", "wind"):                    # a bright band sliding from the guard to the tip
        band = COLLAR + (L - COLLAR + 6) * frame / FRAMES - 3
        for y in range(32):
            for x in range(32):
                u, v = uv(x, y)
                if px[x, y][3] and abs(u - band) < (1.0 if el == "water" else 0.7) and v > spine(u) - 0.4:
                    px[x, y] = mix(px[x, y], hexc("#FFFFFF"), 0.55)
    if el == "flame":                              # embers drifting off the edge
        for _ in range(3):
            u = rnd.uniform(COLLAR + 3, L - 1); v = spine(u) + widths(u)[1] + rnd.uniform(1.0, 2.6)
            x, y = P0[0] + u * DX + v * NX, P0[1] + u * DY + v * NY
            if 0 <= int(x) < 32 and 0 <= int(y) < 32:
                px[int(x), int(y)] = hexc(p["core"])[:3] + (255 if solid else 220,)

def draw(el, part="all", frame=0, solid=False, sparks=None):
    """part: 'hilt', 'blade' or 'all'. frame picks the animation phase of the blade.
    sparks: draw the per-frame accents (default: only on see-through Java art)."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); px = img.load()
    phase = frame / FRAMES
    for y in range(32):
        for x in range(32):
            u, v = uv(x, y)
            c = None
            if part in ("blade", "all"):
                c = blade_pixel(el, u, v, phase, solid)
            if part in ("hilt", "all") and c is None:
                c = hilt_pixel(el, u, v)
            if c:
                px[x, y] = c
    if part in ("blade", "all") and (not solid if sparks is None else sparks):
        sparkle(el, img, frame, solid)
    if part in ("hilt", "all"):
        outline(img)
    return img

def outline(img):
    """Darken hilt pixels that touch empty space, so the handle reads on light and dark slots."""
    src = img.copy().load(); px = img.load()
    for y in range(32):
        for x in range(32):
            if src[x, y][3] == 255 and uv(x, y)[0] < COLLAR and any(
                    not (0 <= x + dx < 32 and 0 <= y + dy < 32) or src[x + dx, y + dy][3] == 0
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = shade(src[x, y], 0.62)

def blade_strip(el):
    """Java: animated blade texture, FRAMES frames stacked top to bottom (needs a .mcmeta)."""
    strip = Image.new("RGBA", (32, 32 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        strip.paste(draw(el, "blade", f), (0, 32 * f))
    return strip

def bedrock_icon(el):
    """Bedrock: one opaque picture, glow painted as a solid light rim."""
    return draw(el, "all", 0, solid=True)

def bedrock_held_frames(el):
    """Bedrock in-hand flipbook: the icon art with the Java blade's moving pattern and sparkle, all
    opaque (entity_alphatest cuts see-through pixels)."""
    return [draw(el, "all", f, solid=True, sparks=True) for f in range(FRAMES)]
