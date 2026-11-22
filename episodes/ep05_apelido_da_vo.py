"""Manual da Madrugada — Noite 05
Se o seu irmão te chamar pelo apelido que só a vó usava… NÃO OLHE PRA TRÁS
"""
from engine.dsl import S, C

TITLE = "Se o seu irmão te chamar pelo apelido que só a vó usava… NÃO OLHE PRA TRÁS"
NOITE = 5
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='NÃO **OLHE**', cena='atras', criatura='coisa_ep05', balao='Tatuzinho?')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': 'd703f08d1ef34302a36945aa3efc7b3f',  # Murilo (imitando o Bento, com efeito)
    'irmao': 'd703f08d1ef34302a36945aa3efc7b3f',  # Murilo (o Bento de verdade, limpo)
    'mae': '914de72ccc244decb2fd1572808fa7e0',    # MM Mãe
}

# a coisa desta noite: imita o Bento de pijama, mas alta demais, cabeça muito torta, sorrindo de olhos fechados,
# braços compridos; o detalhe vermelho é a touca de tricô que a vó fez. Só abre os olhos na virada final.
Q = 'coisa_ep05'
QO = 'coisa_ep05_olhos'
ATRAS = {'monstro': 'atras', 'quem': Q, 'pos': (780, 1012), 's': 0.78, 'escuro': 0.3}           # atrás de você no corredor
ESPELHO = {'monstro': 'janela', 'quem': Q, 'rect': (1601, 362, 128, 244), 'escuro': 0.2}       # no espelho do guarda-roupa
GUARDA = {'monstro': 'fundo', 'quem': Q, 'pos': (1290, 830), 's': 0.62, 'escuro': 0.35}       # em pé ao lado do guarda-roupa
PORTA_QUARTO = {'monstro': 'porta', 'quem': Q, 'rect': (760, 260, 230, 540), 'lado': 'esq', 'abre': 0.28}
JANELA_QUARTO = {'monstro': 'janela', 'quem': Q, 'rect': (220, 160, 300, 280)}
PE_CAMA = {'monstro': 'borda', 'quem': Q, 'pos': (1700, 760), 's': 0.72}
TETO = {'monstro': 'teto', 'quem': Q, 'pos': (1420, 0), 's': 0.6}


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


