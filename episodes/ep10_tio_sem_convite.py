"""Manual da Madrugada — Noite 10
Se o seu tio aparecer pra dormir na sua casa sem ninguém ter convidado… NÃO MOSTRE O SEU QUARTO
"""
from engine.dsl import S, C

TITLE = "Se o seu tio aparecer pra dormir na sua casa sem ninguém ter convidado… NÃO MOSTRE O SEU QUARTO"
NOITE = 10
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='NÃO MOSTRE **SEU QUARTO**', cena='sofa', criatura='coisa_ep10', balao='Qual é o seu quarto?')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '9ce5f601f9e04382bb26141d5a3f839d',  # Afonso (imitando o tio Dirceu, com efeito)
    'tio': '9ce5f601f9e04382bb26141d5a3f839d',    # Afonso (o tio Dirceu de verdade, no viva-voz, limpo)
    'mae': '914de72ccc244decb2fd1572808fa7e0',    # MM Mãe (limpa)
}

# a coisa desta noite: imita o tio Dirceu (irmão do seu pai, mora em Porto Velho) de camisa social e chapéu de aba,
# alto e magro demais, pescoço comprido, cabeça torta, quatro olhos e boca em fenda; sempre com a mala vermelha na mão
# (o único vermelho). Ela passou anos no portão ouvindo a casa: sabe vozes e nomes, mas por dentro só conhece o que
# alguém mostrar — e não sabe o SEU nome (por isso te chama de "sobrinho").
Q = 'coisa_ep10'
LONGE = {'monstro': 'fundo', 'quem': Q, 'pos': (1520, 830), 's': 0.46, 'escuro': 0.78}          # fim do corredor
JANELA_ENTRADA = {'monstro': 'janela', 'quem': Q, 'rect': (300, 240, 260, 360)}                  # janela da porta de entrada
NO_SOFA_ESCURO = {'monstro': 'fundo', 'quem': Q, 'pos': (1100, 860), 's': 0.72, 'escuro': 0.62, 'sentado': True}
NA_CAMA = {'monstro': 'borda', 'quem': Q, 'pos': (1500, 752), 's': 0.78}                          # pé da sua cama
ENCOSTO = {'monstro': 'borda', 'quem': Q, 'pos': (1000, 522), 's': 0.7, 'escuro': 0.35}           # por cima do encosto do sofá
NO_CORREDOR = {'monstro': 'fundo', 'quem': Q, 'pos': (940, 965), 's': 0.6, 'escuro': 0.45}       # no meio do corredor
BANHEIRO = {'monstro': 'porta', 'quem': Q, 'rect': (240, 280, 240, 540), 'lado': 'dir', 'abre': 0.35}
TETO = {'monstro': 'teto', 'quem': Q, 'pos': (1150, 0), 's': 0.62, 'bracos': 'down'}
QUARTINHO = {'monstro': 'borda', 'quem': Q, 'pos': (1330, 742), 's': 0.8}


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


