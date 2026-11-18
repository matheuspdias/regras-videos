"""Manual da Madrugada — Noite 02
Se sua vó te benzer duas vezes na mesma noite… FINJA QUE DORME
"""
from engine.dsl import S, C

TITLE = "Se sua vó te benzer duas vezes na mesma noite… FINJA QUE DORME"
NOITE = 2
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 20.0
THUMB = dict(ordem='FINJA QUE **DORME**', esquerda=('voce', dict(eyes='wide', mouth='o', arms='face', sweat=True)),
             criatura_porta=True, criatura='coisa_vo', balao='Tá dormindo?')

CORTES_TIKTOK = (137.1, 234.3, 347.3, 489.8)   # partes para o TikTok (tools/vertical.py): antes de cartões de regra / depois de sustos

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '045e4a2e57434943bd3bb5db714aad75',  # ESE Vó Cida (com efeito)
    'vo': '045e4a2e57434943bd3bb5db714aad75',     # ESE Vó Cida (limpa)
    'voce': 'd703f08d1ef34302a36945aa3efc7b3f',   # Murilo
}

CAB = (910, 620)     # cabeça do protagonista deitado na cena 'cama'
VL = (430, 300)      # de onde vem a voz ao lado da cama
VC = (1520, 230)     # porta do quarto da vó, no fim do corredor

# onde o monstro aparece (a coisa imita a vó: coque, laço vermelho)
Q = 'coisa_vo'
JANELA_CAMA = {'monstro': 'janela', 'rect': (900, 120, 260, 230), 'quem': Q}
JANELA_QVO = {'monstro': 'janela', 'rect': (200, 170, 280, 260), 'quem': Q}
PORTA_QVO = {'monstro': 'porta', 'rect': (760, 260, 230, 540), 'lado': 'esq', 'abre': 0.45, 'quem': Q}
PORTA_VO = {'monstro': 'porta', 'rect': (1400, 280, 240, 540), 'lado': 'esq', 'abre': 0.3, 'quem': Q}


def deitado(**p):
    d = dict(lie=True, eyes='closed', mouth='flat')
    d.update(p)
    return C('voce', 'deitado', None, **d)


