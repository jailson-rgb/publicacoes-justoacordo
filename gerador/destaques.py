"""Gera as capas dos DESTAQUES do Instagram da Justo Acordo e os stories de cada destaque.
Uso: python gerador/destaques.py rascunhos/DESTAQUES
Capas: 1080x1920 com o ícone no centro (o Instagram recorta um círculo central).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright  # noqa: E402

import render as R  # noqa: E402

S = 'fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"'
ICONES = {
    "Quem somos": f'<img src="{R.u("assets/logo_branco.png")}" style="width:250px">',
    "Como funciona": f'<svg width="260" height="260" viewBox="0 0 260 260" {S}><circle cx="45" cy="200" r="22"/><circle cx="130" cy="130" r="22"/><circle cx="215" cy="60" r="22"/><path d="M62 186 L112 146 M147 116 L197 76"/></svg>',
    "100% no êxito": '<div style="font-family:Corm;font-weight:600;font-size:150px;color:#fff;line-height:1;font-variant-numeric:lining-nums">100%</div>',
    "Resultados": f'<svg width="260" height="260" viewBox="0 0 260 260" {S}><path d="M40 220 H225"/><path d="M70 220 V150 M130 220 V105 M190 220 V55"/></svg>',
    "Garantias": f'<svg width="260" height="260" viewBox="0 0 260 260" {S}><path d="M130 30 L215 62 V130 C215 180 178 215 130 232 C82 215 45 180 45 130 V62 Z"/><path d="M92 132 L120 160 L172 106"/></svg>',
    "Contato": f'<svg width="260" height="260" viewBox="0 0 260 260" {S}><path d="M45 60 H215 V170 H120 L72 212 V170 H45 Z"/><path d="M85 105 H175 M85 135 H150"/></svg>',
}

TEL = "(51) 98975-1608"
STORIES = {
    "Quem somos": [
        {"layout": "story", "chamada": "Quem somos", "titulo": "Mediação extrajudicial entre empresas.",
         "texto": "Recuperamos crédito com método e diálogo: negociamos com o devedor de forma técnica e respeitosa, formalizamos o acordo e acompanhamos cada parcela até a quitação."},
        {"layout": "story", "chamada": "Para quem", "titulo": "Empresas com valores a receber.",
         "texto": "Indústrias, distribuidores, atacadistas, comércio, serviços, agro e cooperativas."},
    ],
    "Como funciona": [
        {"layout": "story", "chamada": "Como funciona · 1/2", "titulo": "1. Você envia o devedor\n2. Nós abrimos a conversa",
         "texto": "Basta mandar as notas e os contatos que tiver. A partir daí, a negociação é conduzida pela nossa equipe, com cordialidade e firmeza."},
        {"layout": "story", "chamada": "Como funciona · 2/2", "titulo": "3. O acordo é formalizado\n4. O dinheiro volta ao caixa",
         "texto": "O termo assinado vira título executivo: se o devedor descumprir, o credor cobra direto, sem discutir a dívida de novo. Acompanhamos cada parcela."},
    ],
    "100% no êxito": [
        {"layout": "story", "chamada": "Sem risco para o credor", "titulo": "Cobrança extrajudicial 100% no êxito.",
         "texto": "Só recebemos quando o devedor paga. Se não houver recebimento, a sua empresa não tem custo."},
    ],
    "Resultados": [
        {"layout": "placar", "valor": "R$ 1,6", "sufixo": "milhão", "acordos": "210", "empresas": "20"},
    ],
    "Garantias": [
        {"layout": "story", "chamada": "Acordo mais seguro", "titulo": "Sempre buscamos uma garantia no acordo.",
         "texto": "Real (como hipoteca, alienação fiduciária ou penhor) ou pessoal (como aval ou fiança de sócio). Acordo com garantia tem mais chance de ser cumprido e, se não for, há mais por onde receber."},
        {"layout": "story", "chamada": "Título executivo", "titulo": "O acordo vira título executivo.",
         "texto": "Assinado pelo devedor e por duas testemunhas, o termo de acordo é título executivo extrajudicial (CPC, art. 784, III). Se houver descumprimento, a cobrança vai direto à execução."},
    ],
    "Contato": [
        {"layout": "story", "chamada": "Fale com a nossa equipe", "titulo": f"WhatsApp\n{TEL}",
         "texto": "justoacordo.com.br\n\nAv. Carlos Gomes, 222, 8º andar\nPorto Alegre/RS\n\nSegunda a sexta, das 9h às 18h."},
    ],
}


def capa(nome):
    corpo = f'''<div style="position:absolute;left:290px;top:710px;width:500px;height:500px;border-radius:50%;background:{R.TERRA};
      display:flex;align-items:center;justify-content:center">{ICONES[nome]}</div>'''
    return R.caixa(R.AREIA, corpo)


def main(saida):
    os.makedirs(saida, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        tmp = os.path.join(saida, "_tmp.html")
        for i, nome in enumerate(STORIES, 1):
            slug = f"{i}-{nome.lower().replace(' ', '-').replace('ê', 'e').replace('%', '')}"
            itens = [("capa", capa(nome))] + [(f"story{k}", R.LAYOUTS[l["layout"]](l, k, 1)) for k, l in enumerate(STORIES[nome], 1)]
            for suf, corpo in itens:
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(f'<!doctype html><html><head><meta charset="utf-8"><style>{R.fontcss()}</style></head><body>{corpo}</body></html>')
                pg.goto("file://" + os.path.abspath(tmp))
                pg.evaluate("document.fonts.ready.then(()=>1)")
                pg.wait_for_timeout(150)
                p = os.path.join(saida, f"{slug}-{suf}.png")
                pg.locator("#r").screenshot(path=p)
                print(p)
        os.remove(tmp)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
