"""Synthesised lightsaber swing ("vwoom") sounds: a buzzy hum whose pitch and
volume swell like a Doppler pass, plus a little filtered whoosh noise."""
import math, random, struct, wave

RATE = 44100

def swing(path, f0=95, rise=1.55, dur=0.55, peak=0.42, seed=1):
    rnd = random.Random(seed)
    n = int(RATE * dur)
    ph1 = ph2 = 0.0; lp = 0.0; out = []
    for i in range(n):
        t = i / n
        env = math.exp(-((t - peak) / 0.22) ** 2)                       # swell around the peak
        f = f0 * (1 + (rise - 1) * env)                                 # doppler-ish pitch bend
        ph1 += 2 * math.pi * f / RATE; ph2 += 2 * math.pi * f * 1.012 / RATE
        hum = sum(math.sin(k * ph1) / k + 0.6 * math.sin(k * ph2) / k for k in range(1, 9))
        lp += (0.08 + 0.25 * env) * (rnd.uniform(-1, 1) - lp)           # whoosh: noise, brighter at peak
        fade = min(1, i / (0.01 * RATE), (n - i) / (0.03 * RATE))
        out.append((0.25 + 0.75 * env) * (hum * 0.55 + lp * 1.4) * fade)
    m = max(abs(x) for x in out) or 1
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(x / m * 0.89 * 32767)) for x in out))

# seven variations, like vanilla's sweep1..sweep7
VARIANTS = [dict(f0=95, rise=1.55, dur=0.55, peak=0.42), dict(f0=88, rise=1.7, dur=0.6, peak=0.45),
            dict(f0=102, rise=1.45, dur=0.5, peak=0.38), dict(f0=92, rise=1.6, dur=0.65, peak=0.5),
            dict(f0=110, rise=1.4, dur=0.45, peak=0.35), dict(f0=85, rise=1.8, dur=0.58, peak=0.4),
            dict(f0=98, rise=1.5, dur=0.52, peak=0.44)]
