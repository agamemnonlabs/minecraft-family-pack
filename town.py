"""The Undersea town around the hub: original cartoon buildings (seashell, coconut and watermelon houses,
a submarine cafe), 6 empty plots for the kids, a jelly meadow, streets, a welcome arch and hidden lights.
Coordinates are relative to the hub centre (undersea.HUB_*): +x east, +z south, y=0 is the ground
(the hub platform's level); buildings stand on it from y=1.
  python3 town.py   -> previews/town-map.png + previews/town-buildings.png
  build.py          -> datapack functions family:undersea/town/*  (admin runs family:undersea/build_town)"""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
M = "minecraft:"
SAND, SANDSTONE, WATER = M + "sand", M + "sandstone", M + "water"
STREET, CURB = M + "smooth_sandstone", M + "pink_terracotta"
LAMP_POST, LAMP = M + "prismarine_wall", M + "sea_lantern"
GLASS = M + "light_blue_stained_glass"
WL_SUFFIX = ("_stairs", "_slab", "_wall", "_fence", "_pane", "_sign", "_trapdoor")
WL_IDS = {M + "iron_bars", M + "lantern", M + "light", M + "sea_pickle"}

def wl(b):
    """Everything here is underwater: waterloggable blocks must say so, or they hold an air pocket."""
    base = b.split("[")[0].split("{")[0]
    if not (base.endswith(WL_SUFFIX) or base in WL_IDS) or "waterlogged" in b:
        return b
    if "[" in b:
        return b.replace("[", "[waterlogged=true,", 1)
    return base + "[waterlogged=true]" + b[len(base):]

def sign(kind, state, *lines):
    msgs = ",".join('{text:"%s"}' % s for s in (list(lines) + ["", "", "", ""])[:4])
    return f"{M}{kind}[{state}]{{front_text:{{messages:[{msgs}]}}}}"

class Town:
    def __init__(self):
        self.v = {}            # (x, y, z) -> block
        self.zones = []        # (x1, z1, x2, z2, top): flattened to sand at y=0, water above up to `top`
        self.parts = {}        # part name -> list of positions, so each builds in its own tick
        self.labels = []       # (x, z, text) for the map preview
        self.part = None

    def set(self, x, y, z, b):
        self.v[(x, y, z)] = b
        self.parts.setdefault(self.part, []).append((x, y, z))

    def box(self, x1, y1, z1, x2, y2, z2, b):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, b)

    def clear(self, x1, z1, x2, z2, top):
        self.zones.append((min(x1, x2), min(z1, z2), max(x1, x2), max(z1, z2), top))

    def lamp(self, x, z, h=3):
        self.box(x, 1, z, x, h, z, LAMP_POST)
        self.set(x, h + 1, z, LAMP)

# ---------------------------------------------------------------- buildings (doors face south unless noted)
def seashell(t, cx, cz):
    """A tall spiral shell: cream with a pink spiral stripe, coral door frame, round windows."""
    t.part = "seashell"; t.labels.append((cx, cz, "Seashell house"))
    H, wall = 17, set()
    for y in range(0, H + 1):
        r = 6.2 * (1 - y / H) ** 0.75 + 0.4
        for dx in range(-7, 8):
            for dz in range(-7, 8):
                d = math.hypot(dx, dz)
                if y == 0 and d <= r:
                    t.set(cx + dx, 0, cz + dz, STREET)
                elif y > 0 and d <= r and (d > r - 1.3 or r < 1.6):
                    turn = (math.atan2(dz, dx) / (2 * math.pi) + y / 7) % 1
                    t.set(cx + dx, y, cz + dz, CURB if turn < 0.3 else M + "white_terracotta")
                    wall.add((cx + dx, y, cz + dz))
    t.set(cx, H + 1, cz, CURB)
    for y in range(1, 6):                                   # door: 3 wide, 4 high, coral frame
        for dx in range(-2, 3):
            for dz in range(1, 8):
                p = (cx + dx, y, cz + dz)
                if p in wall:
                    if abs(dx) <= 1 and y <= 4:
                        del t.v[p]
                    else:
                        t.v[p] = M + "brain_coral_block"
    for y, (ux, uz) in ((7, (1, 0)), (7, (-1, 0)), (11, (0, 1)), (10, (1, -1)), (10, (-1, -1))):
        out = max((p for p in wall if p[1] == y), key=lambda p: (p[0] - cx) * ux + (p[2] - cz) * uz)
        t.v[out] = GLASS
    t.set(cx, 8, cz, M + "light[level=15]")

