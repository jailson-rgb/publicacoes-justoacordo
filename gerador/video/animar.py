"""Renderiza uma animação HTML (CSS animations) em MP4 vertical 1080x1920 para Reels.

Uso:
  python gerador/video/animar.py modelo.html saida.mp4 [segundos]
      vídeo só animado (fundo do próprio modelo). Padrão: 10,5 s.
  python gerador/video/animar.py modelo.html saida.mp4 --sobre video_do_jailson.mp4 [--trilha trilha.mp3]
      SOBREPOSIÇÃO: a animação (fundo transparente) é aplicada por cima do vídeo gravado pelo Jailson.
      A duração é a do vídeo; o áudio é o do vídeo. O vídeo é ajustado para 1080x1920 (corta as sobras).
      No modelo, a variável CSS --fim recebe automaticamente (duração − 3 s), para o encerramento entrar no fim.
  --trilha NOME          trilha instrumental própria da Justo Acordo (gerador/video/trilhas/: confianca, dialogo,
                         conquista, reflexao) ou caminho de um .mp3. No vídeo só animado vira o áudio (com fade);
                         na sobreposição entra baixinha (15%) sob a voz.

O HTML precisa ter um elemento #r de 1080x1920; as animações CSS são congeladas e avançadas quadro a quadro.
"""
import os
import subprocess
import sys
import tempfile

from playwright.sync_api import sync_playwright

args = sys.argv[1:]
sobre = trilha = None
if "--sobre" in args:
    i = args.index("--sobre"); sobre = args[i + 1]; del args[i:i + 2]
if "--trilha" in args:
    i = args.index("--trilha"); trilha = args[i + 1]; del args[i:i + 2]
if trilha and not os.path.exists(trilha):  # aceita só o nome: --trilha confianca
    trilha = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trilhas", f"{trilha}.mp3")
src, out = args[0], args[1]
FPS = 30


def duracao(v):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


DUR = duracao(sobre) if sobre else (float(args[2]) if len(args) > 2 else 10.5)
tmp = tempfile.mkdtemp()
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.abspath(src))
    pg.evaluate(f"document.documentElement.style.setProperty('--fim', '{max(DUR - 3, 0):.2f}s')")
    if sobre:
        pg.add_style_tag(content="html,body,#r{background:transparent!important}")
    pg.evaluate("document.fonts.ready.then(()=>1)")
    pg.wait_for_timeout(300)
    pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
    for i in range(int(FPS * DUR)):
        pg.evaluate(f"document.getAnimations().forEach(a=>a.currentTime={i * 1000 / FPS})")
        pg.locator("#r").screenshot(path=f"{tmp}/{i:04d}.png", omit_background=bool(sobre))
    b.close()

enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
if sobre:
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", sobre, "-framerate", str(FPS), "-i", f"{tmp}/%04d.png"]
    filtro = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[b];"
              "[b][1:v]overlay=0:0:eof_action=pass[v]")
    if trilha:
        cmd += ["-stream_loop", "-1", "-i", trilha]
        filtro += ";[2:a]volume=0.15[t];[0:a][t]amix=inputs=2:duration=first:dropout_transition=0[a]"
        mapa = ["-map", "[v]", "-map", "[a]"]
    else:
        mapa = ["-map", "[v]", "-map", "0:a?"]
    cmd += ["-filter_complex", filtro, *mapa, *enc, "-c:a", "aac", "-b:a", "160k", "-t", f"{DUR:.3f}", out]
else:
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png"]
    if trilha:
        cmd += ["-i", trilha, "-map", "0:v", "-map", "1:a", "-af", f"afade=t=out:st={max(DUR - 1.2, 0):.2f}:d=1.2",
                "-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += [*enc, out]
subprocess.run(cmd, check=True)
print(out)
