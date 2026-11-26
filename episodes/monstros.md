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
| 06 | `coisa_ep06` — imita o pai de uniforme da fábrica, alto demais (h=1.9, curva as costas pra caber debaixo da luz da varanda): `olhos='quatro'` (acendem os quatro no escuro), sorriso largo, `bracos=2.05`, `inclina=0.2`, `pescoco=0.06`; detalhe vermelho: capacete de segurança (`hair='capacete'`; o do pai de verdade é branco). Nunca entra: aparece só do lado de fora (varanda, janelas, olho mágico) | Olho mágico (`mm_olho`): lente redonda enorme à direita com a criatura curvada colada nela, lá fora, sob a luz amarela da varanda; protagonista apavorado à esquerda e o cachorro em primeiro plano rosnando pra porta + balão "Sou eu, filho." |
| 07 | `coisa_ep07` — imita a vó (Vó Zilda) de vestido e coque grisalho, mas alta e magra demais (h=1.75): `olhos='vazios'` com a pupila acesa maior (`pupila=2.4`; não enxerga, acha as coisas varrendo), `boca='costurada'` com linha vermelha (o único vermelho), `pescoco=0.16`, `inclina=0.16`, `bracos=2.4`; sempre com a vassoura de palha na mão (`vassoura=True`, a palha balança no vídeo) | Vassoura (`mm_vassoura`): quartinho de costura da casa da vó, protagonista encolhido em cima da cama de ferro à esquerda, chinelo no chão; a criatura enorme e curvada à direita varrendo pra baixo da cama + balão "Levanta o pé, fio." |
| 08 | `coisa_ep08` — imita a mãe (padeira) de vestido, alta demais (h=1.72): `olhos='um'` (um olho só no meio da testa), `boca='aberta'` (buraco preto), `inclina=0.3`, `bracos=2.2`, `pescoco=0.1`; sempre com o bule de ágata branco na mão (`segura='bule'`); detalhe vermelho: o avental (`avental='#D3242A'`). Não sai da cozinha enquanto o café tá quente | Café (`mm_cafe`): cozinha acesa de madrugada com a mesa posta e três xícaras fumegando em primeiro plano; a criatura curvada atrás da mesa, debaixo da lâmpada, servindo com o bule; protagonista apavorado espiando da porta escura do corredor à esquerda + balão "Vem tomar café, filho." |
| 09 | `coisa_ep09` — imita a irmã mais nova (Larinha, 8 anos) de pijama e maria-chiquinha, mas alta e magra demais (h=1.62): `olhos='dois'` grandes, sorriso largo demais, `pescoco=0.24`, `inclina=0.44`, `bracos=2.35`; sempre abraçada no travesseiro de fronha vermelha (`segura='travesseiro'`, o único vermelho). Não entra em quarto nenhum sem convite; aparece no corredor, na janela, no teto e saindo do quarto vazio | Parede em corte (`mm_parede`): a casa cortada pela parede da sua porta trancada; à esquerda, o seu quarto escuro com o protagonista apavorado na cama, a porta com o trinco fechado e a sombra de dois pés na fresta; à direita, no corredor iluminado de âmbar, a criatura curvada encostada na porta, batendo com o travesseiro vermelho + balão "Deixa eu entrar, mano?" |

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
| 16 cadeira de balanço do avô | imita o avô de suspensório e chapéu de palha, sentado e magro demais (`h=1.8` quando levanta), `pescoco=0.25`, `olhos='fechados'` balançando; detalhe vermelho: lenço no pescoço |
| 17 mãe no espelho | duas mães: a do reflexo com `inclina=0.4` e `boca='vertical'`, escova na mão (`segura='escova'`); a de verdade de costas; detalhe vermelho: a escova |
| 18 pai chama pra pescar | `coisa_pai` de capa de chuva amarela e lanterna, `bracos=2.4`, `olhos='um'`, molhado; aparece na margem do rio na neblina; detalhe vermelho: a boia de pesca |

