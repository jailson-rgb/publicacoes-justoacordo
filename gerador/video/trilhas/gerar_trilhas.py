"""Gera as trilhas instrumentais próprias da Justo Acordo (sintetizadas aqui, sem uso de obra de terceiros:
100% livres de direitos). Persona da marca: segura, amigável, confiante e cordial – "sério sem ser rígido".

Uso: python gerador/video/trilhas/gerar_trilhas.py   (gera os .mp3 nesta pasta)

Trilhas:
  confianca  – Dó maior, 92 bpm, piano elétrico + pad + batida suave. Padrão para placar e resultados.
  dialogo    – Sol maior, 78 bpm, dedilhado + pad, sem bateria. Fundo para o vídeo do Jailson falando.
  conquista  – Ré maior, 104 bpm, piano + baixo + batida. Marcos, mosaico, "Números do mês".
  reflexao   – Lá menor → Dó, 74 bpm, pad + piano esparso. Conteúdo educativo (título executivo, garantias).
"""
import os
import subprocess
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

SR = 44100
AQUI = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)


def hz(n):  # nota MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a=0.005, d=0.3, s=0.0, r=0.2):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rel = int(r * SR)
    if rel and n > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def lp(x, fc, ordem=2):
    b, a = butter(ordem, fc / (SR / 2), "low")
    return lfilter(b, a, x)


def hp(x, fc, ordem=2):
    b, a = butter(ordem, fc / (SR / 2), "high")
    return lfilter(b, a, x)


def epiano(f, dur, vel=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
         + 0.12 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 6))
    x *= 1 + 0.08 * np.sin(2 * np.pi * 4.5 * t)  # tremolo leve
    return vel * x * env(n, 0.004, 0.9, 0.0, 0.15)


def pad(f, dur, vel=0.18):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sign(np.sin(2 * np.pi * f * (1 + d) * t)) * 0.5 + np.sin(2 * np.pi * f * (1 + d) * t)
            for d in (-0.004, 0.0, 0.005))
    x = lp(x, 1400)
    a = np.minimum(t / 0.9, 1) * np.minimum((dur - t) / 0.8, 1)
    return vel * x * np.clip(a, 0, 1) / 3


def pluck(f, dur, vel=0.35):  # Karplus-Strong
    n = int(dur * SR); p = max(int(SR / f), 2)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return vel * lp(out, 3500)


def baixo(f, dur, vel=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    return vel * (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)) * env(n, 0.01, 0.6, 0.35, 0.1)


def bumbo(vel=0.55):
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t * 30)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def chocalho(vel=0.08):
    n = int(0.09 * SR)
    return vel * hp(rng.uniform(-1, 1, n), 6000) * np.exp(-np.arange(n) / SR * 45)


def palma(vel=0.12):
    n = int(0.2 * SR)
    return vel * lp(hp(rng.uniform(-1, 1, n), 900), 5000) * np.exp(-np.arange(n) / SR * 22)


def reverb(x, seg=1.8, mix=0.22):
    n = int(seg * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * (6.9 / seg))
    ir = lp(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    return (1 - mix) * x + mix * fftconvolve(x, ir)[: len(x)]


def acorde(raiz, tipo):
    return [raiz, raiz + (3 if tipo == "m" else 4), raiz + 7, raiz + 12]


def compor(bpm, prog, partes, compassos=16):
    beat = 60 / bpm; bar = 4 * beat
    total = compassos * bar + 2.5
    mix = np.zeros(int(total * SR) + SR)

    def pos(s, sinal):
        i = int(s * SR); mix[i:i + len(sinal)] += sinal[: len(mix) - i]

    for c in range(compassos):
        raiz, tipo = prog[c % len(prog)]
        notas = acorde(raiz, tipo); t0 = c * bar
        entra = c >= 2  # bateria/baixo entram depois de 2 compassos (abertura suave)
        if "pad" in partes:
            for nt in notas[:3]:
                pos(t0, pad(hz(nt), bar + 0.6))
        if "piano" in partes:
            for b in (0, 1.5, 2.5) if partes.get("piano") == "ritmo" else (0, 2):
                for nt in notas[1:]:
                    pos(t0 + b * beat, epiano(hz(nt + 12), beat * 1.6, 0.16))
            pos(t0 + 3.5 * beat, epiano(hz(notas[2] + 24), beat, 0.08))
        if "dedilhado" in partes:
            seq = [notas[0] + 12, notas[1] + 12, notas[2] + 12, notas[3] + 12, notas[2] + 12, notas[1] + 12, notas[2] + 12, notas[3] + 12]
            for k, nt in enumerate(seq):
                pos(t0 + k * beat / 2, pluck(hz(nt), beat * 1.5, 0.22))
        if "baixo" in partes and entra:
            for b in (0, 2.5):
                pos(t0 + b * beat, baixo(hz(raiz - 12), beat * 1.4))
        if "bateria" in partes and entra and c < compassos - 1:
            for b in range(4):
                if b in (0, 2):
                    pos(t0 + b * beat, bumbo())
                if b in (1, 3) and partes.get("bateria") == "palma":
                    pos(t0 + b * beat, palma())
                pos(t0 + (b + 0.5) * beat, chocalho())
    # acorde final
    raiz, tipo = prog[0]
    for nt in acorde(raiz, tipo):
        pos(compassos * bar, epiano(hz(nt + 12), 2.4, 0.18))
        if "pad" in partes:
            pos(compassos * bar, pad(hz(nt), 2.4, 0.12))
    x = reverb(mix)
    x = np.tanh(1.3 * x / (np.max(np.abs(x)) + 1e-9))  # cola e segura picos
    fade = int(1.5 * SR); x[-fade:] *= np.linspace(1, 0, fade)
    return x


TRILHAS = {
    "confianca": (92, [(60, ""), (67, ""), (69, "m"), (65, "")], {"pad": 1, "piano": "ritmo", "baixo": 1, "bateria": 1}),
    "dialogo": (78, [(55, ""), (59, "m"), (60, ""), (62, "")], {"pad": 1, "dedilhado": 1}),
    "conquista": (104, [(62, ""), (69, ""), (71, "m"), (67, "")], {"pad": 1, "piano": "ritmo", "baixo": 1, "bateria": "palma"}),
    "reflexao": (74, [(57, "m"), (53, ""), (60, ""), (55, "")], {"pad": 1, "piano": 1, "baixo": 1}),
}

if __name__ == "__main__":
    for nome, (bpm, prog, partes) in TRILHAS.items():
        x = compor(bpm, prog, partes)
        wav = os.path.join(AQUI, f"{nome}.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 0.95 * 32767).astype(np.int16).tobytes())
        mp3 = os.path.join(AQUI, f"{nome}.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "44100", "-ac", "2", "-b:a", "192k", mp3], check=True)
        os.remove(wav)
        print(mp3, f"{len(x) / SR:.1f}s")
