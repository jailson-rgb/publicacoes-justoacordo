# Rotina semanal de criação de posts – Justo Acordo

Executada todo domingo às 18:43 pelo Claude (tarefa agendada). Lembrete de aprovação: segunda, 08:37.
Também serve de guia para pedidos avulsos.

## Onde fica cada coisa
- Planilha VISÃO GERAL - JASA – `1EWl4M45oD3UbPBsDdoY-8jIS3own-YmZ_ObeFQcF2hI`
  - aba **PUBLICAÇÕES** (aprovação) – a MESMA da Advocacia Soares. Posts da Justo Acordo usam ID **JA2026-NNN**
    (é o prefixo "JA" que manda o post para o Instagram/Facebook da Justo Acordo; sem ele o post iria para a Soares).
    Colunas A–K como na Soares (na coluna K, "ALERTA OAB", registrar alertas de autorização do cliente/sigilo).
    Nunca escrever em L (APROVAR), M (OBSERVAÇÕES), N (STATUS), P1 ("APROVAR TUDO ATÉ", vale para as duas marcas)
    nem Q (MARCA – fórmula).
  - aba **POS ACORDO (CLIENTES)** – fonte dos números (só leitura). Nunca mexer em nenhuma outra aba.
- Drive "PUBLICAÇÕES JUSTO ACORDO" (1BxqMnNDjnLbacZJ5_rGfoQLel35Xpnsc): 01 ENTRADA (1EOfZa3Yj8L14jSHDBBrmJF8LuGrux6CL) (fotos de termos e conteúdos do Jailson/Mariana),
  02 POSTS GERADOS (19Bwb-pF0hQ0ZfJxfAybgFj1d6banPcvO), 03 PLACAR (1_FglkBHLmviv_0q4CC4_z9y_Dfelc8jz) (snapshots semanais – nunca no GitHub), 04 Cartões e Perfis.
- Renderizador: `gerador/render.py`; placar: `gerador/placar.py`.

## Público e tom
- Fala só com **empresas credoras** (indústria, comércio, serviços, agro, cooperativas). Nada dirigido a devedores.
- Sem menção à Advocacia Soares nem à OAB. Nada que pareça oferta de serviço jurídico: a Justo Acordo faz
  **mediação e negociação extrajudicial**.
- Tom do manual da marca: seguro, amigável, confiante, cordial – "sério sem ser rígido". Linguagem de empresário.

## Grade (horário de Brasília)
- Segunda 12:00 – story **Placar** (acumulado) ou **Nesta semana** (se passar no piso, ver abaixo).
- Terça 12:00 – **publicação de feed nº 1** (estatística de crédito/inadimplência ou educativo).
- Quinta 12:00 – **publicação de feed nº 2** (conteúdo do Jailson da pasta ENTRADA ou tema educativo).
- **Acordo fechado** – 1 a 2 stories por semana quando houver acordo novo extrajudicial (terça a sexta, 09:00).
- 1ª semana do mês: a publicação de terça vira **"Números do mês"** (layout `resultado` ou `barras`, em post único ou carrossel curto).
- DESTINO padrão: "Instagram + Facebook".
- As publicações de feed NÃO são sempre carrossel: ver "Variação de formato" abaixo.

## Números (regras aprovadas pelo Jailson em 15/11/2026)
1. Exportar a aba POS ACORDO para CSV e rodar
   `python gerador/placar.py pos.csv snapshot_semana_anterior.csv --novo-snapshot snapshot_hoje.csv`
   (snapshots baixados/enviados para "03 PLACAR").
2. Valor divulgado é sempre o **LÍQUIDO** (o que ficou com o cliente, já descontados os honorários).
   **Nunca** mostrar bruto e líquido no mesmo post, nem o percentual de honorários (dá para deduzir o percentual).
3. Só dinheiro **efetivamente recebido**; valor apenas acordado não entra.
4. Arredondar sempre **para baixo** e por extenso ("R$ 1,9 milhão", "R$ 62 mil"); nunca centavos.
5. Story "Nesta semana" só quando a semana tiver **≥ R$ 30 mil líquidos e ≥ 3 acordos novos**
   (`publicar_semana: true`). Caso contrário, sai o **Placar** acumulado. Objetivo: nunca parecer operação pequena.
6. Antes de publicar o acumulado, conferir duplicidades (mesmo acordo em várias linhas) e saldos negativos;
   em caso de dúvida, preencher ALERTA e explicar.

## Story "Acordo fechado"
- Só acordos **extrajudiciais** (sem número de processo) – acordo judicial nunca vira post.
- Precisa de **autorização do cliente credor** (uma vez por cliente) – registrar em OBSERVAÇÕES/ALERTA se não houver.
- Conteúdo: segmento genérico do credor + UF (ex.: "INDÚSTRIA DE ALIMENTOS · RS"); "Dívida vencida desde mm/aaaa"
  (antiga) ou "há N dias" (recente) – data tirada das notas/contrato na pasta do devedor; se não achar, omitir a linha;
  forma do acordo; valor **líquido** que voltou ao caixa.
- Foto do termo (pasta ENTRADA) entra **sempre desfocada** pelo renderizador, como fundo. Nunca dado legível
  (nome, CPF/CNPJ, assinatura, valor) do devedor ou do credor.