def sentado(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


def close(z=1.6, to=1.75):
    return dict(zoom=z, to=to, cx=CAB[0] + 60, cy=CAB[1] - 20)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se a sua vó te benzer duas vezes na mesma noite, finja que dorme. Não abra os olhos. Não diga amém. E, aconteça o que acontecer, não deixe ela perceber que você tá acordado.",
     S('cama', deitado(), cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(JANELA_CAMA, surge=True)])),
    ('nar', "Eu não tô falando de quando ela te benze no almoço de domingo, porque você chegou da rua com cara de quebranto.",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='point', mouth='smile'), C('voce', 'a', None, eyes='half', mouth='flat'))),
    ('nar', "Também não tô falando de quando ela passa a mão na sua cabeça na rodoviária e reza baixinho pra você fazer boa viagem.",
     S('porta', C('vo', 'b', None, facing=-1, arms='wave', mouth='smile'), C('voce', 'a', None, mouth='smile'))),
    ('nar', "Eu tô falando disso.",
     S('preto')),

    # ---------------------------------------------------------------- A NOITE
    ('nar', "É julho. Você tá passando as férias na casa da sua vó, numa cidadezinha do interior de Minas, a seis horas de ônibus de casa. Seus pais ficaram em São Paulo, trabalhando.",
     S('sala', C('vo', 'sofa2', None, sit=True, facing=-1, mouth='smile'), C('voce', 'sofa', None, sit=True, mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "A casa é antiga. Portão de ferro, fogão a lenha, rádio de pilha em cima da geladeira. E o Tição, um vira-lata preto que escolheu dormir debaixo da sua cama desde o primeiro dia.",
     S('quarto_vo', sentado(mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.1), fx=[{'cachorro': (1720, 830, 'abana')}])),
    ('nar', "De dia é tudo bom. Pão de queijo, goiabada, futebol na rua de terra com os meninos da vizinhança. De noite, a cidade inteira dorme às nove. Não passa carro. Não late cachorro. Só o grilo.",
     S('porta', cam=dict(zoom=1.0, to=1.1, cx=430, cy=420), fx=[{'texto': ['21:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Toda noite, antes de dormir, a sua vó faz a mesma coisa. Ela entra no quarto com um raminho de arruda, faz três cruzes na sua testa e reza baixinho.",
     S('quarto_vo', sentado(eyes='closed', mouth='smile'), C('vo', 'centro', None, arms='point', eyes='closed', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('vo', "Deus te abençoe e te guarde, meu anjo. Agora dorme.",
     S('quarto_vo', sentado(eyes='closed', mouth='smile'), C('vo', 'centro', None, arms='down', eyes='happy', mouth='smile'), cam=dict(focus='vo', zoom=1.4, to=1.5))),
    ('nar', "Ela chama todo mundo de meu anjo. Os netos, o carteiro, o Tição.",
     S('quarto_vo', sentado(eyes='half', mouth='smile'), C('vo', 'centro', None, arms='wave', mouth='smile'), cam=dict(zoom=1.1, to=1.2), fx=[{'cachorro': (1720, 830, 'abana')}])),
    ('nar', "Uma vez só. Ela nunca benze duas vezes. Ela diz que bênção é igual tempero: uma vez é cuidado, duas vezes estraga.",
     S('cama', deitado(mouth='smile'), cam=dict(zoom=1.15, to=1.25, cx=1100, cy=600))),
    ('nar', "Depois ela apaga a luz, encosta a porta e vai pro quarto dela, no fim do corredor. Dez minutos depois, você escuta ela roncando.",
     S('corredor', C('vo', 'p3', None, facing=1, eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "São três e dez da manhã.",
     S('corredor', cam=dict(zoom=1.0, to=1.08), fx=[{'texto': ['03:10'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você acorda com o barulho de um chinelo arrastando no corredor. Devagar. Parando bem na frente da sua porta.",
     S('corredor', cam=dict(zoom=1.15, to=1.35, cx=360, cy=560), fx=[{'monstro': 'fundo', 'quem': Q, 'pos': (560, 830), 's': 0.6, 'escuro': 0.65, 'avanca': True, 'surge': True}])),
    ('nar', "A porta abre. Entra um cheiro de vela. E alguém para do lado da sua cama.",
     S('quarto_vo', cam=dict(zoom=1.05, to=1.2, cx=875, cy=560), fx=[dict(PORTA_QVO, surge=True)])),
    ('coisa', "Fica guardadinho, meu anjo. Fica guardadinho com a vó.",
     S('cama', deitado(), C(Q, 'lado', None, facing=1, mouth='grin', arms='hold'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "A mesma voz. O mesmo raminho roçando na sua testa. As mesmas três cruzes. Só que tem uma coisa errada.",
     S('cama', deitado(sweat=True), cam=close())),
    ('nar', "No fim do corredor, a sua vó continua roncando.",
     S('corredor', cam=dict(zoom=1.2, to=1.4, cx=1520, cy=540), fx=['piscar'])),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá do lado da sua cama conhece essa casa. Conhece o chinelo, o cheiro da vela, a voz da sua vó. Ela já ouviu essa reza muitas vezes. Pela janela.",
     S('quarto_vo', cam=dict(zoom=1.1, to=1.3, cx=380, cy=330), fx=[dict(JANELA_QVO, surge=True)])),
    ('nar', "Mas ela não enxerga quem dorme.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.65, 'surge': True}])),
    ('nar', "Pra ela, quem dorme é só um volume debaixo da coberta, fechado pela primeira bênção. Igual a um travesseiro. Igual a uma pilha de roupa em cima da cadeira.",
     S('cama', deitado(), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Ela só enxerga quem tá acordado. Por isso ela benze de novo. A segunda bênção não é pra te proteger. É pra ver se você acorda.",
     S('cama', deitado(), C(Q, 'lado', None, facing=1, mouth='grin', arms='point'), cam=dict(zoom=1.0, to=1.12))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe aquela vez em que você acordou de madrugada com a sensação de que alguém tinha acabado de sair do seu quarto? A porta um pouquinho mais aberta do que você deixou?",
     S('quarto_vo', sentado(eyes='wide', mouth='flat', look=-1), cam=dict(zoom=1.0, to=1.15))),
    ('nar', "Ou aquele cheiro de vela no quarto que, de manhã, ninguém soube explicar.",
     S('quarto_vo', cam=dict(zoom=1.3, to=1.45, cx=1330, cy=420))),
    ('nar', "Talvez você tenha tido sorte. Talvez você tenha virado pro outro lado e dormido de novo, sem abrir os olhos.",
     S('cama', deitado(), cam=close(1.45, 1.6))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'FINJA QUE **DORME**')}])),
    ('nar', "Finja que dorme. E finja direito, porque quase todo mundo finge errado.",
     S('cama', deitado(), cam=close(1.5, 1.6))),
    ('nar', "Quem finge aperta os olhos. Quem dorme deixa as pálpebras moles. Quem finge prende a respiração. Quem dorme respira devagar, fundo, com a boca um pouquinho aberta.",
     S('cama', deitado(mouth='o'), cam=close(1.3, 1.4))),
    ('nar', "Conta as respirações. Puxa o ar em quatro. Solta em seis. E não engole saliva quando ela chegar perto. Ela escuta quem engole.",
     S('cama', deitado(mouth='o'), C(Q, 'lado', None, facing=1, mouth='grin'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Se ela encostar a mão no seu peito pra sentir o coração, não tem problema. Coração acelerado é normal. Tem gente que sonha correndo.",
     S('cama', deitado(sweat=True), C(Q, 'lado', None, facing=1, mouth='flat', arms='point'), cam=dict(zoom=1.15, to=1.25, cx=700, cy=560))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO DIGA **AMÉM**')}])),
    ('nar', "Quando a reza terminar, ela vai ficar parada do lado da cama. Esperando.",
     S('cama', deitado(), C(Q, 'lado', None, facing=1, mouth='flat'), cam=dict(zoom=1.2, to=1.35, cx=520, cy=560))),
    ('nar', "Você passou a vida inteira respondendo amém pra sua vó. Na mesa, na missa, no portão. A sua boca vai querer responder sozinha.",
     S('cama', deitado(sweat=True), cam=close())),
    ('coisa', "Fala amém, meu anjo. Fala amém pra vó.",
     S('cama', deitado(sweat=True), C(Q, 'lado', None, facing=1, mouth='grin', arms='point'), cam=dict(zoom=1.15, to=1.25, cx=700, cy=540))),
    ('nar', "Não fala. Quem dorme não diz amém. Quem diz amém tá dizendo: eu tô aqui, eu ouvi, eu aceito. E o que ela tá oferecendo não é bênção.",
     S('cama', deitado(), cam=close(1.5, 1.6))),
    ('nar', "E, se você escorregar e um som sair da sua boca, transforma em ronco. Um ronco feio, desajeitado, de boca aberta. Ronco ela entende como sono.",
     S('cama', deitado(mouth='o'), cam=close(1.3, 1.4))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO SE **MEXA**')}])),
    ('nar', "Ela vai passar o raminho de novo. No rosto. No pescoço. Na palma da sua mão.",
     S('cama', deitado(), C(Q, 'lado', None, facing=1, mouth='grin', arms='point'), cam=dict(zoom=1.1, to=1.2, cx=700, cy=560))),
    ('nar', "A arruda da sua vó é verde, cheira a quintal depois da chuva. Essa não. Essa é fria, molhada, e tem cheiro de lugar fechado, de porão que ninguém abre faz anos.",
     S('quarto_vo', cam=dict(zoom=1.4, to=1.6, cx=1110, cy=580))),
    ('nar', "Vai dar coceira. Vai dar vontade de virar pro lado. Não vira. Quem dorme pesado não sente cócega. Deixa a mão aberta em cima da coberta, do jeitinho que tava.",
     S('cama', deitado(), cam=dict(zoom=1.1, to=1.2, cx=1100, cy=620))),
    ('nar', "Se ela segurar a sua mão, deixa ela segurar. Mão mole, dedo solto. Dormindo, ninguém aperta de volta.",
     S('cama', deitado(), C(Q, 'lado', None, facing=1, mouth='grin', arms='hold'), cam=dict(zoom=1.05, to=1.15))),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'DEIXE O TIÇÃO **ROSNAR**')}])),
    ('nar', "Debaixo da cama, o Tição vai acordar. Primeiro vem um rosnado baixo, que você sente vibrando no colchão.",
     S('quarto_vo', cam=dict(zoom=1.2, to=1.35, cx=1500, cy=720), fx=[{'cachorro': (1720, 830, 'rosna')}])),
    ('nar', "Não acalma ele. Não estala os dedos, não chama, não faz psiu. Bicho rosnando é bicho acordado. E é isso que ela vai achar que tá ali: um bicho. Ela não liga pra bicho.",
     S('quarto_vo', cam=dict(zoom=1.0, to=1.1), fx=[{'monstro': 'fundo', 'quem': Q, 'pos': (640, 1000), 's': 0.78, 'escuro': 0.5}, {'cachorro': (1720, 830, 'rosna')}])),
    ('nar', "Ela só liga pra você. E você, essa noite, é um travesseiro.",
     S('cama', deitado(), cam=close(1.4, 1.5))),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'SE ELA DISSER QUE SABE, **DUVIDE**')}])),
    ('nar', "Quando nada funcionar, ela vai chegar bem perto do seu ouvido. Tão perto que você vai perceber que a respiração dela não é quente. É gelada.",
     S('cama', deitado(sweat=True), C(Q, 'lado', None, facing=1, mouth='grin'), cam=dict(zoom=1.25, to=1.4, cx=700, cy=520))),
    ('coisa', "Eu sei que você tá acordado. Eu vi teu olho mexer.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.1}, 'zoom_punch'])),
    ('nar', "Ela não viu nada. Ela não enxerga quem dorme, lembra? Ela tá chutando. Ela fala isso em todo quarto, pra todo mundo, só pra ver quem se assusta.",
     S('preto', fx=[{'olhos': (960, 520)}])),
    ('nar', "Se o seu olho mexeu, mexeu dormindo. Gente dormindo mexe o olho o tempo todo. Continua respirando. Quatro. Seis.",
     S('cama', deitado(mouth='o'), cam=close(1.35, 1.45))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'SE A VELA APAGAR, NÃO **ACENDA**')}])),
    ('nar', "Tem uma velinha acesa no oratório da sua vó, na prateleira do quarto. Ela fica acesa a noite inteira. É a única luz da casa.",
     S('quarto_vo', cam=dict(zoom=1.5, to=1.7, cx=1330, cy=400))),
    ('nar', "Em algum momento, ela vai apagar. Sem vento. Sem sopro. E o quarto vai ficar tão escuro que, mesmo de olho fechado, você vai sentir a diferença.",
     S('quarto_vo_escuro', cam=dict(zoom=1.5, to=1.6, cx=1330, cy=400), fx=['piscar'])),
    ('nar', "Ela não apagou por acaso. Ela quer saber se alguém vai levantar pra acender. Fica deitado. No escuro, você e o travesseiro são exatamente iguais.",
     S('cama_escuro', deitado(), cam=dict(zoom=1.0, to=1.1), fx=[{'monstro': 'fundo', 'quem': Q, 'pos': (400, 1000), 's': 0.9, 'escuro': 0.8, 'surge': True}])),
    ('nar', "Se a tela do seu celular acender com uma notificação, deixa. Não estica a mão. A tela apaga sozinha em trinta segundos. Trinta segundos vão parecer uma hora. Mas apaga.",
     S('cama_escuro', deitado(sweat=True), cam=close(1.3, 1.4))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'NÃO SAIA DA **CAMA**')}])),
    ('nar', "Lá pelas quatro e meia, o ronco no fim do corredor vai parar.",
     S('corredor', cam=dict(zoom=1.05, to=1.2, cx=1300, cy=560), fx=[{'texto': ['04:30'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "E a voz da sua vó vai sair de dentro do quarto dela. Fraca. Cansada.",
     S('corredor', cam=dict(zoom=1.2, to=1.4, cx=1520, cy=540), fx=[dict(PORTA_VO, abre=0.2, surge=True)])),
    ('coisa', "Meu anjo... a vó tá sem ar. Vem cá, liga pra alguém.",
     S('corredor', cam=dict(zoom=1.3, to=1.45, cx=1520, cy=520), fx=[dict(PORTA_VO, boca='flat')])),
    ('nar', "Dessa vez a voz não vem do lado da sua cama. Vem de longe. Do lugar exato onde a sua vó de verdade deveria estar dormindo.",
     S('corredor', cam=dict(zoom=1.15, to=1.3, cx=1520, cy=560), fx=[PORTA_VO])),
    ('nar', "Esse é o pior momento da noite. Porque agora você não sabe mais qual das duas é a sua vó. E porque você ama ela.",
     S('cama_escuro', deitado(eyes='sad', mouth='frown', sweat=True), cam=close())),
    ('nar', "Mas pensa. A sua vó nunca chamou ninguém de madrugada. Quando ela passa mal, ela bate a bengala no chão, três vezes. Foi isso que ela combinou com o seu pai. Não tem batida nenhuma. Só a voz.",
     S('quarto_vo_escuro', sentado(eyes='angry', mouth='flat'), cam=dict(zoom=1.0, to=1.1), fx=[dict(JANELA_QVO, surge=True)])),
    ('nar', "Fica na cama. Continua respirando. E escuta o Tição. Ele parou de rosnar. Isso quer dizer que, do lado da sua cama, não tem mais ninguém.",
     S('quarto_vo_escuro', cam=dict(zoom=1.2, to=1.3, cx=1500, cy=720), fx=[{'cachorro': (1720, 830, 'parado')}])),

    # ---------------------------------------------------------------- REGRA 8 / AMANHECER
    ('nar', "Regra número oito.",
     S('preto', fx=[{'regra': (8, 'SÓ LEVANTE COM O **CAFÉ**')}])),
    ('nar', "Quando o galo cantar e a janela ficar cinza, ainda não levanta. Espera o cheiro.",
     S('quarto_vo_manha', sentado(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Cheiro de café passado no coador de pano. O rádio de pilha tocando baixinho. A colher batendo na xícara. A coisa sabe imitar voz. Mas não sabe passar café.",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "E não vale cheiro sem barulho. Se o cheiro chegar e a casa continuar em silêncio, sem rádio, sem colher, sem chinelo, fecha os olhos de novo. Ainda não acabou.",
     S('quarto_vo_manha', sentado(eyes='closed', mouth='flat'), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('nar', "Aí você levanta, vai até a cozinha e faz o teste. Pede a bênção.",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile'), C('voce', 'a', None, eyes='half', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('voce', "A bênção, vó.",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile'), C('voce', 'a', None, eyes='wide', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('vo', "Deus te abençoe, meu anjo. Dormiu bem?",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='down', mouth='smile', eyes='happy'), C('voce', 'a', None, eyes='wide', mouth='flat'), cam=dict(focus='vo', zoom=1.5, to=1.6))),
    ('nar', "Ela disse Deus. A coisa nunca diz. Ela fala guardado, guardadinho, fica com a vó. Mas esse nome ela não consegue dizer. Agora sim. Agora você pode abraçar a sua vó.",
     S('cozinha', C('vo', 'b', None, facing=-1, mouth='smile', eyes='happy'), C('voce', 'c', None, facing=1, arms='up', eyes='happy', mouth='grin'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "E não conta nada pra ela. Deixa ela tomar o café dela em paz.",
     S('cozinha', C('vo', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile', eyes='half'), C('voce', 'a', None, eyes='half', mouth='smile'), cam=dict(zoom=1.1, to=1.2))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Depois do café, você volta pro quarto pra arrumar a cama. E, em cima do seu travesseiro, tem um raminho de arruda.",
     S('quarto_vo_ramo', cam=dict(zoom=1.3, to=1.5, cx=1350, cy=650))),
    ('nar', "Os raminhos da sua vó são verdes. Esse tá seco, escuro, e amarrado com uma linha vermelha.",
     S('quarto_vo_ramo', cam=dict(zoom=1.9, to=2.1, cx=1290, cy=700), fx=['zoom_punch'])),
    ('nar', "Você pega o raminho na mão. Ele tá frio. Mesmo com o sol entrando pela janela.",
     S('quarto_vo_manha', sentado(eyes='wide', mouth='o', arms='hold'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Você não fala nada. Mas, lá da cozinha, sem você perguntar, a sua vó grita:",
     S('corredor', C('voce', 'p1', None, eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.05, to=1.15), fx=[dict(PORTA_VO, abre=0.15, surge=True)])),
    ('vo', "Não joga fora, não! Ela deixa quando vai voltar. Hoje a gente benze a casa inteira.",
     S('cozinha', C('vo', 'b', None, facing=-1, eyes='half', mouth='flat', arms='hold', prop='caneca'), cam=dict(focus='vo', zoom=1.5, to=1.65))),
    ('nar', "Você ainda tem vinte e três dias de férias.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: você ia conseguir fingir que dorme até o café ficar pronto?",
     S('preto', fx=[{'cta_mm': ('VOCÊ CONSEGUIRIA', 'FINGIR QUE DORME?')}])),
]
