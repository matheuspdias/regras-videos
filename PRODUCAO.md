# Manual da Madrugada — manual de produção diária

Canal de YouTube **Manual da Madrugada**: terror de regras, modelado no canal gringo Lullorin (6,2 mi de views em 16
dias; melhor vídeo "If Your Mom Ever Says Goodnight to You Twice... LOCK YOUR DOOR", 3 mi) e adaptado ao Brasil.
Um vídeo longo por dia, publicado às **20h**. **Não fazemos Shorts.** O Matheus só revisa e agenda: tudo o mais é
produzido aqui.

Este arquivo é a fonte da verdade da automação. Siga na ordem. Não altere episódios já publicados.
O episódio de referência é `episodes/ep01_nome_completo.py`: leia-o inteiro antes de escrever um roteiro novo.

---

## 0. Preparar o ambiente

```bash
pip install --break-system-packages -q pycairo numpy pillow
fc-list | grep -qi poppins || echo "AVISO: fonte Poppins ausente"
git config user.name "Claude"; git config user.email "noreply@anthropic.com"
git pull -q
python3 tools/catalogo.py   # cenários, posições, elenco e poses (os efeitos de terror estão na seção 2 deste arquivo)
```

## 1. Escolher o episódio

- `episodes/agenda.md`: número do próximo episódio e a data de publicação (sempre o dia seguinte à última data da tabela).
- `episodes/temas.md`: pegue o **primeiro tema com status `pendente`**. Use exatamente o título dele.
- ID: `epNN` (ex.: `ep02`). Módulo: `episodes/epNN_<slug>.py`. Pasta: `episodes/epNN/`. `NOITE = NN`.

## 2. Escrever o roteiro (o mais importante)

O formato é um **manual de sobrevivência narrado**: uma voz calma, em "você", explica as regras para escapar de uma
coisa que imita alguém (ou algo) da sua casa. Quase todo o texto é do narrador; a criatura fala poucas vezes, curto.

**Estrutura validada** (vídeo de 3 mi do Lullorin, analisado pela transcrição):

1. **A regra na primeira frase.** O narrador abre lendo a premissa do título e emenda três proibições curtas.
2. **O que conta e o que não conta.** "Eu não tô falando de quando… Eu tô falando disso:" e descreve a cena exata,
   com detalhes sensoriais e cotidianos brasileiros (a hora, o barulho que *não* acontece, onde cada um dorme).
3. **A situação da noite:** quem está em casa, onde estão os adultos (plantão, viagem, turno), o horário na tela.
   Primeiro contato com a coisa (a voz, a palma, o áudio…).
4. **O que é a coisa e como ela age.** O que ela sabe (a casa, a voz) e o que ela *não* sabe (onde você está, quem
   você é). Uma lógica simples e consistente que as regras vão respeitar.
5. **"E pensa bem nisso…"** — gancho que liga à vida real do espectador (uma experiência comum e inofensiva).
6. **Regras numeradas — de 6 a 8.** Cada uma: cartão da regra → o porquê → o que acontece se quebrar → a coisa
   testando a regra. A tensão sobe a cada regra (ela chora, pede ajuda, usa outra voz, sabe algo que não deveria).
7. **O teste final / o amanhecer:** como saber que é a pessoa de verdade (uma senha, uma chave, algo que só ela sabe).
8. **A reviravolta:** "Tem uma coisa que eu ainda não te contei…" — um detalhe que continua depois da noite.
9. **CTA** (última linha): "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos
   comentários: …?" com `fx=[{'cta_mm': (linha1, linha2)}]` (≤ 20 caracteres por linha).

**Regras de texto**
- Segunda pessoa, presente, português falado brasileiro ("tá", "pra"). Frases curtas e médias, ritmo calmo.
- **Tamanho: 1.450 a 1.700 palavras** → vídeo de 9 a 11 min. Confira com `sum(len(l[1].split()) for l in LINES)`.
  O mínimo absoluto é 480 s (anúncio no meio); o ep01 teve 1.211 palavras e deu 8:00 com pausas longas.
- Dê ao protagonista um **nome completo brasileiro** só se a história usar (o espectador é "você").
  Família e casa brasileiras: plantão, turno de fábrica, casa da vó, portão com cadeado, interfone, grupo da família,
  café passado, rede na varanda, cachorro vira-lata.
