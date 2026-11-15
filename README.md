# Publicações – Justo Acordo

Publica automaticamente no Instagram (@justo.acordo) e na Página do Facebook "Justo Acordo" os posts
**aprovados** na aba **PUBLICAÇÕES JA** da planilha VISÃO GERAL - JASA.

Cópia do sistema da Advocacia Soares (`jailson-rgb/publicacoes-soares`), com identidade visual e contas próprias.

## Como funciona

1. A rotina semanal do Claude cria os posts (arte + legenda) – ver `ROTINA_SEMANAL.md`.
2. As artes vão para a pasta do Drive `PUBLICAÇÕES JUSTO ACORDO / 02 POSTS GERADOS` e cada post vira uma linha na aba PUBLICAÇÕES JA.
3. O Jailson revisa e marca **APROVAR = Sim** (ou usa "APROVAR TUDO ATÉ").
4. Este repositório roda de hora em hora (minuto 37): lê a planilha `FILA APROVADA JA` (só os aprovados),
   publica o que já chegou na data/hora e grava o resultado em `status.csv`, que aparece na coluna STATUS.

Para publicar na hora: **Actions → Publicar posts aprovados → Run workflow**.

## Configuração

Settings → Secrets and variables → Actions

| Tipo | Nome | O que é |
|---|---|---|
| Secret | `META_TOKEN` | token do usuário do sistema do app "Soares Advocacia Publicacoes", com acesso aos ativos da Justo Acordo (colado só pelo Jailson) |
| Variable | `FILA_ID` | ID da planilha FILA APROVADA JA |
| Variable | `IG_USER_ID` | ID da conta do Instagram @justo.acordo |
| Variable | `FB_PAGE_ID` | ID da Página Justo Acordo (61596452316521) |

Sem `META_TOKEN`, roda em **modo simulação** (não publica, só testa a fila e as artes).
Sem `FILA_ID`, para com erro – não há fila padrão (para nunca ler a fila da Advocacia Soares).

## Pastas

- `publicar.py` – publicador
- `gerador/render.py` – modelos de arte da Justo Acordo (stories placar / acordo fechado / semana; carrossel)
- `gerador/placar.py` – calcula o placar a partir da aba POS ACORDO (o snapshot fica no Drive, **nunca aqui**)
- `gerador/exemplos/` – JSON de exemplo de cada formato
- `midia/` – imagens já publicadas (precisam de endereço público para a Meta buscar)
- `status.csv` – registro de cada publicação

**Atenção:** o repositório é público (a Meta precisa buscar as imagens). Nada de planilhas, snapshots,
nomes de devedores ou credores aqui – só as artes que já foram aprovadas para publicação.
