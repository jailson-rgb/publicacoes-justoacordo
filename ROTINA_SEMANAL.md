# Rotina semanal de criação de posts – Justo Acordo

Executada todo domingo às 17:43 pelo Claude, na tarefa agendada única "MARKETING JASA – Posts da semana" (depois da Advocacia Soares, com resumo único). Não há lembrete de aprovação na segunda.
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

## Conteúdo do Jailson (pasta 01 ENTRADA) – tem prioridade sobre a pesquisa
- O Jailson (ou a Mariana) coloca na pasta **01 ENTRADA** qualquer material: texto, anotação, áudio transcrito,
  print, PDF, foto, ou um simples arquivo .txt / Google Doc com a ideia. Pode ter instruções no nome ou no texto,
  por exemplo: `PRIORIDADE`, `QUINTA`, `POST ÚNICO`, `CARROSSEL`, `MOSAICO`, `NÃO PUBLICAR ANTES DE dd/mm`.
- Toda rodada de domingo:
  1. Listar os arquivos da 01 ENTRADA e descartar os já usados (comparar com o campo `"entrada"` dos post.json em
     `rascunhos/`).
  2. Material novo vira a publicação de **quinta 12:00** (e, se for mais de um, também a de terça, no lugar da
     pesquisa). O que tiver `PRIORIDADE` entra na semana seguinte; o resto entra em ordem de chegada.
  3. Aproveitar o conteúdo no formato que pedir (ou o que o rodízio indicar), reescrevendo na linguagem da marca,
     mas sem mudar o sentido técnico. Na dúvida sobre um ponto técnico, NÃO publicar a dúvida: preencher ALERTA
     com a pergunta para o Jailson.
  4. Gravar no post.json `"entrada": "<nome do arquivo> (<id do Drive>)"` e citar no resumo de domingo qual
     material foi usado e o que ainda está na fila.
  5. Nunca apagar nem mover arquivos da 01 ENTRADA.
- Pedido avulso: o Jailson também pode pedir direto numa conversa; vale este mesmo guia.

## Pilares de conteúdo (temas práticos aprovados pelo Jailson, 15/11/2026)
1. **Placar e resultados** (stories, mosaico, "Números do mês") – regras da seção Números.
2. **O acordo vira título executivo** – o termo de acordo assinado pelo devedor e por 2 testemunhas é título
   executivo extrajudicial (CPC, art. 784, III); homologado em juízo, vira título executivo judicial (CPC, art. 515, III).
   Mensagem prática: se o devedor descumprir, o credor não volta à estaca zero – cobra o título diretamente, sem
   discutir de novo a dívida. Explicar em linguagem de empresário, sem prometer prazo nem resultado.
3. **Garantias** – a Justo Acordo sempre busca uma garantia no acordo: **real** (ex.: hipoteca, alienação fiduciária,
   penhor) ou **pessoal** (ex.: aval, fiança de sócio). Mensagem prática: acordo com garantia tem mais chance de ser
   cumprido e, se não for, há mais por onde receber. Sem revelar como a garantia é negociada nem critérios internos.
4. **Inadimplência no Brasil** (Serasa, Banco Central) – sempre com fonte e mês.
5. **Boas práticas do credor** – documentos que guardar (nota, comprovante de entrega, contrato), não deixar a
   dívida envelhecer, prescrição em termos gerais.
6. **Bastidores e aprendizados** (layout `nota`) – sem caso identificável.
- Cada mês deve passar por pelo menos 3 pilares diferentes; os pilares 2 e 3 entram pelo menos 1 vez por mês cada.

## Vídeos (Reels) – aprovado pelo Jailson em 15/11/2026
Dois tipos, ambos publicados automaticamente (TIPO "Reels" com o MP4 em ARQUIVOS, ex.: `repo:rascunhos/<ID>/video.mp4`).
Reels SEM MP4 em ARQUIVOS (trend com áudio da biblioteca do Instagram) continuam "Manual" (Jailson publica pelo app).

