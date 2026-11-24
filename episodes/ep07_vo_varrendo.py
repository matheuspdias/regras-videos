"""Manual da Madrugada — Noite 07
Se a sua vó estiver varrendo a casa às 3 da manhã… NÃO DEIXE ELA VARRER O SEU PÉ
"""
from engine.dsl import S, C

TITLE = "Se a sua vó estiver varrendo a casa às 3 da manhã… NÃO DEIXE ELA VARRER O SEU PÉ"
NOITE = 7
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='NÃO DEIXE **VARRER**', cena='vassoura', criatura='coisa_ep07', balao='Levanta o pé, fio.')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '045e4a2e57434943bd3bb5db714aad75',  # ESE Vó Cida (imitando a vó, com efeito)
    'vo': '045e4a2e57434943bd3bb5db714aad75',     # ESE Vó Cida (a vó de verdade, limpa)
}

# a coisa desta noite: imita a vó (coque grisalho, vestido), mas alta e magra demais, pescoço comprido, cabeça torta,
# olhos vazios (não enxerga: acha as coisas varrendo), braços compridos e a boca costurada com linha vermelha.
# Está sempre com a vassoura de palha na mão.
Q = 'coisa_ep07'
PORTA_QUARTO = {'monstro': 'porta', 'quem': Q, 'rect': (760, 260, 230, 540), 'lado': 'esq', 'abre': 0.4}
PE_DA_CAMA = {'monstro': 'borda', 'quem': Q, 'pos': (1790, 765), 's': 0.62}             # espiando por cima do pé da cama
NO_QUARTO = {'monstro': 'fundo', 'quem': Q, 'pos': (1130, 980), 's': 0.62, 'escuro': 0.35}  # em pé do lado da cama, varrendo
CORREDOR_LONGE = {'monstro': 'fundo', 'quem': Q, 'pos': (1180, 830), 's': 0.42, 'escuro': 0.75}
NA_COZINHA = {'monstro': 'fundo', 'quem': Q, 'pos': (1450, 840), 's': 0.5, 'escuro': 0.45}   # na porta dos fundos aberta


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


