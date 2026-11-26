# Experimentos — Manual da Madrugada

Cada rodada de analytics avalia os testes abertos e decide: **manter** (vira regra), **reverter** ou **continuar**
(dado insuficiente). Um teste por variável por vídeo; espere 3+ dias e 500+ impressões novas antes de decidir.
Títulos/thumbs de vídeos publicados são trocados por um pedido em `ajustes/*.json` (Action `atualizar`).

| # | Início | Teste | Hipótese | Base (antes) | Como medir | Status |
|---|---|---|---|---|---|---|
| E1 | 25/11 | primeiro contato com a coisa até 0:50: depois de "Eu tô falando disso.", no máximo 3 frases de ambientação, só com detalhes que a regra usa (quem tem a chave, onde cada um dorme); o resto da ambientação vem depois do primeiro contato. Vale a partir do ep09 | a maior perda depois dos 25 s é a ambientação genérica: ep01 caiu de 85% para 59% entre 0:24 e 0:38 ("Sua mãe é enfermeira…") e o ep02 de 77% para 48% entre 0:31 e 1:14 ("É julho… De dia é tudo bom…"). O ep03, cuja ambientação era só sobre a chave do pai, perdeu 8 pontos | ep01–ep03: 1º contato entre 0:49 e 1:24; ret. 60 s 54–61% | ret. aos 60 s e 90 s e % assistido de ep09–ep10 vs ep01–ep08 | aberto |
| E2 | 26/11 | pedido de inscrição de 1 frase logo depois da regra 3, a partir do ep09 (só o CTA final antes) | o canal tem 0 inscritos em 206 views, mas ~35–45% ainda assiste aos 3–4 min; pedir ali, com o público engajado, rende inscrito sem custo de retenção | ep01–ep08: 0 inscritos; queda na curva no trecho do pedido = a medir | inscritos por 1.000 views de ep09–ep10 vs ep01–ep08; queda da retenção nos 15 s do pedido (não pode passar de 3 pontos) | aberto (aprovado pelo Matheus em 26/11) |