def tio(**p):
    d = dict(sit=True, facing=-1, mouth='grin')
    d.update(p)
    return C(Q, 'visita', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se o seu tio aparecer pra dormir na sua casa sem ninguém ter convidado, não mostre o seu quarto. Não diga o seu nome. Não aponte pra sua porta. E não deixe ele te ver entrando nela.",
     S('corredor_tio', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(LONGE, surge=True)])),
    ('nar', "Eu não tô falando do tio que avisa no grupo da família e chega com uma caixa de manga.",
     S('porta_manha', C('vizinho', 'porta', None, arms='wave', mouth='grin', prop='sacola'), C('voce', 'a', None, mouth='smile', eyes='happy'))),
    ('nar', "Nem do padrinho que cochila no sofá depois do almoço de domingo.",
     S('sala_manha', C('vizinho', 'sofa', None, sit=True, eyes='closed', mouth='o'), C('voce', 'centro', None, mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "Sábado, quase meia-noite. Os seus pais dormem no quarto do fundo, e o seu quarto é a porta do meio do corredor. A campainha toca uma vez só.",
     S('corredor_tio_escuro', cam=dict(zoom=1.05, to=1.18, cx=940, cy=560), fx=[{'texto': ['23:52'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Ô de casa! Sou eu, o tio Dirceu! Vim de longe. Deixa eu dormir aí só hoje?",
     S('porta', cam=dict(zoom=1.3, to=1.45, cx=520, cy=460), fx=[dict(JANELA_ENTRADA, surge=True), 'zoom_punch'])),
    ('nar', "O tio Dirceu é irmão do seu pai e mora em Porto Velho. Faz seis anos que ninguém vê ele. E ninguém lembra de ter falado com ele essa semana.",
     S('porta', C('voce', 'b', None, eyes='wide', mouth='flat', facing=-1), cam=dict(zoom=1.0, to=1.1), fx=[JANELA_ENTRADA])),
    ('nar', "Mas o seu pai, de chinelo e meio dormindo, reconhece a voz do irmão. Abre o portão, dá um abraço sem acender a luz da garagem. E a sua mãe arruma o sofá com lençol limpo.",
     S('sala_tio', C(Q, 'porta', None, facing=-1, mouth='grin'), C('pai', 'centro', None, arms='wave', mouth='smile', eyes='half'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Você vê tudo do corredor. E repara numa coisa. Ele chama o seu pai de Toninho. Chama a sua mãe pelo nome. Mas olha pra você e diz só: e aí, sobrinho.",
     S('sala_tio', tio(), C('voce', 'corredor', None, eyes='wide', mouth='flat', facing=1), cam=dict(zoom=1.05, to=1.15))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá no seu sofá passou anos do lado de fora, no portão, ouvindo. Ela sabe a voz de cada parente, o nome de cada um e a hora em que a casa apaga.",
     S('sala_tio_escuro', cam=dict(zoom=1.0, to=1.15), fx=[dict(NO_SOFA_ESCURO, surge=True)])),
    ('nar', "Mas ela nunca tinha entrado. Por dentro, ela só conhece o que alguém mostrar. E ela não sabe quem você é. Nem o seu nome.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.6, 'surge': True}])),
    ('nar', "Ela não quer o sofá. Nem o quartinho dos fundos, cheio de caixa, que não é de ninguém. Ela veio por causa do seu quarto. Se descobrir qual porta é a sua, hoje ela dorme lá.",
     S('quarto', cam=dict(zoom=1.0, to=1.12), fx=[dict(NA_CAMA, surge=True)])),
    ('nar', "E amanhã, quem acorda na sua cama é ela, com a sua cara e a sua voz. E você acorda no sofá da sala, com uma mala vermelha do lado. E ninguém da casa lembra de ter te convidado.",
     S('sala_tio_manha', C('voce', 'sofa', None, sit=True, eyes='wide', mouth='o', sweat=True, prop='mala', arms='hold', facing=1), cam=dict(focus='voce', zoom=1.3, to=1.45))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe aquele parente que aparece em todo aniversário, que todo mundo abraça, e que na volta, no carro, ninguém sabe dizer de que lado da família ele é?",
     S('sala_manha', C('pai', 'sofa', None, sit=True, eyes='half', mouth='flat', facing=1), C('mae', 'sofa2', None, sit=True, eyes='half', mouth='flat', arms='shrug', facing=-1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Ninguém pergunta. Dá vergonha perguntar. E ele sempre vai embora depois de conhecer a casa inteira.",
     S('corredor_tio', cam=dict(zoom=1.1, to=1.25, cx=1100, cy=560))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO MOSTRE O **SEU QUARTO**')}])),
    ('nar', "Não mostre o seu quarto. Ele vai pedir de um jeito simpático, de tio, com o chapéu na mão e o sorriso esticado demais.",
     S('corredor_tio', C('voce', 'p1', None, eyes='wide', mouth='flat', facing=-1), cam=dict(zoom=1.05, to=1.15))),
    ('coisa', "Qual é o seu quarto, sobrinho? Quero ver como você cresceu.",
     S('sala_tio', tio(mouth='grin'), C('voce', 'corredor', None, eyes='wide', mouth='flat', sweat=True, facing=1), cam=dict(zoom=1.2, to=1.32, cx=900, cy=520))),
    ('nar', "Não aponta. Não diz é a do meio. E não olha pro corredor, porque o olho da gente vai sozinho pra própria porta. Diz só: amanhã eu te mostro, tio. Amanhã ele já foi.",
     S('sala_tio', C('voce', 'centro', None, eyes='half', mouth='flat', facing=1), cam=dict(focus='voce', zoom=1.5, to=1.62))),
    ('nar', "E nunca diga o seu nome. Se ele perguntar como é mesmo que te chamam, ri e muda de assunto. Quem não sabe o seu nome não sabe qual cama é sua.",
     S('corredor_tio', C('voce', 'p2', None, eyes='angry', mouth='flat', facing=-1), cam=dict(zoom=1.1, to=1.22))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO ENTRE COM ELE **OLHANDO**')}])),
    ('nar', "Do sofá dá pra ver o corredor inteiro. E ele não vai dormir. Vai ficar deitado de lado, com o lençol até o queixo, de olho aberto. Os quatro.",
     S('sala_tio_escuro', cam=dict(zoom=1.1, to=1.25, cx=1000, cy=480), fx=[dict(ENCOSTO, surge=True)])),
    ('nar', "Então não vai direto pro seu quarto. Vai até a cozinha, bebe um copo d'água, entra no banheiro, dá descarga. Faz ele pensar que você tá só andando pela casa.",
     S('cozinha', C('voce', 'a', None, eyes='half', mouth='flat', arms='hold', prop='caneca'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Se ele perguntar aonde você vai, diz que vai fazer xixi. Banheiro não é quarto de ninguém.",
     S('sala_tio_escuro', tio(mouth='grin'), C('voce', 'corredor', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Espera o ronco. Ronco de verdade, comprido, daqueles que fazem o sofá ranger. Só aí você atravessa o corredor de meia, encostado na parede, e entra sem acender a luz.",
     S('corredor_tio_escuro', C('voce', 'p2', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Se ele ouvir a sua porta fechando, ele não vai saber se foi a do banheiro, a dos seus pais ou a sua. Porta fechando, de madrugada, é tudo igual.",
     S('corredor_tio_escuro', cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO LEVE **NADA** PRA ELE')}])),
    ('nar', "Depois de uma hora, ele vai sentir frio. Ou sede. Ou vai querer um travesseiro mais macio. E vai chamar baixinho, na direção do corredor.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('coisa', "Sobrinho? Me traz o seu cobertor? Tá frio aqui na sala.",
     S('sala_tio_escuro', tio(mouth='grin'), cam=dict(zoom=1.25, to=1.4, cx=1100, cy=520))),
    ('nar', "Não leva nada. Nem cobertor, nem copo d'água, nem o travesseiro do armário. Tudo que sai do seu quarto leva o cheiro dele. E cheiro mostra o caminho de volta.",
     S('quarto', quarto(eyes='angry', mouth='flat', arms='hold'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "Visita de verdade, quando passa frio, pega a toalha do banheiro e se vira. Visita de verdade não pede nada do quarto dos outros.",
     S('corredor_tio_escuro', cam=dict(zoom=1.05, to=1.15, cx=360, cy=560))),

    # ---------------------------------------------------------------- PEDIDO DE INSCRIÇÃO (teste E2)
    ('nar', "Antes da regra quatro: se você ainda tá acordado, se inscreve. O próximo manual chega amanhã, às oito da noite.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.08), fx=[{'texto': ['INSCREVA-SE'], 'pos': 'topo', 'cor': '#E5262B'}])),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO RESPONDA DE **DENTRO**')}])),
    ('nar', "Lá pelas três, o sofá para de ranger. E você ouve passos no corredor. Passos devagar, de quem não sabe o caminho.",
     S('corredor_tio_escuro', cam=dict(zoom=1.0, to=1.12), fx=[dict(LONGE, avanca=True, s=0.5), {'texto': ['03:00'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Ele vai abrir a porta do banheiro e olhar lá dentro. Depois vai bater de leve na porta dos seus pais. Depois na sua. E em cada porta ele pergunta a mesma coisa.",
     S('corredor_tio', cam=dict(zoom=1.15, to=1.3, cx=500, cy=560), fx=[dict(BANHEIRO, surge=True)])),
    ('coisa', "Sobrinho? É aqui que você dorme?",
     S('corredor_tio_escuro', cam=dict(zoom=1.3, to=1.45, cx=940, cy=540), fx=[NO_CORREDOR, 'zoom_punch'])),
    ('nar', "Não responde. Nem não. Nem um gemido de sono. Uma voz de dentro de um quarto conta pra ele quem dorme ali. Silêncio é porta de armário. Silêncio é quarto vazio.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.6))),
    ('nar', "Se a maçaneta girar, não se mexe. Ele não entra em quarto nenhum sem ter certeza. Ele só quer ouvir a sua voz do outro lado.",
     S('quarto', cam=dict(zoom=1.3, to=1.45, cx=875, cy=540), fx=['shake'])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Ele vai ficar parado do lado de fora um tempão. Pela fresta de baixo da porta, você vê a sombra de dois pés compridos demais. E a ponta de uma mala, encostada no chão.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True, arms='face'), cam=dict(zoom=1.15, to=1.3, cx=1100, cy=600))),
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'NÃO **CORRIJA** O TIO')}])),
    ('nar', "Quando nenhuma porta responder, ele muda de jeito. Ele começa a adivinhar. Em voz alta, do meio do corredor, bem calmo.",
     S('corredor_tio_escuro', cam=dict(zoom=1.0, to=1.1, cx=1100, cy=500))),
    ('coisa', "Seu quarto é o do fundo, né? O da cortina azul? Com a cama do lado da porta?",
     S('corredor_tio_escuro', cam=dict(zoom=1.0, to=1.1), fx=[dict(TETO, surge=True)])),
    ('nar', "Tudo errado. E vai dar uma coceira enorme de corrigir. É assim que ela pega a gente: errando de propósito. Não corrige. Correção também é resposta.",
     S('quarto', quarto(eyes='angry', mouth='wavy', arms='face', sweat=True), cam=dict(focus='voce', zoom=1.4, to=1.5))),
    ('nar', "Ele vai falar da sua parede, do seu armário, do cheiro do seu travesseiro. Tudo inventado. Tudo pra você sussurrar: não, tio, não é assim.",
     S('corredor_tio_escuro', cam=dict(zoom=1.05, to=1.15, cx=940, cy=500))),
    ('nar', "E, se ele acertar alguma coisa, o lado da cama, a cor da parede, também não reage. Ele tá chutando. Ele só sabe o que você deixou escapar.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'NÃO DÊ A SUA **CAMA**')}])),
    ('nar', "Perto das quatro, você ouve um baque no corredor. Alguém caindo. E uma respiração chiando, curta, do lado de fora.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.1, to=1.25), fx=['shake'])),
    ('coisa', "Sobrinho... o meu peito. Me deixa deitar numa cama de verdade. Só um pouquinho.",
     S('corredor_tio_escuro', cam=dict(zoom=1.3, to=1.42, cx=940, cy=560), fx=[dict(NO_CORREDOR, boca='flat', s=0.66, escuro=0.3)])),
    ('nar', "Esse é o pior momento da noite. Porque é a voz do seu tio. E ninguém quer ser o sobrinho que deixou o tio passando mal no chão.",
     S('quarto', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Ele vai dizer que tem o coração fraco. Que viajou três dias de ônibus. Que só sobrinho ingrato deixa o tio dormir no chão.",
     S('corredor_tio_escuro', cam=dict(zoom=1.15, to=1.25, cx=940, cy=640))),
    ('nar', "Lembra de uma coisa: tio passando mal chama o irmão. Grita Toninho. Pede pra ligar pro SAMU. Tio passando mal não pede cama. Ele só quer uma cama. A sua.",
     S('quarto', quarto(eyes='angry', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Fica deitado. Põe o travesseiro em cima da cabeça. Uma hora a respiração chiando vira ronco. E o ronco volta, devagarinho, pro sofá.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'SÓ SAIA PELO **SEU NOME**')}])),
    ('nar', "Quando clarear, não sai pra ver se ele foi embora. Não abre a porta pra espiar o sofá. Espera alguém te chamar.",
     S('quarto_manha', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1), fx=[{'texto': ['06:20'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Sobrinho, vem tomar café! O tio já vai embora, vem se despedir.",
     S('corredor_tio_manha', cam=dict(zoom=1.2, to=1.35, cx=420, cy=520), fx=[{'monstro': 'fundo', 'quem': Q, 'pos': (360, 962), 's': 0.6, 'escuro': 0.2, 'surge': True}])),
    ('nar', "Não sai. Quem é da família sabe o seu nome. A sua mãe nunca te chamou de sobrinho na vida.",
     S('quarto_manha', quarto(eyes='angry', mouth='flat'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "Espera o cheiro de café de verdade, o rádio da cozinha ligado e a voz da sua mãe, impaciente, do jeito de sempre.",
     S('corredor_tio_manha', cam=dict(zoom=1.0, to=1.1))),
    ('mae', "Caio! O café tá esfriando, menino!",
     S('corredor_tio_manha', C('mae', 'p1', None, arms='hip', mouth='o', eyes='angry', facing=1), cam=dict(zoom=1.1, to=1.2, cx=700, cy=560))),
    ('nar', "Aí sim. Pode sair. O sofá tá vazio. O lençol tá dobrado em cima do braço. E não tem mala nenhuma.",
     S('sala_tio_manha', C('voce', 'centro', None, eyes='wide', mouth='flat', facing=1), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "O seu pai, ainda de pijama, liga pro irmão no viva-voz, coçando a cabeça.",
     S('cozinha_manha', C('pai', 'mesa', None, sit=True, facing=1, arms='hold', prop='celular', eyes='half', mouth='flat'), C('mae', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='flat', eyes='half'), cam=dict(zoom=1.0, to=1.1))),
    ('tio', "Dormir aí? Ô, Toninho, eu tô em Porto Velho, rapaz! Faz seis anos que eu não piso nessa casa. Manda um abraço pro Caio.",
     S('cozinha_manha', C('pai', 'mesa', None, sit=True, facing=1, arms='hold', prop='celular', eyes='wide', mouth='o'), C('mae', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='o', eyes='wide'), cam=dict(zoom=1.25, to=1.35, cx=800, cy=600))),
    ('nar', "O tio de verdade sabe o seu nome. E ninguém na mesa fala nada por um bom tempo.",
     S('cozinha_manha', C('voce', 'c', None, eyes='half', mouth='flat'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "No domingo à noite, você vai buscar o ventilador velho no quartinho dos fundos. E a cama de armar, que vivia fechada atrás das caixas, tá montada. Com lençol esticado. E um chinelo do lado.",
     S('quartinho', cam=dict(zoom=1.0, to=1.15))),
    ('nar', "Ninguém da casa arrumou. Quarto que não é de ninguém não precisa ser mostrado. E visita que tem quarto não vai embora.",
     S('quartinho', cam=dict(zoom=1.2, to=1.35, cx=1250, cy=600), fx=[dict(QUARTINHO, surge=True)])),
    ('nar', "A mala vermelha tá ali, encostada na cama de armar. Vazia. Do tamanho certinho pra caber as suas coisas.",
     S('quartinho', cam=dict(zoom=1.45, to=1.6, cx=1560, cy=820))),
    ('nar', "Hoje, quando a casa apaga, você ouve uma voz lá do fundo. Calma, de tio, no tom de quem tem a noite inteira.",
     S('corredor_tio_escuro', cam=dict(zoom=1.0, to=1.15))),
    ('coisa', "Boa noite, sobrinho. Amanhã você me mostra o seu.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 2.8, 'pos': (960, 620), 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: tem algum parente na sua família que ninguém sabe de que lado veio?",
     S('preto', fx=[{'cta_mm': ('TEM UM TIO', 'ASSIM AÍ?')}])),
]
