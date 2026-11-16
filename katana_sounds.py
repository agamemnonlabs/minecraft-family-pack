"""Synthesised katana sounds (all original): a swing whoosh per element and one bigger sound per special move.
Building blocks: filtered noise whooshes, fire crackle, water bloops, electric buzz/crackle, wind whistle."""
import math, random, struct, wave

RATE = 44100

class BandPass:
    """State-variable filter; cutoff can change every sample (for sweeping whooshes)."""
    def __init__(self, q=0.9):
        self.low = self.band = 0.0; self.q = q
    def __call__(self, x, fc):
        f = 2 * math.sin(math.pi * min(fc, RATE / 6) / RATE)
        self.low += f * self.band
        high = x - self.low - self.q * self.band
        self.band += f * high
        return self.band

def bell(t, centre, width):
    return math.exp(-((t - centre) / width) ** 2)

def events(rnd, rate, dur):
    """Random times (Poisson-ish) for crackles and bloops."""
    out, t = [], 0.0
    while True:
        t += rnd.expovariate(rate)
        if t >= dur:
            return out
        out.append(t)

def render(path, dur, fn, seed):
    rnd = random.Random(seed)
    n = int(RATE * dur)
    out = fn(rnd, n)
    fade = int(0.02 * RATE)
    for i in range(min(fade, n)):                               # click-free ends
        out[i] *= i / fade; out[n - 1 - i] *= i / fade
    m = max(abs(x) for x in out) or 1
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(x / m * 0.89 * 32767)) for x in out))

def whoosh(rnd, n, f_lo, f_hi, centre, width, q=0.9):
    bp = BandPass(q); out = []
    for i in range(n):
        e = bell(i / n, centre, width)
        out.append(bp(rnd.uniform(-1, 1), f_lo + (f_hi - f_lo) * e) * e)
    return out

def add_crackle(out, rnd, rate, amp, ms=4.0, env=lambda t: 1.0):
    n = len(out); dur = n / RATE
    for t in events(rnd, rate, dur):
        a = amp * rnd.uniform(0.3, 1.0) * env(t / dur); start = int(t * RATE); length = int(ms / 1000 * RATE)
        prev = 0.0
        for k in range(length):
            if start + k >= n:
                break
            x = rnd.uniform(-1, 1); hp = x - prev; prev = x          # crude high-pass: sharp clicks
            out[start + k] += a * hp * math.exp(-k / (length / 4))

def add_bloops(out, times, amp, f0=320, f1=900, ms=55):
    n = len(out)
    for t, a in times:
        start = int(t * RATE); length = int(ms / 1000 * RATE); ph = 0.0
        for k in range(length):
            if start + k >= n:
                break
            f = f0 + (f1 - f0) * k / length; ph += 2 * math.pi * f / RATE
            out[start + k] += amp * a * math.sin(ph) * math.sin(math.pi * k / length)

def add_tone(out, f0, f1, amp, centre, width, wobble=0.0):
    n = len(out); ph = 0.0
    for i in range(n):
        t = i / n; f = f0 + (f1 - f0) * t + wobble * math.sin(2 * math.pi * 6 * t)
        ph += 2 * math.pi * f / RATE
        out[i] += amp * bell(t, centre, width) * math.sin(ph)

def add_buzz(out, rnd, f, amp, env):
    n = len(out); ph = 0.0
    for i in range(n):
        ph += (f * (1 + rnd.uniform(-0.08, 0.08))) / RATE
        out[i] += amp * env(i / n) * (2 * (ph % 1.0) - 1)          # jittery sawtooth = electric hum

def low_rumble(rnd, n, fc, env):
    lp = 0.0; out = []
    k = 2 * math.pi * fc / RATE
    for i in range(n):
        lp += k * (rnd.uniform(-1, 1) - lp)
        out.append(lp * env(i / n))
    return out

