"""
Renderizador de artes da Justo Acordo (manual da marca: terra #A45248, verde #1C4220 só em palavras-chave).

Uso:  python gerador/render.py post.json pasta_saida/
O JSON descreve um post:
{
  "id": "JA2026-001",
  "tipo": "Story" | "Carrossel",
  "laminas": [
    # STORIES (1080x1920)
    {"layout": "placar",  "valor": "R$ 1,9", "sufixo": "milhão", "acordos": "234", "empresas": "20"},
    {"layout": "acordo",  "segmento": "INDÚSTRIA DE ALIMENTOS · RS", "vencida": "desde mar/2025" | "há 40 dias",
                          "forma": "10 parcelas mensais", "valor": "R$ 38 mil", "foto": "caminho/da/foto.jpg"},
    {"layout": "semana",  "valor": "R$ 62", "sufixo": "mil", "acordos": "5", "acumulado": "R$ 1,9 milhão"},
    {"layout": "story_numero", "chamada": "Número do mês", "numero": "9,3 mi", "titulo": "...", "fonte": "Serasa Experian, out/2026"},
    {"layout": "story", "chamada": "Você sabia?", "titulo": "...", "texto": "..."},
    # CARROSSEL (1080x1350)
    {"layout": "capa", "tema": "Inadimplência", "titulo": "...", "subtitulo": "..."},
    {"layout": "topico", "numero": "1", "titulo": "...", "texto": "..."},
    {"layout": "numero", "numero": "R$ 1,9 mi", "titulo": "...", "texto": "..."},
    {"layout": "fechamento", "titulo": "...", "texto": "..."}
  ]
}
Campos opcionais: "vencida" (some se vazio), "foto" (sem foto, o topo fica só com a cor da marca).
A foto do termo é SEMPRE desfocada aqui (nunca publicar dados legíveis do devedor).
Gera 01.png, 02.png...
"""
import html
import json
import os
import sys

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
TERRA, VERDE, AREIA, ROSA, ROSA2, INK = "#A45248", "#1C4220", "#F7F1EC", "#EACBBB", "#CA9A8E", "#3B2F2C"


def e(t):
    return html.escape(str(t or "")).replace("\n", "<br>")


def u(rel):
    return "file://" + os.path.join(AQUI, rel)


def fontcss():
    css = "".join(f"@font-face{{font-family:Cabin;font-weight:{w};src:url('{u(f'fonts/cabin-latin-{w}-normal.woff2')}')}}"
                  for w in (400, 500, 600, 700))
    css += "".join(f"@font-face{{font-family:Corm;font-weight:{w};src:url('{u(f'fonts/cormorant-garamond-latin-{w}-normal.woff2')}')}}"
                   for w in (500, 600))
    return css + " body{margin:0} p,span{font-variant-numeric:lining-nums}"


def caixa(bg, corpo, h=1920):
    return (f'<div id="r" style="width:1080px;height:{h}px;background:{bg};position:relative;overflow:hidden;'
            f'font-family:Cabin,sans-serif;box-sizing:border-box">{corpo}</div>')


def simbolo(op, lado="dir", top=520, h=1300):
    pos = "right:-160px" if lado == "dir" else "left:-160px;transform:scaleX(-1)"
    return f'<img src="{u("assets/simb_terra.png")}" style="position:absolute;{pos};top:{top}px;height:{h}px;opacity:{op}">'


def selo(cor=INK, dest=TERRA, size=30):
    return (f'<div style="font-size:{size}px;line-height:1.35;color:{cor}">Cobrança extrajudicial '
            f'<b style="color:{dest}">100% no êxito</b>:<br>só recebemos quando o devedor paga.</div>')


def logo(branco=False, w=430):
    return f'<img src="{u("assets/logo_branco.png" if branco else "assets/logo_terra.png")}" style="width:{w}px">'


