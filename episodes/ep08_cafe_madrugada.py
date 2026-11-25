"""Manual da Madrugada — Noite 08
Se você sentir cheiro de café passado às 3h da manhã… NÃO VÁ À COZINHA
"""
from engine.dsl import S, C

TITLE = "Se você sentir cheiro de café passado às 3h da manhã… NÃO VÁ À COZINHA"
NOITE = 8
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='FIQUE NO **QUARTO**', cena='cafe', criatura='coisa_ep08', balao='Vem tomar café, filho.')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '914de72ccc244decb2fd1572808fa7e0',  # MM Mãe (imitando a mãe, com efeito)
    'mae': '914de72ccc244decb2fd1572808fa7e0',    # MM Mãe (a mãe de verdade, limpa)
    'voce': 'd703f08d1ef34302a36945aa3efc7b3f',   # Murilo
}

# a coisa desta noite: imita a mãe (padeira) de avental, alta demais, com um olho só no meio da testa, a boca aberta
# num buraco preto, a cabeça torta e os braços compridos. Está sempre com o bule de ágata na mão. Avental vermelho.
Q = 'coisa_ep08'
NO_FOGAO = {'monstro': 'fundo', 'quem': Q, 'pos': (1470, 900), 's': 0.6, 'escuro': 0.3}          # na cozinha, do lado do coador
NA_MESA = {'monstro': 'fundo', 'quem': Q, 'pos': (1230, 960), 's': 0.7, 'escuro': 0.2}           # do lado da mesa posta
NO_BALCAO = {'monstro': 'borda', 'quem': Q, 'pos': (430, 600), 's': 0.85}                         # espiando por cima da pia
NA_PORTA_COZINHA = {'monstro': 'fundo', 'quem': Q, 'pos': (1520, 830), 's': 0.47, 'escuro': 0.8}  # em contraluz no fim do corredor
NO_CORREDOR = {'monstro': 'fundo', 'quem': Q, 'pos': (1160, 900), 's': 0.55, 'escuro': 0.6, 'avanca': True}
NA_SUA_PORTA = {'monstro': 'fundo', 'quem': Q, 'pos': (600, 960), 's': 0.64, 'escuro': 0.45}     # do lado da sua porta, com a xícara no chão
PORTA_QUARTO = {'monstro': 'porta', 'quem': Q, 'rect': (760, 260, 230, 540), 'lado': 'esq', 'abre': 0.4}


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se você sentir cheiro de café passado às três da manhã, não vá até a cozinha. Não abra a porta do quarto. Não diga como você toma. E, aconteça o que acontecer, não beba nada que deixarem pra você.",
     S('cozinha_cafe', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(NO_FOGAO, surge=True)])),
    ('nar', "Eu não tô falando de domingo de manhã, quando a sua mãe passa café no coador de pano e a casa inteira acorda com o cheiro.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile', eyes='happy'), C('voce', 'a', None, mouth='smile', eyes='half'))),
    ('nar', "Também não tô falando do cheirinho que vem da padaria da esquina, às seis, quando você passa correndo pra não perder o ônibus.",
     S('corredor_cafe', C('voce', 'meio', None, mouth='smile', eyes='happy', facing=1), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "A sua mãe é padeira. De segunda a sábado, ela sai de casa às duas e meia da manhã, pra fornada das cinco ficar pronta antes de abrir a padaria.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='wave', mouth='smile'), C('voce', 'a', None, mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Ela nunca passa café em casa em dia de semana. Diz que o fogão é velho, que só acende no fósforo, e que café de padaria é outra coisa.",
     S('cozinha_vazia', cam=dict(zoom=1.2, to=1.35, cx=1550, cy=620))),
    ('nar', "Você ouviu quando ela saiu. O portão rangendo. A chave girando duas vezes no cadeado. O barulho da moto dela sumindo na rua.",
     S('quarto_cafe_manha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Você tem quinze anos. Já fica sozinho faz tempo. Toda noite, ela deixa um bilhete na geladeira: tem pão de ontem no armário, tranca a porta, te amo.",
     S('cozinha_vazia', cam=dict(zoom=1.4, to=1.5, cx=700, cy=560))),
    ('nar', "São três horas da manhã.",
     S('preto', fx=[{'texto': ['03:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "E você acorda com o cheiro. Café passadinho. Forte. Quente. Debaixo da sua porta, uma risca de luz amarela. E lá da cozinha, uma colher batendo na xícara. Tlim. Tlim. Tlim.",
     S('quarto_cafe', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.25, to=1.38, cx=1100, cy=640), fx=['piscar'])),
    ('nar', "Você conhece esse barulho. É a sua mãe mexendo o café dela nas manhãs de domingo. Três voltas pra um lado, três pro outro. Sem pressa nenhuma."),
    ('coisa', "Acordou, filho? A mãe passou um cafezinho. Vem, enquanto tá quente.",
     S('corredor_cafe', cam=dict(zoom=1.2, to=1.38, cx=1450, cy=560), fx=[dict(NA_PORTA_COZINHA, surge=True), 'zoom_punch'])),
    ('nar', "A voz da sua mãe. Mas a sua mãe tá do outro lado do bairro, com as mãos enfiadas na massa. E ninguém abriu o portão.",
     S('quarto_cafe', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá na sua cozinha mora nas casas onde alguém levanta de madrugada. Ela aprendeu tudo. O cheiro do pó. O barulho da água no coador. A voz de quem serve.",
     S('cozinha_cafe', cam=dict(zoom=1.1, to=1.25, cx=1250, cy=560), fx=[dict(NO_FOGAO, s=0.66)])),
    ('nar', "Ela não come. Ela não bebe. Ela só serve. Do mesmo jeito que tem gente que pesca com minhoca, ela pesca com cheiro.",
     S('cozinha_cafe', cam=dict(zoom=1.4, to=1.55, cx=960, cy=640))),
    ('nar', "Mas ela não sabe quem mora aqui. Nem quantos.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.6, 'surge': True}])),
    ('nar', "Por isso ela põe a mesa e espera. Cada xícara é um lugar. E quem senta na mesa dela e toma o café dela, não levanta mais.",
     S('cozinha_cafe', cam=dict(zoom=1.25, to=1.4, cx=1000, cy=640), fx=[dict(NA_MESA, surge=True)])),
    ('nar', "Tem uma coisa que ela não faz: ela não sai da cozinha enquanto o café tá quente. Ela não precisa ir até você. O cheiro vai.",
     S('corredor_cafe', cam=dict(zoom=1.05, to=1.2, cx=1200, cy=560))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe quando você acorda de madrugada com cheiro de comida, de bolo, de café, e não tem ninguém acordado em casa? Você acha que veio do vizinho. E volta a dormir.",
     S('quarto_cafe', quarto(eyes='half', mouth='flat', look=-1), cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Talvez tenha vindo mesmo do vizinho. Ou talvez alguém tenha passado um café pra você. E você só não foi.",
     S('cozinha_cafe', cam=dict(zoom=1.0, to=1.1), fx=[dict(NO_BALCAO, surge=True)])),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'FIQUE NO **QUARTO**')}])),
    ('nar', "Fique no quarto. Não vá até a cozinha. Nem pra beber água, nem pra ir ao banheiro, nem pra só dar uma olhadinha.",
     S('quarto_cafe', quarto(eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "O seu corpo vai querer ir. Cheiro de café às três da manhã é cheiro de casa, de gente acordada, de alguém cuidando de você. É exatamente por isso que ela usa.",
     S('corredor_cafe', cam=dict(zoom=1.1, to=1.3, cx=1400, cy=600))),
    ('nar', "Se você pisar na cozinha, a luz vai estar acesa, a mesa vai estar posta e vai ter uma cadeira puxada. Esperando você.",
     S('cozinha_cafe', cam=dict(zoom=1.3, to=1.45, cx=960, cy=660))),
    ('nar', "E a cadeira é sempre a sua. A da ponta, encostada na parede. A mesma que você senta desde pequeno."),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'TAPE A **FRESTA**')}])),
    ('nar', "Pega a toalha que tá pendurada atrás da porta, enrola e tapa a fresta de baixo. Bem apertada. Sem fazer barulho.",
     S('quarto_toalha', C('voce', 'porta', None, eyes='half', mouth='flat', arms='down', facing=1), cam=dict(zoom=1.2, to=1.3, cx=875, cy=640))),
    ('nar', "O cheiro é o chamado. Quanto mais você respira, mais você quer ir. Depois de um tempo, você não vai nem lembrar por que tava com medo. Vai achar que é a sua mãe mesmo. Que ela voltou mais cedo.",
     S('quarto_toalha', quarto(eyes='half', mouth='wavy'), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('nar', "E, quando a toalha tapar a fresta, a risca de luz some. Pra quem tá lá na cozinha, é como se o seu quarto tivesse apagado.",
     S('quarto_toalha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.3, to=1.4, cx=875, cy=700))),
    ('nar', "Se o cheiro ainda entrar, respira dentro da gola do moletom. Cheiro de amaciante. Cheiro seu. Ele não engana ninguém.",
     S('quarto_toalha', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(zoom=1.1, to=1.2))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO CORRIJA O **AÇÚCAR**')}])),
    ('nar', "Quando ela perceber que você não vem, ela vai fazer uma pergunta. Uma pergunta boba, de mãe.",
     S('cozinha_cafe', cam=dict(zoom=1.0, to=1.12))),
    ('coisa', "Quantas colheres de açúcar, filho? Duas, né? Você gosta com duas.",
     S('cozinha_cafe', cam=dict(zoom=1.3, to=1.45, cx=1300, cy=520), fx=[dict(NA_MESA, s=0.74), 'zoom_punch'])),
    ('nar', "Você não toma com duas. Você toma puro, sem açúcar, desde os doze anos. A sua mãe vive dizendo que é café de velho.",
     S('quarto_toalha', quarto(eyes='wide', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Ela errou de propósito. Ela quer que você corrija. Porque quem responde sem açúcar, mãe, conta três coisas de uma vez: que tá acordado, onde tá, e como gosta do café. E aí a xícara já tem dono.",
     S('quarto_toalha', quarto(eyes='closed', mouth='flat', arms='face', sweat=True), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Ela vai perguntar de novo. Mais alto. Meio irritada, do jeito que a sua mãe fica quando você finge que não ouviu. Morde a língua. Deixa ela errar.",
     S('cozinha_cafe', cam=dict(zoom=1.15, to=1.3, cx=1100, cy=600))),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO ABRA PRA **XÍCARA**')}])),
    ('nar', "Lá pelas quatro, o café começa a esfriar. A luz da cozinha começa a piscar. E aí ela sai.",
     S('corredor_frio', cam=dict(zoom=1.0, to=1.15), fx=[NO_CORREDOR, {'texto': ['04:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você vai ouvir o chinelo no piso do corredor. Devagar. E um tlim de louça, bem baixinho, bem na frente da sua porta.",
     S('corredor_frio', cam=dict(zoom=1.05, to=1.2, cx=700, cy=520), fx=[{'monstro': 'teto', 'quem': Q, 'pos': (640, 0), 's': 0.5, 'surge': True}])),
    ('coisa', "Deixei a sua xícara aqui na porta, filho. Pra você não ter que levantar.",
     S('corredor_xicara', cam=dict(zoom=1.2, to=1.35, cx=560, cy=620), fx=[dict(NA_SUA_PORTA, surge=True)])),
    ('nar', "Não abre. Se você abrir a porta pra pegar a xícara, ela não vai estar no fim do corredor. Ela vai estar ali. Abaixada. Com a cara na altura da sua.",
     S('quarto_toalha', cam=dict(zoom=1.15, to=1.3, cx=875, cy=560), fx=[dict(PORTA_QUARTO, surge=True)])),
    ('nar', "Se a toalha escorregar, você vai ver pela fresta a sombra dos pés dela. Dois pés parados. Compridos demais. Empurra a toalha de volta com o pé. E não olha.",
     S('quarto_cafe', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.4, to=1.55, cx=875, cy=760))),
    ('nar', "Deixa o café esfriar no chão. Café frio não chama ninguém.",
     S('quarto_toalha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'SE ELA SE QUEIMAR, **FIQUE**')}])),
    ('nar', "Quando nada funcionar, você vai ouvir a chaleira caindo no chão da cozinha. E um grito.",
     S('cozinha_fria', cam=dict(zoom=1.2, to=1.35, cx=1550, cy=620), fx=['shake'])),
    ('coisa', "Ai! Filho! Queimei a mão na chaleira! Traz a pomada, pelo amor de Deus!",
     S('cozinha_fria', cam=dict(zoom=1.2, to=1.35, cx=1350, cy=540), fx=[dict(NO_FOGAO, s=0.68, escuro=0.25, boca='flat')])),
    ('nar', "Esse é o pior momento da noite. Porque é a voz da sua mãe, chorando de dor. E tudo dentro de você vai gritar pra levantar e correr.",
     S('quarto_toalha', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Lembra: a sua mãe passa o dia inteiro do lado de um forno. Ela já se queimou cem vezes. Ela xinga o forno, enfia a mão na água fria e continua trabalhando. Ela nunca pediu socorro por causa de uma queimadura.",
     S('cozinha_vazia', cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Fica. Ela vai chorar até cansar. E choro que ninguém responde, uma hora, para.",
     S('quarto_toalha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.08))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'NÃO **DURMA**')}])),
    ('nar', "Depois disso, a casa fica quieta. Quieta demais. E você vai sentir um sono pesado, quentinho, que nem depois de um almoço de domingo.",
     S('quarto_toalha', quarto(eyes='half', mouth='flat'), cam=dict(focus='voce', zoom=1.4, to=1.55))),
    ('nar', "Não dorme. Se você dormir, você vai sonhar que tá na cozinha. Sentado na mesa. Com a xícara na mão.",
     S('cozinha_cafe', C('voce', 'mesa', None, sit=True, facing=1, eyes='half', mouth='flat', arms='hold', prop='caneca'), cam=dict(zoom=1.1, to=1.2), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (980, 960), 's': 0.66, 'escuro': 0.3, 'surge': True}])),
    ('nar', "No sonho, a cozinha é perfeita. O café tá no ponto. Ninguém tá com pressa. E a sua mãe tá ali, do seu lado, sorrindo. Só que ela não pisca. Nunca."),
    ('coisa', "Bebe, filho. Tá quentinho.",
     S('cozinha_cafe', C('voce', 'mesa', None, sit=True, facing=1, eyes='closed', mouth='flat', arms='hold', prop='caneca'), cam=dict(zoom=1.35, to=1.5, cx=820, cy=560), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (860, 960), 's': 0.7, 'escuro': 0.15}])),
    ('nar', "E no sonho, você bebe. E não acorda mais.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.1, 'escuro': 0.3}, 'zoom_punch'])),
    ('nar', "Então abre a janela. Deixa o vento gelado da madrugada bater na sua cara. Belisca o braço. Conta os carros que passam lá fora. Mas fica acordado.",
     S('quarto_toalha', quarto(eyes='wide', mouth='flat', arms='point', look=-1), cam=dict(zoom=1.05, to=1.15, cx=700, cy=540))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'ESPERE O **FÓSFORO**')}])),
    ('nar', "Quando o céu começar a clarear, você vai ouvir o portão. A moto. A chave girando duas vezes. E a voz da sua mãe, chamando o seu nome.",
     S('quarto_cafe_manha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1), fx=[{'texto': ['06:20'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Ainda não sai. Não abre a porta quando ouvir o seu nome. Fica sentado na cama. E escuta.",
     S('quarto_cafe_manha', quarto(eyes='half', mouth='flat', look=-1), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('nar', "A coisa sabe a voz, sabe o portão, sabe o barulho da chave. Mas tem uma coisa que ela não sabe fazer. Ela nunca acende o fogo.",
     S('preto', fx=[{'olhos': (960, 470), 'surge': True}])),
    ('nar', "O café dela fica pronto sozinho. Sem fogo, sem chaleira apitando, sem fósforo. Espera o barulho que só a sua mãe faz.",
     S('cozinha_vazia', cam=dict(zoom=1.3, to=1.45, cx=1600, cy=640))),
    ('nar', "O risco do fósforo. A boca do fogão estalando. E ela reclamando, do jeito de sempre:",
     S('cozinha_manha', C('mae', 'b', None, facing=1, arms='hold', mouth='flat', eyes='angry'), cam=dict(focus='mae', zoom=1.4, to=1.5))),
    ('mae', "Esse fogão velho ainda me mata! Filho? Acorda, que eu trouxe pão quentinho!",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='hold', prop='sacola', mouth='smile', eyes='happy'), cam=dict(focus='mae', zoom=1.5, to=1.6))),
    ('nar', "Aí sim. Aí pode tirar a toalha da porta e correr pra cozinha. Com cheiro de pão e de farinha.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='up', mouth='smile', eyes='closed'), C('voce', 'a', None, arms='up', eyes='happy', mouth='grin'), cam=dict(zoom=1.05, to=1.12))),
    ('nar', "Ela vai rir da sua cara amassada e perguntar se você virou a noite no celular. Fala que sim. Ela não precisa saber.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='hip', mouth='grin', eyes='happy'), C('voce', 'a', None, eyes='half', mouth='smile'), cam=dict(zoom=1.2, to=1.3, cx=950, cy=620))),
    ('nar', "No chão do corredor, na frente da sua porta, não tem xícara nenhuma. Só uma rodinha de café seco no piso.",
     S('corredor_mancha', cam=dict(zoom=1.5, to=1.7, cx=420, cy=840))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "No domingo, a sua mãe passa café. Do jeito dela, no coador de pano. Ela põe a mesa pra vocês dois. Mas quando você senta, tem três xícaras.",
     S('cozinha_domingo', C('mae', 'mesa2', None, sit=True, facing=-1, mouth='smile', eyes='half'), C('voce', 'mesa', None, sit=True, facing=1, eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('voce', "Mãe, pra quem é essa?",
     S('cozinha_domingo', C('mae', 'mesa2', None, sit=True, facing=-1, mouth='flat', eyes='half'), C('voce', 'mesa', None, sit=True, facing=1, eyes='wide', mouth='flat', arms='point'), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('mae', "Sei lá, filho. Força do hábito. Essa semana, toda vez que eu chego da padaria, tem uma xícara a mais no escorredor. Lavadinha. E ainda morna.",
     S('cozinha_domingo', C('mae', 'mesa2', None, sit=True, facing=-1, mouth='flat', eyes='half'), C('voce', 'mesa', None, sit=True, facing=1, eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.08, to=1.18, cx=960, cy=520), fx=[{'monstro': 'janela', 'quem': Q, 'rect': (700, 200, 240, 200), 'surge': True, 'escuro': 0.2}])),
    ('nar', "Você olha pro escorredor. Tem uma xícara lá, de boca pra baixo. E por baixo dela, bem devagar, tá saindo vapor.",
     S('cozinha_domingo', cam=dict(zoom=1.7, to=1.85, cx=580, cy=540))),
    ('nar', "Hoje é domingo. Ela vai dormir cedo. E às três da manhã, você sente o cheiro.",
     S('quarto_cafe', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[{'texto': ['03:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Senta, filho. Guardei o seu lugar.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 2.7, 'pos': (960, 600), 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: você ia conseguir não corrigir o açúcar?",
     S('preto', fx=[{'cta_mm': ('VOCÊ CORRIGIRIA', 'O AÇÚCAR?')}])),
]
