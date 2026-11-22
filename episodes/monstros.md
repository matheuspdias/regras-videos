# Monstros e capas já usados — Manual da Madrugada

Leia ANTES de desenhar o monstro e a capa de um episódio novo. Cada episódio precisa de um monstro com
**silhueta/rosto diferentes dos 2 últimos** e uma **capa com composição diferente das 3 últimas**. Acrescente a linha do
episódio ao terminar.

| Ep | Monstro (id no CAST e traços) | Capa (composição) |
|---|---|---|
| 01 | `coisa` — imita a mãe: rabo de cavalo, presilha vermelha, 2 olhos, sorriso largo | Porta entreaberta à direita com a criatura espiando + protagonista em pânico à esquerda + balão "Lucas Henrique?" |
| 02 | `coisa_vo` — imita a vó: coque grisalho, laço vermelho, 2 olhos, sorriso largo | Cama: protagonista deitado fingindo dormir + criatura debruçada atrás da cama, mão na cabeça dele + balão "Tá dormindo?" |
| 03 | `coisa_ep03` — imita o pai: camisa social, gravata vermelha, `pescoco=0.3` (espia por cima do muro), `olhos='vazios'`, `bracos=2.1`, `inclina=0.12`, h=1.6 | Portão (`mm_portao`): de dentro de casa, protagonista com medo à esquerda na frente da cortina; lá fora, a criatura atrás da grade do portão com os braços para cima (batendo palma) + balão "Abre, filho." |
| 04 | `coisa_ep04` — imita a irmã (Duda) de camisola: cabelo molhado `hair='mecha'` cobrindo metade do rosto (só um olho aparece), `boca='vertical'`, `inclina=0.38`, `bracos=2.25`, h=1.55; detalhe vermelho: a xuxinha que a irmã perdeu no ralo (`xuxinha_red`) | Banheiro (`mm_banheiro`): box de vidro embaçado à direita com a criatura de pé lá dentro, rosto numa faixa limpa do vapor e marcas de mão no vidro + protagonista apavorado à esquerda + balão "Canta comigo?" |
| 05 | `coisa_ep05` — imita o irmão (Bento, 7 anos) de pijama, mas alto demais (h=1.5): `olhos='fechados'` (sorri de olhos fechados; só abre na virada final, variante `coisa_ep05_olhos`), `inclina=0.5`, `bracos=2.3`, `pescoco=0.1`; detalhe vermelho: touca de tricô com pompom que a vó fez (`hair='touca'`). Olhos fechados não acendem no escuro | Atrás de você (`mm_atras`): no corredor com o guarda-roupa da vó ao fundo, protagonista paralisado de frente pra câmera e a criatura enorme debruçada por cima do ombro dele, mão no ombro + balão "Tatuzinho?" |

## Ideias de monstro para a fila (sugestão; adapte ao roteiro)

| Tema | Monstro sugerido |
|---|---|
| 03 pai bate palma no portão | `coisa_pai` com `pescoco=0.3` (aparece por cima do muro), `olhos='vazios'` |
| 04 irmã cantando no banheiro | imita a irmã: cabelo comprido cobrindo metade do rosto, `boca='vertical'`, vista pelo vapor do box |
| 05 irmão com o apelido da vó | `coisa_irmao` com `inclina=0.5` (cabeça torta), `olhos='fechados'` sorrindo |
| 06 cachorro rosna pro pai | `coisa_pai` alto demais (`h=1.9`), `olhos='quatro'`, curvado pra passar na porta |
| 07 vó varrendo às 3h | `coisa_vo` com `bracos=2.3` segurando a vassoura, `boca='costurada'` |
| 08 cheiro de café | imita a mãe de avental, `olhos='um'`, de costas no fogão (vire o rosto só no susto) |
| 09 irmã pede pra dormir no seu quarto | duas irmãs iguais; a falsa com `olhos='vazios'` e `boca='aberta'` |
| 10 tio sem convite | tio de chapéu e camisa social, `pescoco=0.2`, sorriso largo demais, mala na mão |
| 11 pai volta duas vezes | dois pais lado a lado; o falso com `inclina=0.35` e `olhos='quatro'` |
| 12 alguém embaixo da cama | criatura magra deitada (`lie=True`), só braços compridos e olhos debaixo da cama |
| 13 pai vendo TV sem som | `coisa_pai` iluminado pela TV (chiado), `boca='aberta'` rindo sem som |
| 14 rádio da vó | vulto `coisa_sombra` com `olhos='um'` atrás do rádio, voz vindo do rádio |
| 15 pai lavando o carro | `coisa_pai` com `bracos=2.3` e balde, `olhos='fechados'` |