- **Terror psicológico, não violento.** Nada de sangue, ferimentos detalhados, morte de criança ou animal, suicídio ou
  autolesão. A ameaça é sugerida (olhos, voz, porta, sombra). Personagens reais da família terminam bem.
- **História sempre original.** Do Lullorin vem só a fórmula do título e a estrutura; nunca copie cenas, falas ou
  reviravoltas. Sem pessoas reais, marcas ou políticos.
- Falas da criatura: falante `'coisa'` (voz de quem ela imita, com efeito grave e eco automático; legenda vermelha).
  A pessoa verdadeira usa o próprio id (`'mae'`, `'vo'`, `'pai'`…) sem efeito. Máximo ~10 falas que não sejam do
  narrador por episódio.
- Não use áudio-tags.

**Formato do arquivo** (copie a estrutura de `episodes/ep01_nome_completo.py`):

```python
from engine.dsl import S, C
TITLE = "Se … … NÃO RESPONDA"
NOITE = 2
LEAD = 2.0; GAP_NAR = 0.75; PAUSA_REGRA = 2.0; PAUSA_VOZ = 1.2; TAIL = 20.0
THUMB = dict(ordem='NÃO **RESPONDA**',                 # ordem do título; palavra-chave entre ** fica vermelha
             esquerda=('voce', dict(eyes='wide', mouth='o', arms='face', sweat=True)),
             criatura_porta=True, criatura='coisa',         # a mesma variante que aparece no vídeo
             balao='Lucas Henrique?')                        # balão vermelho (frase curta da coisa) ou None
VOICES = {...}                                          # copie da tabela da seção 3
LINES = [ (falante, texto, S(bg, C(id, slot, None, **pose), cam=dict(...), fx=[...])), ... ]
```

- Toda linha que muda de lugar/plano leva um `S(...)`; linhas sem cena continuam o plano anterior. Varie planos
  (um corte a cada 4–8 s); use `cam=dict(focus='voce', zoom=1.5, to=1.65)` para closes e `cx/cy` para enquadrar portas.
- A legenda gravada (maiúsculas, embaixo), a marca "MANUAL DA MADRUGADA · NOITE NN · REGRA N", o chiado de imagem, a
  música e o "boom" dos cartões são automáticos.

**O monstro tem que aparecer** (pedido do Matheus): o vídeo não pode ficar só em "olhos no escuro". A criatura
aparece de corpo inteiro ou espiando **em 12 a 18 planos** do episódio, em lugares estratégicos, e é o mesmo monstro
da thumbnail. Use `{'olhos': …}` só em 1 ou 2 momentos de suspense (cena preta antes de um susto). Regras de uso:
- **Toda fala da `coisa`** acontece com o monstro em quadro (porta, janela, ao lado da cama, rosto). O balão vermelho
  sai da cabeça dele automaticamente — não use `{'voz': …}` nesses planos.
- **Escalada:** começa longe e escondido (fundo do corredor, fresta da porta, janela) e chega cada vez mais perto
  (na porta do quarto, ao lado da cama, atrás de você, no teto em cima de você). O `rosto` gigante fica reservado para
  2 ou 3 sustos fortes (a frase "ela sabe quem você é", a ameaça mais direta, a reviravolta final com `zoom_punch`).
- **Lugares sinistros:** a porta do seu quarto entreaberta enquanto você "dorme", a janela atrás de você, o fim do
  corredor, pendurado no teto, espiando por cima do pé da cama, atrás do protagonista sem ele perceber.
- Não repita o mesmo modo em mais de 3 planos seguidos.

`fx` do monstro — `{'monstro': modo, 'quem': <variante>, ...}`; comuns: `surge=True` (aparece aos poucos),
`boca='grin'|'flat'` (flat quando finge estar triste/machucado):

