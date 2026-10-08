#!/usr/bin/env python3
"""Original synthesized audio for Gothic Whip (no samples, no franchise audio).
All sounds are procedural numpy synthesis -> 44.1 kHz 16-bit WAV.
"""
import numpy as np, wave, os, struct

SR = 44100
OUT = os.path.expanduser("~/workspace/gothic-whip/game/art/audio")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261008)

def save(name, data, stereo=False):
    data = np.clip(data, -1.0, 1.0)
    if stereo and data.ndim == 1:
        data = np.column_stack([data, data])
    pcm = (data * 32767).astype(np.int16)
    path = os.path.join(OUT, name)
    with wave.open(path, "wb") as w:
        w.setnchannels(2 if stereo else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", path, f"{len(data)/SR:.2f}s")

def t(dur): return np.arange(int(SR * dur)) / SR
def env_exp(tt, tau): return np.exp(-tt / tau)
def env_adsr(tt, a=0.005, d=0.1, s=0.0, dur=None):
    e = np.exp(-np.maximum(tt - a, 0) / max(d, 1e-4)) * (1 - np.exp(-tt / max(a, 1e-4)))
    return e
def sine(f, tt, phase=0.0): return np.sin(2 * np.pi * f * tt + phase)
def noise(tt): return rng.uniform(-1, 1, len(tt))

def bandpass_sweep(dur, f0, f1, q_gain=1.0):
    """Crude swept resonant noise: amplitude-modulated filtered noise via
    time-varying sine gating (good enough for a whip whoosh)."""
    tt = t(dur)
    n = noise(tt)
    # simple one-pole lowpass with moving cutoff approx via cumulative filter
    out = np.zeros_like(n)
    cutoff = np.linspace(f0, f1, len(tt))
    for i in range(1, len(tt)):
        a = np.clip(cutoff[i] / SR, 0.01, 0.9)
        out[i] = out[i-1] + a * (n[i] - out[i-1])
    swoosh = out * np.sin(np.pi * tt / dur) ** 1.5
    return swoosh * 2.4 * q_gain

# --- SFX -----------------------------------------------------------------
# whip swing: whoosh down-sweeping, 0.22 s
save("sfx_whip_swing.wav", bandpass_sweep(0.22, 5000, 500) * 0.8)

# whip hit: crack burst + body thump
tt = t(0.18)
crack = noise(tt) * env_exp(tt, 0.012) * 0.9
thump = sine(110, tt) * env_exp(tt, 0.05) * 0.8
save("sfx_whip_hit.wav", crack + thump)

# jump: soft rising blip
tt = t(0.16)
f = 300 + 500 * (tt / 0.16)
ph = 2 * np.pi * np.cumsum(f) / SR
save("sfx_jump.wav", np.sin(ph) * env_exp(tt, 0.09) * 0.45)

# land: low thud
tt = t(0.14)
save("sfx_land.wav", (sine(85, tt) * env_exp(tt, 0.045) + noise(tt) * env_exp(tt, 0.015) * 0.5) * 0.8)

# hurt: harsh descending blip
tt = t(0.22)
f = 500 - 900 * (tt / 0.22)
ph = 2 * np.pi * np.cumsum(np.clip(f, 60, None)) / SR
save("sfx_hurt.wav", (np.sin(ph) + 0.4 * np.sign(np.sin(ph))) * env_exp(tt, 0.09) * 0.4)

# death: slow descending minor tones
tt = t(1.1)
sig = np.zeros_like(tt)
for i, (f0, st) in enumerate([(392, 0.0), (311, 0.22), (233, 0.45), (155, 0.7)]):
    m = tt >= st
    sig[m] += sine(f0, tt[m] - st) * np.exp(-(tt[m] - st) / 0.35)
save("sfx_death.wav", sig * 0.5 * env_exp(tt, 0.9))

# enemy tell: two-tone eerie alert
tt = t(0.35)
sig = np.where(tt < 0.16, sine(660, tt), sine(520, tt)) * env_adsr(tt, 0.01, 0.12)
save("sfx_enemy_tell.wav", sig * 0.5)

# checkpoint: warm minor chime arpeggio (A C E A)
tt = t(0.9)
sig = np.zeros_like(tt)
for i, f0 in enumerate([440, 523.25, 659.25, 880]):
    st = i * 0.11
    m = tt >= st
    sig[m] += sine(f0, tt[m] - st) * np.exp(-(tt[m] - st) / 0.28)
    sig[m] += 0.4 * sine(f0 * 2, tt[m] - st) * np.exp(-(tt[m] - st) / 0.12)
save("sfx_checkpoint.wav", sig * 0.45)

# boss tell: low bell toll
tt = t(1.4)
sig = (sine(98, tt) + 0.6 * sine(147.3, tt) + 0.35 * sine(251, tt) + 0.2 * sine(389, tt)) * np.exp(-tt / 0.5)
save("sfx_boss_tell.wav", sig * 0.7)

# --- Loops ----------------------------------------------------------------
# ambience: wind - slow-breathing lowpassed noise, 32 s, loop-seamless
dur = 32.0
tt = t(dur)
n = noise(tt)
wind = np.zeros_like(n)
a_lp = 0.002
for i in range(1, len(tt)):
    wind[i] = wind[i-1] + a_lp * (n[i] - wind[i-1])
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * tt / 23.0) * np.sin(2 * np.pi * tt / 7.7)
amb = wind * lfo * 1.6
# crossfade ends for seamless loop
xf = int(SR * 2.0)
amb[-xf:] = amb[-xf:] * (1 - np.linspace(0, 1, xf)) + amb[:xf] * np.linspace(0, 1, xf)
save("mus_ambience_loop.wav", amb * 0.8, stereo=True)

# music: dark drone + sparse bells, A minor, 32 s loop
tt = t(dur)
drone = (sine(55, tt) * 0.5 + sine(110, tt) * 0.28 + sine(164.8, tt) * 0.15
         + sine(220, tt) * 0.08 * (0.7 + 0.3 * np.sin(2 * np.pi * tt / 16.0)))
# beating detune shimmer
drone += sine(110.7, tt) * 0.1
mus = drone.copy()
bell_notes = [(220, 2.0), (261.6, 6.0), (196, 10.0), (164.8, 14.0),
              (220, 18.0), (329.6, 22.0), (261.6, 26.0), (196, 29.0)]
for f0, st in bell_notes:
    m = tt >= st
    lt = tt[m] - st
    bell = (sine(f0, lt) + 0.5 * sine(f0 * 2.76, lt) + 0.25 * sine(f0 * 5.4, lt)) * np.exp(-lt / 1.6)
    mus[m] += bell * 0.35
mus *= 0.55
xf = int(SR * 2.0)
mus[-xf:] = mus[-xf:] * (1 - np.linspace(0, 1, xf)) + mus[:xf] * np.linspace(0, 1, xf)
save("mus_stage_loop.wav", mus, stereo=True)

# boss sting (short loop-able tension bed, 16 s) - extra, boss uses music loop too
print("audio done")