def big(txt, size, cor, extra=""):
    return f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:{size}px;line-height:.98;color:{cor};{extra}">{e(txt)}</p>'


# ------------------------------------------------------------------ stories
def l_placar(l, n, total):
    c = f'''{simbolo(0.16)}
    <div style="position:absolute;inset:150px 96px 140px 96px;display:flex;flex-direction:column;justify-content:space-between">
      {logo(True)}
      <div>
        <p style="margin:0 0 30px;font-size:30px;font-weight:600;letter-spacing:6px;color:{ROSA}">{e(l.get("chamada", "PLACAR JUSTO ACORDO"))}</p>
        {big(l.get("valor"), 190, "#fff")}{big(l.get("sufixo"), 96, "#fff", "margin-top:8px")}
        <div style="width:150px;height:6px;background:{ROSA};margin:46px 0"></div>
        <p style="margin:0;font-size:50px;line-height:1.3;color:#fff">{e(l.get("texto", "já voltaram ao caixa das empresas que confiam na Justo Acordo."))}</p>
      </div>
      <div style="background:{AREIA};border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:26px">
        <div style="display:flex;gap:60px">
          <div>{big(l.get("acordos"), 96, VERDE)}<p style="margin:6px 0 0;font-size:28px;color:{INK}">acordos firmados</p></div>
          <div>{big(l.get("empresas"), 96, VERDE)}<p style="margin:6px 0 0;font-size:28px;color:{INK}">empresas credoras</p></div>
        </div>
        <div style="height:2px;background:{ROSA}"></div>{selo()}
      </div>
    </div>'''
    return caixa(TERRA, c)


def l_acordo(l, n, total):
    foto = l.get("foto")
    topo = (f'<div style="position:absolute;left:-40px;right:-40px;top:-40px;height:900px;background:url(\'file://{os.path.abspath(foto)}\') center/cover;'
            f'filter:blur(14px)"></div>') if foto else f'<div style="position:absolute;left:0;right:0;top:0;height:820px;background:{ROSA}"></div>'
    venc = f'<p style="margin:0">Dívida vencida <b>{e(l["vencida"])}</b></p>' if l.get("vencida") else ""
    c = f'''{topo}
    <div style="position:absolute;left:0;right:0;top:0;height:820px;background:linear-gradient(180deg,rgba(247,241,236,0) 55%,{AREIA} 100%)"></div>
    <div style="position:absolute;top:120px;left:96px;padding:18px 34px;background:{TERRA};border-radius:999px;font-size:30px;font-weight:700;letter-spacing:5px;color:#fff">ACORDO FECHADO</div>
    {simbolo(0.07)}
    <div style="position:absolute;left:96px;right:96px;top:760px;bottom:140px;display:flex;flex-direction:column;justify-content:space-between">
      <div>
        <p style="margin:0;font-size:34px;font-weight:600;letter-spacing:2px;color:{TERRA}">{e(l.get("segmento"))}</p>
        <div style="display:flex;flex-direction:column;gap:14px;margin-top:34px;font-size:38px;color:{INK}">{venc}
          <p style="margin:0">Acordo: <b>{e(l.get("forma"))}</b></p></div>
        <div style="width:150px;height:6px;background:{TERRA};margin:52px 0 40px"></div>
        <p style="margin:0;font-size:44px;line-height:1.25;color:{VERDE};font-weight:600">Voltaram ao caixa do cliente</p>
        {big(l.get("valor"), 170, TERRA, "margin-top:10px")}
        <p style="margin:0;font-size:32px;color:{INK}">já descontados os honorários</p>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:flex-end">{selo()}{logo(w=300)}</div>
    </div>'''
    return caixa(AREIA, c)


