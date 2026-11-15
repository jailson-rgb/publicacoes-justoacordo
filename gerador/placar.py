"""
Placar da Justo Acordo a partir da aba POS ACORDO (CLIENTES) da VISÃO GERAL - JASA.

Uso:
  python gerador/placar.py pos_acordo.csv [snapshot_anterior.csv] --novo-snapshot snapshot_atual.csv

- pos_acordo.csv: a aba exportada (cabeçalho na 1ª linha: CLIENTE, DEVEDOR, MODALIDADE, ANDAMENTO, ...,
  PARCELA, QUANTIDADE, PERIODICIDADE, ..., RECEBIDO LIQUIDO, ...).
- snapshot: foto da semana anterior (gerada por este script). Contém nomes e valores:
  NUNCA versionar no GitHub (repositório público) — guardar na pasta do Drive "PUBLICAÇÕES JUSTO ACORDO / 03 PLACAR".

Regras (aprovadas pelo Jailson em 15/11/2026):
- Valor divulgado = RECEBIDO LÍQUIDO (o que ficou com o cliente, já descontados os honorários). Nunca bruto e líquido juntos.
- Só dinheiro efetivamente recebido entra; valor apenas acordado não.
- Semana entra no story "Nesta semana" só se líquido da semana >= PISO_SEMANA e novos acordos >= PISO_ACORDOS;
  caso contrário sai só o placar acumulado.
- Só acordos extrajudiciais (sem nº de processo) entram no placar e no "Acordo fechado".
Saída: JSON no terminal (para a rotina), com os valores já formatados para as artes.
"""
import csv
import json
import re
import sys

PISO_SEMANA = 30000.0
PISO_ACORDOS = 3
PROCESSO = re.compile(r"\d{7}-\d{2}\.\d{4}")


def num(x):
    x = (x or "").replace("R$", "").strip()
    if not x or x in ("-",):
        return 0.0
    try:
        return float(x.replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0


def chave_linha(r):
    return "|".join((r.get("CLIENTE", "").strip(), r.get("DEVEDOR", "").strip(), r.get("PARCELA", "").strip(),
                     r.get("QUANTIDADE", "").strip(), r.get("PERIODICIDADE", "").strip()))


def chave_acordo(r):
    dev = re.sub(r"\(.*?\)|\*|-.*$", "", r.get("DEVEDOR", "")).strip().upper()
    return r.get("CLIENTE", "").strip().upper() + "|" + dev


def ler(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    cab = [c.strip().upper() for c in rows[0]]
    out = []
    for l in rows[1:]:
        d = {cab[i]: (l[i] if i < len(l) else "") for i in range(len(cab))}
        if d.get("CLIENTE", "").strip():
            out.append(d)
    return out


def moeda_curta(v):
    """R$ 1,9 milhão / R$ 62 mil — arredonda sempre PARA BAIXO (nunca inflar o número) e sem centavos."""
    import math
    if v >= 1_000_000:
        m = math.floor(v / 100_000) / 10
        s = f"{m:.1f}".replace(".", ",").replace(",0", "")
        return f"R$ {s}", "milhão" if m < 2 else "milhões"
    return f"R$ {math.floor(v / 1000)}", "mil"


def main():
    args = sys.argv[1:]
    novo = None
    if "--novo-snapshot" in args:
        i = args.index("--novo-snapshot")
        novo = args[i + 1]
        del args[i:i + 2]
    pos = [r for r in ler(args[0]) if not PROCESSO.search(r.get("MODALIDADE", "") + " " + r.get("SITUAÇÂO", r.get("SITUAÇÃO", "")))]
    # só acordos extrajudiciais entram nos números divulgados (acordos em processo ficam fora)
    anterior = {}
    if len(args) > 1:
        with open(args[1], encoding="utf-8") as f:
            for l in csv.reader(f):
                if l and l[0] != "CHAVE":
                    anterior[l[0]] = (num(l[1]), l[2])

    acumulado = sum(max(0.0, num(r.get("RECEBIDO LIQUIDO"))) for r in pos)
    acordos = {chave_acordo(r) for r in pos}
    empresas = {r.get("CLIENTE", "").strip().upper() for r in pos}

    semana = 0.0
    novos = []
    if anterior:
        ja = {v[1] for v in anterior.values()}
        for r in pos:
            k = chave_linha(r)
            semana += max(0.0, max(0.0, num(r.get("RECEBIDO LIQUIDO"))) - anterior.get(k, (0.0, ""))[0])
        vistos = set()
        for r in pos:
            ka = chave_acordo(r)
            if ka not in ja and ka not in vistos:
                vistos.add(ka)
                extrajud = not PROCESSO.search(r.get("MODALIDADE", "") + " " + r.get("SITUAÇÂO", r.get("SITUAÇÃO", "")))
                novos.append({"cliente": r.get("CLIENTE"), "devedor": r.get("DEVEDOR"), "extrajudicial": extrajud,
                              "forma": f'{r.get("QUANTIDADE", "")}x {r.get("PERIODICIDADE", "").lower()}'})

    if novo:
        with open(novo, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["CHAVE", "RECEBIDO_LIQUIDO", "ACORDO"])
            for r in pos:
                w.writerow([chave_linha(r), f"{max(0.0, num(r.get('RECEBIDO LIQUIDO'))):.2f}", chave_acordo(r)])

    v, suf = moeda_curta(acumulado)
    sv, ssuf = moeda_curta(semana) if semana else ("", "")
    print(json.dumps({
        "acumulado_liquido": round(acumulado, 2), "placar": {"valor": v, "sufixo": suf, "acordos": str(len(acordos)), "empresas": str(len(empresas))},
        "semana_liquido": round(semana, 2), "semana_novos_acordos": len(novos),
        "publicar_semana": bool(anterior) and semana >= PISO_SEMANA and len(novos) >= PISO_ACORDOS,
        "semana": {"valor": sv, "sufixo": ssuf, "acordos": str(len(novos)), "acumulado": f"{v} {suf}"},
        "novos_acordos": novos,
        "aviso": "Conferir duplicidades (mesmo acordo em várias linhas) e valores negativos antes de publicar o acumulado.",
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
