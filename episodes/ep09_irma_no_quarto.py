"""Manual da Madrugada — Noite 09
Se a sua irmã pedir pra dormir no seu quarto porque tem alguém no dela… NÃO DEIXE ELA ENTRAR
"""
from engine.dsl import S, C

TITLE = "Se a sua irmã pedir pra dormir no seu quarto porque tem alguém no dela… NÃO DEIXE ELA ENTRAR"
NOITE = 9
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='NÃO DEIXE **ENTRAR**', cena='parede', criatura='coisa_ep09', balao='Deixa eu entrar, mano?')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',         # MM Narrador
    'coisa': 'e808da2329754929803c8bd98dc36857',       # Lucilene (imitando a Larinha, com efeito)
    'coisa_voce': 'd703f08d1ef34302a36945aa3efc7b3f',  # Murilo (a coisa imitando a SUA voz, com efeito)
    'larinha': 'e808da2329754929803c8bd98dc36857',     # Lucilene (a Larinha de verdade, limpa)
}

# a coisa desta noite: imita a Larinha (8 anos) de pijama e maria-chiquinha, mas alta e magra demais, pescoço
# comprido, cabeça muito torta, braços compridos; sempre abraçada no travesseiro de fronha vermelha (o único vermelho).
# Ela não entra em quarto nenhum sem ser convidada. Quarto vazio não precisa de convite.
Q = 'coisa_ep09'
NA_SUA_PORTA = {'monstro': 'fundo', 'quem': Q, 'pos': (560, 960), 's': 0.62, 'escuro': 0.45}      # colada na sua porta
NA_PORTA_DELA = {'monstro': 'fundo', 'quem': Q, 'pos': (1130, 960), 's': 0.6, 'escuro': 0.5}     # na porta da Larinha
NO_FUNDO = {'monstro': 'fundo', 'quem': Q, 'pos': (1520, 830), 's': 0.42, 'escuro': 0.8}          # no fim do corredor
SAINDO_DO_QUARTO = {'monstro': 'porta', 'quem': Q, 'rect': (820, 280, 240, 540), 'lado': 'esq', 'abre': 0.35}
JANELA = {'monstro': 'janela', 'quem': Q, 'rect': (220, 160, 300, 280)}
JANELA_LARA = {'monstro': 'janela', 'quem': Q, 'rect': (1420, 170, 280, 260)}
PORTA_ABERTA = {'monstro': 'porta', 'quem': Q, 'rect': (760, 260, 230, 540), 'lado': 'dir', 'abre': 0.45}
TETO = {'monstro': 'teto', 'quem': Q, 'pos': (640, 0), 's': 0.5}
NA_CAMA_DELA = {'monstro': 'borda', 'quem': Q, 'pos': (430, 770), 's': 0.8}


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se a sua irmã bater na sua porta de madrugada pedindo pra dormir aí, porque tem alguém no quarto dela, não deixe ela entrar. Não abra a porta. Não diga pode.",
     S('corredor_irma', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(NO_FUNDO, surge=True)])),
    ('nar', "Eu não tô falando de noite de trovoada, quando ela aparece chorando, com o travesseiro debaixo do braço.",
     S('quarto_trinco', quarto(mouth='smile', eyes='half'), C('larinha', 'centro', None, eyes='sad', mouth='frown', arms='hold', facing=1))),
    ('nar', "Também não tô falando de quando ela vê filme de terror escondida e dorme uma semana no seu colchão.",
     S('quarto_trinco', quarto(mouth='smile', eyes='half'), C('larinha', 'porta', None, eyes='wide', mouth='o', facing=1), cam=dict(zoom=1.05, to=1.12))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "A Larinha tem oito anos e dorme no quarto da frente, com uma luzinha de estrela acesa na tomada.",
     S('quarto_lara', C('larinha', 'cama', None, sit=True, eyes='closed', mouth='smile', facing=1), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Ela nunca bateu na sua porta: quando tem pesadelo, ela entra direto e pula na sua cama. Seus pais dormem no fundo, com o ventilador no três.",
     S('corredor_irma', cam=dict(zoom=1.05, to=1.15, cx=1200, cy=560))),
    ('nar', "Três e dez. Três batidinhas na sua porta.",
     S('quarto_trinco', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.25, to=1.38, cx=875, cy=560), fx=[{'texto': ['03:10'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('coisa', "Mano? Deixa eu dormir aí? Tem alguém no meu quarto.",
     S('corredor_irma', cam=dict(zoom=1.2, to=1.35, cx=480, cy=560), fx=[dict(NA_SUA_PORTA, surge=True), 'zoom_punch'])),
    ('nar', "A voz da Larinha. Chorosa, do jeitinho dela. Mas a Larinha nunca bateu numa porta. E, pela fresta de baixo da sua, você vê a sombra de dois pés. Longe demais um do outro.",
     S('quarto_trinco', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "Você tem quatorze anos. A sua mãe pega no posto de saúde às seis, o seu pai abre a oficina às sete, e às dez da noite a casa inteira já tá apagada. É uma casa pequena: um corredor, três portas e o barulho do ventilador lá no fundo.",
     S('corredor_irma', cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá no corredor conhece a voz da sua irmã, o nome dos seus pais e o lugar de cada móvel. Ela anda pela casa inteira.",
     S('corredor_irma_escuro', cam=dict(zoom=1.0, to=1.15), fx=[dict(NO_FUNDO, avanca=True, s=0.5)])),
    ('nar', "Mas ela não sabe quem dorme em cada quarto. Ela só conhece as vozes. E ela não tem pressa. Ela já passou noites inteiras em outras casas, em outros corredores, batendo devagarinho, esperando alguém dizer pode.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.6, 'surge': True}])),
    ('nar', "E tem uma coisa que ela não pode fazer. Ela não entra em quarto nenhum sem ser convidada. Ela não arromba porta. Ela só precisa de um sim.",
     S('quarto_trinco', cam=dict(zoom=1.2, to=1.35, cx=875, cy=540))),
    ('nar', "Por isso ela inventou alguém no quarto da Larinha. Medo é o jeito mais fácil de fazer alguém abrir uma porta. Você abre pra proteger. E, quando abre, convidou.",
     S('corredor_irma', cam=dict(zoom=1.1, to=1.25, cx=940, cy=560), fx=[dict(SAINDO_DO_QUARTO, surge=True)])),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Quantas vezes alguém bateu na porta do seu quarto e você disse entra, sem nem levantar a cabeça do celular?",
     S('quarto_trinco', quarto(eyes='half', mouth='flat', arms='hold', prop='celular'), cam=dict(zoom=1.0, to=1.12))),
    ('nar', "Quase sempre era a sua mãe, com a roupa dobrada. Quase sempre.",
     S('quarto_trinco', quarto(eyes='half', mouth='flat', look=-1), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO ABRA A **PORTA**')}])),
    ('nar', "Não abra a porta. Nem um pouquinho. Nem pra espiar. Nem pra passar um cobertor pela fresta.",
     S('quarto_trinco', quarto(eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "O trinco tá fechado. Você mesmo fechou antes de dormir, porque amanhã tem prova e você não queria a Larinha pulando na sua cama às seis da manhã.",
     S('quarto_trinco', cam=dict(zoom=1.8, to=1.95, cx=935, cy=490))),
    ('nar', "Se você quiser conferir, encosta a mão no ferro frio, sem mexer. Se ele correr um milímetro, ela vai ouvir. E vai saber que tem alguém acordado, do lado de lá da porta.",
     S('quarto_trinco', C('voce', 'porta', None, eyes='wide', mouth='flat', arms='point', facing=1), cam=dict(zoom=1.3, to=1.4, cx=875, cy=600))),
    ('nar', "Ela vai bater de novo. Três batidinhas. Sempre três. Volta pra cama devagar e puxa o cobertor até o queixo.",
     S('corredor_irma', cam=dict(zoom=1.15, to=1.3, cx=500, cy=600), fx=['shake'])),
    ('nar', "E não adianta gritar pelos seus pais. Com o ventilador no três, eles não ouvem nem o despertador. Quem ia acordar com o grito era a Larinha.",
     S('corredor_irma', cam=dict(zoom=1.4, to=1.55, cx=1520, cy=560))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO DIGA **PODE**')}])),
    ('nar', "Não diga pode. Nem entra, nem tá bom, nem vem. Nenhuma palavra que pareça um sim. Ela vai fazer perguntas. Perguntas que dão vontade de responder.",
     S('quarto_trinco', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.1, to=1.2))),
    ('coisa', "Mano, você tá acordado? Posso entrar? Só um pouquinho?",
     S('corredor_irma', cam=dict(zoom=1.35, to=1.5, cx=560, cy=520), fx=[dict(NA_SUA_PORTA, s=0.7, escuro=0.3)])),
    ('nar', "Pra ela, um sim é uma chave. Até um tá resmungado, meio dormindo, abre a porta por dentro. E você vai ouvir o trinco correr sozinho.",
     S('quarto_trinco', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.3, to=1.45, cx=875, cy=560))),
    ('nar', "Ela também vai tentar te fazer rir. Vai cantar a musiquinha do desenho que vocês viam juntos, errando a letra de propósito, pra você corrigir. Não corrige. Correção também é resposta.",
     S('corredor_irma_escuro', cam=dict(zoom=1.15, to=1.3, cx=520, cy=560))),
    ('nar', "Se o silêncio ficar insuportável, finge que ronca. Ronco não é resposta. Ronco é só alguém dormindo.",
     S('quarto_trinco', quarto(eyes='closed', mouth='o'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO OLHE PRA **JANELA**')}])),
    ('nar', "Quando a porta não funcionar, ela vai dar a volta. A casa é térrea, e a janela do seu quarto dá pro quintal.",
     S('quarto_trinco', cam=dict(zoom=1.2, to=1.35, cx=420, cy=380))),
    ('nar', "Você vai ouvir unha no vidro. Tec. Tec. Tec. E a mesma voz, agora do lado de fora.",
     S('quarto_trinco', quarto(eyes='wide', mouth='flat', look=-1), cam=dict(zoom=1.0, to=1.12))),
    ('coisa', "Abre a janela então, mano. Tá frio aqui fora.",
     S('quarto_trinco', cam=dict(zoom=1.4, to=1.55, cx=420, cy=340), fx=[JANELA, 'zoom_punch'])),
    ('nar', "Não olha. Vira pra parede e fecha os olhos. Se você olhar, vai ver que o rosto dela tá colado no vidro. E a sua janela fica a quase dois metros do chão.",
     S('quarto_trinco', quarto(eyes='closed', mouth='flat', arms='face', facing=1), cam=dict(focus='voce', zoom=1.45, to=1.6))),
    ('nar', "E nem pensa em acender a luz pra enxergar melhor. Com a luz acesa, quem tá lá fora vê tudo aqui dentro. E você não vê nada lá fora.",
     S('quarto_trinco', quarto(eyes='half', mouth='flat', arms='hold', prop='celular', facing=1), cam=dict(zoom=1.1, to=1.22, cx=1250, cy=560))),
    ('nar', "A Larinha não alcança nem o interruptor da sala.",
     S('quarto_trinco', cam=dict(zoom=1.2, to=1.3, cx=420, cy=360), fx=[dict(JANELA, boca='flat')])),

    # ---------------------------------------------------------------- PEDIDO DE INSCRIÇÃO (teste E2)
    ('nar', "Antes da regra quatro: se você ainda tá acordado, se inscreve. O próximo manual chega amanhã, às oito da noite.",
     S('quarto_trinco', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.08), fx=[{'texto': ['INSCREVA-SE'], 'pos': 'topo', 'cor': '#E5262B'}])),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO SAIA DO **QUARTO**')}])),
    ('nar', "Uma hora, ela volta pro corredor. E muda de assunto.",
     S('corredor_irma_escuro', cam=dict(zoom=1.05, to=1.2), fx=[TETO])),
    ('coisa', "Mano, ele tá debaixo da minha cama. Vai lá ver. Por favor.",
     S('corredor_irma', cam=dict(zoom=1.25, to=1.4, cx=940, cy=520), fx=[dict(SAINDO_DO_QUARTO, boca='flat', abre=0.4)])),
    ('nar', "Ela quer que você saia. O corredor não é quarto de ninguém. Se você puser o pé ali fora, você tá na casa dela. E na casa dela, ninguém precisa te convidar pra nada.",
     S('corredor_irma_escuro', cam=dict(zoom=1.1, to=1.25, cx=700, cy=560))),
    ('nar', "Pensa na Larinha. Ela deve estar no quarto dela, encolhida debaixo do cobertor, com a luzinha acesa. A coisa não entra lá. Ninguém convidou.",
     S('quarto_lara', cam=dict(zoom=1.15, to=1.3, cx=600, cy=640))),
    ('nar', "E não manda mensagem pros seus pais pedindo pra eles irem ver. Se o seu pai sair no corredor de madrugada, morrendo de sono, e ouvir a Larinha pedindo colo, ele vai dizer vem, filha. Sem pensar.",
     S('corredor_irma_escuro', cam=dict(zoom=1.05, to=1.18, cx=1300, cy=560))),
    ('nar', "Enquanto ela dormir, ela tá segura.",
     S('quarto_lara', cam=dict(zoom=1.0, to=1.1), fx=[dict(JANELA_LARA, surge=True)])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'BATA NA **PAREDE**')}])),
    ('nar', "Agora vem a parte difícil. Ela vai parar de falar com você. E vai bater na porta da Larinha. Com a sua voz.",
     S('corredor_irma', cam=dict(zoom=1.1, to=1.25, cx=1000, cy=560))),
    ('coisa_voce', "Larinha, é o mano. Deixa eu dormir aí com você?",
     S('corredor_irma', cam=dict(zoom=1.35, to=1.5, cx=1080, cy=520), fx=[NA_PORTA_DELA, 'zoom_punch'])),
    ('nar', "E a Larinha tem oito anos. Ela ama você. Se ela acordar, ela diz pode sem nem pensar.",
     S('quarto_lara', cam=dict(zoom=1.3, to=1.45, cx=420, cy=700))),
    ('nar', "A cabeceira da sua cama tá encostada na parede do quarto dela. Bate na parede. Três batidas rápidas e duas devagar. É o código de vocês, desde a noite em que faltou luz e ela não parava de chorar.",
     S('quarto_trinco', quarto(eyes='angry', mouth='flat', arms='point', facing=1), cam=dict(zoom=1.2, to=1.3, cx=1350, cy=600), fx=[{'texto': ['TOC TOC TOC ... TOC ... TOC'], 'pos': 'topo', 'cor': '#E5262B'}])),
    ('nar', "Três e duas quer dizer: fica quieta, eu tô aqui. E, do outro lado da parede, alguém bate de volta. Três rápidas. Duas devagar.",
     S('quarto_lara', cam=dict(zoom=1.1, to=1.2), fx=[{'texto': ['TOC TOC TOC ... TOC ... TOC'], 'pos': 'topo', 'cor': '#E5262B'}])),
    ('nar', "No corredor, a batida na porta dela para. Ninguém lá dentro disse pode. E a coisa fica ali, parada, com a mão na maçaneta e o rosto encostado na madeira.",
     S('corredor_irma_escuro', cam=dict(zoom=1.2, to=1.35, cx=1050, cy=600))),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'NÃO ABRA PRO **CHORO**')}])),
    ('nar', "Quando nada mais funcionar, ela volta pra sua porta. E chora. O choro da Larinha. Aquele soluço engasgado que você conhece desde que ela era bebê.",
     S('preto', fx=[{'olhos': (960, 470), 'surge': True}])),
    ('coisa', "Mano, abre! Ele pegou o meu pé! Ele tá me puxando! Abre, por favor!",
     S('corredor_irma', cam=dict(zoom=1.3, to=1.45, cx=520, cy=560), fx=[dict(NA_SUA_PORTA, s=0.72, escuro=0.25, boca='flat'), 'shake'])),
    ('nar', "Esse é o pior momento da noite. Porque é a sua irmã. E tudo dentro de você vai gritar pra levantar e abrir.",
     S('quarto_trinco', quarto(eyes='sad', mouth='frown', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.7))),
    ('nar', "Ela vai dizer que tá doendo. Vai chamar a mãe. Vai dizer que a culpa é sua. Cada frase mais baixinha. Mais perto da fresta.",
     S('quarto_trinco', cam=dict(zoom=1.45, to=1.6, cx=875, cy=650))),
    ('nar', "Lembra das batidas. Alguém respondeu três e duas, lá do quarto dela. A Larinha tá lá. Quem tá chorando na sua porta não é ela.",
     S('quarto_trinco', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Tapa os ouvidos com o travesseiro. Conta as batidas do seu coração. Choro que ninguém responde, uma hora, para.",
     S('quarto_trinco', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'QUEM É DE CASA **NÃO PEDE**')}])),
    ('nar', "Quando o céu começar a clarear, levanta e corre o trinco. Só destranca. Não abre a porta. Volta pra cama e não diz nada.",
     S('quarto_trinco_alvorada', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1), fx=[{'texto': ['05:40'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "A coisa nunca entra sem convite. Nem com a porta destrancada. Nem com a porta escancarada. Ela fica no batente, esperando. E pergunta.",
     S('quarto_trinco_manha', cam=dict(zoom=1.1, to=1.25, cx=875, cy=540))),
    ('coisa', "Posso entrar, mano?",
     S('quarto_trinco_manha', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.15, to=1.3, cx=1000, cy=560), fx=[dict(PORTA_ABERTA, surge=True)])),
    ('nar', "Fica quieto. Quem é de casa não pede. Quem é de casa entra. A Larinha nunca pediu licença na vida. Nem pra entrar no banheiro, nem pra pegar o seu fone. Você nunca vai gostar tanto disso.",
     S('quarto_trinco_alvorada', quarto(eyes='closed', mouth='flat'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "Até que você ouve o chinelinho arrastando, a porta abrindo de uma vez e um corpinho pulando na sua cama. Com o pé gelado.",
     S('quarto_trinco_manha', quarto(eyes='wide', mouth='o'), C('larinha', 'centro', None, arms='up', eyes='happy', mouth='grin', facing=1), cam=dict(zoom=1.0, to=1.08))),
    ('larinha', "Chega pra lá, mano. Eu tive um sonho muito esquisito.",
     S('quarto_trinco_manha', quarto(eyes='happy', mouth='smile'), C('larinha', 'porta', None, eyes='half', mouth='smile', arms='hold', facing=1), cam=dict(zoom=1.2, to=1.3, cx=1100, cy=640))),
    ('nar', "Aí sim. Abraça ela. E deixa ela roubar o seu cobertor.",
     S('quarto_trinco_manha', quarto(eyes='closed', mouth='smile'), cam=dict(zoom=1.05, to=1.12))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "No café da manhã, a sua mãe pergunta por que vocês dois acordaram amontoados na mesma cama. A Larinha dá de ombros, com a boca cheia de pão.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile', eyes='half'), C('larinha', 'mesa', None, sit=True, facing=1, mouth='smile', eyes='happy'), cam=dict(zoom=1.0, to=1.1))),
    ('larinha', "Eu fiquei com medo e fui dormir na cama da mãe, lá pelas duas. Só de manhã que eu fui pra sua.",
     S('cozinha_manha', C('mae', 'b', None, facing=-1, arms='hold', prop='caneca', mouth='smile', eyes='half'), C('larinha', 'mesa', None, sit=True, facing=1, mouth='smile', eyes='half', arms='shrug'), cam=dict(focus='larinha', zoom=1.4, to=1.5))),
    ('nar', "A sua mãe confirma, rindo: levou chute a noite inteira. Você para de mastigar. Porque às três e meia, alguém respondeu as suas batidas. Três e duas. Do quarto dela. Do quarto vazio.",
     S('quarto_lara_vazio', cam=dict(zoom=1.05, to=1.2), fx=[dict(NA_CAMA_DELA, surge=True)])),
    ('nar', "Quarto vazio não tem ninguém pra dizer não. E ela aprendeu o código de vocês.",
     S('quarto_lara_vazio', cam=dict(zoom=1.3, to=1.45, cx=500, cy=640))),
    ('nar', "Hoje à noite, quando você apaga a luz, a parede da cabeceira bate sozinha. Três rápidas. Duas devagar.",
     S('quarto_trinco', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[{'texto': ['TOC TOC TOC ... TOC ... TOC'], 'pos': 'topo', 'cor': '#E5262B'}])),
    ('coisa', "Fica quieto, mano. Agora eu tô aqui.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 2.8, 'pos': (960, 600), 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: você ia conseguir não abrir pra sua irmã chorando?",
     S('preto', fx=[{'cta_mm': ('VOCÊ ABRIRIA', 'PRA SUA IRMÃ?')}])),
]