def corredor(slot='meio', **p):
    d = dict(eyes='wide', mouth='flat', facing=1)
    d.update(p)
    return C('voce', slot, None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se o seu irmão te chamar pelo apelido que só a sua vó usava, não olhe pra trás. Não diga oi. Não pergunte o que ele quer. E, aconteça o que acontecer, não vire o rosto pra conferir se é ele mesmo.",
     S('corredor_vo', corredor('meio', eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(ATRAS, surge=True, escuro=0.6)])),
    ('nar', "Eu não tô falando de quando o seu irmão te chama de chato porque você não emprestou o controle do videogame.",
     S('sala', C('irmao', 'sofa2', None, sit=True, eyes='angry', mouth='frown'), C('voce', 'sofa', None, sit=True, mouth='smile', arms='hold', prop='controle'))),
    ('nar', "Também não tô falando de quando ele grita o seu nome do quintal porque a bola caiu de novo na casa do vizinho.",
     S('quintal_manha', C('irmao', 'a', None, arms='wave', mouth='o'), C('voce', 'b', None, eyes='half', mouth='flat', facing=-1))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "A sua vó, a Vó Dita, morou com vocês até o inverno retrasado. Ela te chamava de Tatuzinho. Desde bebê, porque você dormia todo enrolado, que nem tatu-bola. A última coisa que ela tricotou foi uma touca vermelha pro Bento. Sumiu do varal uma semana depois.",
     S('quarto_vo', C('vo', 'centro', None, mouth='smile', eyes='happy', arms='wave'), C('voce', 'cama', None, sit=True, facing=-1, mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Ninguém mais te chama assim. Nem a sua mãe. Quando a vó se foi, o apelido foi junto. E o guarda-roupa dela veio pro fim do corredor, porque ninguém teve coragem de doar.",
     S('corredor_vo', cam=dict(zoom=1.15, to=1.35, cx=1570, cy=540))),
    ('nar', "Hoje a sua mãe tá no turno da noite, na fábrica de embalagens. Entra às dez e sai às seis. O seu pai tá na estrada com o caminhão, em algum lugar entre Cuiabá e Goiânia.",
     S('sala', C('mae', 'porta', None, facing=-1, arms='wave', mouth='smile'), C('voce', 'sofa', None, sit=True, mouth='smile'), C('irmao', 'centro', None, mouth='smile', arms='wave'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Você ficou com o Bento, o seu irmão de sete anos. Ele dorme no quarto do meio, com a luzinha da tomada acesa, porque tem medo do escuro.",
     S('quarto_bento', C('irmao', 'cama', None, lie=True, eyes='closed', mouth='smile'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "São três e vinte da manhã.",
     S('preto', fx=[{'texto': ['03:20'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você levantou pra beber água. Tá no meio do corredor, de costas pro guarda-roupa da vó, quando ouve. Atrás de você. A voz do Bento.",
     S('corredor_vo', corredor('meio', eyes='half', mouth='flat'), cam=dict(zoom=1.05, to=1.2))),
    ('coisa', "Tatuzinho?",
     S('corredor_vo', corredor('meio', eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.3, to=1.45, cx=720, cy=500), fx=[ATRAS, 'zoom_punch'])),
    ('nar', "Tatuzinho. O apelido que só a vó usava. Uma palavra que o Bento nunca ouviu, porque ele era pequeno demais quando ela se foi.",
     S('corredor_vo', corredor('meio', eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "E ela falou do jeito da vó. Esticando o i no final, devagarinho, do jeito de quem chama alguém pra tomar café."),
    ('nar', "E a porta do quarto dele tá entreaberta. Na luz da tomada, dá pra ver o Bento lá dentro. Dormindo. De boca aberta, abraçado no travesseiro.",
     S('quarto_bento', C('irmao', 'cama', None, lie=True, eyes='closed', mouth='o'), cam=dict(zoom=1.25, to=1.4, cx=480, cy=640))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá atrás de você morou sessenta anos dentro daquele guarda-roupa. Ouviu cada conversa da vó. Cada reza. Cada apelido.",
     S('corredor_vo', cam=dict(zoom=1.3, to=1.5, cx=1600, cy=520), fx=[dict(ESPELHO, surge=True)])),
    ('nar', "Por isso a vó, toda noite antes de deitar, passava a chave no guarda-roupa e pendurava o terço no puxador. Desde que ele veio pra cá, ninguém mais passou a chave."),
    ('nar', "Ela sabe a voz de todo mundo da casa. E escolheu a do Bento, porque é a única voz de que você nunca ia desconfiar.",
     S('corredor_vo', cam=dict(zoom=1.05, to=1.2), fx=[dict(GUARDA, avanca=True)])),
    ('nar', "Mas ela não enxerga. Ela anda de olhos fechados, sorrindo. Sempre atrás de alguém.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.5, 'surge': True}])),
    ('nar', "Ela sabe o apelido. Mas não sabe de quem ele é. E o único jeito de descobrir é você virar. Quem vira quando ouve um nome tá dizendo: sou eu. E é aí que ela abre os olhos.",
     S('corredor_vo', corredor('meio', eyes='closed', mouth='flat'), cam=dict(zoom=1.1, to=1.25))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe aquela sensação de que tem alguém parado atrás de você? No corredor escuro, na fila do mercado, no banho. Você não ouviu nada. Mas a nuca arrepiou inteira.",
     S('cozinha', C('voce', 'c', None, eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.15), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (1080, 1012), 's': 0.78, 'escuro': 0.7, 'surge': True}])),
    ('nar', "E você virou. E não tinha ninguém. Talvez não tivesse mesmo. Ou talvez ela só não soubesse o seu nome ainda.",
     S('cozinha', C('voce', 'c', None, eyes='half', mouth='flat', facing=-1), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Na próxima vez, antes de virar, pensa um segundo: quem é que sabe o meu nome nesta casa?"),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO OLHE PRA **TRÁS**')}])),
    ('nar', "Não olhe pra trás. Nem um pouquinho. Nem de canto de olho. Nem pra conferir se é o Bento de verdade.",
     S('corredor_vo', corredor('meio', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "Isso é mais difícil do que parece. Quando alguém chama, o pescoço vira sozinho. É reflexo. Trava o queixo no peito e olha pro chão. Pros seus pés.",
     S('corredor_vo', corredor('meio', eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.2, to=1.3))),
    ('nar', "Se você não virar, ela chama de novo. Mais perto. Tão perto que dá pra sentir um vento frio na nuca.",
     S('corredor_vo', corredor('meio', eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.15, to=1.3, cx=720, cy=540), fx=[dict(ATRAS, s=0.86, pos=(800, 1012), surge=True)])),
    ('coisa', "Tatuzinho... olha pra mim.",
     S('corredor_vo', corredor('meio', eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.45, to=1.6, cx=720, cy=470), fx=[dict(ATRAS, s=0.86, pos=(800, 1012))])),
    ('nar', "Não olha. Anda pra frente, devagar, sem tirar os olhos do chão, até o seu quarto.",
     S('corredor_vo', corredor('p1', eyes='half', facing=-1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "E não corre. Quem corre tá fugindo de alguma coisa. E quem foge sabe que tem alguma coisa atrás."),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'COSTAS NA **PAREDE**')}])),
    ('nar', "Entra no quarto e senta na cama com as costas coladas na parede. Bem coladas. Do ombro até a cintura.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Ela só existe atrás das pessoas. Se não tem espaço atrás de você, não tem espaço pra ela.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('nar', "Então ela vai procurar outro lugar. A porta. O teto. O pé da cama. Qualquer lugar onde ela possa ficar fora da sua frente.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[dict(PORTA_QUARTO, surge=True)])),
    ('nar', "Você vai ouvir ela andando pelo quarto. Pé descalço de criança no piso frio. Mas os passos são compridos demais. Ninguém de sete anos dá passos daquele tamanho."),
    ('nar', "E não levanta da cama. Nem pra fechar a porta. Pra fechar a porta, você ia ter que dar as costas pra ela.",
     S('quarto', quarto(eyes='angry', mouth='flat', arms='cross'), cam=dict(zoom=1.15, to=1.25))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO OLHE NO **REFLEXO**')}])),
    ('nar', "De madrugada, toda janela vira espelho. A tela apagada do celular vira espelho. Até o vidro do porta-retrato vira espelho.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.2, to=1.35, cx=520, cy=420), fx=[dict(JANELA_QUARTO, surge=True)])),
    ('nar', "Num reflexo, o que tá atrás de você aparece na sua frente. Você não precisou virar. E ela te achou do mesmo jeito.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.65))),
    ('nar', "Vira o celular com a tela pra baixo. Não olha pra janela. Se precisar olhar pra alguma coisa, olha pros seus joelhos.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='hold', prop='celular'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "E, se você já olhou, se já viu a touca vermelha no vidro, não grita. Fecha os olhos devagar, como se tivesse só piscado. Ela ainda não tem certeza."),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO RESPONDA PELA **VÓ**')}])),
    ('nar', "Quando ela perceber que o Bento não tá funcionando, ela vai mudar o jeito de falar. A voz continua sendo dele. Mas as palavras vão ser da vó.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.1), fx=[{'olhos': (1700, 700), 'surge': True}])),
    ('coisa', "Tatuzinho, vem tomar a bênção. A vó fez bolinho de chuva.",
     S('quarto', quarto(eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.15, to=1.3, cx=1400, cy=560), fx=[dict(PE_CAMA, surge=True)])),
    ('nar', "A vó nunca fez bolinho de chuva de madrugada. Ela dizia que fritura depois das dez dava pesadelo."),
    ('nar', "Toda noite, antes de dormir, a vó falava isso. E você respondia: tô aqui, vó. Sempre. Você deve ter respondido isso umas três mil vezes na vida.",
     S('quarto_vo', C('vo', 'centro', None, mouth='smile', eyes='happy', arms='hold', prop='bolo'), C('voce', 'cama', None, sit=True, facing=-1, mouth='grin', eyes='happy'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "A sua boca vai querer responder sozinha. Não responde. A vó de verdade nunca te chamava de longe. Ela vinha até você, sentava na beirada da cama e fazia o sinal da cruz na sua testa.",
     S('quarto', quarto(eyes='closed', mouth='wavy', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.6))),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'TAPE OS OLHOS DO **BENTO**')}])),
    ('nar', "Lá pelas quatro, o Bento vai acordar. Ele vai ouvir a própria voz no corredor. E vai vir correndo pro seu quarto, chorando.",
     S('quarto_bento', C('irmao', 'centro', None, eyes='sad', mouth='o', sweat=True), cam=dict(zoom=1.0, to=1.12))),
    ('irmao', "Tem alguém lá fora falando igual eu!",
     S('quarto', quarto(eyes='wide', mouth='flat'), C('irmao', 'centro', None, eyes='sad', mouth='o', sweat=True), cam=dict(focus='irmao', zoom=1.4, to=1.55))),
    ('nar', "Deixa ele entrar. Puxa ele pra cama e encosta as costas dele na parede também. E tapa os olhos dele com a mão.",
     S('quarto', quarto(eyes='angry', mouth='flat', arms='point'), C('irmao', 'centro', None, eyes='closed', mouth='frown'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Porque agora ela tá na porta. E o Bento ainda não sabe as regras. Criança olha. Criança sempre olha.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), C('irmao', 'centro', None, eyes='closed', mouth='frown'), cam=dict(zoom=1.0, to=1.1), fx=[dict(PORTA_QUARTO, abre=0.4, surge=True)])),
    ('coisa', "Bento... pergunta pro Tatuzinho se ele tá com medo.",
     S('quarto', cam=dict(zoom=1.3, to=1.45, cx=875, cy=500), fx=[dict(PORTA_QUARTO, abre=0.45)])),
    ('nar', "Ela tá tentando descobrir qual de vocês dois é o Tatuzinho. Não deixa o Bento falar nada. Sussurra no ouvido dele: fecha o olho e conta carneirinho comigo.",
     S('quarto', quarto(eyes='half', mouth='flat'), C('irmao', 'centro', None, eyes='closed', mouth='flat'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Ele vai querer espiar. Ele vai dizer que tá ouvindo ele mesmo. Segura firme. Conta junto com ele, bem baixinho, até cem. Depois, de novo."),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'VIRE **TATU-BOLA**')}])),
    ('nar', "Antes de amanhecer, ela vai tentar o último jeito. Ela vai encostar em você.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[dict(TETO, surge=True)])),
    ('nar', "Uma mão fria, no seu ombro. No mesmo lugar onde a vó punha a mão pra te acordar pra escola.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.4, to=1.55), fx=[{'monstro': 'lateral', 'quem': Q, 'lado': 'dir', 'y': 1180, 's': 1.15, 'surge': True}])),
    ('coisa', "Tatuzinho... vira só um pouquinho.",
     S('quarto', quarto(eyes='closed', mouth='wavy', sweat=True), cam=dict(zoom=1.2, to=1.35, cx=1450, cy=560), fx=[dict(PE_CAMA, s=0.8, pos=(1640, 760))])),
    ('nar', "Lembra por que a vó te deu esse apelido. Quando você tinha medo, você virava tatu-bola. Faz isso agora. Abraça os joelhos. Esconde o rosto. Fecha os olhos com força.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Tatu-bola não tem frente nem costas. Não tem pra onde virar. E ela não consegue achar o rosto de quem escondeu o rosto.",
     S('preto', fx=['piscar'])),
    ('nar', "Ela vai ficar ali até o céu clarear. Você vai sentir o colchão afundar do lado do seu pé. Fica enrolado. Respira pelo nariz. Ela cansa antes de você."),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'SÓ OLHE PRA QUEM ESTÁ NA **FRENTE**')}])),
    ('nar', "Às seis e meia, você vai ouvir o portão. O molho de chaves. A sua mãe chegando do turno, com cheiro de papelão e café de garrafa térmica.",
     S('porta', C('mae', 'porta', None, facing=-1, eyes='half', mouth='flat', arms='hold', prop='sacola'), cam=dict(zoom=1.0, to=1.1), fx=[{'fechadura': True}])),
    ('nar', "Ela vai entrar no quarto e chamar vocês dois. Não levanta a cabeça ainda. Primeiro, escuta de onde vem a voz.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), C('irmao', 'centro', None, eyes='closed'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Se a voz vier da porta, das suas costas ou de cima, fica quieto. Pode ser ela, estreando a voz da sua mãe."),
    ('nar', "A coisa só chama de trás. A sua mãe de verdade vai dar a volta na cama, ajoelhar na sua frente e levantar o seu queixo com a mão. Do jeito que a vó fazia.",
     S('quarto', quarto(eyes='closed', mouth='flat'), C('mae', 'centro', None, facing=1, mouth='smile', eyes='half', arms='point'), cam=dict(zoom=1.1, to=1.2))),
    ('mae', "Que cara é essa, meu amor? Vocês dormiram sentados?",
     S('quarto', quarto(eyes='half', mouth='flat'), C('mae', 'centro', None, facing=1, mouth='smile'), cam=dict(focus='mae', zoom=1.45, to=1.6))),
    ('nar', "Agora sim. Pode abrir os olhos. Olha pra ela. Ela tá na sua frente. Você abraça ela com tanta força que a garrafa térmica cai no chão.",
     S('sala_manha', C('mae', 'sofa2', None, facing=-1, mouth='smile', eyes='happy'), C('voce', 'sofa', None, facing=1, eyes='closed', mouth='smile'), C('irmao', 'centro', None, mouth='smile', arms='up'), cam=dict(zoom=1.0, to=1.08))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Umas semanas depois, o Bento tá desenhando na mesa da cozinha. Ele desenha a família. A mãe, o pai com o caminhão, ele e você.",
     S('cozinha', C('irmao', 'b', None, facing=-1, mouth='smile', arms='hold', prop='caderno'), C('voce', 'a', None, mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Atrás de você, em todos os desenhos, tem mais alguém. Bem alto. De touca vermelha. Sorrindo de olhos fechados.",
     S('cozinha', C('voce', 'a', None, eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.15, to=1.3, cx=640, cy=560), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (690, 1012), 's': 0.86, 'escuro': 0.45, 'surge': True}])),
    ('irmao', "É o Tatuzinho. Ele anda atrás de você desde aquela noite. Ele falou que tá esperando.",
     S('cozinha', C('irmao', 'b', None, facing=-1, mouth='flat', eyes='half', arms='hold', prop='caderno'), C('voce', 'a', None, eyes='wide', mouth='flat'), cam=dict(focus='irmao', zoom=1.5, to=1.65))),
    ('nar', "Você pergunta esperando o quê. E o Bento responde, sem tirar o olho do papel:",
     S('cozinha', C('voce', 'a', None, eyes='wide', mouth='flat', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.65))),
    ('irmao', "Você virar.",
     S('cozinha', C('irmao', 'b', None, facing=-1, mouth='flat', eyes='closed', arms='hold', prop='caderno'), cam=dict(focus='irmao', zoom=1.7, to=1.8))),
    ('nar', "Não vira.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': QO, 's': 3.0}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: qual apelido só a sua vó usava?",
     S('preto', fx=[{'cta_mm': ('QUAL APELIDO', 'SÓ A VÓ USAVA?')}])),
]