- Proibido: nome do devedor ou do credor, cidade, valor da dívida, percentual de honorários.

## Selo e argumento
- "Cobrança extrajudicial **100% no êxito**: só recebemos quando o devedor paga." – vale só para a cobrança
  extrajudicial (o RVP/pré-processo é cobrado à parte; não generalizar).

## Fontes para os carrosséis
- Serasa Experian (inadimplência das empresas, recuperações judiciais e falências) e Banco Central
  (Estatísticas Monetárias e de Crédito – inadimplência PJ). Sempre citar fonte e mês de referência.
- Conteúdo do Jailson na pasta ENTRADA. Nunca inventar número.

## Sigilo do know-how
- Não revelar método, ferramentas de pesquisa patrimonial, critérios de seleção de casos, roteiros de negociação.

## Variação de formato (pedido do Jailson, 15/11/2026)
O feed não pode parecer sempre o mesmo carrossel. Variar o FORMATO (uma lâmina x várias) e o LAYOUT (estrutura visual).

**Formatos de feed** (coluna TIPO):
- **Post único** – uma lâmina só (1080x1350). Bom para frase de impacto, um número forte, pergunta e resposta, mito x verdade, resultado do mês.
- **Carrossel curto** – 3 lâminas.
- **Carrossel longo** – 5 a 7 lâminas (conteúdo educativo que pede passo a passo).

**Layouts disponíveis** (`gerador/render.py`; exemplo de todos em `gerador/exemplos/exemplo-formatos.json`):
- clássicos de carrossel: `capa`, `topico`, `numero`, `fechamento`;
- variados (servem para post único e para montar carrosséis diferentes): `frase`, `dado`, `mito`, `comparativo`,
  `checklist`, `passos`, `pergunta`, `barras`, `resultado`.
- Vários aceitam `"fundo": "terra" | "areia" | "rosa"` – alternar o fundo também conta como variação.

**Regras de rodízio**
1. Antes de criar, ler os `post.json` de `rascunhos/` das **últimas 3 semanas** (campo `"formato"` e os layouts usados).
2. Por semana, as duas publicações de feed têm de ser de **formatos diferentes** (ex.: um post único + um carrossel).
3. Pelo menos **1 post único por semana**, e no máximo 1 carrossel longo por semana.
4. Não repetir a mesma "receita" (formato + layout principal) em semanas seguidas; o mesmo layout principal só
   volta depois de 2 semanas.
5. Carrossel não precisa começar sempre com `capa` nem terminar com `fechamento`: pode abrir com `pergunta`,
   `dado` ou `mito`, e fechar com `checklist` ou `frase`.
6. Escolher o layout pelo conteúdo: número forte → `dado`/`resultado`; série histórica → `barras`; crença comum →
   `mito`; antes x depois → `comparativo`; lista prática → `checklist`; processo → `passos`; dúvida → `pergunta`.
7. `barras` só com dados reais e fonte citada (Serasa, Banco Central ou a aba POS ACORDO agregada por mês).
8. Gravar no `post.json` o campo `"formato"` (ex.: `"post único · dado"`, `"carrossel curto · mito+passos"`),
   para o rodízio da semana seguinte.

**Stories**: 1 lâmina (`placar`, `semana`, `acordo`, `story_numero`, `story`). Alternar entre `story_numero` e
`story` nas semanas em que não houver acordo novo.

**Legenda**: 400–900 caracteres (post único pode ter legenda mais curta, 250–500), parágrafos curtos, 3–6 hashtags
(#recuperacaodecredito #cobrancaextrajudicial #inadimplencia #negociacao #mediacao), terminar com "Justo Acordo ·
Mediação extrajudicial entre empresas · justoacordo.com.br".

## Passo a passo
1. Ler a aba PUBLICAÇÕES (último ID no formato JA2026-NNN).
2. Rodar o placar; ver acordos novos extrajudiciais e fotos na pasta ENTRADA.
3. Conferir o rodízio (seção "Variação de formato"), escrever o JSON de cada post e renderizar (`python gerador/render.py post.json saida/`).
4. Converter as artes para JPEG e versionar em `rascunhos/<ID>/01.jpg, 02.jpg...` (com o `post.json`); na coluna ARQUIVOS
   usar `repo:rascunhos/<ID>/01.jpg,repo:rascunhos/<ID>/02.jpg...` e em PRÉVIA o link da pasta no GitHub.
   (Atenção: o repositório é público – rascunhos ficam visíveis antes da aprovação; nunca colocar ali dado de devedor/credor.)
   Cópia opcional no Drive "02 POSTS GERADOS" (1SAJ5nG8yN9r5r2Q9nOmdXLxKU9ma3Kl7 é a pasta do JA2026-001).
5. Acrescentar uma linha por post no fim da aba PUBLICAÇÕES (A–K), sempre com ID JA2026-NNN.
6. Resumo curto para o Jailson: posts, datas, alertas e o placar da semana (com e sem publicação).

## LinkedIn
- Publicar na Página Justo Acordo e depois compartilhar no perfil pessoal do Jailson ("Compartilhar com ideias",
  frase curta dele). Sempre com legenda e hashtags; carrossel como PDF.
