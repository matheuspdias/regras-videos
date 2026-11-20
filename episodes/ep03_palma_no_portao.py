"""Manual da Madrugada — Noite 03
Se o seu pai bater palma no portão de madrugada… NÃO ATENDA
"""
from engine.dsl import S, C

TITLE = "Se o seu pai bater palma no portão de madrugada… NÃO ATENDA"
NOITE = 3
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 20.0
THUMB = dict(ordem='NÃO **ATENDA**', cena='portao', criatura='coisa_ep03', balao='Abre, filho.')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '9ce5f601f9e04382bb26141d5a3f839d',  # Afonso (imitando o pai, com efeito)
    'pai': '9ce5f601f9e04382bb26141d5a3f839d',    # Afonso (limpo)
}

# a coisa desta noite: imita o pai, pescoço comprido (espia por cima do muro), olhos vazios, gravata vermelha
Q = 'coisa_ep03'
PORTAO = {'monstro': 'atras', 'quem': Q, 'pos': (960, 830), 's': 0.72, 'escuro': 0.35}          # parado atrás da grade
MURO = {'monstro': 'borda', 'quem': Q, 'pos': (1330, 470), 's': 0.85}                             # pescoço por cima do muro
MURO_ESQ = {'monstro': 'borda', 'quem': Q, 'pos': (560, 470), 's': 0.9}
JANELA_QUARTO = {'monstro': 'janela', 'rect': (220, 160, 300, 280), 'quem': Q}
JANELA_SALA = {'monstro': 'janela', 'rect': (300, 240, 260, 360), 'quem': Q}
NA_CORTINA = {'monstro': 'atras', 'quem': Q, 'pos': (960, 640), 's': 0.3, 'escuro': 0.3}         # visto pela janela da sala


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


