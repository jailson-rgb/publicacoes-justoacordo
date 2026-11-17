"""
Renderizador de artes da Justo Acordo (manual da marca: terra #A45248, verde #1C4220 só em palavras-chave).

Uso:  python gerador/render.py post.json pasta_saida/
O JSON descreve um post:
{
  "id": "JA2026-001",
  "tipo": "Story" | "Carrossel" | "Post único" (uma lâmina só no feed),
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
    # LAYOUTS EXTRAS (feed 1080x1350): servem para POST ÚNICO (1 lâmina) ou para variar a estrutura do carrossel
    {"layout": "frase", "frase": "...", "assinatura": "Justo Acordo", "fundo": "terra|areia|rosa"},
    {"layout": "dado", "chamada": "...", "numero": "9,3 mi", "titulo": "...", "texto": "...", "fonte": "...", "fundo": "rosa|areia|terra"},
    {"layout": "mito", "mito": "...", "verdade": "..."},
    {"layout": "comparativo", "titulo": "...", "esquerda": "...", "itens_esquerda": [...], "direita": "...", "itens_direita": [...]},
    {"layout": "checklist", "titulo": "...", "itens": ["...", "..."], "fundo": "areia|terra"},
    {"layout": "passos", "titulo": "...", "passos": [{"titulo": "...", "texto": "..."}]},
    {"layout": "pergunta", "chamada": "Pergunta de empresário", "pergunta": "...", "resposta": "...", "fundo": "areia|terra"},
    {"layout": "barras", "chamada": "...", "titulo": "...", "dados": [{"rotulo": "jun", "valor": 8.9, "texto": "8,9 mi"}], "fonte": "..."},
    {"layout": "resultado", "chamada": "Resultado de outubro", "valor": "R$ 210", "sufixo": "mil", "acordos": "18", "empresas": "9"}
    {"layout": "nota", "data": "15/11/2026", "titulo": "...", "texto": "...", "assinatura": "Equipe Justo Acordo"}
  ]
}
PEÇAS LARGAS (em vez de "laminas", usar "largo"; o renderizador desenha uma arte larga e corta):
  {"id": "...", "tipo": "Mosaico", "largo": {"layout": "mosaico", "chamada": "...", "titulo": "R$ 1,6 milhão",
     "texto": "...", "rodapes": ["...", "...", "..."], "fundo": "terra|areia"}}
     -> 01 (esquerda), 02 (meio), 03 (direita): 3 posts que formam uma imagem na grade do perfil.
  {"id": "...", "tipo": "Carrossel", "largo": {"layout": "jornada", "tema": "...", "titulo": "...", "subtitulo": "...",
     "passos": [{"titulo": "...", "texto": "..."}]}}  -> carrossel panorâmico contínuo (capa + 1 lâmina por etapa).
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


def l_acordo_frase(l, n, total):
    """Story de acordo recém-fechado (ainda sem valor recebido): termo desfocado + frase do Jailson."""
    foto = l.get("foto")
    topo = (f'<div style="position:absolute;left:150px;top:250px;width:780px;height:420px;background:#fff;border-radius:14px;'
            f'box-shadow:0 30px 70px rgba(80,40,30,.18);transform:rotate(-4deg);overflow:hidden">'
            f'<div style="position:absolute;inset:-20px;background:#fff url(\'file://{os.path.abspath(foto)}\') center/88% auto no-repeat;'
            f'filter:blur(7px)"></div></div>') if foto else ""
    seg = f'<p style="margin:0 0 30px;font-size:34px;font-weight:600;letter-spacing:2px;color:{TERRA}">{e(l["segmento"])}</p>' if l.get("segmento") else ""
    c = f'''{topo}
    <div style="position:absolute;top:120px;left:96px;padding:18px 34px;background:{TERRA};border-radius:999px;font-size:30px;font-weight:700;letter-spacing:5px;color:#fff;z-index:2">ACORDO FECHADO HOJE</div>
    {simbolo(0.07)}
    <div style="position:absolute;left:96px;right:96px;top:760px;bottom:140px;display:flex;flex-direction:column;justify-content:space-between">
      <div>{seg}
        {big(l.get("frase"), 150, TERRA, "line-height:1.02")}
        <div style="width:150px;height:6px;background:{TERRA};margin:56px 0 40px"></div>
        <p style="margin:0;font-size:42px;line-height:1.3;color:{INK}">{e(l.get("texto"))}</p>
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


LAYOUTS = {"placar": l_placar, "acordo": l_acordo, "acordo_frase": l_acordo_frase, "semana": l_semana, "story_numero": l_story_numero, "story": l_story,
           "capa": l_capa, "topico": l_topico, "numero": l_numero, "fechamento": l_fechamento}


# ------------------------------------------------------------------ layouts extras (feed 1080x1350)
# Servem para POST ÚNICO (uma lâmina só) e para compor carrosséis com estruturas diferentes.
# Vários aceitam "fundo": "terra" | "areia" | "rosa".
def cores(l, padrao):
    f = l.get("fundo", padrao)
    if f == "terra":
        return TERRA, "#fff", ROSA, True
    if f == "rosa":
        return ROSA, INK, TERRA, False
    return AREIA, INK, TERRA, False


def topo_feed(n, total, txt, claro):
    return f'<div style="display:flex;justify-content:space-between;align-items:center">{logo(claro, 260)}{contador(n, total, txt)}</div>'


def base_feed(txt, dest, claro):
    linha = ROSA if claro else ROSA2
    return (f'<div style="display:flex;justify-content:flex-end;border-top:2px solid {linha};padding-top:22px">'
            f'{selo(txt, ROSA if claro else TERRA, 22)}</div>')


def l_frase(l, n, total):
    bg, txt, dest, claro = cores(l, "terra")
    aspas = ROSA if claro else TERRA
    c = f'''{simbolo(0.12 if claro else 0.06, top=250, h=1150)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, txt, claro)}
      <div>{big("“", 260, aspas, "height:150px")}
        <p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 84)}px;line-height:1.08;color:{txt}">{e(l.get("frase"))}</p>
        <p style="margin:36px 0 0;font-size:30px;letter-spacing:3px;font-weight:600;color:{aspas}">{e(l.get("assinatura", "")).upper()}</p></div>
      {base_feed(txt, dest, claro)}
    </div>'''
    return caixa(bg, c, 1350)


def l_dado(l, n, total):
    bg, txt, dest, claro = cores(l, "rosa")
    num = "#fff" if claro else TERRA
    cham = ROSA if claro else VERDE
    fonte = ("Fonte: " + e(l["fonte"])) if l.get("fonte") else ""
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, txt, claro)}
      <div style="text-align:center">
        <p style="margin:0 0 20px;font-size:28px;font-weight:700;letter-spacing:6px;color:{cham}">{e(l.get("chamada", "")).upper()}</p>
        {big(l.get("numero"), l.get("tamanho", 210), num, "white-space:nowrap")}
        <p style="margin:26px auto 0;max-width:820px;font-size:50px;font-weight:700;line-height:1.15;color:{txt}">{e(l.get("titulo"))}</p>
        <p style="margin:22px auto 0;max-width:800px;font-size:32px;line-height:1.4;color:{txt}">{e(l.get("texto"))}</p>
        <p style="margin:26px 0 0;font-size:24px;color:{txt};opacity:.75">{fonte}</p></div>
      {base_feed(txt, dest, claro)}
    </div>'''
    return caixa(bg, c, 1350)


def l_mito(l, n, total):
    c = f'''<div style="position:absolute;left:0;right:0;top:0;height:640px;background:{ROSA}"></div>
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, INK, False)}
      <div style="height:400px;display:flex;flex-direction:column;justify-content:center">
        <p style="margin:0 0 18px;font-size:30px;font-weight:700;letter-spacing:8px;color:{TERRA}">MITO</p>
        <p style="margin:0;font-size:{l.get("tamanho", 56)}px;font-weight:700;line-height:1.15;color:{INK};text-decoration:line-through;text-decoration-color:{TERRA};text-decoration-thickness:4px">{e(l.get("mito"))}</p></div>
      <div style="height:420px;display:flex;flex-direction:column;justify-content:center">
        <p style="margin:0 0 18px;font-size:30px;font-weight:700;letter-spacing:8px;color:{VERDE}">VERDADE</p>
        <p style="margin:0;font-size:40px;line-height:1.4;color:{INK}">{e(l.get("verdade"))}</p></div>
      {base_feed(INK, TERRA, False)}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_comparativo(l, n, total):
    def col(t, itens, cor, bg):
        li = "".join(f'<p style="margin:0;font-size:31px;line-height:1.35;color:{INK}">{e(i)}</p>' for i in itens)
        return (f'<div style="flex:1;background:{bg};border-radius:26px;padding:40px 36px;display:flex;flex-direction:column;gap:24px">'
                f'<p style="margin:0;font-size:28px;font-weight:700;letter-spacing:3px;color:{cor}">{e(t).upper()}</p>'
                f'<div style="height:3px;background:{cor};width:80px"></div>{li}</div>')
    esq = col(l.get("esquerda", ""), l.get("itens_esquerda", []), ROSA2, "#fff")
    dir_ = col(l.get("direita", ""), l.get("itens_direita", []), VERDE, ROSA)
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, INK, False)}
      <div><p style="margin:0 0 44px;font-size:{l.get("tamanho", 60)}px;font-weight:700;line-height:1.12;color:{TERRA}">{e(l.get("titulo"))}</p>
        <div style="display:flex;gap:28px">{esq}{dir_}</div></div>
      {base_feed(INK, TERRA, False)}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_checklist(l, n, total):
    bg, txt, dest, claro = cores(l, "areia")
    circ, marca, tit = ("#fff", TERRA, "#fff") if claro else (TERRA, "#fff", TERRA)
    itens = "".join(
        f'<div style="display:flex;gap:28px;align-items:flex-start"><div style="flex:none;width:62px;height:62px;border-radius:50%;'
        f'background:{circ};color:{marca};font-size:38px;font-weight:700;display:flex;align-items:center;justify-content:center">✓</div>'
        f'<p style="margin:6px 0 0;font-size:38px;line-height:1.3;color:{txt}">{e(i)}</p></div>' for i in l.get("itens", []))
    c = f'''{simbolo(0.06, top=300, h=1100)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, txt, claro)}
      <div><p style="margin:0 0 50px;font-size:{l.get("tamanho", 62)}px;font-weight:700;line-height:1.12;color:{tit}">{e(l.get("titulo"))}</p>
        <div style="display:flex;flex-direction:column;gap:38px">{itens}</div></div>
      {base_feed(txt, dest, claro)}
    </div>'''
    return caixa(bg, c, 1350)


def l_passos(l, n, total):
    ps = l.get("passos", [])
    blocos = []
    for i, p in enumerate(ps, 1):
        linha = f'<div style="width:4px;flex:1;background:{ROSA2};min-height:40px"></div>' if i < len(ps) else ""
        blocos.append(
            f'<div style="display:flex;gap:34px"><div style="flex:none;display:flex;flex-direction:column;align-items:center">'
            f'<div style="width:78px;height:78px;border-radius:50%;border:4px solid {TERRA};font-family:Corm;font-weight:600;font-size:48px;'
            f'color:{TERRA};display:flex;align-items:center;justify-content:center">{i}</div>{linha}</div>'
            f'<div style="padding-bottom:34px"><p style="margin:12px 0 0;font-size:40px;font-weight:700;color:{VERDE}">{e(p.get("titulo"))}</p>'
            f'<p style="margin:10px 0 0;font-size:31px;line-height:1.4;color:{INK}">{e(p.get("texto"))}</p></div></div>')
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, INK, False)}
      <div><p style="margin:0 0 46px;font-size:{l.get("tamanho", 60)}px;font-weight:700;line-height:1.12;color:{TERRA}">{e(l.get("titulo"))}</p>{"".join(blocos)}</div>
      {base_feed(INK, TERRA, False)}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_pergunta(l, n, total):
    bg, txt, dest, claro = cores(l, "areia")
    interrog, cham, perg, traco = (ROSA2, ROSA, "#fff", ROSA) if claro else (ROSA, VERDE, TERRA, TERRA)
    c = f'''<div style="position:absolute;right:70px;top:170px;font-family:Corm;font-weight:600;font-size:720px;line-height:1;color:{interrog};opacity:.55">?</div>
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, txt, claro)}
      <div style="position:relative"><p style="margin:0 0 26px;font-size:28px;font-weight:700;letter-spacing:6px;color:{cham}">{e(l.get("chamada", "PERGUNTA DE EMPRESÁRIO")).upper()}</p>
        <p style="margin:0;font-size:{l.get("tamanho", 72)}px;font-weight:700;line-height:1.1;color:{perg}">{e(l.get("pergunta"))}</p>
        <div style="width:120px;height:6px;background:{traco};margin:42px 0"></div>
        <p style="margin:0;font-size:38px;line-height:1.42;color:{txt}">{e(l.get("resposta"))}</p></div>
      {base_feed(txt, dest, claro)}
    </div>'''
    return caixa(bg, c, 1350)


def l_barras(l, n, total):
    dados = l.get("dados", [])  # [{"rotulo": "jun", "valor": 8.9, "texto": "8,9 mi"}] – o último fica destacado
    mx = max([d["valor"] for d in dados] or [1])
    col = []
    for i, d in enumerate(dados):
        cor = TERRA if i == len(dados) - 1 else ROSA2
        txtc = TERRA if i == len(dados) - 1 else INK
        alt = max(6, 100 * d["valor"] / mx)
        col.append(
            f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:14px;height:100%">'
            f'<p style="margin:0;font-size:28px;font-weight:700;color:{txtc}">{e(d.get("texto", d["valor"]))}</p>'
            f'<div style="width:100%;height:{alt:.1f}%;background:{cor};border-radius:14px 14px 0 0"></div>'
            f'<p style="margin:0;font-size:26px;color:{INK}">{e(d.get("rotulo"))}</p></div>')
    fonte = ("Fonte: " + e(l["fonte"])) if l.get("fonte") else ""
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, INK, False)}
      <div><p style="margin:0 0 14px;font-size:28px;font-weight:700;letter-spacing:6px;color:{VERDE}">{e(l.get("chamada", "")).upper()}</p>
        <p style="margin:0;font-size:{l.get("tamanho", 58)}px;font-weight:700;line-height:1.12;color:{TERRA}">{e(l.get("titulo"))}</p>
        <div style="display:flex;gap:22px;height:520px;margin-top:50px;border-bottom:3px solid {INK}">{"".join(col)}</div>
        <p style="margin:24px 0 0;font-size:24px;color:{INK};opacity:.75">{fonte}</p></div>
      {base_feed(INK, TERRA, False)}
    </div>'''
    return caixa(AREIA, c, 1350)


def l_resultado(l, n, total):
    """Placar em formato de feed (post único de resultado do mês ou do ano)."""
    c = f'''{simbolo(0.14, top=250, h=1150)}
    <div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, "#fff", True)}
      <div><p style="margin:0 0 24px;font-size:28px;font-weight:600;letter-spacing:6px;color:{ROSA}">{e(l.get("chamada", "RESULTADO")).upper()}</p>
        {big(l.get("valor"), 200, "#fff")}{big(l.get("sufixo"), 84, "#fff", "margin-top:6px")}
        <p style="margin:34px 0 0;font-size:42px;line-height:1.3;color:#fff">{e(l.get("texto", "voltaram ao caixa das empresas clientes."))}</p></div>
      <div style="background:{AREIA};border-radius:24px;padding:34px 40px;display:flex;justify-content:space-between;align-items:center">
        <div style="display:flex;gap:46px">
          <div>{big(l.get("acordos"), 80, VERDE)}<p style="margin:4px 0 0;font-size:24px;color:{INK}">acordos</p></div>
          <div>{big(l.get("empresas"), 80, VERDE)}<p style="margin:4px 0 0;font-size:24px;color:{INK}">empresas</p></div></div>
        {selo(size=22)}</div>
    </div>'''
    return caixa(TERRA, c, 1350)


LAYOUTS.update({"frase": l_frase, "dado": l_dado, "mito": l_mito, "comparativo": l_comparativo, "checklist": l_checklist,
                "passos": l_passos, "pergunta": l_pergunta, "barras": l_barras, "resultado": l_resultado})


def l_nota(l, n, total):
    """Post estilo 'bloco de notas' (tendência de posts com cara de anotação pessoal)."""
    data = e(l.get("data", ""))
    c = f'''<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">
      {topo_feed(n, total, INK, False)}
      <div style="background:#fff;border-radius:34px;box-shadow:0 18px 50px rgba(59,47,44,.14);padding:54px 56px 60px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:34px">
          <div style="display:flex;gap:12px"><span style="width:18px;height:18px;border-radius:50%;background:{TERRA}"></span>
            <span style="width:18px;height:18px;border-radius:50%;background:{ROSA2}"></span><span style="width:18px;height:18px;border-radius:50%;background:{ROSA}"></span></div>
          <p style="margin:0;font-size:24px;color:{INK};opacity:.6">{data}</p></div>
        <p style="margin:0 0 26px;font-size:{l.get("tamanho", 50)}px;font-weight:700;line-height:1.15;color:{TERRA}">{e(l.get("titulo"))}</p>
        <p style="margin:0;font-size:36px;line-height:1.5;color:{INK}">{e(l.get("texto"))}</p>
        <p style="margin:34px 0 0;font-size:28px;font-weight:600;color:{VERDE}">— {e(l.get("assinatura", "Equipe Justo Acordo"))}</p></div>
      {base_feed(INK, TERRA, False)}
    </div>'''
    return caixa(AREIA, c, 1350)


LAYOUTS.update({"nota": l_nota})



# ------------------------------------------------------------------ formatos novos (16/11/2026) – mesmos desenhos
# da Advocacia Soares, na identidade da Justo Acordo (terra/areia/rosa, Cabin + Cormorant):
# foto, foto_fundo, lei, dicionario, serie, split, palavra, linha_tempo, grade, marcatexto, fluxo, moldura, ranking.
def moldura_ja(bg, claro, n, total, meio, extra="", txt=INK):
    return caixa(bg, extra + f'<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:space-between">'
                 f'{topo_feed(n, total, "#fff" if claro else txt, claro)}{meio}{base_feed("#fff" if claro else txt, TERRA, claro)}</div>', 1350)


def _img(img, estilo, rotulo="FOTO"):
    if img and os.path.exists(img):
        return f'<img src="file://{os.path.abspath(img)}" style="{estilo};object-fit:cover">'
    return (f'<div style="{estilo};background:repeating-linear-gradient(135deg,{ROSA} 0 34px,#F0D9CD 34px 68px);display:flex;align-items:center;justify-content:center">'
            f'<p style="margin:0;padding:14px 26px;background:rgba(247,241,236,.9);border-radius:12px;font-size:28px;font-weight:700;letter-spacing:3px;color:{TERRA}">{rotulo}</p></div>')


def cham(t, cor=TERRA):
    return f'<p style="margin:0 0 16px;font-size:26px;font-weight:700;letter-spacing:5px;color:{cor}">{e(t).upper()}</p>' if t else ""


def l_foto(l, n, total):
    """Foto da equipe/bastidor (01 ENTRADA) com frase. Nunca termo, documento ou pessoa de cliente/devedor."""
    veu = f'<div style="position:absolute;left:0;right:0;bottom:0;height:60%;background:linear-gradient(180deg,rgba(164,82,72,0),rgba(164,82,72,.9) 45%,{TERRA})"></div>'
    c = (_img(l.get("imagem"), "position:absolute;inset:0;width:100%;height:100%", "FOTO DA EQUIPE / BASTIDOR") + veu +
         f'<div style="position:absolute;left:64px;top:64px;padding:20px 28px;background:rgba(164,82,72,.92);border-radius:18px">{logo(True, 250)}</div>'
         f'<div style="position:absolute;left:88px;right:88px;bottom:88px;display:flex;flex-direction:column;gap:30px">'
         f'<div style="width:110px;height:6px;background:{ROSA}"></div>'
         f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 76)}px;line-height:1.05;color:#fff">{e(l.get("frase"))}</p>'
         f'<div style="border-top:2px solid {ROSA};padding-top:22px;display:flex;justify-content:flex-end">{selo("#fff", ROSA, 22)}</div></div>')
    return caixa(TERRA, c, 1350)


def l_foto_fundo(l, n, total):
    """Qualquer foto do Jailson em tela cheia, com a identificação nos 4 cantos (logo, @, site, selo) e filete rosa."""
    c = (_img(l.get("imagem"), "position:absolute;inset:0;width:100%;height:100%", "FOTO") +
         '<div style="position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient(180deg,rgba(60,30,26,.72),rgba(60,30,26,0))"></div>'
         '<div style="position:absolute;left:0;right:0;bottom:0;height:380px;background:linear-gradient(0deg,rgba(60,30,26,.85),rgba(60,30,26,0))"></div>'
         + (f'<div style="position:absolute;inset:36px;border:2px solid {ROSA};border-radius:6px"></div>' if l.get("filete", True) else "") +
         (f'<p style="position:absolute;left:88px;right:88px;bottom:200px;margin:0;font-size:{l.get("tamanho", 42)}px;font-weight:700;line-height:1.2;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.45)">{e(l.get("legenda"))}</p>' if l.get("legenda") else "") +
         f'<div style="position:absolute;left:84px;top:84px">{logo(True, 250)}</div>'
         f'<p style="position:absolute;right:84px;top:100px;margin:0;font-size:27px;font-weight:600;color:#fff">@justo.acordo</p>'
         f'<div style="position:absolute;left:84px;right:84px;bottom:84px;display:flex;justify-content:space-between;align-items:flex-end">'
         f'<p style="margin:0;font-size:24px;font-weight:600;color:#fff">justoacordo.com.br</p>{selo("#fff", ROSA, 21)}</div>')
    return caixa(TERRA, c, 1350)


def l_lei(l, n, total):
    """Na lei / no tribunal: regra no alto (terra) + "o que significa para o credor" (areia)."""
    c = (f'<div style="position:absolute;left:0;right:0;top:0;height:770px;background:{TERRA};overflow:hidden">{simbolo(0.12, top=150, h=900)}'
         f'<div style="position:absolute;left:88px;right:88px;top:88px;display:flex;justify-content:space-between;align-items:center">{logo(True, 250)}'
         f'<p style="margin:0;padding:10px 24px;border:2px solid {ROSA};border-radius:999px;font-size:21px;font-weight:700;letter-spacing:3px;color:{ROSA}">{e(l.get("etiqueta", "NA LEI")).upper()}</p></div>'
         f'<div style="position:absolute;left:88px;right:88px;top:230px;bottom:90px;display:flex;align-items:center;gap:34px">'
         f'<div style="flex:none;align-self:stretch;width:8px;background:{ROSA}"></div><div>'
         f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 74)}px;line-height:1.05;color:#fff">{e(l.get("regra"))}</p>'
         f'<p style="margin:24px 0 0;font-size:26px;font-weight:600;color:{ROSA}">{e(l.get("referencia"))}</p></div></div></div>'
         f'<div style="position:absolute;left:88px;right:88px;top:830px;bottom:88px;display:flex;flex-direction:column;justify-content:space-between">'
         f'<div>{cham("O que significa para o credor", VERDE)}<p style="margin:0;font-size:34px;line-height:1.45;color:{INK}">{e(l.get("pratica"))}</p></div>'
         f'{base_feed(INK, TERRA, False)}</div>')
    return caixa(AREIA, c, 1350)


def l_dicionario(l, n, total):
    """Dicionário do crédito: um termo explicado em linguagem de empresário."""
    meio = (f'<div>{cham("Dicionário do crédito · nº " + str(l.get("numero", "01")))}'
            f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 96)}px;line-height:.98;color:{TERRA}">{e(l.get("termo"))}</p>'
            f'<p style="margin:14px 0 0;font-size:28px;font-style:italic;color:{INK};opacity:.7">{e(l.get("classe", ""))}</p>'
            f'<div style="width:110px;height:6px;background:{TERRA};margin:32px 0"></div>'
            f'<p style="margin:0;font-size:35px;line-height:1.45;color:{INK}">{e(l.get("definicao"))}</p>'
            f'<div style="margin-top:36px;background:#fff;border-radius:24px;padding:30px 36px">{cham("Na prática", VERDE)}'
            f'<p style="margin:0;font-size:30px;line-height:1.42;color:{INK}">{e(l.get("pratica"))}</p></div></div>')
    return moldura_ja(AREIA, False, n, total, meio, simbolo(0.06, top=-80, h=700))


def l_serie(l, n, total):
    """Quadro fixo de série (ex.: "Os 3 caminhos do credor"); "destaque" = coluna em terra."""
    cols = l.get("colunas", [])
    dst = l.get("destaque", -1)
    cab = '<div style="width:170px"></div>' + "".join(
        f'<div style="flex:1;background:{TERRA if i == dst else VERDE};border-radius:16px 16px 0 0;padding:20px 14px;text-align:center;font-size:25px;font-weight:700;line-height:1.15;color:#fff">{e(c)}</div>'
        for i, c in enumerate(cols))
    linhas = "".join(
        f'<div style="display:flex;gap:10px;margin-top:10px"><div style="width:170px;padding:20px 0;font-size:22px;font-weight:700;letter-spacing:1px;color:{TERRA}">{e(r.get("rotulo")).upper()}</div>'
        + "".join(f'<div style="flex:1;background:{"#F8E3D9" if i == dst else "#fff"};padding:20px 16px;font-size:24px;line-height:1.35;color:{INK}">{e(t)}</div>' for i, t in enumerate(r.get("itens", [])))
        + '</div>' for r in l.get("linhas", []))
    meio = (f'<div>{cham("Série · " + l.get("serie", "") + " · nº " + str(l.get("numero", "1")))}'
            f'<p style="margin:0 0 40px;font-size:{l.get("tamanho", 52)}px;font-weight:700;line-height:1.12;color:{VERDE}">{e(l.get("titulo"))}</p>'
            f'<div style="display:flex;gap:10px">{cab}</div>{linhas}<p style="margin:26px 0 0;font-size:22px;color:{INK};opacity:.7">{e(l.get("nota", ""))}</p></div>')
    return moldura_ja(AREIA, False, n, total, meio)


def l_split(l, n, total):
    c = (f'<div style="position:absolute;left:0;top:0;width:540px;height:1350px;background:{TERRA};overflow:hidden">{simbolo(0.14, "esq", top=700, h=800)}'
         f'<div style="position:absolute;left:70px;top:70px">{logo(True, 230)}</div>'
         f'<div style="position:absolute;left:70px;right:56px;top:340px">{cham(l.get("chamada", ""), ROSA)}'
         f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 76)}px;line-height:1.02;color:#fff">{e(l.get("titulo"))}</p></div></div>'
         f'<div style="position:absolute;left:600px;right:80px;top:400px"><div style="width:90px;height:6px;background:{TERRA};margin-bottom:34px"></div>'
         f'<p style="margin:0;font-size:34px;line-height:1.48;color:{INK}">{e(l.get("texto"))}</p></div>'
         f'<div style="position:absolute;left:600px;right:80px;bottom:80px;border-top:2px solid {ROSA2};padding-top:20px">{selo(INK, TERRA, 20)}</div>')
    return caixa(AREIA, c, 1350)


def l_palavra(l, n, total):
    bg, txt, dest, claro = cores(l, "terra")
    meio = (f'<div><p data-fit="904" style="margin:0;white-space:nowrap;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 340)}px;line-height:.9;color:{ROSA if claro else TERRA}">{e(l.get("palavra"))}</p>'
            f'<div style="width:120px;height:6px;background:{ROSA if claro else TERRA};margin:40px 0 34px"></div>'
            f'<p style="margin:0;max-width:860px;font-size:46px;font-weight:600;line-height:1.3;color:{txt}">{e(l.get("frase"))}</p></div>')
    return moldura_ja(bg, claro, n, total, meio, simbolo(0.1 if claro else 0.05, top=250, h=1150))


def l_linha_tempo(l, n, total):
    ms = l.get("marcos", [])
    itens = ""
    for i, m in enumerate(ms):
        ult = i == len(ms) - 1
        trilho = "" if ult else f'<div style="width:4px;flex:1;background:{ROSA2}"></div>'
        itens += (f'<div style="display:flex;gap:30px"><div style="flex:none;width:180px;text-align:right;padding-top:2px;font-family:Corm;font-weight:600;font-size:40px;line-height:1;color:{TERRA}">{e(m.get("quando"))}</div>'
                  f'<div style="flex:none;display:flex;flex-direction:column;align-items:center"><div style="width:34px;height:34px;border-radius:50%;margin-top:4px;background:{VERDE if ult else TERRA};border:5px solid {AREIA};box-shadow:0 0 0 3px {VERDE if ult else TERRA}"></div>{trilho}</div>'
                  f'<div style="padding-bottom:40px"><p style="margin:0;font-size:36px;font-weight:700;color:{VERDE}">{e(m.get("titulo"))}</p>'
                  f'<p style="margin:8px 0 0;font-size:28px;line-height:1.4;color:{INK}">{e(m.get("texto"))}</p></div></div>')
    meio = f'<div>{cham(l.get("chamada", ""))}<p style="margin:0 0 50px;font-size:{l.get("tamanho", 56)}px;font-weight:700;line-height:1.1;color:{VERDE}">{e(l.get("titulo"))}</p>{itens}</div>'
    return moldura_ja(AREIA, False, n, total, meio)


def l_grade(l, n, total):
    cards = ""
    for i, b in enumerate(l.get("blocos", [])[:4]):
        esc = i in (0, 3)
        cards += (f'<div style="background:{TERRA if esc else "#fff"};border-radius:26px;padding:36px 34px;display:flex;flex-direction:column;gap:12px">'
                  f'<p style="margin:0;font-family:Corm;font-weight:600;font-size:70px;line-height:.9;color:{ROSA if esc else TERRA}">{e(b.get("topo", f"{i+1:02d}"))}</p>'
                  f'<p style="margin:0;font-size:34px;font-weight:700;line-height:1.15;color:{"#fff" if esc else VERDE}">{e(b.get("titulo"))}</p>'
                  f'<p style="margin:0;font-size:26px;line-height:1.4;color:{"#fff" if esc else INK}">{e(b.get("texto"))}</p></div>')
    meio = (f'<div><p style="margin:0 0 40px;font-size:{l.get("tamanho", 54)}px;font-weight:700;line-height:1.12;color:{VERDE}">{e(l.get("titulo"))}</p>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:330px;gap:22px">{cards}</div></div>')
    return moldura_ja(ROSA, False, n, total, meio)


def l_marcatexto(l, n, total):
    folha = (f'<div style="background:#fff;border-radius:6px;box-shadow:0 20px 50px rgba(59,47,44,.16);padding:60px 60px 66px;transform:rotate(-1.2deg)">'
             f'<p style="margin:0 0 26px;font-size:24px;font-weight:700;letter-spacing:3px;color:{INK};opacity:.65">{e(l.get("cabecalho", ""))}</p>'
             f'<p style="margin:0;font-family:Georgia,serif;font-size:40px;line-height:1.6;color:{INK}">{e(l.get("antes"))} '
             f'<span style="background:linear-gradient(180deg,transparent 45%,rgba(234,203,187,.95) 45%);font-weight:700;color:{TERRA}">{e(l.get("grifo"))}</span> {e(l.get("depois"))}</p></div>')
    nota = (f'<div style="display:flex;justify-content:flex-end;gap:14px;margin-top:34px;padding-right:20px">'
            f'<svg width="80" height="70" viewBox="0 0 80 70"><path d="M70 64 C60 30 40 14 10 8 M10 8 L26 2 M10 8 L22 20" fill="none" stroke="{TERRA}" stroke-width="4" stroke-linecap="round"></path></svg>'
            f'<p style="margin:20px 0 0;max-width:560px;font-size:32px;font-weight:700;line-height:1.3;color:{VERDE}">{e(l.get("nota"))}</p></div>')
    return moldura_ja(AREIA, False, n, total, f'<div>{cham(l.get("chamada", ""))}<div style="height:24px"></div>{folha}{nota}</div>')


def l_fluxo(l, n, total):
    def box(t, bg, c, w="100%"):
        return f'<div style="width:{w};box-sizing:border-box;background:{bg};border-radius:22px;padding:30px;font-size:32px;font-weight:700;line-height:1.25;color:{c};text-align:center">{e(t)}</div>'
    seta = (f'<svg width="904" height="150" viewBox="0 0 904 150"><path d="M452 0 V40 M452 40 H226 V140 M452 40 H678 V140 M214 124 L226 144 L238 124 M666 124 L678 144 L690 124" fill="none" stroke="{TERRA}" stroke-width="4"></path>'
            f'<rect x="150" y="62" width="150" height="44" rx="22" fill="{AREIA}" stroke="{TERRA}" stroke-width="2"></rect><text x="225" y="92" text-anchor="middle" font-family="Cabin" font-weight="700" font-size="24" fill="{TERRA}">{e(l.get("rot_sim", "Sim"))}</text>'
            f'<rect x="603" y="62" width="150" height="44" rx="22" fill="{AREIA}" stroke="{TERRA}" stroke-width="2"></rect><text x="678" y="92" text-anchor="middle" font-family="Cabin" font-weight="700" font-size="24" fill="{TERRA}">{e(l.get("rot_nao", "Não"))}</text></svg>')
    meio = (f'<div><p style="margin:0 0 44px;font-size:{l.get("tamanho", 56)}px;font-weight:700;line-height:1.12;color:{VERDE}">{e(l.get("titulo"))}</p>'
            f'{box(l.get("pergunta"), TERRA, "#fff")}{seta}<div style="display:flex;gap:28px">{box(l.get("sim"), VERDE, "#fff", "50%")}{box(l.get("nao"), "#fff", INK, "50%")}</div></div>')
    return moldura_ja(AREIA, False, n, total, meio)


def l_moldura(l, n, total):
    foto = (f'<div style="position:absolute;left:110px;top:200px;width:560px;background:#fff;padding:22px 22px 70px;box-shadow:0 22px 50px rgba(0,0,0,.25);transform:rotate(-3deg)">'
            f'{_img(l.get("imagem"), "display:block;width:516px;height:600px")}'
            f'<p style="margin:18px 0 0;font-family:Corm;font-style:italic;font-size:30px;color:{INK};text-align:center">{e(l.get("legenda", ""))}</p></div>')
    c = (simbolo(0.12, top=150, h=1000) + f'<div style="position:absolute;right:88px;top:88px">{logo(True, 230)}</div>' + foto +
         f'<div style="position:absolute;left:88px;right:88px;top:1000px"><p style="margin:0;font-family:Corm;font-weight:600;font-size:{l.get("tamanho", 62)}px;line-height:1.05;color:#fff">{e(l.get("titulo"))}</p>'
         f'<p style="margin:14px 0 0;font-size:30px;line-height:1.4;color:#fff">{e(l.get("texto"))}</p></div>')
    return caixa(TERRA, c, 1350)


def l_ranking(l, n, total):
    its = ""
    for i, it in enumerate(l.get("itens", [])[:4], 1):
        its += (f'<div style="display:flex;gap:34px;align-items:center;padding:24px 0;border-top:2px solid {ROSA2}">'
                f'<p style="margin:0;flex:none;width:140px;font-family:Corm;font-weight:600;font-size:190px;line-height:.75;color:{TERRA if i == 1 else VERDE}">{i}</p>'
                f'<div><p style="margin:0;font-size:38px;font-weight:700;line-height:1.15;color:{VERDE}">{e(it.get("titulo"))}</p>'
                f'<p style="margin:8px 0 0;font-size:28px;line-height:1.4;color:{INK}">{e(it.get("texto"))}</p></div></div>')
    meio = f'<div>{cham(l.get("chamada", ""))}<p style="margin:0 0 36px;font-size:{l.get("tamanho", 56)}px;font-weight:700;line-height:1.1;color:{VERDE}">{e(l.get("titulo"))}</p>{its}</div>'
    return moldura_ja(AREIA, False, n, total, meio)


LAYOUTS.update({"foto": l_foto, "foto_fundo": l_foto_fundo, "lei": l_lei, "dicionario": l_dicionario, "serie": l_serie,
                "split": l_split, "palavra": l_palavra, "linha_tempo": l_linha_tempo, "grade": l_grade,
                "marcatexto": l_marcatexto, "fluxo": l_fluxo, "moldura": l_moldura, "ranking": l_ranking})

# ------------------------------------------------------------------ peças largas (cortadas em várias imagens)
# 1) MOSAICO: 3 posts que formam uma imagem só na grade do perfil (tendência "puzzle feed").
#    O perfil mostra cada post recortado em 3:4 (1012 px centrais de cada imagem 1080x1350): a arte larga
#    tem 3 x 1012 px visíveis + 34 px de sobra nas bordas, e cada imagem leva 34 px extras de cada lado.
# 2) PANORAMA: carrossel contínuo (a arte atravessa as lâminas ao deslizar).
GRADE_VIS, GRADE_SOBRA = 1012, 34


def w_mosaico(p):
    bg, txt, dest, claro = cores(p, "terra")
    W = 3 * GRADE_VIS + 2 * GRADE_SOBRA
    x0 = GRADE_SOBRA
    rod = p.get("rodapes", ["", "", ""])
    rodapes = "".join(
        f'<div style="position:absolute;left:{x0 + i * GRADE_VIS + 70}px;width:{GRADE_VIS - 140}px;bottom:96px;font-size:30px;line-height:1.35;color:{txt}">{e(t)}</div>'
        for i, t in enumerate(rod))
    faixa = ROSA if claro else ROSA
    corpo = f'''
    <img src="{u("assets/simb_terra.png")}" style="position:absolute;right:-60px;top:-80px;height:1520px;opacity:{0.22 if claro else 0.09}">
    <div style="position:absolute;left:0;right:0;top:930px;height:10px;background:{faixa}"></div>
    <div style="position:absolute;left:{x0 + 70}px;top:96px">{logo(claro, 300)}</div>
    <p style="position:absolute;left:{x0 + 70}px;top:300px;margin:0;font-size:34px;font-weight:700;letter-spacing:8px;color:{ROSA if claro else VERDE}">{e(p.get("chamada", "")).upper()}</p>
    <p data-fit="{3 * GRADE_VIS - 150}" style="position:absolute;left:{x0 + 50}px;top:350px;margin:0;white-space:nowrap;font-family:Corm;font-weight:600;font-size:{p.get("tamanho", 400)}px;line-height:1;color:{"#fff" if claro else TERRA}">{e(p.get("titulo"))}</p>
    <p style="position:absolute;left:{x0 + 70}px;top:985px;width:{2 * GRADE_VIS}px;margin:0;font-size:52px;line-height:1.25;color:{txt}">{e(p.get("texto"))}</p>
    {rodapes}
    <div style="position:absolute;left:{x0 + 2 * GRADE_VIS + 70}px;width:{GRADE_VIS - 140}px;bottom:200px">{selo(txt, ROSA if claro else TERRA, 28)}</div>'''
    return W, f'<div id="r" style="width:{W}px;height:1350px;background:{bg};position:relative;overflow:hidden;font-family:Cabin,sans-serif">{corpo}</div>', \
        [(i * GRADE_VIS, 1080) for i in range(3)]


def w_jornada(p):
    """Carrossel panorâmico: uma linha contínua atravessa as lâminas, com uma etapa em cada."""
    passos = p.get("passos", [])
    n = len(passos) + 1
    W = n * 1080
    Y = 760
    marcos = ""
    for i, s in enumerate(passos, 1):
        cx = i * 1080 + 540
        ultimo = i == len(passos)
        cor = TERRA if ultimo else VERDE
        marcos += f'''
        <div style="position:absolute;left:{cx - 70}px;top:{Y - 70}px;width:140px;height:140px;border-radius:50%;background:{TERRA if ultimo else AREIA};border:6px solid {TERRA};
             display:flex;align-items:center;justify-content:center;font-family:Corm;font-weight:600;font-size:76px;color:{"#fff" if ultimo else TERRA}">{i}</div>
        <p style="position:absolute;left:{i * 1080 + 110}px;width:860px;top:300px;margin:0;font-size:28px;font-weight:700;letter-spacing:6px;color:{ROSA2}">ETAPA {i} DE {len(passos)}</p>
        <p style="position:absolute;left:{i * 1080 + 700}px;top:20px;margin:0;font-family:Corm;font-weight:600;font-size:440px;line-height:1;color:{ROSA};opacity:.4">{i}</p>
        <p style="position:absolute;left:{i * 1080 + 110}px;width:860px;top:350px;margin:0;font-size:{s.get("tamanho", 78)}px;font-weight:700;line-height:1.1;color:{cor}">{e(s.get("titulo"))}</p>
        <p style="position:absolute;left:{i * 1080 + 110}px;width:820px;top:{Y + 130}px;margin:0;font-size:44px;line-height:1.4;color:{INK}">{e(s.get("texto"))}</p>
        <div style="position:absolute;left:{i * 1080 + 88}px;right:{W - (i + 1) * 1080 + 88}px;bottom:88px;display:flex;justify-content:space-between;align-items:flex-end;border-top:2px solid {ROSA2};padding-top:22px">
          <p style="margin:0;font-size:28px;color:{INK}"><b>{i + 1:02d}</b> / {n:02d}</p>{selo(INK, TERRA, 22)}</div>'''
    corpo = f'''
    <div style="position:absolute;left:0;top:0;width:1080px;height:1350px;background:{TERRA}"></div>
    <div style="position:absolute;left:0;top:0;width:1080px;height:1350px;overflow:hidden"><img src="{u("assets/simb_terra.png")}" style="position:absolute;right:-180px;top:250px;height:1150px;opacity:.14"></div>
    <div style="position:absolute;left:88px;top:88px">{logo(True, 330)}</div>
    <p style="position:absolute;left:88px;top:330px;margin:0;font-size:28px;font-weight:600;letter-spacing:6px;color:{ROSA}">{e(p.get("tema", "")).upper()}</p>
    <p style="position:absolute;left:88px;width:880px;top:390px;margin:0;font-size:{p.get("tamanho", 80)}px;font-weight:700;line-height:1.08;color:#fff">{e(p.get("titulo"))}</p>
    <p style="position:absolute;left:88px;width:860px;top:{Y + 90}px;margin:0;font-size:38px;line-height:1.35;color:{ROSA}">{e(p.get("subtitulo", ""))}</p>
    <p style="position:absolute;left:88px;bottom:88px;margin:0;font-size:28px;color:#fff"><b>01</b> / {n:02d}</p>
    <p style="position:absolute;right:{W - 1080 + 88}px;bottom:88px;margin:0;font-size:28px;font-weight:600;color:#fff">Arraste →</p>
    <div style="position:absolute;left:640px;right:540px;top:{Y - 5}px;height:10px;background:{ROSA2}"></div>
    <div style="position:absolute;left:560px;top:{Y - 40}px;width:80px;height:80px;border-radius:50%;background:{ROSA}"></div>
    {marcos}'''
    return W, f'<div id="r" style="width:{W}px;height:1350px;background:{AREIA};position:relative;overflow:hidden;font-family:Cabin,sans-serif">{corpo}</div>', \
        [(i * 1080, 1080) for i in range(n)]


LARGOS = {"mosaico": w_mosaico, "jornada": w_jornada}


def renderizar_largo(post, saida, chrome=None):
    """Renderiza a peça larga uma vez e corta nas imagens. No mosaico, 01 = esquerda, 02 = meio, 03 = direita
    (na planilha, publicar 03 primeiro, depois 02 e por último 01)."""
    os.makedirs(saida, exist_ok=True)
    p = post["largo"]
    W, corpo, cortes = LARGOS[p["layout"]](p)
    arquivos = []
    with sync_playwright() as pw:
        kw = {"executable_path": chrome} if chrome else {}
        b = pw.chromium.launch(args=["--allow-file-access-from-files"], **kw)
        pg = b.new_page(viewport={"width": W, "height": 1350})
        tmp = os.path.join(saida, "_tmp.html")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><html><head><meta charset="utf-8"><style>{fontcss()}</style></head><body>{corpo}</body></html>')
        pg.goto("file://" + os.path.abspath(tmp))
        pg.evaluate("document.fonts.ready.then(()=>1)")
        pg.evaluate("""() => document.querySelectorAll('[data-fit]').forEach(el => {
            const alvo = +el.dataset.fit, fs = parseFloat(getComputedStyle(el).fontSize);
            el.style.fontSize = Math.min(fs * alvo / el.scrollWidth, 540) + 'px'; })""")
        pg.wait_for_timeout(300)
        pg.locator("#r").screenshot(path=os.path.join(saida, "_inteira.png"))
        for i, (x, w) in enumerate(cortes, 1):
            a = os.path.join(saida, f"{i:02d}.png")
            pg.screenshot(path=a, clip={"x": x, "y": 0, "width": w, "height": 1350})
            arquivos.append(a)
        os.remove(tmp)
        b.close()
    return arquivos


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
            pg.evaluate("""() => document.querySelectorAll('[data-fit]').forEach(el => {
                const alvo = +el.dataset.fit, fs = parseFloat(getComputedStyle(el).fontSize);
                if (el.scrollWidth > alvo) el.style.fontSize = (fs * alvo / el.scrollWidth) + 'px'; })""")
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
    fn = renderizar_largo if "largo" in post else renderizar
    for a in fn(post, sys.argv[2], os.environ.get("CHROME_PATH")):
        print(a)
