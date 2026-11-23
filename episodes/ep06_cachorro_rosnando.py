"""Manual da Madrugada — Noite 06
Se o seu cachorro rosnar para o seu pai na porta de casa… NÃO ABRA
"""
from engine.dsl import S, C

TITLE = "Se o seu cachorro rosnar para o seu pai na porta de casa… NÃO ABRA"
NOITE = 6
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 8.0          # tela final: 8 s depois da última fala
THUMB = dict(ordem='NÃO **ABRA**', cena='olho', criatura='coisa_ep06', balao='Sou eu, filho.')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': '9ce5f601f9e04382bb26141d5a3f839d',  # Afonso (imitando o pai, com efeito)
    'pai': '9ce5f601f9e04382bb26141d5a3f839d',    # Afonso (o pai de verdade, limpo)
}

# a coisa desta noite: imita o pai de uniforme da fábrica, mas alta demais (curva as costas pra caber debaixo da luz
# da varanda), quatro olhos, braços compridos; o detalhe vermelho é o capacete (o do pai de verdade é branco).
# Ela não entra sozinha: aparece sempre do lado de fora (varanda, janelas, olho mágico).
Q = 'coisa_ep06'
JANELA_PORTA = {'monstro': 'janela', 'quem': Q, 'rect': (300, 240, 260, 360)}          # janela ao lado da porta
JANELA_SALA = {'monstro': 'janela', 'quem': Q, 'rect': (140, 170, 280, 250)}
JANELA_QUARTO = {'monstro': 'janela', 'quem': Q, 'rect': (220, 160, 300, 280)}
NA_PORTA = {'monstro': 'fundo', 'quem': Q, 'pos': (960, 925), 's': 0.6, 'escuro': 0.3}  # na varanda, colada na porta
LONGE = {'monstro': 'fundo', 'quem': Q, 'pos': (1560, 905), 's': 0.42, 'escuro': 0.7}   # no canto escuro da varanda
OLHO = {'monstro': 'olho', 'quem': Q, 'perto': 0.3}
OLHO_PERTO = {'monstro': 'olho', 'quem': Q, 'perto': 0.85, 'incl': -0.3}
BIDU_PORTA = {'cachorro': (1180, 990, 'rosna', -1)}        # de pé na frente da porta, rosnando
BIDU_SALA = {'cachorro': (1500, 990, 'rosna', -1)}


def quarto(**p):
    d = dict(sit=True, facing=-1)
    d.update(p)
    return C('voce', 'cama', None, **d)