1. **Vídeo só animado** – modelos em `gerador/video/` (ex.: `modelo-placar.html`, placar com contador rolando).
   `python gerador/video/animar.py gerador/video/<modelo>.html rascunhos/<ID>/video.mp4 10`
   Variações: placar, "cobrança extrajudicial x judicial", "como funciona" (jornada), título executivo,
   garantias. Criar modelo novo copiando a estrutura (CSS @keyframes + animation-delay, elemento #r 1080x1920),
   sempre com a identidade da Justo Acordo. Duração 10 a 30 s; o último quadro tem a informação completa
   (vira a capa automaticamente).
2. **Vídeo do Jailson falando + intervenções ilustrativas** – ele grava (celular na vertical) e coloca o vídeo na
   pasta 01 ENTRADA. A rotina:
   - pode ser pedido avulso (vídeo mandado no chat): fazer na hora, sem esperar o domingo; objetivo: deixar DIDÁTICO;
   - transcrição com tempos: o ambiente do Claude não baixa modelos de voz – usar a transcrição automática do Drive
     (vídeo na 01 ENTRADA, read_file_content), a legenda exportada do celular/CapCut ou o roteiro/tópicos do Jailson;
     sem nenhuma delas, pedir os tópicos e momentos-chave antes de montar;
   - CORTES (pedido do Jailson, 16/11/2026: vídeo fluido): antes das ilustrações,
     `python gerador/video/cortar.py bruto.mp4 cortado.mp4 [--cortar "0:42-0:45,..."]` – pausas longas saem
     sozinhas (fica ~0,25 s de respiro); gaguejos, repetições e frases recomeçadas vão em --cortar (pela transcrição
     com tempos ou pelos trechos que o Jailson indicar). O cortado.txt lista o que saiu e vai junto na aprovação.
     Na dúvida, não cortar conteúdo; os tempos das ilustrações são marcados no vídeo JÁ cortado;
   - marca os momentos-chave e escolhe a ilustração de cada um (lei citada → cartão grifado; comparação → cartões;
     etapas → passos; número agregado/fonte → número animado; ideias → palavras-chave) + legendas da fala;
   - copia `gerador/video/modelo-sobreposicao.html` para `rascunhos/<ID>/`, troca os textos (nome, número em
     destaque, palavras-chave) e ajusta os tempos (animation-delay) às falas; gráficos só no terço de cima
     (y 220–760) e no de baixo (y 1320–1760), para não cobrir o rosto;
   - `python gerador/video/animar.py rascunhos/<ID>/modelo.html rascunhos/<ID>/video.mp4 --sobre <video do Jailson já cortado>`
     (o áudio é o dele; o encerramento entra sozinho nos 3 s finais);
   - vídeo bruto do Jailson NUNCA vai para o GitHub sem passar pela aprovação: só o MP4 final em `rascunhos/`.
     Vídeos acima de 90 s ou de 100 MB: avisar no resumo (cortar ou publicar manualmente).
- **Áudio (decisão do Jailson, 15/11/2026)**: todo vídeo leva trilha instrumental alinhada à persona da marca
  (segura, amigável, confiante, cordial). Usar as trilhas PRÓPRIAS em `gerador/video/trilhas/` (sintetizadas por
  `gerar_trilhas.py`, sem obra de terceiros – livres de direitos), com `--trilha <nome>`:
  - `confianca` – placar, resultados, acordo fechado (padrão);
  - `conquista` – marcos, mosaico, "Números do mês";
  - `reflexao` – educativo (título executivo, garantias, inadimplência);
  - `dialogo` – fundo do vídeo do Jailson falando (entra a 15%, sob a voz).
  Alternar para não repetir a mesma trilha em vídeos seguidos; registrar no post.json `"trilha"`. Nunca usar
  música baixada da internet nem da biblioteca do Instagram/YouTube. Novas trilhas: acrescentar em
  `gerar_trilhas.py` (outra progressão/andamento) mantendo a persona.
- **Frequência**: 1 vídeo a cada 15 dias no rodízio (conta como publicação de feed da semana); vídeo do Jailson
  entra assim que chegar na ENTRADA, com prioridade.
- **LinkedIn**: vídeos NÃO vão para o LinkedIn (decisão do Jailson, 16/11/2026). Ver seção LinkedIn.
- Legenda e regras de conteúdo iguais às dos outros posts (terminar com pergunta quando couber).

## Selo e argumento
- "Cobrança extrajudicial **100% no êxito**: só recebemos quando o devedor paga." – vale só para a cobrança
  extrajudicial (o RVP/pré-processo é cobrado à parte; não generalizar).

## Fontes para os carrosséis (quando não houver material na 01 ENTRADA)
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
  `checklist`, `passos`, `pergunta`, `barras`, `resultado`, `nota`;
- largos (cortados em várias imagens): `mosaico` (3 posts na grade) e `jornada` (carrossel panorâmico).
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


**Formatos novos (aprovados em 16/11/2026; catálogo no Drive: JUSTO ACORDO > IDENTIDADE VISUAL - SITE >
"Formatos de posts – aprovados 16-11-2026"; exemplos em gerador/exemplos/exemplo-novos-16-11.json)** – os mesmos
desenhos da Advocacia Soares, na identidade da Justo Acordo:
- `foto` (equipe/bastidor + frase), `foto_fundo` (QUALQUER foto do Jailson em tela cheia com logo, @justo.acordo,
  site e selo 100% no êxito nos cantos; legenda opcional), `lei` ("na lei": regra + "o que significa para o credor"),
  `dicionario` (Dicionário do crédito, numerado), `serie` (quadro fixo, ex.: "Os 3 caminhos do credor").
- Estruturas: `split`, `palavra`, `linha_tempo`, `grade` (2x2), `marcatexto`, `fluxo`, `moldura`, `ranking`.
- Fotos: só as que o Jailson/Mariana mandarem para a 01 ENTRADA; nunca termo, documento, cliente ou devedor (o termo
  continua só no story "acordo fechado", sempre desfocado). Post de foto a cada 15 dias, só quando houver foto nova.

### Formatos de tendência (pedido do Jailson, 15/11/2026)
- **Mosaico na grade (3 posts = 1 imagem)** – layout largo `mosaico` (`gerador/exemplos/exemplo-mosaico.json`).
  Uso: no máximo **1 vez por mês**, para um marco forte (placar acumulado redondo, resultado do mês, campanha).
  - O renderizador gera 01 (esquerda), 02 (meio) e 03 (direita), já com a margem que a grade 3:4 do perfil corta.
  - Na planilha: **3 linhas** "Post único", IDs seguidos, DESTINO **"Instagram"** (mosaico não faz sentido na Página
    do Facebook), mesmo dia, publicando **03 primeiro**, depois 02 e por último 01, com 1 minuto de diferença
    (ex.: 12:00 = imagem 03, 12:01 = 02, 12:02 = 01). O publicador segue a ordem de data/hora.
  - Na semana do mosaico, ele substitui a publicação de feed daquele dia; legendas curtas e complementares
    (cada post também precisa funcionar sozinho no feed). Avisar no resumo que os 3 precisam ser aprovados juntos.
  - Só fica alinhado enquanto o número de posts de feed seguintes for múltiplo de 3; não tentar "manter" o mosaico.
- **Carrossel panorâmico contínuo** – layout largo `jornada` (`gerador/exemplos/exemplo-jornada.json`): uma linha
  atravessa as lâminas ao deslizar. Bom para processos e "caminho do crédito". Conta como carrossel longo no rodízio.
- **Post estilo nota** – layout `nota` (post único com cara de anotação). Bom para aprendizados e bastidores
  ("O que aprendemos em 210 acordos"), sempre sem caso identificável.
- Posts com **pergunta** na legenda geram mais comentários: terminar ao menos 1 legenda por semana com uma pergunta
  ao empresário.
- Peças largas usam `"largo"` no JSON em vez de `"laminas"` (ver o cabeçalho de `gerador/render.py`).

**Stories**: 1 lâmina (`placar`, `semana`, `acordo`, `story_numero`, `story`). Alternar entre `story_numero` e
`story` nas semanas em que não houver acordo novo.

**Legenda**: 400–900 caracteres (post único pode ter legenda mais curta, 250–500), parágrafos curtos, 3–6 hashtags
(#recuperacaodecredito #cobrancaextrajudicial #inadimplencia #negociacao #mediacao), terminar com "Justo Acordo ·
Mediação extrajudicial entre empresas · justoacordo.com.br".

## Intercalar com a Advocacia Soares (regra do Jailson, 16/11/2026)
As duas marcas usam os MESMOS desenhos (cada uma na sua identidade). Para os perfis não parecerem iguais:
1. Antes de escolher os layouts da semana, ver os da outra marca: as publicações da semana que está sendo criada
   (na rodada única de domingo a Soares é feita primeiro) e as das 2 semanas anteriores – campo "formato"/layouts dos
   post.json (Soares: `<ID>-post.json` na pasta 02 POSTS GERADOS da Soares; Justo Acordo: `rascunhos/<ID>/post.json`
   do repositório publicacoes-justoacordo) e a coluna TIPO da aba PUBLICAÇÕES.
2. No MESMO DIA, as duas marcas nunca publicam o mesmo layout principal nem o mesmo formato (ex.: se a Soares sai com
   carrossel `passos` na terça, a Justo Acordo sai com post único ou outro layout).
3. Na MESMA SEMANA, não repetir entre as marcas a mesma "receita" (formato + layout principal); mosaico, panorâmico e
   post de foto: no máximo uma das marcas por semana.
4. Gravar o "formato" no post.json (como já é feito) para a outra marca conseguir conferir.

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

## LinkedIn (decisão do Jailson, 16/11/2026: só mini artigos)
- O LinkedIn da Justo Acordo recebe SOMENTE **mini artigos** em texto – rede mais profissional. Nada de vídeo/Reels,
  stories, placar animado nem carrossel de Instagram.
- Toda rodada de domingo: escrever **1 mini artigo por semana**, a partir do pilar mais "de gestor" da semana
  (título executivo, garantias, inadimplência com dados, boas práticas do credor, aprendizados).
  - 1.300 a 2.000 caracteres; título forte na 1ª linha; parágrafos de 1 a 3 frases; linguagem de diretor
    financeiro/empresário; 1 ideia central + 1 exemplo prático genérico (sem caso identificável); fecho com pergunta
    ao leitor; 3 a 5 hashtags; assinatura "Justo Acordo · Mediação extrajudicial entre empresas · justoacordo.com.br".
  - Mesmas regras de conteúdo do Instagram (sem escritório/OAB, sem percentual de honorários, sem método/know-how,
    números só agregados e com fonte).
- O mini artigo NÃO entra na aba PUBLICAÇÕES (o publicador automático não posta no LinkedIn). Salvar em
  `linkedin/AAAA-MM-DD.md` (data da segunda-feira da semana) e colar o texto completo no resumo de domingo, pronto
  para o Jailson publicar na Página Justo Acordo e compartilhar no perfil pessoal ("Compartilhar com ideias", frase
  curta dele). Sugerir o melhor dia: terça ou quarta, entre 8h e 10h.
