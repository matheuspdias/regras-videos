"""Manual da Madrugada — Noite 01
Se sua mãe te chamar pelo nome completo de dentro de um quarto vazio… NÃO RESPONDA
"""
from engine.dsl import S, C

TITLE = "Se sua mãe te chamar pelo nome completo de dentro de um quarto vazio… NÃO RESPONDA"
NOITE = 1
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 20.0
THUMB = dict(ordem='NÃO **RESPONDA**', cena='corredor', esquerda=('voce', dict(eyes='wide', mouth='o', arms='face', sweat=True)),
             criatura_porta=True, balao='Lucas Henrique?')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '914de72ccc244decb2fd1572808fa7e0',  # MM Mãe (com efeito)
    'mae': '914de72ccc244decb2fd1572808fa7e0',    # MM Mãe (limpa)
}

V = (940, 230)       # de onde vem a voz no corredor (porta do meio)
VQ = (1590, 380)     # porta entreaberta do quarto da mãe


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se a sua mãe te chamar pelo nome completo de dentro de um quarto vazio, não responda. Não diga senhora. Não acenda a luz. E, aconteça o que acontecer, não vá ver o que ela quer.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.12), fx=['piscar'])),
    ('nar', "Eu não tô falando de quando ela grita o seu nome da cozinha porque você deixou a toalha molhada em cima da cama.",
     S('cozinha', C('mae', 'b', None, facing=-1, eyes='angry', arms='hip', mouth='o'), C('voce', 'a', None, eyes='half', mouth='flat'))),
    ('nar', "Também não tô falando de quando ela chama do portão pra você ajudar com as sacolas do mercado.",
     S('porta', C('mae', 'b', None, facing=-1, arms='wave', mouth='smile'), C('voce', 'a', None, mouth='smile'))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "Sua mãe é enfermeira. Hoje é noite de plantão. Ela saiu às sete, deixou a janta no micro-ondas e mandou mensagem às dez dizendo que o hospital tá cheio.",
     S('sala', C('mae', 'porta', None, facing=-1, arms='wave', mouth='smile'), C('voce', 'sofa', None, sit=True, mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Você tá sozinho em casa com o seu irmão mais novo, o Théo. E com a Pipoca, que dorme no pé da sua cama.",
     S('quarto', quarto(mouth='smile', eyes='half'), C('irmao', 'centro', None, mouth='smile'), fx=[{'cachorro': (1720, 830, 'parado')}])),
    ('nar', "São duas e quarenta da manhã. A casa tá quieta.",
     S('corredor', cam=dict(zoom=1.0, to=1.1), fx=[{'texto': ['02:40'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "E aí, do quarto da sua mãe, o quarto que você mesmo viu vazio antes de dormir, com a cama arrumada, vem a voz dela.",
     S('quarto_mae', cam=dict(zoom=1.05, to=1.2, cx=700, cy=600))),
    ('coisa', "Lucas Henrique Ferreira da Silva!",
     S('corredor', cam=dict(zoom=1.3, to=1.45, cx=940, cy=500), fx=[{'voz': V}, 'zoom_punch'])),
    ('nar', "O seu nome inteiro. Com todos os sobrenomes. No mesmo tom de quando você fez alguma coisa muito errada.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "Ninguém abriu o portão. Ninguém girou a chave. A Pipoca não latiu. Só a voz. Do lado de lá de uma porta que deveria estar vazia.",
     S('corredor', cam=dict(zoom=1.15, to=1.35, cx=940, cy=540), fx=['piscar'])),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá naquele quarto conhece a voz da sua mãe. Conhece a casa. Sabe onde fica cada degrau e cada interruptor.",
     S('quarto_mae', cam=dict(zoom=1.0, to=1.15), fx=[{'olhos': (1590, 560), 'surge': True}])),
    ('nar', "Mas ela não sabe quem você é.",
     S('preto', fx=[{'olhos': (960, 520), 'surge': True}])),
    ('nar', "Apelido, qualquer um tem. Tem um monte de Lucas na sua escola. Mas o nome completo, aquele com todos os sobrenomes, só pertence a uma pessoa. E ela tá testando.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Quando ela chama o seu nome inteiro, ela não tá te chamando. Ela tá perguntando: esse nome é seu? E o único jeito de você dizer que sim é respondendo.",
     S('corredor', cam=dict(zoom=1.2, to=1.4, cx=940, cy=520), fx=[{'olhos': (940, 470)}])),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe aquela vez em que você acordou de madrugada com a certeza de que alguém tinha te chamado? Você ficou esperando, ouvindo. E não tinha ninguém.",
     S('quarto', quarto(eyes='wide', mouth='flat', look=-1), cam=dict(zoom=1.0, to=1.15))),
    ('nar', "Talvez você tenha tido sorte. Talvez você tenha dormido de novo antes de responder.",
     S('quarto', quarto(eyes='closed', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.65))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO **RESPONDA**')}])),
    ('nar', "Não responda. Nem senhora. Nem oi. Nem já vou.",
     S('quarto', quarto(eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Isso é mais difícil do que parece. Você passou a vida inteira respondendo senhora quando a sua mãe chama. A sua boca vai querer responder sozinha. Morde a língua, se precisar.",
     S('quarto', quarto(eyes='closed', mouth='wavy', arms='face', sweat=True), cam=dict(zoom=1.2, to=1.3))),
    ('nar', "Se você ficar em silêncio, ela vai chamar de novo. Talvez mais baixo. Talvez com carinho.",
     S('corredor', cam=dict(zoom=1.1, to=1.25))),
    ('coisa', "Lucas Henrique... vem cá, filho.",
     S('corredor', cam=dict(zoom=1.35, to=1.5, cx=940, cy=500), fx=[{'voz': V}])),
    ('nar', "Continua quieto. Cada vez que ela chama e ninguém responde, ela fica um pouco menos certa de que você está na casa.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO ACENDA A **LUZ**')}])),
    ('nar', "Não acenda nenhuma luz. Nem a do quarto, nem a do corredor, nem a lanterna do celular.",
     S('quarto', quarto(eyes='wide', arms='hold', prop='celular'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Do quarto da sua mãe dá pra ver a fresta debaixo de todas as portas. Uma fresta acesa às três da manhã é a mesma coisa que dizer: tem alguém acordado aqui.",
     S('corredor_luz', cam=dict(zoom=1.0, to=1.12), fx=[{'olhos': (940, 470), 'surge': True}])),
    ('nar', "Abaixa o brilho da tela. Vira o celular pra parede. Fica no escuro. O escuro, essa noite, tá do seu lado.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='hold', prop='celular'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'PROTEJA O **THÉO**')}])),
    ('nar', "Se ela parar de chamar o seu nome e começar a chamar o nome do seu irmão, levanta devagar e vai até o quarto dele.",
     S('corredor', C('voce', 'p1', None, eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('coisa', "Théo Gabriel Ferreira da Silva...",
     S('corredor', C('voce', 'p1', None, eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.2, to=1.3, cx=700, cy=540), fx=[{'voz': V}])),
    ('nar', "Não corre. Pisa na beirada do piso, perto da parede, onde a madeira não range. O Théo tem oito anos. Ele ainda responde tudo.",
     S('corredor', C('voce', 'meio', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Senta do lado dele. Se ele acordar, coloca o dedo na frente da boca. E, se ele já estiver com a boca aberta pra responder, tapa com a mão. Com carinho. Mas tapa.",
     S('quarto', C('irmao', 'cama', None, sit=True, facing=-1, eyes='wide', mouth='o'), C('voce', 'centro', None, eyes='angry', mouth='flat', arms='point'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Ele vai ficar bravo com você amanhã. Deixa ele ficar bravo.",
     S('quarto', C('irmao', 'cama', None, sit=True, facing=-1, eyes='angry', mouth='frown'), C('voce', 'centro', None, eyes='half', mouth='smile'), cam=dict(focus='irmao', zoom=1.5, to=1.6))),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'MANDE **MENSAGEM**')}])),
    ('nar', "Mande mensagem pra sua mãe. Não ligue. Uma ligação faz barulho. E a voz que atende do outro lado conta pra casa inteira onde você tá.",
     S('quarto', quarto(eyes='half', arms='hold', prop='celular'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Escreve só isso: mãe, a senhora tá em casa?",
     S('preto', fx=[{'celular': [('eu', 'mãe, a senhora tá em casa?')]}])),
    ('nar', "Se ela não responder, tá tudo bem. Ela tá no meio do plantão, correndo de um leito pro outro. Isso é bom. Isso é normal.",
     S('preto', fx=[{'celular': [('eu', 'mãe, a senhora tá em casa?')]}])),
    ('nar', "Mas, se a resposta chegar rápido demais, olha como ela te chamou. A sua mãe, a de verdade, escreve que nem mãe: tudo em minúscula, cheio de figurinha, te chamando de Lu.",
     S('preto', fx=[{'celular': [('eu', 'mãe, a senhora tá em casa?'), ('ela', 'oi lu, tô no plantão ainda, dorme filho')]}])),
    ('nar', "Se a mensagem chegar te chamando de Lucas Henrique Ferreira da Silva... vira o celular pra baixo. E não responde mais nada.",
     S('preto', fx=[{'celular': [('eu', 'mãe, a senhora tá em casa?'), ('ela', 'Lucas Henrique Ferreira da Silva. Vem no meu quarto.')], 'vermelho': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'NÃO ABRA PRA **PIPOCA**')}])),
    ('nar', "Se a Pipoca descer da cama e for até a porta do quarto da sua mãe, não vai atrás dela. Ela vai abanar o rabo. Vai arranhar a porta, do jeitinho que faz quando a sua mãe chega do trabalho.",
     S('corredor', cam=dict(zoom=1.1, to=1.22), fx=[{'cachorro': (760, 960, 'abana')}])),
    ('nar', "Cachorro não se engana com cheiro. Mas se engana com voz. E a coisa sabe imitar a voz que a Pipoca mais ama.",
     S('corredor', cam=dict(zoom=1.3, to=1.45, cx=900, cy=600), fx=[{'cachorro': (760, 960, 'abana')}, {'olhos': (940, 470), 'surge': True}])),
    ('nar', "Chama a Pipoca de volta sem falar. Estala os dedos. Bate de leve no colchão. E, se ela não vier, deixa ela lá. Ela vai ficar bem. Ninguém lá dentro quer a Pipoca.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='point'), cam=dict(zoom=1.1, to=1.2))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'SE ELA CHORAR, **FIQUE**')}])),
    ('nar', "Em algum momento, ela vai mudar de estratégia. A voz não vai mais brigar. Ela vai chorar.",
     S('corredor', cam=dict(zoom=1.1, to=1.3), fx=['piscar'])),
    ('coisa', "Filho... eu caí. Eu não consigo levantar. Me ajuda, por favor.",
     S('corredor', cam=dict(zoom=1.3, to=1.45, cx=940, cy=520), fx=[{'voz': V}])),
    ('nar', "Esse é o pior momento da noite. Porque você ama a sua mãe. E tudo dentro de você vai gritar pra levantar e ir.",
     S('quarto', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Lembra de uma coisa: mãe machucada grita de dor. Fala palavrão. Pede pra você ligar pro SAMU. Mãe machucada não chama ninguém pelo nome completo.",
     S('quarto', quarto(eyes='angry', mouth='flat'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Fica onde você tá. Abraça o Théo. Conta as respirações dele. Ela vai chorar até cansar. E coisa que chora sem resposta, uma hora, desiste.",
     S('quarto', C('irmao', 'cama', None, sit=True, facing=-1, eyes='closed'), C('voce', 'centro', None, eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.12))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'SÓ ABRA PRA QUEM TEM A **CHAVE**')}])),
    ('nar', "Quando o dia começar a clarear, a voz vai mudar de lugar. Vai sair do quarto da sua mãe e vai pra porta da frente.",
     S('porta', cam=dict(zoom=1.0, to=1.12))),
    ('coisa', "Lu, abre aqui pra mim. Esqueci a chave.",
     S('porta', cam=dict(zoom=1.25, to=1.4, cx=960, cy=470), fx=[{'voz': (960, 230)}])),
    ('nar', "Ela agora te chama de Lu. Ela aprendeu. Ela passou a noite inteira ouvindo a casa.",
     S('porta', C('voce', 'a', None, eyes='wide', mouth='flat', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Não abre. A sua mãe nunca esqueceu a chave na vida. Ela tem uma cópia na bolsa, outra no carro e outra com a vizinha.",
     S('porta', C('voce', 'a', None, eyes='angry', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Espera o barulho. Primeiro o portão. Depois o molho de chaves batendo. Depois a chave entrando na fechadura e girando duas vezes, porque ela sempre tranca duas vezes.",
     S('preto', fx=[{'fechadura': True}])),
    ('nar', "A coisa sabe imitar qualquer voz. Mas não sabe usar chave. Ela só sabe chamar.",
     S('porta', cam=dict(zoom=1.2, to=1.3, cx=960, cy=470), fx=[{'olhos': (960, 300), 'surge': True}])),
    ('nar', "Quando a porta abrir por fora, com cheiro de hospital e café de máquina, aí sim. Aí pode correr.",
     S('sala_manha', C('mae', 'porta', None, facing=-1, mouth='smile', eyes='half'), C('voce', 'centro', None, arms='up', eyes='happy', mouth='grin'), cam=dict(zoom=1.0, to=1.08))),
    ('mae', "Ué, que abraço é esse? Aconteceu alguma coisa?",
     S('sala_manha', C('mae', 'sofa2', None, facing=-1, mouth='smile'), C('voce', 'sofa', None, facing=1, eyes='closed', mouth='smile'), cam=dict(zoom=1.3, to=1.4, cx=940, cy=560))),
    ('nar', "Não conta nada pra ela. Pelo menos não ainda.",
     S('sala_manha', C('mae', 'sofa2', None, facing=-1, mouth='smile', eyes='half'), C('voce', 'sofa', None, facing=1, eyes='half', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.6))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Umas semanas depois dessa noite, você vai perceber que a sua mãe parou de te chamar pelo nome completo. Nem quando você deixa a toalha molhada em cima da cama. Nem quando ela tá muito brava.",
     S('cozinha', C('mae', 'b', None, facing=-1, eyes='half', mouth='flat', arms='cross'), C('voce', 'a', None, eyes='half'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "E um dia você pergunta por quê. Ela fica quieta um tempo. Mexe no café. E diz, sem olhar pra você:",
     S('cozinha', C('mae', 'b', None, facing=-1, eyes='closed', mouth='flat', arms='hold', prop='caneca'), C('voce', 'a', None, eyes='wide'), cam=dict(focus='mae', zoom=1.5, to=1.65))),
    ('mae', "Porque, numa noite de plantão, eu liguei pra casa. E quem atendeu foi a minha voz. Me chamando pelo meu nome completo.",
     S('cozinha', C('mae', 'b', None, facing=-1, eyes='sad', mouth='flat'), C('voce', 'a', None, eyes='wide', mouth='o'), cam=dict(focus='mae', zoom=1.7, to=1.8))),
    ('nar', "E ela respondeu.",
     S('preto', fx=[{'olhos': (960, 520), 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: qual dessas regras você quebraria primeiro?",
     S('preto', fx=[{'cta_mm': ('QUAL REGRA VOCÊ', 'QUEBRARIA PRIMEIRO?')}])),
]