def l_semana(l, n, total):
    c = f'''{simbolo(0.09, "esq")}
    <div style="position:absolute;inset:150px 96px 140px 96px;display:flex;flex-direction:column;justify-content:space-between">
      {logo()}
      <div>
        <p style="margin:0 0 30px;font-size:30px;font-weight:700;letter-spacing:6px;color:{VERDE}">NESTA SEMANA</p>
        {big(l.get("valor"), 200, TERRA)}{big(l.get("sufixo"), 80, TERRA, "margin-top:6px")}
        <p style="margin:40px 0 0;font-size:48px;line-height:1.3;color:{INK}">voltaram ao caixa das empresas clientes.</p>
        <div style="margin-top:60px;display:inline-block;padding:26px 40px;border:3px solid {VERDE};border-radius:24px">
          <span style="font-family:Corm;font-weight:600;font-size:80px;color:{VERDE}">{e(l.get("acordos"))}</span>
          <span style="font-size:36px;color:{VERDE};margin-left:12px">novos acordos firmados</span></div>
      </div>
      <div style="display:flex;flex-direction:column;gap:30px">
        <p style="margin:0;font-size:32px;color:{INK}">Acumulado: <b style="color:{TERRA}">{e(l.get("acumulado"))}</b> restituídos</p>
        <div style="height:2px;background:{ROSA2}"></div>{selo()}
      </div>
    </div>'''
    return caixa(AREIA, c)


def l_story_numero(l, n, total):
    c = f'''{simbolo(0.09)}
    <div style="position:absolute;inset:150px 96px 140px 96px;display:flex;flex-direction:column;justify-content:space-between">
      {logo()}
      <div>
        <p style="margin:0 0 30px;font-size:30px;font-weight:700;letter-spacing:6px;color:{VERDE}">{e(l.get("chamada", "NÚMERO DO MÊS")).upper()}</p>
        {big(l.get("numero"), 210, TERRA)}
        <p style="margin:40px 0 0;font-size:56px;font-weight:600;line-height:1.2;color:{INK}">{e(l.get("titulo"))}</p>
        <p style="margin:30px 0 0;font-size:26px;color:{INK};opacity:.75">Fonte: {e(l.get("fonte"))}</p>
      </div>
      {selo()}
    </div>'''
    return caixa(AREIA, c)


def l_story(l, n, total):
    c = f'''{simbolo(0.14)}
    <div style="position:absolute;inset:150px 96px 140px 96px;display:flex;flex-direction:column;justify-content:space-between">
      {logo(True)}
      <div>
        <p style="margin:0 0 36px;font-size:30px;font-weight:600;letter-spacing:6px;color:{ROSA}">{e(l.get("chamada", "VOCÊ SABIA?")).upper()}</p>
        <p style="margin:0;font-size:{l.get("tamanho", 76)}px;font-weight:700;line-height:1.15;color:#fff">{e(l.get("titulo"))}</p>
        <div style="width:150px;height:6px;background:{ROSA};margin:46px 0"></div>
        <p style="margin:0;font-size:42px;line-height:1.4;color:#fff">{e(l.get("texto"))}</p>
      </div>
      {selo("#fff", ROSA)}
    </div>'''
    return caixa(TERRA, c)


# ------------------------------------------------------------------ carrossel 1080x1350
def contador(n, total, cor):
    return f'<p style="margin:0;font-size:30px;color:{cor}"><b>{n:02d}</b> / {total:02d}</p>' if total > 1 else ""


def l_capa(l, n, total):
    c = f'''{simbolo(0.14, top=300, h=1150)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:space-between;align-items:center">{logo(True, 330)}
        <p style="margin:0;padding:12px 26px;border:2px solid {ROSA};border-radius:999px;font-size:20px;font-weight:600;letter-spacing:3px;color:{ROSA}">{e(l.get("tema", "")).upper()}</p></div>
      <div><div style="width:120px;height:6px;background:{ROSA};margin-bottom:36px"></div>
        <p style="margin:0;font-size:{l.get("tamanho", 86)}px;font-weight:700;line-height:1.08;color:#fff">{e(l.get("titulo"))}</p>
        <p style="margin:30px 0 0;font-size:40px;line-height:1.3;color:{ROSA}">{e(l.get("subtitulo"))}</p></div>
      <div style="display:flex;justify-content:space-between;color:#fff">{contador(n, total, "#fff")}<p style="margin:0;font-size:28px;font-weight:600">Arraste →</p></div>
    </div>'''
    return caixa(TERRA, c, 1350)