| modo | parâmetros | efeito |
| --- | --- | --- |
| `porta` | `rect=(x,y,w,h)` da porta, `lado='esq'\|'dir'`, `abre=0.15..0.5` | porta entreaberta com ela espiando pela fresta |
| `fundo` | `pos=(x, y_pés)`, `s`, `escuro=0..0.85`, `avanca=True` | em pé, longe, no escuro, olhos acesos; `avanca` chega mais perto |
| `atras` | `pos=(x, y_pés)`, `s` | atrás dos personagens do plano, debruçada (desenhada antes deles) |
| `teto` | `pos=(x, y_teto)`, `s` | pendurada de cabeça pra baixo no teto |
| `janela` | `rect=(x,y,w,h)` da janela | o rosto aparecendo na janela |
| `borda` | `pos=(x, y_borda)`, `s` | espiando por cima de uma borda (pé da cama, sofá, balcão) |
| `lateral` | `lado`, `y`, `s` | entrando pela beirada da tela |
| `rosto` | `s≈3.0`, `escuro` | o rosto enorme, colado na câmera (em `'preto'`) |

Portas e janelas dos cenários (use estes `rect`): corredor — portas `(240,280,240,540)`, `(820,280,240,540)`,
`(1400,280,240,540)`; quarto e quarto_vo — porta `(760,260,230,540)`, janela do quarto `(220,160,300,280)`, janela do
quarto_vo `(200,170,280,260)`; cama — janela `(900,120,260,230)`; porta (entrada) — janela lateral `(300,240,260,360)`.
Exemplos prontos: `episodes/ep01_nome_completo.py` e `episodes/ep02_benzer_duas_vezes.py` (procure `monstro`).

**Variantes da criatura** (`quem` no fx, ou o id no `C(...)` para pô-la em cena como personagem): a coisa copia quem
ela imita, sempre alta, com olhos amarelos, sorriso largo e **um** detalhe vermelho.

| id | imita | detalhe vermelho |
| --- | --- | --- |
| `coisa` | mãe (rabo de cavalo) | presilha |
| `coisa_vo` | vó (coque grisalho) | laço no coque |
| `coisa_pai` | pai (camisa social) | gravata |
| `coisa_irmao` | irmão/criança | tênis |
| `coisa_vizinho` | vizinho, porteiro, motorista | boné |
| `coisa_crianca` | criança desconhecida (festa junina, esconde-esconde) | presilha |
| `coisa_sombra` | nada — um vulto escuro e muito alto (mata, folclore, ônibus) | — (só os olhos) |

**Cada episódio tem o SEU monstro** (pedido do Matheus: "capriche nos monstros e nas capas, não deixe tudo igual").
Antes de desenhar, leia `episodes/monstros.md` (o que já foi usado + ideias para a fila). Crie no `CAST` uma variante
própria do episódio (ex.: `coisa_ep03`) combinando os traços disponíveis — a silhueta e o rosto têm que ser diferentes
dos 2 episódios anteriores:
- `olhos`: `'dois'` (padrão), `'quatro'`, `'um'` (ciclope), `'vazios'` (buracos pretos com pontinho amarelo), `'fechados'` (sorrindo de olhos fechados)
- `boca`: `'sorriso'` (padrão, largo demais), `'vertical'` (fenda com dentes), `'costurada'` (pontos vermelhos), `'aberta'` (buraco preto)
- `pescoco`: 0–0,35 (pescoço comprido demais) · `inclina`: 0–0,6 rad (cabeça torta) · `bracos`: 1,6–2,4 (braços compridos)
- `h` (altura, 0,9–1,95), cabelo/roupa de quem ela imita e **um único detalhe vermelho** (presilha, laço, gravata, tênis, boné, costura)
Ao terminar, acrescente a linha do episódio em `episodes/monstros.md` (monstro e composição da capa).

**A capa também muda a cada episódio:** composição diferente das 3 últimas de `episodes/monstros.md`, mostrando a
cena do tema (portão, banheiro, cozinha, TV, garagem…) com o monstro grande e bem visível, o protagonista reagindo e o
balão vermelho. Crie a função da capa em `engine/thumb.py` no padrão de `mm_cama` (cenário do episódio + zoom +
escurecer bordas + ordem no topo) e chame-a por `THUMB['cena']`. Confira a capa nova lado a lado com as 2 anteriores
(`ffmpeg ... hstack`) antes de entregar: se parecer a mesma, refaça.

Precisa de um monstro novo para a história (ex.: imitando a vizinha, um vulto da mata com chapéu)? Crie uma variante
em `CAST` de `engine/chars.py` copiando uma dessas (`face='creature'`, `h` entre 1.3 e 1.9, um único detalhe vermelho)
e confira numa still antes de seguir. Use a mesma variante no `THUMB` com `criatura='<id>'`.