def deitado(**p):
    d = dict(lie=True, eyes='closed', mouth='flat')
    d.update(p)
    return C('voce', 'deitado', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se a sua vó estiver varrendo a casa às três da manhã, não deixe ela varrer o seu pé. Não ponha o pé no chão. Não dê licença. E, aconteça o que acontecer, não segure a vassoura pra ela.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(PORTA_QUARTO, surge=True)])),
    ('nar', "Eu não tô falando de quando ela varre a cozinha depois do almoço e manda você tirar o pé do caminho.",
     S('cozinha_vo_manha', C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='o', eyes='angry'), C('voce', 'a', None, mouth='smile', eyes='half'))),
    ('nar', "Também não tô falando de quando ela acorda antes do galo pra varrer o terreiro, com o radinho tocando moda de viola.",
     S('terreiro_manha', C('vo', 'b', None, facing=1, arms='hold', prop='vassoura', mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "Você tá passando as férias de julho na casa da sua vó, no interior de Minas. Casa antiga, de chão de cimento vermelho encerado, que brilha de tão limpo.",
     S('cozinha_vo_manha', C('vo', 'b', None, facing=-1, mouth='smile', arms='hold', prop='caneca'), C('voce', 'a', None, mouth='grin', arms='wave'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "A Vó Zilda varre essa casa todo santo dia. Sempre de dentro pra fora. Dos quartos até a cozinha, e da cozinha pro terreiro. Ela diz que é pra tirar o que não presta.",
     S('terreiro_manha', C('vo', 'a', None, facing=1, arms='hold', prop='vassoura', mouth='flat', eyes='half'), cam=dict(zoom=1.1, to=1.2, cx=700, cy=640))),
    ('nar', "E toda vez que a vassoura chega perto de você, ela avisa, rindo:",
     S('cozinha_vo_manha', C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='grin', eyes='happy'), C('voce', 'a', None, mouth='o', eyes='wide'), cam=dict(zoom=1.2, to=1.3, cx=820, cy=640))),
    ('vo', "Sai da frente, menino, senão eu varro o seu pé e você não casa nunca!",
     S('cozinha_vo_manha', C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='grin', eyes='happy'), C('voce', 'a', None, mouth='grin', arms='up'), cam=dict(focus='vo', zoom=1.5, to=1.6))),
    ('nar', "Ela dorme cedo. Às nove, já tá roncando no quarto do fundo, com o radinho de pilha chiando baixinho do lado do travesseiro.",
     S('corredor_vo', cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Você dorme no quartinho de costura, numa cama de ferro alta, do lado da máquina de pedal. O seu chinelo fica no chão, do lado da cama.",
     S('quarto_costura', quarto(eyes='half', mouth='smile'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "São três horas da manhã.",
     S('preto', fx=[{'texto': ['03:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você acorda com um barulho que conhece. Chhh. Chhh. Chhh. Uma vassoura de palha raspando no cimento. Devagar. Lá do fundo do corredor.",
     S('corredor_vo', cam=dict(zoom=1.05, to=1.2, cx=1100, cy=600), fx=['piscar'])),
    ('nar', "Pela fresta debaixo da porta, nenhuma luz. Quem tá varrendo, tá varrendo no escuro.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.3, to=1.45, cx=875, cy=640))),
    ('nar', "E aí a vassoura para. E a voz da sua vó pergunta, lá do corredor:"),
    ('coisa', "Tá acordado, fio? A vó só vai dar uma varridinha.",
     S('corredor_vo', cam=dict(zoom=1.2, to=1.35, cx=1100, cy=560), fx=[dict(CORREDOR_LONGE, avanca=True, escuro=0.5), 'zoom_punch'])),
    ('nar', "A sua vó não varre de noite. Nunca. Ela diz que varrer depois que escurece espanta a sorte da casa. E, atravessando a parede, do quarto do fundo, ainda dá pra ouvir o ronco dela. E o chiado do radinho.",
     S('quarto_costura', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá no corredor mora nas casas onde alguém varre todo dia. Ela aprendeu o jeito da sua vó. O passo arrastado. O chinelo de dedo. A voz.",
     S('corredor_vo', cam=dict(zoom=1.15, to=1.3, cx=1100, cy=560))),
    ('nar', "Ela não varre poeira. Ela varre o que não é da casa.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.6, 'surge': True}])),
    ('nar', "A sua vó é da casa. A máquina de costura é da casa. O pé de arruda no terreiro é da casa. Você, não. Você chegou faz uma semana, com uma mochila e um par de chinelos.",
     S('quarto_costura', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.1, to=1.2, cx=1300, cy=640))),
    ('nar', "E tudo que a vassoura dela encosta, ela leva pra fora. Pela porta da cozinha. Pro sereno. E fecha a porta.",
     S('cozinha_vo_aberta', cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Mas ela não enxerga. Aqueles dois buracos no rosto dela não servem pra olhar. Ela acha as coisas do mesmo jeito que você acha um grão de arroz caído no chão. Varrendo. Até a palha encostar.",
     S('cozinha_vo_aberta', cam=dict(zoom=1.3, to=1.5, cx=1450, cy=520), fx=[dict(NA_COZINHA, surge=True)])),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe quando alguém varre o seu pé sem querer, e todo mundo grita que agora você não casa mais? Todo mundo ri. Você ri também.",
     S('cozinha_vo_manha', C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='grin', eyes='happy'), C('voce', 'a', None, mouth='grin', eyes='happy'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Ninguém lembra de onde veio essa história. Talvez ela nunca tenha sido sobre casamento. Talvez ela seja sobre quem fica dentro de casa. E quem é varrido pra fora.",
     S('terreiro', cam=dict(zoom=1.0, to=1.12))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'TIRE O PÉ DO **CHÃO**')}])),
    ('nar', "Tire o pé do chão. Agora. Puxa as pernas pra cima da cama e encolhe. Nada pendurado pra fora. Nem pé, nem mão, nem a ponta do lençol.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "A vassoura só conhece o chão. O que tá em cima da cama, pra ela, não existe. Ela pode passar a palha a um palmo do seu calcanhar e não vai saber que você tá ali.",
     S('quarto_costura', quarto(eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.15, to=1.25, cx=1300, cy=700))),
    ('nar', "Ela vai entrar no quarto. Você vai ouvir a porta abrindo devagar. A palha correndo debaixo da cama, batendo no pé de ferro. Tec. Tec.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.1), fx=[dict(PORTA_QUARTO, abre=0.6, surge=True)])),
    ('coisa', "Levanta o pezinho, fio. Deixa a vó varrer debaixo da cama.",
     S('quarto_costura', quarto(eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.15, to=1.3, cx=1250, cy=600), fx=[dict(NO_QUARTO, s=0.7, surge=True)])),
    ('nar', "Não levanta nada. O seu pé já tá em cima. Se você mexer, a cama de ferro range. E rangido, pra ela, é a mesma coisa que dizer: tem alguém aqui.",
     S('quarto_costura', quarto(eyes='half', mouth='flat', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.7))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO DÊ **LICENÇA**')}])),
    ('nar', "Quando ela não achar nada no chão, ela vai pedir licença. Bem educada. Do jeitinho que a sua vó pede quando vai passar com a panela quente.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('coisa', "Dá licença, fio? Deixa a vó passar.",
     S('quarto_costura', quarto(eyes='closed', mouth='flat', sweat=True), cam=dict(zoom=1.3, to=1.45, cx=1600, cy=560), fx=[dict(PE_DA_CAMA, surge=True), 'zoom_punch'])),
    ('nar', "Não responde. Nem pode passar, nem fica à vontade, nem com licença. Licença é convite. Se você der licença, ela não precisa mais da vassoura pra te achar. Ela já sabe de onde veio a voz.",
     S('quarto_costura', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Fica quieto até a palha voltar a raspar o chão. Chhh. Chhh. Se afastando, de volta pro corredor.",
     S('corredor_vo', cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'DEIXE O **CHINELO**')}])),
    ('nar', "O seu chinelo tá no chão, do lado da cama. Não pega ele de volta. Deixa ele lá.",
     S('quarto_costura', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.6, to=1.75, cx=1260, cy=800))),
    ('nar', "Ele tem o seu cheiro. O suor do seu pé, a terra do quintal. Quando a vassoura bater nele, ela vai achar que encontrou você.",
     S('quarto_costura', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Você vai ouvir o chinelo sendo arrastado pelo corredor. Até a cozinha. Depois a porta dos fundos abrindo, o vento frio entrando por baixo da sua porta. E a porta fechando.",
     S('cozinha_vo_aberta', cam=dict(zoom=1.1, to=1.25, cx=1350, cy=600), fx=[dict(NA_COZINHA, s=0.46, escuro=0.6)])),
    ('nar', "Por um tempo, a casa fica quieta. Ela acha que já terminou. Aproveita. Respira. Mas não dorme.",
     S('quarto_costura_vazio', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.08))),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO SEGURE A **PORTA**')}])),
    ('nar', "Lá pelas quatro, a vassoura volta. Mais rápida. Ela percebeu que chinelo não respira.",
     S('corredor_vo', cam=dict(zoom=1.0, to=1.15), fx=[{'monstro': 'teto', 'quem': Q, 'pos': (640, 0), 's': 0.5, 'surge': True}, {'texto': ['04:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Fio, vem cá segurar a porta da cozinha pra vó. O vento tá batendo e a vó não dá conta.",
     S('cozinha_vo_aberta', cam=dict(zoom=1.25, to=1.4, cx=1450, cy=520), fx=[dict(NA_COZINHA, s=0.55, escuro=0.3, boca='flat')])),
    ('nar', "Não vai. Pra segurar a porta, você tem que ficar em pé na soleira. Com um pé dentro e outro fora. E basta uma vassourada pra você ficar do lado de fora.",
     S('quarto_costura_vazio', quarto(eyes='angry', mouth='flat'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "E do lado de fora, no sereno, não tem chão encerado. Não tem casa. Não tem vó. Só tem o terreiro escuro, e tudo que ela já varreu antes de você.",
     S('terreiro', cam=dict(zoom=1.0, to=1.15, cx=1000, cy=560), fx=[{'olhos': (1060, 600), 'surge': True}])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'NÃO PEGUE A **VASSOURA**')}])),
    ('nar', "Quando nada funcionar, ela vai ficar cansada. Ou vai fingir.",
     S('quarto_costura_vazio', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.12))),
    ('coisa', "Ai, minhas costas, fio. A vó não aguenta mais. Pega a vassoura e termina pra mim. Só o corredor.",
     S('quarto_costura_vazio', cam=dict(zoom=1.1, to=1.25, cx=875, cy=580), fx=[dict(PORTA_QUARTO, abre=0.3, boca='flat', s=0.5)])),
    ('nar', "Esse é o pior momento da noite. Porque é a voz da sua vó, cansada, com dor. E você ama a sua vó. Tudo em você vai querer levantar e ajudar.",
     S('quarto_costura_vazio', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Lembra: a sua vó não deixa ninguém pegar a vassoura dela. Nem a sua mãe. Ela diz que vassoura é que nem escova de dente. Cada um tem a sua.",
     S('cozinha_vo', cam=dict(zoom=1.3, to=1.45, cx=1600, cy=640))),
    ('nar', "E quem pega a vassoura dela às três da manhã não termina o corredor. Termina a casa. E depois a próxima. E a próxima. Pra sempre. Varrendo no escuro, procurando alguém que não é da casa.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.1, 'escuro': 0.3}, 'zoom_punch'])),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'SE COBRE COM O **FUXICO**')}])),
    ('nar', "Quando ela desistir do chão, ela vai tentar a cama. Você vai sentir a palha encostando no colchão. Raspando o lençol. Subindo devagar, do pé da cama até o seu travesseiro.",
     S('cama_escuro', deitado(eyes='wide'), cam=dict(zoom=1.0, to=1.1), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (1500, 900), 's': 0.62, 'escuro': 0.55, 'surge': True}])),
    ('nar', "Puxa a colcha de fuxico que tá dobrada no pé da cama e se cobre inteiro. Da cabeça ao pé. Foi a sua vó que costurou, retalho por retalho, naquela máquina do seu lado.",
     S('cama_escuro', deitado(), cam=dict(zoom=1.2, to=1.3, cx=1200, cy=640))),
    ('nar', "A colcha é da casa. E o que tá debaixo dela, essa noite, também é."),
    ('nar', "A vassoura vai passar por cima de você. Uma vez. Duas. Leve, que nem uma mão fazendo carinho. Não se mexe.",
     S('cama_escuro', deitado(sweat=True), cam=dict(zoom=1.3, to=1.4, cx=1000, cy=620))),
    ('coisa', "Cadê o pezinho, fio? A vó só quer limpar.",
     S('cama_escuro', deitado(sweat=True, mouth='wavy'), cam=dict(zoom=1.12, to=1.25, cx=1100, cy=600), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (1050, 900), 's': 0.66, 'escuro': 0.3}, 'shake'])),
    ('nar', "Fica debaixo do fuxico. Conta os retalhos com a ponta dos dedos. Uma hora a palha para. Uma hora o chhh vai embora.",
     S('cama_escuro', deitado(), cam=dict(zoom=1.0, to=1.08))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'ESPERE ELA **AVISAR**')}])),
    ('nar', "Quando o galo cantar e a janela clarear, você vai ouvir a vassoura de novo. No terreiro, agora. E o radinho tocando moda de viola.",
     S('terreiro_chinelo', C('vo', 'c', None, facing=-1, arms='hold', prop='vassoura', mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Não sai correndo. Vai até a porta da cozinha devagar e para do lado de dentro. Com os dois pés no cimento.",
     S('cozinha_vo_manha', C('voce', 'porta', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.1, to=1.2, cx=1300, cy=620))),
    ('nar', "A coisa sabe a voz, o passo, o jeito de segurar a vassoura. Mas tem uma coisa que ela nunca faz. Ela nunca avisa. Ela quer o seu pé.",
     S('preto', fx=[{'olhos': (960, 470), 'surge': True}])),
    ('nar', "A sua vó, a de verdade, avisa. Sempre.",
     S('terreiro_chinelo', C('voce', 'a', None, eyes='wide', mouth='flat', facing=1), C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='flat', eyes='half'), cam=dict(zoom=1.05, to=1.12))),
    ('vo', "Sai da frente, menino, senão eu varro o seu pé e você não casa nunca!",
     S('terreiro_chinelo', C('voce', 'a', None, eyes='happy', mouth='grin', facing=1), C('vo', 'b', None, facing=-1, arms='hold', prop='vassoura', mouth='grin', eyes='happy'), cam=dict(focus='vo', zoom=1.45, to=1.55))),
    ('nar', "Aí sim. Aí pode descer o degrau e abraçar ela, com cheiro de café e de terra molhada.",
     S('terreiro_chinelo', C('voce', 'a', None, eyes='closed', mouth='smile', arms='up', facing=1), C('vo', 'b', None, facing=-1, mouth='smile', eyes='closed', arms='up'), cam=dict(zoom=1.1, to=1.2, cx=760, cy=640))),
    ('nar', "No meio do terreiro, perto do pé de arruda, tá o seu chinelo. Molhado de sereno. Virado de sola pra cima.",
     S('terreiro_chinelo', cam=dict(zoom=1.6, to=1.8, cx=1150, cy=900))),
    ('vo', "Ué, que chinelo é esse no sereno? Deixa que a vó guarda na sua mochila.",
     S('terreiro_chinelo', C('vo', 'b', None, facing=1, arms='point', mouth='o', eyes='wide'), C('voce', 'a', None, eyes='wide', mouth='flat', facing=1), cam=dict(zoom=1.15, to=1.25, cx=900, cy=660))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "As férias acabam. Você volta pra casa, na cidade. Apartamento pequeno, piso frio, onde ninguém varre nada há semanas.",
     S('quarto', quarto(eyes='half', mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Na primeira noite, você desfaz a mochila. E lá no fundo, embrulhado num saquinho de pão, tá o seu chinelo. Ainda úmido. Com um fiapo de palha preso na tira.",
     S('quarto', quarto(eyes='wide', mouth='o'), cam=dict(zoom=1.5, to=1.65, cx=1300, cy=780))),
    ('nar', "Ela não varreu o seu chinelo pra jogar fora. Ela varreu pra guardar o seu cheiro. Pra saber o caminho.",
     S('terreiro_chinelo', cam=dict(zoom=1.3, to=1.5, cx=1150, cy=880))),
    ('nar', "São três horas da manhã. E do corredor do seu apartamento vem um barulho que você conhece. Chhh. Chhh. Chhh.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[dict(PORTA_QUARTO, abre=0.3, surge=True), {'texto': ['03:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Levanta o pezinho, fio.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 2.7, 'pos': (960, 600), 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: você ia conseguir ficar quieto quando ela pedisse licença?",
     S('preto', fx=[{'cta_mm': ('VOCÊ DARIA', 'LICENÇA?')}])),
]