def coconut(t, cx, cz):
    """A hairy brown coconut with white flesh inside, three eyes, a striped straw and a paper umbrella."""
    t.part = "coconut"; t.labels.append((cx, cz, "Coconut house"))
    rnd, R, cy = random.Random(7), 6.5, 6.0
    for x in range(-7, 8):
        for y in range(0, 13):
            for z in range(-7, 8):
                d = math.sqrt(x * x + (y + 0.5 - cy) ** 2 + z * z)
                if y == 0 and d <= R:
                    t.set(cx + x, 0, cz + z, STREET)
                elif y > 0 and 5.0 < d <= R:
                    if d > 5.7:
                        k = rnd.random()
                        b = M + ("brown_terracotta" if k < 0.65 else "brown_wool" if k < 0.9 else "dark_oak_planks")
                    else:
                        b = M + "white_concrete"
                    t.set(cx + x, y, cz + z, b)
    for x, z in ((-2, -1), (2, -1), (0, 2)):                # the three eyes, on the shell near the top
        t.set(cx + x, 11, cz + z, M + "black_terracotta")
    for y in range(1, 5):                                   # door, flesh showing around it
        for x in range(-1, 2):
            for z in range(3, 8):
                t.v.pop((cx + x, y, cz + z), None)
    for side in (-1, 1):                                    # side windows through both layers
        for y in range(5, 8):
            for z in range(-1, 2):
                for x in range(4, 8):
                    p = (cx + side * x, y, cz + z)
                    if p in t.v:
                        t.v[p] = GLASS if t.v[p] != M + "white_concrete" else None
    for p in [p for p, b in t.v.items() if b is None]:
        del t.v[p]
    for i in range(0, 34):                                  # straw: red and white stripes, leaning out
        s = i / 33
        x, y, z = cx + 1 + 5 * s, 10 + 9 * s, cz + 1 + 2 * s
        for ox, oz in ((0, 0), (1, 0)):
            t.set(round(x) + ox, round(y), round(z) + oz, M + ("red_concrete" if (round(y) // 2) % 2 else "white_concrete"))
    px, pz = cx - 2, cz - 2                                 # umbrella: pole + striped canopy
    t.box(px, 12, pz, px, 16, pz, M + "oak_fence")
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            d = math.hypot(dx, dz)
            if d <= 3.4:
                y = 18 if d < 1.6 else 17
                sector = int((math.atan2(dz, dx) + math.pi) / (math.pi / 4)) % 2
                t.set(px + dx, y, pz + dz, M + ("yellow_concrete" if sector else "orange_concrete"))
    t.set(cx, 7, cz, M + "light[level=15]")

def watermelon(t, cx, cz):
    """A quarter of a giant watermelon: striped green dome at the back, the cut face (red, with
    black-glass seeds as windows) at the front facing south, door in the middle."""
    t.part = "watermelon"; t.labels.append((cx, cz - 4, "Watermelon house"))
    R = 8.4
    seeds = {(round(4.6 * math.cos(a)), round(4.6 * math.sin(a))) for a in map(math.radians, (25, 55, 90, 125, 155))}
    seeds |= {(round(2.6 * math.cos(a)), round(2.6 * math.sin(a))) for a in map(math.radians, (50, 130))}
    for x in range(-9, 10):
        for y in range(0, 10):
            for z in range(-9, 1):
                d = math.sqrt(x * x + y * y + z * z)
                if d > R:
                    continue
                p = (cx + x, y, cz + z)
                if y == 0:
                    t.set(*p, STREET)
                elif z == 0:                                # the cut face
                    f = math.hypot(x, y)
                    b = "green_concrete" if f > 7.4 else "white_concrete" if f > 6.4 else "red_concrete"
                    if (x, y) in seeds:
                        b = "black_stained_glass"
                    if abs(x) <= 1 and y <= 4:
                        continue                            # door
                    t.set(*p, M + b)
                elif d > 7.2:                               # striped rind
                    stripe = int((math.atan2(x, -z) + math.pi) / (math.pi / 9)) % 2
                    t.set(*p, M + ("green_concrete" if stripe else "lime_concrete"))
    t.set(cx, 5, cz - 4, M + "light[level=15]")

def submarine(t, cx, cz):
    """A sunken orange submarine, door on the north side: the Bubble Cafe, with a counter, tables
    and hanging lanterns inside."""
    t.part = "cafe"; t.labels.append((cx, cz, "Bubble Cafe (submarine)"))
    R, L, cy, hull = 4.5, 8, 4.0, set()
    def radius(x):
        e = abs(x) - L
        return R if e <= 0 else math.sqrt(R * R - e * e) if e < R else -1
    for x in range(-13, 14):
        r = radius(x)
        for y in range(0, 10):
            for dz in range(-5, 6):
                d = math.hypot(y + 0.5 - cy, dz)
                if d > r:
                    continue
                p = (cx + x, y, cz + dz)
                if d > r - 1.2 or abs(x) >= L + R - 1:
                    dy = y + 0.5 - cy
                    b = "white_concrete" if 0.5 <= dy < 1.5 else "orange_concrete"
                    if x >= L + 2 and abs(dy) <= 1.5 and abs(dz) <= 1:
                        b = "light_blue_stained_glass"      # nose window
                    t.set(*p, M + b); hull.add(p)
                elif y == 1:
                    t.set(*p, M + "spruce_planks")
    for x in range(-8, 9, 4):                               # portholes
        for dz in (-4, 4):
            t.v[(cx + x, 5, cz + dz)] = GLASS
    for x in range(-3, 3):                                  # conning tower, periscope, hatch
        for z in range(-2, 3):
            if abs(z) == 2 and x in (-3, 2):
                continue
            t.box(cx + x, 9, cz + z, cx + x, 11, cz + z, M + ("white_concrete" if x in (-3, 2) or abs(z) == 2 else "orange_concrete"))
    t.set(cx - 1, 12, cz, M + "iron_trapdoor[half=bottom]")
    t.box(cx + 1, 12, cz, cx + 1, 14, cz, M + "iron_bars")
    t.set(cx + 1, 15, cz, M + "iron_block"); t.set(cx + 2, 15, cz, M + "light_blue_stained_glass")
    for y in (9, 10):                                       # tail fin + propeller at the back (west)
        t.box(cx - 12, y, cz, cx - 10, y, cz, M + "orange_concrete")
    t.set(cx - 14, 4, cz, M + "iron_block"); t.set(cx - 13, 4, cz, M + "iron_bars")
    for y, z in ((5, 0), (6, 0), (3, 0), (2, 0), (4, 1), (4, 2), (4, -1), (4, -2)):
        t.set(cx - 14, y, cz + z, M + "iron_bars")
    for y in range(1, 4):                                   # door in the north side, white frame
        for x in range(-1, 2):
            for z in range(-5, -2):
                t.v.pop((cx + x, y, cz + z), None)
    t.set(cx, 4, cz - 5, sign("oak_wall_sign", "facing=north", "~ Bubble Cafe ~", "Kelp shakes", "Coral cookies"))
    t.box(cx + 1, 2, cz + 2, cx + 6, 2, cz + 2, M + "smooth_quartz")            # counter
    t.set(cx + 7, 2, cz + 2, M + "barrel[facing=up]")
    for tx in (-3, -7):                                                       # tables + chairs
        t.set(cx + tx, 2, cz - 1, M + "spruce_slab[type=top]")
        t.set(cx + tx - 1, 2, cz - 1, M + "spruce_stairs[facing=west]")
        t.set(cx + tx + 1, 2, cz - 1, M + "spruce_stairs[facing=east]")
    for x in (-6, -2, 2, 6):
        t.set(cx + x, 7, cz, M + "lantern[hanging=true]")
    t.box(cx - 1, 0, 4, cx + 1, 0, cz - 6, CURB)                           # path to the street
    t.clear(cx - 1, 4, cx + 1, cz - 6, 4)

def plot(t, n, px, pz):
    """An empty 11x11 sand plot with a coral-pink border, a lamp post and a sign, front to the north."""
    t.part = "plots"; t.labels.append((px, pz, f"Plot {n}"))
    for x in range(-5, 6):
        for z in range(-5, 6):
            t.set(px + x, 0, pz + z, CURB if 5 in (abs(x), abs(z)) else SAND)
    t.lamp(px - 5, pz - 5, 2)
    t.set(px - 4, 1, pz - 6, sign("oak_sign", "rotation=8", f"Plot {n}", "Build your", "house here!"))

def jelly(t, x, y, z, glass, core):
    for dx in range(-3, 4):
        for dy in range(0, 4):
            for dz in range(-3, 4):
                d = math.sqrt(dx * dx + dy * dy + dz * dz)
                if d <= 2.6:
                    t.set(x + dx, y + dy, z + dz, M + (core if d <= 1.3 else glass))
    for (dx, dz), n in zip(((-2, 0), (2, 0), (0, -2), (0, 2), (0, 0)), (4, 3, 5, 3, 5)):
        t.box(x + dx, y - n, z + dz, x + dx, y - 1, z + dz, M + glass + "_pane")

def meadow(t, x1, z1, x2, z2):
    """Rolling green hills (moss) with seagrass and glowing sea pickles; big jellyfish float above."""
    t.part = "meadow"; t.labels.append(((x1 + x2) // 2, (z1 + z2) // 2, "Jelly meadow"))
    rnd = random.Random(3)
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            h = round(1.4 + 1.2 * math.sin(x / 4.0) + 1.0 * math.cos(z / 3.4) + 0.8 * math.sin((x + z) / 6.0))
            h = max(0, min(4, h)) if min(x - x1, x2 - x, z - z1, z2 - z) > 1 else 0
            t.box(x, 0, z, x, h, z, M + "moss_block")
            k = rnd.random()
            if k < 0.22:
                t.set(x, h + 1, z, M + "seagrass")
            elif k < 0.26:
                t.set(x, h + 1, z, M + "tall_seagrass[half=lower]"); t.set(x, h + 2, z, M + "tall_seagrass[half=upper]")
            elif k < 0.29:
                t.set(x, h + 1, z, M + "sea_pickle[pickles=3]")
    t.part = "jellies"
    for (x, y, z), (glass, core) in zip(
            ((-16, 9, -44), (-6, 12, -38), (5, 10, -46), (15, 13, -40), (-12, 14, -33), (20, 9, -47), (-20, 12, -49), (9, 15, -34)),
            [("pink_stained_glass", "pearlescent_froglight"), ("magenta_stained_glass", "pearlescent_froglight"),
             ("light_blue_stained_glass", "verdant_froglight")] * 3):
        jelly(t, x, y, z, glass, core)
    t.part = "meadow"
    t.set(0, 1, z2 + 1, sign("oak_sign", "rotation=0", "", "Jelly Meadow", "", ""))

# ---------------------------------------------------------------- the town
STREETS = {"north": (0, -1, 27), "south": (0, 1, 40), "east": (1, 0, 40), "west": (-1, 0, 46)}

def build():
    t = Town()
    t.part = "streets"
    for name, (ux, uz, end) in STREETS.items():
        for s in range(9, end + 1):
            for o in range(-3, 4):
                if ux:
                    x, z = ux * s, o
                else:
                    x, z = o, uz * s
                t.set(x, 0, z, CURB if abs(o) == 3 else STREET)
        if ux:
            t.clear(ux * 9, -4, ux * end, 4, 12)
        else:
            t.clear(-4, uz * 9, 4, uz * end, 12)
    seashell(t, 16, -17); t.clear(8, -26, 24, -8, 20)
    coconut(t, 31, -17); t.clear(23, -26, 39, -8, 20)
    watermelon(t, -16, -10); t.clear(-26, -20, -6, -7, 11)
    submarine(t, 24, 13); t.clear(9, 6, 39, 20, 17)
    for n, (px, pz) in enumerate(((-12, 12), (-26, 12), (-40, 12), (-12, 27), (-26, 27), (-40, 27)), 1):
        plot(t, n, px, pz); t.clear(px - 6, pz - 6, px + 6, pz + 6, 8)
    t.part = "streets"
    t.box(-45, 0, 19, -4, 0, 20, CURB); t.clear(-45, 19, -4, 20, 6)               # footpath between plot rows
    meadow(t, -24, -50, 24, -28); t.clear(-26, -52, 26, -27, 18)
    t.part = "square"                                                          # square, arch, bus stop
    for x, z in ((7, 7), (-7, 7), (7, -7), (-7, -7)):
        t.lamp(x, z)
    for z, f in ((-8, "north"), (8, "south")):
        for x in (-6, -5, -4, 4, 5, 6):
            t.set(x, 1, z, M + f"spruce_stairs[facing={f}]")
    for x in (-4, 4):
        t.box(x, 1, -12, x, 7, -12, M + "brain_coral_block")
    t.box(-4, 8, -12, 4, 8, -12, M + "horn_coral_block")
    t.box(-3, 9, -12, 3, 9, -12, M + "tube_coral_block")
    t.set(0, 8, -13, sign("oak_wall_sign", "facing=north", "Welcome to", "", "(name me!)"))
    t.set(0, 8, -11, sign("oak_wall_sign", "facing=south", "Welcome to", "", "(name me!)"))
    for x, z in ((5, 12), (5, 16), (7, 12), (7, 16)):
        t.box(x, 1, z, x, 3, z, M + "spruce_fence")
    for x in range(5, 8):
        for z in range(12, 17):
            t.set(x, 4, z, M + ("tube_coral_block" if (x + z) % 2 else "horn_coral_block"))
    t.box(6, 1, 13, 6, 1, 15, M + "spruce_stairs[facing=east]")
    t.set(4, 1, 12, sign("oak_sign", "rotation=4", "", "BUS STOP", "", ""))
    t.clear(4, 11, 8, 17, 6)
    t.part = "streets"                                                         # street lamps
    taken = {(x, z) for (x, y, z) in t.v if y > 0}
    for name, (ux, uz, end) in STREETS.items():
        for s in range(14, end + 1, 8):
            for o in (-4, 4):
                x, z = (ux * s, o) if ux else (o, uz * s)
                if all((x + a, z + b) not in taken for a in (-1, 0, 1) for b in (-1, 0, 1)):
                    t.lamp(x, z)
    t.part = "lights"                                                          # hidden light, daylight-bright
    for x in range(-49, 43, 7):
        for z in range(-52, 41, 7):
            if any(a <= x <= c and b <= z <= d for a, b, c, d, _ in t.zones) or math.hypot(x, z) <= 11:
                if (x, 5, z) not in t.v:
                    t.set(x, 5, z, M + "light[level=15]")
    return t

# ---------------------------------------------------------------- datapack functions
def datapack(data, put, dim, hub):
    hx, hy, hz = hub
    t = build()
    at = f"execute in {dim} positioned {hx} {hy} {hz} run "
    xs = [x for (x, _, _) in t.v] + [a for a, *_ in t.zones] + [c for _, _, c, *_ in t.zones]
    zs = [z for (_, _, z) in t.v] + [b for _, b, *_ in t.zones] + [d for *_, d, _ in t.zones]
    area = f"{hx + min(xs)} {hz + min(zs)} {hx + max(xs)} {hz + max(zs)}"
    f = f"{data}/data/family/function/undersea"
    def fills(positions, only_water=False):
        out, done = [], set()
        for (x, y, z) in sorted(positions, key=lambda p: (p[1], p[2], p[0])):
            if (x, y, z) in done or (x, y, z) not in t.v:
                continue
            b, x2 = t.v[(x, y, z)], x
            while (x2 + 1, y, z) in t.v and t.v[(x2 + 1, y, z)] == b and (x2 + 1, y, z) not in done and "{" not in b:
                x2 += 1
            done.update((i, y, z) for i in range(x, x2 + 1))
            out.append(f"{at}fill ~{x} ~{y} ~{z} ~{x2} ~{y} ~{z} {wl(b)}" + (" replace minecraft:water" if only_water else ""))
        return out
    prep = []
    for x1, z1, x2, z2, top in t.zones:
        prep += [f"{at}fill ~{x1} ~-4 ~{z1} ~{x2} ~-1 ~{z2} {SANDSTONE} replace #minecraft:replaceable",
                 f"{at}fill ~{x1} ~0 ~{z1} ~{x2} ~0 ~{z2} {SAND}"]
        for y1 in range(1, top + 1, 8):              # water in slabs (fill is capped at 32768 blocks)
            prep.append(f"{at}fill ~{x1} ~{y1} ~{z1} ~{x2} ~{min(top, y1 + 7)} ~{z2} {WATER}")
    order = ["prep", "streets", "square", "seashell", "coconut", "watermelon", "cafe", "plots", "meadow", "jellies", "lights"]
    bodies = {"prep": prep, **{p: fills(t.parts[p], p == "lights") for p in order[1:]}}
    for i, p in enumerate(order):
        nxt = (f"schedule function family:undersea/town/{order[i + 1]} 1s replace" if i + 1 < len(order) else
               f"execute in {dim} run forceload remove {area}")
        put(f"{f}/town/{p}.mcfunction", "\n".join(bodies[p] + [nxt]) + "\n")
    put(f"{f}/build_town.mcfunction", "\n".join([
        f"execute in {dim} run forceload add {area}",
        "schedule function family:undersea/town/start 4s replace"]) + "\n")
    put(f"{f}/town/start.mcfunction", "\n".join([
        f"execute in {dim} positioned {hx} {hy} {hz} unless loaded ~{min(xs)} ~ ~{min(zs)} run return run "
        "schedule function family:undersea/town/start 2s replace",
        f"execute in {dim} positioned {hx} {hy} {hz} unless loaded ~{max(xs)} ~ ~{max(zs)} run return run "
        "schedule function family:undersea/town/start 2s replace",
        "function family:undersea/town/prep"]) + "\n")
    return {p: len(b) for p, b in bodies.items()}

# ---------------------------------------------------------------- previews
COLOURS = {
    "sand": "#DBCF9C", "sandstone": "#D8CB94", "smooth_sandstone": "#E3D7A5", "pink_terracotta": "#C47F7F",
    "white_terracotta": "#E8D6CB", "brown_terracotta": "#5E3E2A", "brown_wool": "#734A2C", "dark_oak_planks": "#43301B",
    "white_concrete": "#F2F4F4", "black_terracotta": "#26170F", "red_concrete": "#C8312D", "yellow_concrete": "#F5C21F",
    "orange_concrete": "#EE7A12", "oak_fence": "#A8864F", "green_concrete": "#4C6B20", "lime_concrete": "#79C02A",
    "black_stained_glass": "#2A2A33", "light_blue_stained_glass": "#8FD3F0", "spruce_planks": "#73532F",
    "smooth_quartz": "#ECE6DE", "barrel": "#8C6239", "spruce_slab": "#73532F", "spruce_stairs": "#73532F",
    "iron_bars": "#9DA3A6", "iron_block": "#DADADA", "iron_trapdoor": "#C4C4C4", "lantern": "#F2B33D",
    "prismarine_wall": "#62A396", "sea_lantern": "#D6F0E8", "brain_coral_block": "#D45C9E", "horn_coral_block": "#E6D33A",
    "tube_coral_block": "#3657D6", "moss_block": "#5F8C30", "seagrass": "#3E8A2E", "tall_seagrass": "#3E8A2E",
    "sea_pickle": "#9AB04A", "pink_stained_glass": "#F4A6CB", "magenta_stained_glass": "#D77BE6",
    "pink_stained_glass_pane": "#F4A6CB", "magenta_stained_glass_pane": "#D77BE6",
    "light_blue_stained_glass_pane": "#8FD3F0", "pearlescent_froglight": "#F2D9EC", "verdant_froglight": "#E3F0C9",
    "oak_sign": "#B8945A", "oak_wall_sign": "#B8945A", "spruce_fence": "#73532F", "light": None}

def colour(b):
    name = b.split("[")[0].split("{")[0].removeprefix(M)
    if name not in COLOURS:
        raise KeyError(f"no preview colour for {name}")
    c = COLOURS[name]
    return None if c is None else tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))

def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)

def iso(vox, unit=12, pad=20, bg=(28, 64, 92)):
    from PIL import Image, ImageDraw
    vox = {p: c for p, b in vox.items() if (c := colour(b))}
    P = lambda x, y, z: ((x - z) * unit, (x + z) * unit / 2 - y * unit)
    pts = [P(x + a, y + b, z + c) for (x, y, z) in vox for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    minx, miny = min(p[0] for p in pts), min(p[1] for p in pts)
    W, H = int(max(p[0] for p in pts) - minx) + 2 * pad, int(max(p[1] for p in pts) - miny) + 2 * pad
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    S = lambda x, y, z: (P(x, y, z)[0] - minx + pad, P(x, y, z)[1] - miny + pad)
    for (x, y, z) in sorted(vox, key=lambda p: (p[0] + p[1] + p[2], p[1])):
        c = vox[(x, y, z)]
        if (x, y + 1, z) not in vox:
            d.polygon([S(x, y + 1, z), S(x + 1, y + 1, z), S(x + 1, y + 1, z + 1), S(x, y + 1, z + 1)], fill=c)
        if (x + 1, y, z) not in vox:
            d.polygon([S(x + 1, y, z), S(x + 1, y + 1, z), S(x + 1, y + 1, z + 1), S(x + 1, y, z + 1)], fill=shade(c, 0.78))
        if (x, y, z + 1) not in vox:
            d.polygon([S(x, y, z + 1), S(x + 1, y, z + 1), S(x + 1, y + 1, z + 1), S(x, y + 1, z + 1)], fill=shade(c, 0.6))
    return img

def previews():
    from PIL import Image, ImageDraw, ImageFont
    t = build()
    os.makedirs(f"{HERE}/previews", exist_ok=True)
    font = ImageFont.load_default(size=15); big = ImageFont.load_default(size=22)
    # top-down map: 6 px per block, reef left as is shown dark teal
    xs = [x for (x, _, _) in t.v]; zs = [z for (_, _, z) in t.v]
    x0, z0, x1, z1 = min(xs) - 3, min(zs) - 3, max(xs) + 3, max(zs) + 3
    k = 7
    img = Image.new("RGB", ((x1 - x0 + 1) * k, (z1 - z0 + 1) * k + 40), (24, 70, 84)); d = ImageDraw.Draw(img)
    top = {}
    for (x, y, z), b in t.v.items():
        if colour(b) and ((x, z) not in top or y > top[(x, z)][0]):
            top[(x, z)] = (y, colour(b))
    for zx in t.zones:
        for x in range(zx[0], zx[2] + 1):
            for z in range(zx[1], zx[3] + 1):
                top.setdefault((x, z), (0, colour(SAND)))
    for x in range(-10, 11):                                 # existing hub + sand ring
        for z in range(-10, 11):
            if math.hypot(x, z) <= 10.5:
                top.setdefault((x, z), (0, colour(SAND)))
    for x in range(-5, 6):
        for z in range(-5, 6):
            top[(x, z)] = (0, (120, 170, 160))
    top[(5, 5)] = (1, (110, 220, 240))
    for (x, z), (y, c) in top.items():
        d.rectangle([(x - x0) * k, (z - z0) * k, (x - x0 + 1) * k - 1, (z - z0 + 1) * k - 1], fill=shade(c, 0.85 + 0.03 * min(y, 5)))
    for x, z, s in t.labels + [(0, 0, "Hub"), (0, -12, "Welcome arch"), (6, 14, "Bus stop")]:
        w = d.textlength(s, font=font)
        cx, cy = (x - x0 + 0.5) * k, (z - z0 + 0.5) * k
        d.rectangle([cx - w / 2 - 3, cy - 9, cx + w / 2 + 3, cy + 9], fill=(255, 255, 255))
        d.text((cx - w / 2, cy - 8), s, fill=(20, 20, 20), font=font)
    d.text((10, img.height - 32), "North is up. Dark teal = reef left as it is. Streets lead off the round square at the hub.",
           fill=(255, 255, 255), font=font)
    img.save(f"{HERE}/previews/town-map.png")
    # buildings, one isometric close-up each, in a grid
    shots = []
    for part, title in (("seashell", "Seashell house"), ("coconut", "Coconut house"), ("watermelon", "Watermelon house"),
                        ("cafe", "Bubble Cafe (submarine)"), ("square", "Square: arch, benches, bus stop, lamps"),
                        ("plots", "Kids' plots (one shown)"), ("meadow", "Jelly meadow")):
        ps = set(t.parts[part]) | (set(t.parts["jellies"]) if part == "meadow" else set())
        if part == "plots":
            ps = {p for p in ps if -18 <= p[0] <= -6 and 5 <= p[2] <= 18}
        vox = {p: t.v[p] for p in ps if p in t.v}
        if part not in ("meadow",):
            bx = [p[0] for p in vox]; bz = [p[2] for p in vox]
            for x in range(min(bx) - 1, max(bx) + 2):
                for z in range(min(bz) - 1, max(bz) + 2):
                    vox.setdefault((x, -1, z), SAND)
        shots.append((title, iso(vox, unit=9 if part in ("meadow", "square") else 12)))
    cols, gap = 2, 16
    cw = max(i.width for _, i in shots); ch = max(i.height for _, i in shots) + 34
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * gap, math.ceil(len(shots) / cols) * (ch + gap) + gap), (16, 40, 58))
    sd = ImageDraw.Draw(sheet)
    for i, (title, im) in enumerate(shots):
        x, y = gap + (i % cols) * (cw + gap), gap + (i // cols) * (ch + gap)
        sheet.paste(im, (x + (cw - im.width) // 2, y + 34))
        sd.text((x + 6, y + 4), title, fill=(255, 255, 255), font=big)
    sheet.save(f"{HERE}/previews/town-buildings.png")
    return t

if __name__ == "__main__":
    t = previews()
    print(len(t.v), "blocks;", len(t.zones), "clear zones; parts:", {p: len(v) for p, v in t.parts.items()})