**Outros efeitos** (itens de `fx`):

| efeito | uso |
| --- | --- |
| `{'regra': (n, 'NÃO **RESPONDA**')}` | cartão preto da regra (use no cenário `'preto'`, numa linha curta "Regra número n.") |
| `{'voz': (x, y)}` | balão de onde vem a voz quando ninguém está em quadro (raro: prefira mostrar o monstro) |
| `{'olhos': (x, y), 'surge': True}` | só os olhos amarelos no escuro (1 ou 2 vezes por episódio) |
| `{'cachorro': (x, y, 'abana' \| 'rosna' \| 'parado')}` | cachorro (pés em y≈960 no chão; no quarto, ~(1720, 830)) |
| `{'celular': [('eu', 'texto'), ('ela', 'texto')], 'vermelho': True}` | conversa de celular em tela cheia; `vermelho` marca a última mensagem |
| `{'fechadura': True}` | chave girando na fechadura |
| `{'texto': ['02:40'], 'pos': 'centro', 'cor': '#E5262B'}` | texto solto na tela (horário, placa) |
| `'piscar'`, `'zoom_punch'`, `'shake'` | luz piscando, soco de zoom, tremida |
| `{'cta_mm': ('QUAL REGRA VOCÊ', 'QUEBRARIA PRIMEIRO?')}` | tela final |

**Elenco** (`chars.py`): `voce` (protagonista, moletom), `mae`, `pai` (gravata), `vo` (coque e óculos), `irmao`
(criança), `vizinho` (boné; serve para porteiro e motorista) e as variantes da criatura acima.

**Cenários** (`scenes.py`): quarto, corredor, corredor_luz, quarto_mae, sala, sala_manha, cozinha, porta, preto.
Precisa de um novo (portão/rua, varanda com rede, prédio/interfone, ônibus, mata, festa junina)? Crie em
`engine/scenes.py` com os helpers MM (`mm_room`, `lr`, `door`, `amber`, `moon_window`, `bed`): fundo quase preto, traço
claro fino, uma luz âmbar fraca. Registre em `BG` e `SLOTS` e confira com stills antes de gerar vozes.

**Thumbnail (`THUMB`)** — padrão do Lullorin: só a ordem do título no topo, enorme, branco + palavra-chave vermelha;
protagonista com medo à esquerda; criatura espiando da porta à direita; balão vermelho com uma frase curta da coisa
(o nome, "abre pra mim", "vem cá"). Confira o `thumb.jpg` com Read.
**Não repita a mesma composição de capa em episódios seguidos** (o Matheus pediu): além da porta (`criatura_porta=True`),
existe `cena='cama'` (protagonista fingindo dormir e a criatura debruçada atrás da cama, ver ep02). Se o tema pedir outra
cena (portão, janela, corredor, celular), crie uma função nova em `engine/thumb.py` no mesmo estilo, com a cena do
episódio, a criatura bem visível e o balão vermelho.

## 3. Vozes (HeyGen, pela API)

| falante | voz | voice_id |
| --- | --- | --- |
| nar | MM Narrador | f22a680983644e699676e5b8879923c6 |
| mae (e `coisa` imitando a mãe) | MM Mãe | 914de72ccc244decb2fd1572808fa7e0 |
| vo (e `coisa` imitando a vó) | ESE Vó Cida | 045e4a2e57434943bd3bb5db714aad75 |
| pai, vizinho, porteiro, homens adultos (e `coisa` imitando eles) | Afonso (público) | 9ce5f601f9e04382bb26141d5a3f839d |
| outras mulheres adultas | Lucilene (público) | e808da2329754929803c8bd98dc36857 |
| voce, irmao (e `coisa` imitando eles) | Murilo (público) | d703f08d1ef34302a36945aa3efc7b3f |

Em `VOICES`, o id `'coisa'` recebe o voice_id de quem ela imita naquele episódio.

**O roteiro fica congelado antes de gerar as vozes.** Se precisar mudar falas depois, apague
`episodes/epNN/tts.tsv` e `media/epNN/` e gere tudo de novo — nunca reaproveite índices.