# ------------------------------------------------------------------------------ the sounds
def swing(el, rnd, n):
    if el == "flame":
        out = whoosh(rnd, n, 300, 2200, 0.4, 0.22)
        add_crackle(out, rnd, 70, 0.9, env=lambda t: bell(t, 0.45, 0.3))
        for i, r in enumerate(low_rumble(rnd, n, 160, lambda t: bell(t, 0.45, 0.25))):
            out[i] += 2.5 * r
    elif el == "water":
        out = whoosh(rnd, n, 220, 1500, 0.4, 0.24, q=1.1)
        add_bloops(out, [(rnd.uniform(0.15, 0.6) * n / RATE, rnd.uniform(0.4, 1.0)) for _ in range(4)], 0.35)
    elif el == "thunder":
        out = whoosh(rnd, n, 800, 4200, 0.35, 0.18)
        add_buzz(out, rnd, 95, 0.12, lambda t: bell(t, 0.35, 0.2))
        add_crackle(out, rnd, 150, 1.4, ms=3, env=lambda t: bell(t, 0.35, 0.25))
    else:   # wind
        out = whoosh(rnd, n, 400, 1900, 0.45, 0.26, q=0.7)
        add_tone(out, 950, 1350, 0.09, 0.45, 0.2, wobble=40)
    return out

def special(el, rnd, n):
    if el == "flame":       # a roaring rush of fire
        out = whoosh(rnd, n, 250, 1600, 0.35, 0.3)
        for i, r in enumerate(low_rumble(rnd, n, 220, lambda t: bell(t, 0.45, 0.35))):
            out[i] += 4.0 * r
        add_crackle(out, rnd, 260, 1.0, env=lambda t: bell(t, 0.5, 0.35))
    elif el == "water":     # a wave rolling past and splashing
        out = whoosh(rnd, n, 250, 1300, 0.4, 0.3, q=1.2)
        for i in range(n):
            out[i] *= 0.75 + 0.25 * math.sin(2 * math.pi * 4 * i / RATE)
        add_bloops(out, [(rnd.uniform(0.1, 0.7) * n / RATE, rnd.uniform(0.3, 1.0)) for _ in range(12)], 0.3)
        splash = whoosh(rnd, n, 1500, 5000, 0.72, 0.12, q=0.6)
        for i, s in enumerate(splash):
            out[i] += 0.45 * s
    elif el == "thunder":   # buzz, a sharp crack, then a rolling rumble
        out = [0.0] * n
        add_buzz(out, rnd, 90, 0.18, lambda t: bell(t, 0.08, 0.06))
        crack = int(0.14 * RATE)
        boom = low_rumble(rnd, int(0.12 * RATE), 900, lambda t: math.exp(-t * 5))
        for k, b in enumerate(boom):                                   # the crack: sharp, then a dull thud
            out[crack + k] += 2.2 * b + (rnd.uniform(-1, 1) * math.exp(-k / (0.006 * RATE)) if k < 0.03 * RATE else 0)
        for i, r in enumerate(low_rumble(rnd, n, 140, lambda t: 0 if t < 0.12 else math.exp(-(t - 0.12) * 2.6))):
            out[i] += 16.0 * r
        add_crackle(out, rnd, 90, 0.7, ms=3, env=lambda t: math.exp(-t * 4))
    else:                   # a howling gust
        out = whoosh(rnd, n, 300, 2100, 0.45, 0.32, q=0.6)
        add_tone(out, 700, 1500, 0.08, 0.45, 0.28, wobble=60)
    return out

SWING_SECONDS, SPECIAL_SECONDS = 0.5, 1.2
SWING_VARIANTS = 3

def make(el, kind, path, seed):
    if kind == "swing":
        render(path, SWING_SECONDS, lambda rnd, n: swing(el, rnd, n), seed)
    else:
        render(path, SPECIAL_SECONDS, lambda rnd, n: special(el, rnd, n), seed)