def rodape():
    return f'<div style="display:flex;justify-content:space-between;align-items:flex-end;border-top:2px solid {ROSA2};padding-top:24px">{logo(w=260)}{selo(size=22)}</div>'


def l_topico(l, n, total):
    num = big(l.get("numero"), 180, TERRA) if l.get("numero") else ""
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:flex-end">{contador(n, total, INK)}</div>
      <div>{num}<p style="margin:20px 0 0;font-size:{l.get("tamanho", 62)}px;font-weight:700;line-height:1.12;color:{VERDE}">{e(l.get("titulo"))}</p>
        <p style="margin:28px 0 0;font-size:36px;line-height:1.45;color:{INK}">{e(l.get("texto"))}</p></div>
      {rodape()}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_numero(l, n, total):
    c = f'''{simbolo(0.07, top=250, h=1100)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:flex-end">{contador(n, total, INK)}</div>
      <div>{big(l.get("numero"), 170, TERRA)}
        <p style="margin:30px 0 0;font-size:54px;font-weight:700;line-height:1.15;color:{VERDE}">{e(l.get("titulo"))}</p>
        <p style="margin:24px 0 0;font-size:34px;line-height:1.45;color:{INK}">{e(l.get("texto"))}</p></div>
      {rodape()}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_fechamento(l, n, total):
    c = f'''{simbolo(0.14, top=300, h=1150)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:flex;justify-content:flex-end">{contador(n, total, "#fff")}</div>
      <div><div style="width:120px;height:6px;background:{ROSA};margin-bottom:36px"></div>
        <p style="margin:0;font-size:{l.get("tamanho", 70)}px;font-weight:700;line-height:1.1;color:#fff">{e(l.get("titulo"))}</p>
        <p style="margin:30px 0 0;font-size:36px;line-height:1.45;color:#fff">{e(l.get("texto"))}</p></div>
      <div style="display:flex;justify-content:space-between;align-items:flex-end">{logo(True, 320)}{selo("#fff", ROSA, 24)}</div>
    </div>'''
    return caixa(TERRA, c, 1350)


LAYOUTS = {"placar": l_placar, "acordo": l_acordo, "semana": l_semana, "story_numero": l_story_numero, "story": l_story,
           "capa": l_capa, "topico": l_topico, "numero": l_numero, "fechamento": l_fechamento}


def renderizar(post, saida, chrome=None):
    os.makedirs(saida, exist_ok=True)
    laminas = post["laminas"]
    arquivos = []
    with sync_playwright() as pw:
        kw = {"executable_path": chrome} if chrome else {}
        b = pw.chromium.launch(args=["--allow-file-access-from-files"], **kw)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        tmp = os.path.join(saida, "_tmp.html")
        for i, l in enumerate(laminas, 1):
            corpo = LAYOUTS[l.get("layout", "topico")](l, i, len(laminas))
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(f'<!doctype html><html><head><meta charset="utf-8"><style>{fontcss()}</style></head><body>{corpo}</body></html>')
            pg.goto("file://" + os.path.abspath(tmp))
            pg.evaluate("document.fonts.ready.then(()=>1)")
            pg.wait_for_timeout(200)
            p = os.path.join(saida, f"{i:02d}.png")
            pg.locator("#r").screenshot(path=p)
            arquivos.append(p)
        os.remove(tmp)
        b.close()
    return arquivos


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        post = json.load(f)
    for a in renderizar(post, sys.argv[2], os.environ.get("CHROME_PATH")):
        print(a)