As vozes são geradas pela **API do HeyGen dentro de uma GitHub Action** (`.github/workflows/tts.yml`), paga com o
saldo pré-pago da API (segredo `HEYGEN_API_KEY` do repositório). **Não use as ferramentas do HeyGen desta conversa
(`create_speech_without_player`) para as vozes** — elas gastam a assinatura, que o Matheus vai cancelar. O shell
daqui não acessa o HeyGen; quem gera e baixa é a Action. `VOICES` no episódio usa os voice_ids da tabela acima.

## 4. Gerar e baixar os áudios (GitHub Action `tts`)

```bash
python3 tools/tts_jobs.py episodes.epNN_<slug> epNN        # cria tts_in/epNN_*.json com as falas sem áudio
git add -A && git commit -qm "epNN: roteiro" && git -c push.negotiate=true push -q
sleep 60; for i in $(seq 1 20); do git pull -q; [ ! -e tts_in ] || ! ls tts_in/epNN_* >/dev/null 2>&1 && break; sleep 20; done
ls tts_out 2>/dev/null && cat tts_out/*                        # erros da API, se houver
python3 tools/verify_audio.py episodes.epNN_<slug> epNN        # TEM que dar "ok"
```

A Action gera 4 falas por vez (um episódio leva 1–3 min), salva `media/epNN/audio/NNN.mp3`, preenche
`episodes/epNN/tts.tsv` e apaga o pedido. Se uma fala falhar, o pedido fica em `tts_in/` e o erro em `tts_out/`:
leia o erro; se for temporário, apague `tts_out/`, faça commit e dispare de novo com
`gh api -X POST repos/matheuspdias/regras-videos/actions/workflows/tts.yml/dispatches -f ref=main` (só refaz as que faltam).
Se for falta de saldo ("insufficient"/"balance"/402), pare e avise o Matheus para colocar saldo na API do HeyGen.

## 5. Conferir antes de renderizar

```bash
python3 -m engine.render episodes.epNN_<slug> epNN --shots    # duração total na última linha (meta 540–660 s, mínimo 480)
python3 -m engine.render episodes.epNN_<slug> epNN --stills t1,t2,...   # 16–24 instantes: todos os planos com o monstro + cenas novas
cd build/epNN && ffmpeg -v error -y -pattern_type glob -i 'still_*.png' -vf "scale=480:270,tile=4x5:padding=4" -frames:v 1 sheet.png
```

Abra a `sheet.png` com Read e corrija: personagem cortado ou escondido, legenda cobrindo rosto, cartão de regra com
texto estourando, cenário vazio demais, monstro cortado/escondido demais ou aparecendo pouco (tem que estar em
12 a 18 planos). Se a duração ficar abaixo de 480 s, suba `GAP_NAR`
(máx. 1.0) / `PAUSA_REGRA` (máx. 2.5) ou acrescente falas **antes** de gerar vozes.

## 6. Produzir

Escreva antes `episodes/epNN/youtube.md` no modelo de `episodes/ep01/youtube.md`: título, descrição (gancho de 2–3
parágrafos curtos em "você", a pergunta do CTA, "Se inscreve antes que a luz apague.", "Todas as histórias deste
canal são ficção." e hashtags `#ManualDaMadrugada #Terror #HistóriasDeTerror #RegrasDeTerror #Creepypasta`), tags, e o
bloco "Ao publicar" (agendar 20h).

```bash
tools/produce.sh episodes.epNN_<slug> epNN     # ~10–15 min: render, legenda, thumbnail, pacote em build/epNN/entrega
```

Confira `build/epNN/conferencia.png` (12 quadros do vídeo final) e `build/epNN/thumb.jpg` com Read.

## 7. Entregar

1. Atualize `episodes/temas.md` (status `feito — epNN, DD/MM`) e `episodes/agenda.md`. Commit e push (sem `build/`).
2. Envie com **SendUserFile** os arquivos de `build/epNN/entrega/` (vídeo, thumb, legenda, título/descrição).
3. Mande com **SendUserMessage** um resumo curto: título, data/horário em que deve ser agendado (20h), duração,
   e qualquer coisa que ele deva olhar. Se algo falhou, diga o que e em que passo parou.

Lembretes que vão na mensagem: legenda "Com tempo", "Conteúdo alterado ou sintético: Sim", agendar (não Estreia).