LINES = [
    # ---------------------------------------------------------------- A REGRA
    ('nar', "Se o seu cachorro rosnar para o seu pai na porta de casa, não abra. Não destranque. Não acenda a luz da sala. E, aconteça o que acontecer, não mande o cachorro ficar quieto.",
     S('porta', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(JANELA_PORTA, surge=True), BIDU_PORTA])),
    ('nar', "Eu não tô falando de quando o seu pai chega com a bota suja de barro e o cachorro pula nele querendo brincar.",
     S('sala_manha', C('pai', 'porta', None, facing=-1, arms='wave', mouth='grin'), C('voce', 'centro', None, mouth='smile'), fx=[{'cachorro': (1380, 990, 'abana')}])),
    ('nar', "Também não tô falando de quando ele late pro carteiro, pro motoboy ou pro gato do vizinho andando em cima do muro.",
     S('varanda_manha', C('vizinho', 'b', None, facing=-1, arms='hold', prop='sacola', eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.06), fx=[{'cachorro': (700, 990, 'parado')}])),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "O seu pai trabalha no turno da noite, numa fábrica de autopeças do outro lado da cidade. Entra às dez, sai às seis. Pega o ônibus das seis e dez e chega em casa às seis e quarenta. Todo dia. Faz onze anos.",
     S('porta', C('pai', 'porta', None, facing=1, arms='wave', mouth='smile'), C('voce', 'a', None, mouth='smile', arms='wave'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "A sua mãe foi passar a semana na casa da sua tia, em Minas. Então hoje é você e o Bidu.",
     S('sala', C('voce', 'sofa', None, sit=True, mouth='smile', eyes='half', arms='hold', prop='celular'), cam=dict(zoom=1.0, to=1.08), fx=[{'cachorro': (1380, 990, 'parado', -1)}])),
    ('nar', "O Bidu é um vira-lata caramelo. O seu pai achou ele filhote, tremendo de frio, no portão da fábrica. Desde aquele dia, ele espera o seu pai toda manhã no capacho, abanando o rabo antes mesmo de o portão abrir.",
     S('porta_manha', cam=dict(zoom=1.1, to=1.2, cx=960, cy=700), fx=[{'cachorro': (1180, 990, 'abana', -1)}])),
    ('nar', "O Bidu não rosna pra ninguém. Nem pra quem merece."),
    ('nar', "São duas e dez da manhã.",
     S('preto', fx=[{'texto': ['02:10'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você acorda com um barulho que nunca ouviu dentro da sua casa. Um ronco baixo, comprido, vindo da sala. É o Bidu. De pé na frente da porta da rua, com o pelo das costas todo arrepiado.",
     S('porta', cam=dict(zoom=1.25, to=1.4, cx=1100, cy=780), fx=[BIDU_PORTA])),
    ('nar', "E aí, do lado de fora, alguém bate três vezes. Toc. Toc. Toc. E a voz do seu pai diz:",
     S('varanda', cam=dict(zoom=1.0, to=1.12), fx=[dict(NA_PORTA, surge=True)])),
    ('coisa', "Filho, abre aí. Liberaram a gente mais cedo.",
     S('varanda', cam=dict(zoom=1.3, to=1.45, cx=960, cy=480), fx=[NA_PORTA, 'zoom_punch'])),
    ('nar', "Mais cedo. Quatro horas mais cedo. Numa fábrica que não para nem no Natal.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "E, quando a fábrica libera mais cedo, o seu pai avisa no grupo da família. Sempre. Nem que seja com um joinha. O seu celular tá do lado do travesseiro. Nenhuma mensagem nova.",
     S('preto', fx=[{'celular': [('ela', 'pai: tranca o portão e vai dormir'), ('eu', 'blz pai, bom trampo')]}])),
    ('nar', "E o Bidu, que espera o seu pai faz onze anos, não abana o rabo. Ele mostra os dentes.",
     S('porta', cam=dict(zoom=1.5, to=1.7, cx=1230, cy=800), fx=[BIDU_PORTA, 'shake'])),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá na sua porta anda pelas estradas de madrugada, atrás de quem volta do turno da noite. Ela senta no último banco do ônibus. Escuta as conversas. Aprende as vozes.",
     S('varanda_jaqueta', cam=dict(zoom=1.0, to=1.15), fx=[dict(LONGE, avanca=True, surge=True)])),
    ('nar', "Ela sabe como o seu pai fala. Sabe onde ele mora. Sabe até o nome do cachorro."),
    ('nar', "Mas tem duas coisas que ela não sabe. Ela não sabe o que tem dentro da casa. E ela não sabe enganar um nariz.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.55, 'surge': True}])),
    ('nar', "E ela não pode entrar sozinha. Alguém de dentro tem que abrir. Por isso ela escolhe a única voz pra quem você abriria a porta sem nem pensar.",
     S('porta', C('voce', 'a', None, eyes='wide', mouth='flat', facing=1), cam=dict(zoom=1.05, to=1.15), fx=[BIDU_PORTA])),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Sabe quando o seu cachorro fica parado, olhando pra um canto vazio da casa? Ou rosnando baixinho pra porta, no meio da noite? E você ri, chama ele de bobo e volta a dormir.",
     S('sala', C('voce', 'sofa', None, sit=True, eyes='half', mouth='smile'), cam=dict(zoom=1.0, to=1.12), fx=[dict(JANELA_SALA, surge=True), {'cachorro': (1380, 990, 'rosna', -1)}])),
    ('nar', "Talvez ele não fosse bobo. Talvez ele só estivesse fazendo o trabalho dele.",
     S('sala', C('voce', 'sofa', None, sit=True, eyes='wide', mouth='flat'), cam=dict(zoom=1.3, to=1.4, cx=1100, cy=700), fx=[{'cachorro': (1380, 990, 'parado', -1)}])),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO **ABRA**')}])),
    ('nar', "Não abra. Nem a porta, nem a janela, nem o portão pelo controle. Não gire a chave nem pra conferir se tá trancada.",
     S('porta', C('voce', 'a', None, eyes='wide', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),
    ('nar', "Uma porta destrancada, pra ela, já é uma porta aberta. Ela sente o trinco correndo do outro lado da madeira.",
     S('porta', cam=dict(zoom=1.4, to=1.6, cx=1160, cy=540))),
    ('nar', "Se você ficar quieto, ela bate de novo. Mais forte. Do jeito que o seu pai bate quando tá com pressa.",
     S('porta', cam=dict(zoom=1.1, to=1.25, cx=1000, cy=560), fx=[BIDU_PORTA, 'shake'])),
    ('coisa', "Ô, filho! Tá frio aqui fora. Abre pro pai.",
     S('porta', C('voce', 'b', None, eyes='closed', mouth='wavy', sweat=True, facing=-1), cam=dict(zoom=1.05, to=1.15, cx=900, cy=540), fx=[JANELA_PORTA, BIDU_PORTA])),
    ('nar', "O seu pai tem a chave. Sempre tem. Fica presa no passador da calça, junto com o crachá da fábrica. Faz onze anos que ele não precisa bater nessa porta.",
     S('porta', C('voce', 'a', None, eyes='angry', mouth='flat'), cam=dict(focus='voce', zoom=1.5, to=1.6))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'ACREDITE NO **BIDU**')}])),
    ('nar', "Acredite no Bidu. Não importa a voz. Não importa o que ela diga. Se o Bidu rosnar, quem tá lá fora não é o seu pai.",
     S('porta', cam=dict(zoom=1.35, to=1.5, cx=1180, cy=780), fx=[BIDU_PORTA])),
    ('nar', "Voz se imita. Cheiro não. E o que tá do lado de lá da porta tem cheiro de asfalto molhado, de ferro enferrujado, de coisa que nunca dormiu numa cama.",
     S('porta', cam=dict(zoom=1.6, to=1.75, cx=1330, cy=800), fx=[BIDU_PORTA])),
    ('nar', "Senta no chão da sala, perto dele. Encosta a mão nas costas dele. Sente o rosnado vibrando debaixo da sua mão. Enquanto ele rosnar, você sabe que ela continua ali.",
     S('sala', C('voce', 'centro', None, sit=True, eyes='half', mouth='flat', arms='point', facing=1), cam=dict(zoom=1.1, to=1.2, cx=800, cy=640), fx=[{'cachorro': (760, 990, 'rosna')}])),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'TAPE O **OLHO MÁGICO**')}])),
    ('nar', "Não olhe pelo olho mágico. Eu sei que você quer. Você quer ver a cara do seu pai e acabar logo com isso.",
     S('porta', C('voce', 'porta', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.3, to=1.45, cx=960, cy=420))),
    ('nar', "Mas o olho mágico é um buraco. Pequeno, mas é um buraco. E tudo que dá pra ver de dentro pra fora também dá pra ver de fora pra dentro.",
     S('preto', fx=[dict(OLHO, surge=True)])),
    ('nar', "Se você já olhou, você já viu. O capacete vermelho, quando o do seu pai é branco. O corpo tão comprido que ela precisa curvar as costas pra caber debaixo da luz da varanda. E os olhos. Quatro. Todos virados pro mesmo buraquinho.",
     S('preto', fx=[OLHO_PERTO, 'zoom_punch'])),
    ('nar', "Pega a fita crepe na gaveta da cozinha e tapa o olho mágico. Duas voltas. E depois sai da frente da porta.",
     S('porta_fita', C('voce', 'b', None, eyes='angry', mouth='flat', facing=-1), cam=dict(zoom=1.2, to=1.3, cx=1150, cy=480))),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "E, se você ouvir uma unha raspando de leve na madeira, bem na altura do olho mágico, não se assusta. É ela procurando o buraquinho que sumiu."),
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'LIGUE PRA **PORTARIA**')}])),
    ('nar', "Não ligue pro celular do seu pai. Na linha de produção, o celular fica trancado no armário. Quem atender, se alguém atender, não vai ser ele.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='hold', prop='celular'), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "Liga pro número que tá no ímã da geladeira. A portaria da fábrica. O seu Valdir atende no segundo toque. Ele sempre atende.",
     S('cozinha', C('voce', 'b', None, eyes='wide', mouth='flat', arms='hold', prop='celular', facing=1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Pede pra chamar o seu pai. E espera um minuto inteiro, ouvindo o barulho das máquinas do outro lado da linha.",
     S('cozinha', C('voce', 'b', None, eyes='closed', mouth='flat', arms='hold', prop='celular', facing=-1), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('pai', "Filho? Que foi? Eu tô aqui na linha três. Escuta: não abre essa porta pra ninguém. Fica com o Bidu.",
     S('cozinha', C('voce', 'b', None, eyes='wide', mouth='o', arms='hold', prop='celular', facing=-1), cam=dict(focus='voce', zoom=1.6, to=1.7))),
    ('nar', "Agora você tem certeza. E ela também. Porque, do outro lado da porta, a voz do seu pai pergunta, bem baixinho:",
     S('porta', cam=dict(zoom=1.2, to=1.35, cx=960, cy=420), fx=[BIDU_PORTA])),
    ('coisa', "Quem é no telefone, filho?",
     S('porta', cam=dict(zoom=1.35, to=1.5, cx=440, cy=440), fx=[JANELA_PORTA, 'zoom_punch'])),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'SIGA O **FOCINHO**')}])),
    ('nar', "Quando ela entender que a porta não vai abrir, ela vai dar a volta na casa. Você não vai ouvir passo nenhum. Mas vai ver o Bidu.",
     S('varanda_jaqueta', cam=dict(zoom=1.0, to=1.1), fx=[{'monstro': 'lateral', 'quem': Q, 'lado': 'esq', 'y': 1150, 's': 0.9, 'surge': True}])),
    ('nar', "Ele vai virar a cabeça devagar. Da porta pra janela da sala. Da sala pra cozinha. Da cozinha pro corredor. O focinho dele aponta sempre pra onde ela tá.",
     S('sala', cam=dict(zoom=1.0, to=1.1), fx=[JANELA_SALA, {'cachorro': (900, 990, 'rosna', -1)}])),
    ('nar', "E repara: o Bidu não tá com medo. Ele tá de guarda. Cachorro com medo se esconde debaixo da cama. O Bidu não sai do lugar."),
    ('nar', "Fica sempre do lado contrário. Se o Bidu olhar pra cozinha, você vai pra sala. Se ele olhar pro seu quarto, você não entra no seu quarto.",
     S('corredor', C('voce', 'p1', None, eyes='wide', mouth='flat', facing=1), cam=dict(zoom=1.05, to=1.15), fx=[{'cachorro': (1150, 990, 'rosna')}])),
    ('nar', "Lá pelas quatro, o Bidu vai olhar pro seu quarto. E de lá vai vir um barulho de unha no vidro. Devagar. De cima pra baixo.",
     S('quarto', cam=dict(zoom=1.0, to=1.15), fx=[dict(JANELA_QUARTO, surge=True)])),
    ('coisa', "Filho, abre a janela pro pai. Só a janela.",
     S('quarto', cam=dict(zoom=1.3, to=1.45, cx=420, cy=380), fx=[JANELA_QUARTO])),
    ('nar', "A sua janela tem grade. Ela não passa pela grade. Mas, se você abrir o vidro, ela nem precisa passar. Ela só precisa que alguém de dentro abra alguma coisa.",
     S('corredor', C('voce', 'p2', None, eyes='wide', mouth='flat', sweat=True, facing=-1), cam=dict(zoom=1.15, to=1.25), fx=[{'cachorro': (560, 990, 'rosna')}])),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'NÃO PRENDA O **BIDU**')}])),
    ('nar', "Antes do dia clarear, ela vai tentar tirar o Bidu do caminho. Mas ela não vai fazer isso sozinha. Ela vai pedir pra você.",
     S('cortina', cam=dict(zoom=1.0, to=1.12), fx=[{'olhos': (960, 470), 'surge': True}])),
    ('coisa', "Filho, prende esse cachorro na lavanderia. Ele tá estranho. Ele não gosta mais do pai.",
     S('cortina', cam=dict(zoom=1.15, to=1.3, cx=960, cy=460), fx=[{'monstro': 'atras', 'quem': Q, 'pos': (960, 700), 's': 0.42, 'escuro': 0.25, 'boca': 'flat', 'surge': True}])),
    ('nar', "A voz agora tá triste. Cansada. É a voz do seu pai no fim de um turno de doze horas, pedindo uma coisa pequena. Só prender o cachorro.",
     S('sala', C('voce', 'centro', None, sit=True, eyes='sad', mouth='frown', facing=1), cam=dict(focus='voce', zoom=1.5, to=1.65))),
    ('nar', "Não prende. Com o Bidu trancado, ninguém mais rosna. E você fica sozinho com uma voz que você ama, sem ninguém pra te avisar que ela é mentira.",
     S('sala', C('voce', 'centro', None, sit=True, eyes='angry', mouth='flat', facing=1), cam=dict(zoom=1.05, to=1.15), fx=[{'cachorro': (760, 990, 'rosna')}])),
    ('nar', "Abraça o Bidu. Ele vai tremer. Você vai tremer. Mas ele não vai parar de rosnar. E esse vai ser o barulho mais bonito que você vai ouvir a noite inteira.",
     S('sala', C('voce', 'centro', None, sit=True, eyes='closed', mouth='flat', arms='point', facing=1), cam=dict(zoom=1.3, to=1.4, cx=700, cy=720), fx=[{'cachorro': (760, 990, 'rosna')}])),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'SÓ ABRA QUANDO ELE **ABANAR**')}])),
    ('nar', "Às seis e quarenta, o Bidu vai mudar. O rosnado para. A orelha levanta. E o rabo começa a bater no chão, tum, tum, tum, antes de você ouvir qualquer coisa.",
     S('porta_manha', cam=dict(zoom=1.2, to=1.35, cx=1150, cy=760), fx=[{'cachorro': (1180, 990, 'abana', -1)}])),
    ('nar', "Depois vem o portão. O molho de chaves. A chave entrando na fechadura e girando duas vezes.",
     S('preto', fx=[{'fechadura': True}])),
    ('nar', "Mesmo assim, espera. Deixa ele abrir sozinho. A coisa não tem chave. O seu pai tem."),
    ('nar', "E olha pro Bidu uma última vez. Se o rabo parar no meio do caminho, se a orelha baixar, se o ronco voltar, volta pro corredor e espera mais."),
    ('nar', "Quando a porta abrir por fora, com o seu pai cheirando a graxa e a café de garrafa térmica, o capacete branco debaixo do braço, o Bidu vai pular nele chorando de alegria. Aí sim. Aí pode abraçar.",
     S('sala_manha', C('pai', 'porta', None, facing=-1, mouth='smile', eyes='half', arms='up'), C('voce', 'centro', None, arms='up', eyes='happy', mouth='grin'), cam=dict(zoom=1.0, to=1.08), fx=[{'cachorro': (1380, 990, 'abana')}])),
    ('pai', "Que festa é essa? Parece que eu fiquei um mês fora.",
     S('sala_manha', C('pai', 'sofa2', None, facing=-1, mouth='grin'), C('voce', 'sofa', None, facing=1, eyes='closed', mouth='smile'), cam=dict(zoom=1.3, to=1.4, cx=940, cy=560))),
    ('nar', "Na varanda, o capacho tá molhado. E a jaqueta reserva do seu pai, a que ficava pendurada no gancho do lado da porta, sumiu. Ninguém fala nada.",
     S('varanda_manha', cam=dict(zoom=1.15, to=1.3, cx=1150, cy=600))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Umas semanas depois, numa noite qualquer, você acorda de novo às duas e dez. A casa tá quieta. O seu pai tá de folga, roncando no quarto dele.",
     S('quarto', quarto(eyes='half', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "E da sala vem um barulho que você conhece. Tum, tum, tum. O rabo do Bidu batendo no chão. Ele tá na frente da porta. Abanando. Feliz.",
     S('porta', cam=dict(zoom=1.15, to=1.3, cx=1000, cy=700), fx=[{'cachorro': (1180, 990, 'abana', -1)}])),
    ('nar', "Do lado de fora, alguém bate três vezes. E agora tem cheiro de graxa. De café. Da jaqueta do seu pai.",
     S('varanda_jaqueta', cam=dict(zoom=1.1, to=1.25, cx=960, cy=560), fx=[NA_PORTA])),
    ('coisa', "Filho, abre aí. Sou eu.",
     S('preto', fx=[dict(OLHO_PERTO, perto=1.0)])),
    ('nar', "O seu pai tá dormindo no quarto dele.",
     S('cama_escuro', C('pai', 'deitado', None, lie=True, eyes='closed', mouth='o'), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Não abre.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: o seu cachorro já rosnou pro nada no meio da noite?",
     S('preto', fx=[{'cta_mm': ('SEU CACHORRO JÁ', 'ROSNOU PRO NADA?')}])),
]