def cortina(**p):
    d = dict(facing=1, eyes='wide', mouth='flat')
    d.update(p)
    return C('voce', 'lado', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se o seu pai bater palma no portão de madrugada, não atenda. Não grite quem é. Não abra a cortina. E, aconteça o que acontecer, não leve a chave até lá.",
     S('quintal', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(PORTAO, surge=True)])),
    ('nar', "Eu não tô falando de quando ele chega do mercado com as mãos cheias de sacola e bate palma pra você vir abrir.",
     S('quintal_manha', C('pai', 'b', None, facing=-1, arms='wave', mouth='smile', prop='sacola'), C('voce', 'a', None, mouth='smile'))),
    ('nar', "Também não tô falando do moço do gás, nem da vizinha pedindo pra pegar a bola que caiu no seu quintal.",
     S('quintal_manha', C('vizinho', 'b', None, facing=-1, arms='point', mouth='smile'), C('voce', 'a', None, eyes='half', mouth='smile'))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "O seu pai trabalha no turno da noite, numa fábrica do outro lado da cidade. Entra às dez, sai às seis. Volta no ônibus fretado, que para na esquina às seis e vinte.",
     S('sala', C('pai', 'porta', None, facing=-1, arms='wave', mouth='smile', prop='sacola'), C('voce', 'sofa', None, sit=True, mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "A sua mãe foi com a sua irmã pro casamento de uma prima no interior. Volta domingo. Essa noite, a casa é sua. Sua e da Paçoca, a vira-lata caramelo que dorme na casinha do quintal.",
     S('quintal', C('voce', 'b', None, mouth='smile', arms='wave', facing=-1), cam=dict(zoom=1.0, to=1.1), fx=[{'cachorro': (330, 960, 'abana')}])),
    ('nar', "O seu pai saiu às nove e meia. Trancou o cadeado do portão, sacudiu a corrente duas vezes pra conferir, como ele sempre faz, e levou a chave no bolso.",
     S('preto', fx=[{'fechadura': True}])),
    ('nar', "Você jantou o resto do arroz com ovo, ficou vendo vídeo no celular até meia-noite e apagou. A rua tá quieta. Nem moto, nem cachorro de vizinho. Só o zumbido do poste lá fora.",
     S('quarto', quarto(eyes='closed', mouth='smile', arms='hold', prop='celular'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "São três e cinco da manhã.",
     S('quintal', cam=dict(zoom=1.0, to=1.1), fx=[{'texto': ['03:05'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "E aí, lá da frente, vem o barulho. Três palmas. Secas. Bem espaçadas. Do jeito que visita bate quando não tem campainha.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.2))),
    ('coisa', "Ô de casa!",
     S('quintal', cam=dict(zoom=1.2, to=1.32, cx=960, cy=440), fx=[PORTAO, 'zoom_punch'])),
    ('nar', "É a voz do seu pai. O mesmo tom, a mesma rouquidão de quem passou a noite no meio do barulho das máquinas.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "Só que o seu pai tem a chave. Ele nunca bateu palma no próprio portão. E a Paçoca, que late até pra folha caindo, não latiu.",
     S('quintal', cam=dict(zoom=1.2, to=1.35, cx=330, cy=780), fx=[{'cachorro': (330, 960, 'parado')}])),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá no seu portão mora na rua. Ela sabe tudo o que dá pra ver e ouvir do lado de fora.",
     S('quintal', cam=dict(zoom=1.0, to=1.15), fx=[dict(MURO, surge=True)])),
    ('nar', "Ela ouviu o seu pai dando bom dia pro vizinho. Ouviu o nome da cachorra. Sabe a cor do portão e qual é a janela do seu quarto.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.1, to=1.3, cx=380, cy=330))),
    ('nar', "Mas ela não sabe nada do lado de dentro. E ela não pode passar do portão sozinha.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.65, 'surge': True}])),
    ('nar', "Bater palma é pedir licença. E licença só existe quando alguém de dentro atende. Um quem é, um já vou, um pode entrar. Qualquer resposta serve. Qualquer resposta abre.",
     S('quintal', cam=dict(zoom=1.15, to=1.3, cx=960, cy=560))),
    ('nar', "Por isso ela usa a voz do seu pai. Não é pra te enganar de longe. É pra fazer você responder no automático, do mesmo jeito que você responde ele todo santo dia.",
     S('sala', C('voce', 'sofa', None, sit=True, eyes='wide', mouth='flat'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe quando alguém bate palma no portão e você grita quem é antes mesmo de pensar? Ninguém te ensinou isso. Você aprendeu ouvindo os adultos, desde pequeno.",
     S('sala', C('voce', 'sofa', None, sit=True, eyes='half', mouth='o'), cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Agora tenta lembrar de quantas vezes você gritou quem é e ninguém respondeu. Você foi até a janela, não viu ninguém e achou que era criança fazendo graça.",
     S('cortina', cortina(eyes='half'), cam=dict(zoom=1.0, to=1.1), fx=[dict(NA_CORTINA, surge=True)])),
    ('nar', "Talvez fosse. Talvez.",
     S('cortina', cam=dict(zoom=1.4, to=1.6, cx=960, cy=460))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO **ATENDA**')}])),
    ('nar', "Não atenda. Nem quem é. Nem pai. Nem espera aí.",
     S('quarto', quarto(eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "A sua garganta vai fazer o trabalho sozinha. Você passou a vida inteira respondendo palma. Tapa a boca com o travesseiro, se precisar.",
     S('quarto', quarto(eyes='closed', mouth='wavy', arms='face', sweat=True), cam=dict(zoom=1.2, to=1.3))),
    ('nar', "Ela vai bater de novo. Mais forte. E vai falar do jeito que o seu pai fala quando tá cansado e sem paciência.",
     S('quintal', cam=dict(zoom=1.1, to=1.25, cx=960, cy=640))),
    ('coisa', "Filho? Abre aqui pro pai.",
     S('quintal', cam=dict(zoom=1.25, to=1.4, cx=960, cy=430), fx=[dict(PORTAO, boca='flat')])),
    ('nar', "Fica quieto. Cada palma sem resposta é uma pergunta que ela não consegue responder: tem alguém aí dentro?",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO MEXA NA **CORTINA**')}])),
    ('nar', "Você vai querer olhar. Só uma frestinha, só pra ter certeza. Não olha.",
     S('cortina', cortina(arms='point'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Ela não enxerga o lado de dentro. Mas enxerga o tecido. Uma cortina que balança às três da manhã, sem vento, é a mesma coisa que dizer: tem alguém aqui. E é desse lado que ele tá.",
     S('cortina', cortina(eyes='wide', sweat=True), cam=dict(zoom=1.2, to=1.35, cx=760, cy=520), fx=[NA_CORTINA])),
    ('nar', "Se você já mexeu, deita no chão. Encosta na parede, embaixo da janela. Lá fora, ela vai parar de bater palma. E vai ficar olhando. Muito tempo.",
     S('quarto', cam=dict(zoom=1.1, to=1.3, cx=380, cy=330), fx=[dict(JANELA_QUARTO, boca='flat')])),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'ESCUTE A **PAÇOCA**')}])),
    ('nar', "Quando o seu pai chega de verdade, a Paçoca sabe antes de todo mundo. Ela ouve o ônibus lá na avenida e já corre pro portão, chorando de alegria, rodando atrás do próprio rabo.",
     S('quintal_manha', cam=dict(zoom=1.05, to=1.15), fx=[{'cachorro': (700, 960, 'abana')}])),
    ('nar', "Essa noite ela tá no fundo da casinha. Encolhida. Com o rabo entre as pernas. Sem um latido.",
     S('quintal', cam=dict(zoom=1.4, to=1.55, cx=300, cy=800), fx=[{'cachorro': (330, 960, 'parado')}])),
    ('nar', "Cachorro não confunde cheiro. Se a voz diz que é o seu pai e a Paçoca diz que não é, acredita na Paçoca.",
     S('quintal', cam=dict(zoom=1.0, to=1.1), fx=[{'cachorro': (330, 960, 'parado')}])),
    ('coisa', "Paçoca! Vem, menina. Vem cá.",
     S('quintal', cam=dict(zoom=1.05, to=1.15, cx=800, cy=500), fx=[PORTAO, {'cachorro': (330, 960, 'parado')}])),
    ('nar', "Ela não vai. E você também não vai buscar ela. Ela tá mais segura lá do que você estaria no caminho.",
     S('quarto', quarto(eyes='sad', mouth='flat'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "E, se você ouvir ela ganindo baixinho, não chama ela pelo nome. Nem sussurrando. Lá fora, tem alguém ouvindo cada barulho da casa, esperando descobrir se tem gente aí dentro.",
     S('quintal', cam=dict(zoom=1.3, to=1.4, cx=420, cy=760), fx=[{'cachorro': (330, 960, 'parado')}])),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO JOGUE A **CHAVE**')}])),
    ('nar', "Lá pelas quatro, a coisa vai ter uma ideia. Uma ideia que parece muito razoável.",
     S('quintal', cam=dict(zoom=1.05, to=1.2), fx=[{'texto': ['04:10'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Perdi a chave do cadeado, filho. Joga a sua pela janela.",
     S('quintal', cam=dict(zoom=1.25, to=1.4, cx=640, cy=440), fx=[dict(MURO_ESQ, surge=True)])),
    ('nar', "Tem uma cópia na gaveta da cozinha. Você sabe disso. E ela também sabe que você sabe.",
     S('cozinha', C('voce', 'a', None, eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Mas uma chave jogada da janela é uma resposta. É a sua mão dizendo pode entrar. E o seu pai nunca perdeu uma chave na vida. Ele prende o molho no passador da calça com um mosquetão.",
     S('preto', fx=[{'fechadura': True}])),
    ('nar', "Deixa a chave na gaveta. Fecha a gaveta devagar. E volta pro quarto pisando no tapete.",
     S('corredor', C('voce', 'meio', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Se ela insistir, vai começar a sacudir a corrente. Devagar. Duas vezes. O mesmo barulho que o seu pai faz pra conferir se tá trancado. Ela aprendeu isso também, olhando ele sair toda noite.",
     S('quintal', cam=dict(zoom=1.6, to=1.75, cx=960, cy=660), fx=['shake'])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'NÃO OLHE PRO **MURO**')}])),
    ('nar', "Quando ela perceber que ninguém vai abrir, ela vai tentar te ver de outro jeito.",
     S('quintal', cam=dict(zoom=1.2, to=1.35, cx=1330, cy=560))),
    ('nar', "Você vai ouvir um rangido comprido, que nem uma corda esticando. É o pescoço dela. Subindo por cima do muro, por cima dos cacos de vidro, até a altura da sua janela.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.0, to=1.15), fx=[dict(JANELA_QUARTO, surge=True)])),
    ('coisa', "Você deixou a bicicleta no quintal de novo.",
     S('quarto', cam=dict(zoom=1.35, to=1.5, cx=370, cy=300), fx=[JANELA_QUARTO])),
    ('nar', "Ela vai falar coisas que só quem mora aí sabe. Mas repara: é tudo coisa que dá pra ver da rua.",
     S('quarto', quarto(eyes='half', mouth='flat', look=-1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Os olhos dela não têm fundo. São dois buracos com um pontinho amarelo lá dentro. E, se você olhar pra eles, ela não precisa mais de resposta. O seu olhar já respondeu.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.1}, 'zoom_punch'])),
    ('nar', "Puxa o lençol por cima da cabeça. Vira pra parede. E conta as tábuas do forro, se precisar contar alguma coisa.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'NÃO ATENDA NEM O **CELULAR**')}])),
    ('nar', "Às cinco da manhã, o seu celular vai tocar. Na tela, o nome que você salvou quando ganhou o primeiro celular: Pai.",
     S('preto', fx=[{'celular': [('ela', 'Chamada de voz: Pai')]}])),
    ('nar', "Na fábrica, celular fica trancado no armário até o fim do turno. Sempre foi assim. O seu pai de verdade não pode te ligar às cinco da manhã.",
     S('quarto', quarto(eyes='wide', mouth='flat', arms='hold', prop='celular'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "E, se você prestar atenção, vai ouvir o mesmo toque. Baixinho. Vindo lá do portão.",
     S('quintal', cam=dict(zoom=1.2, to=1.4, cx=960, cy=560), fx=[dict(PORTAO, avanca=True)])),
    ('nar', "Atender o telefone também é atender. Deixa tocar até parar. Depois chega a mensagem.",
     S('preto', fx=[{'celular': [('ela', 'Chamada perdida: Pai (4)'), ('ela', 'atende filho. to no portao. ta frio')], 'vermelho': True}])),
    ('nar', "Não responde a mensagem. Não manda nem um ponto de interrogação. Apaga a tela e enfia o celular embaixo do travesseiro.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='hold', prop='celular'), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('coisa', "Filho... me assaltaram. Levaram tudo. Abre, pelo amor de Deus.",
     S('quintal', cam=dict(zoom=1.3, to=1.45, cx=1330, cy=420), fx=[dict(MURO, boca='flat')])),
    ('nar', "Esse é o pior momento da noite. Porque você ama o seu pai. E se fosse verdade?",
     S('quarto', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Mas pai assaltado não bate palma. Grita o seu nome inteiro, esmurra o portão, acorda a rua toda. E a Paçoca continua lá no fundo da casinha. Quieta.",
     S('quintal', cam=dict(zoom=1.0, to=1.1), fx=[{'cachorro': (330, 960, 'parado')}])),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'ESPERE A PAÇOCA **LATIR**')}])),
    ('nar', "Quando o céu ficar cinza, as palmas vão parar. Não sai ainda. Silêncio não quer dizer que ela foi embora.",
     S('quintal_manha', cam=dict(zoom=1.05, to=1.2, cx=960, cy=560), fx=[{'olhos': (960, 330), 'surge': True}])),
    ('nar', "Espera o freio do ônibus fretado lá na esquina. Espera os passos arrastados. Espera o barulho da corrente escorregando pela grade e o clique do cadeado abrindo.",
     S('preto', fx=[{'texto': ['06:20'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "E espera a Paçoca. Se ela sair da casinha latindo, pulando no portão, rodando atrás do rabo, aí sim. Aí pode correr.",
     S('quintal_manha', C('pai', 'b', None, facing=-1, arms='wave', mouth='smile'), cam=dict(zoom=1.0, to=1.1), fx=[{'cachorro': (980, 960, 'abana')}])),
    ('pai', "Ô, Paçoca! Que festa é essa? E você, filho, acordado uma hora dessas?",
     S('quintal_manha', C('pai', 'b', None, facing=-1, arms='down', mouth='smile', eyes='happy'), C('voce', 'a', None, arms='up', eyes='happy', mouth='grin'), cam=dict(zoom=1.1, to=1.2), fx=[{'cachorro': (980, 960, 'abana')}])),
    ('nar', "Abraça ele. Não conta nada. Não ainda.",
     S('quintal_manha', C('pai', 'b', None, facing=-1, mouth='smile', eyes='closed'), C('voce', 'a', None, eyes='half', mouth='flat'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('pai', "Fiz pão na chapa pra nós dois. Vem, entra que tá frio.",
     S('cozinha', C('pai', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile'), C('voce', 'a', None, eyes='half', mouth='smile'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Na mesa, ele vai reclamar da máquina que quebrou, do encarregado chato, do café ralo da fábrica. Você vai rir. E vai perceber como é bom ouvir essa voz de perto, com cheiro de graxa e de rua.",
     S('cozinha', C('pai', 'b', None, facing=-1, arms='shrug', mouth='grin'), C('voce', 'a', None, eyes='happy', mouth='grin'), cam=dict(zoom=1.15, to=1.25))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Na hora do almoço, a Dona Neide, a vizinha da frente, que mora sozinha, vem devolver a forma de bolo da sua mãe. E comenta, rindo:",
     S('porta', C('voce', 'a', None, eyes='half', mouth='smile'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Teu pai chegou cedo ontem, hein? Lá pelas três, bateu palma no meu portão. Disse que tinha esquecido a chave e pediu pra entrar e esperar o dia clarear.",
     S('cortina', cortina(eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.2, to=1.35, cx=760, cy=500))),
    ('nar', "Você pergunta se ela abriu. Ela dá de ombros. Diz que gritou da janela: já vou, seu Paulo. E, quando chegou no portão, não tinha mais ninguém na rua.",
     S('porta', C('voce', 'a', None, eyes='wide', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Desde esse dia, toda madrugada, às três e cinco, a luz da sala da Dona Neide acende. E tem alguém parado na janela dela. Alto demais pra ser ela. Olhando pro seu portão.",
     S('quintal', cam=dict(zoom=1.9, to=2.2, cx=1325, cy=390), fx=[{'monstro': 'janela', 'quem': Q, 'rect': (1270, 330, 110, 100), 'surge': True}])),
    ('nar', "Esperando alguém atender.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: alguém já bateu palma no seu portão de madrugada?",
     S('preto', fx=[{'cta_mm': ('JÁ BATERAM PALMA', 'NO SEU PORTÃO?')}])),
]
