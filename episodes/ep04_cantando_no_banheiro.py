"""Manual da Madrugada — Noite 04
Se a sua irmã estiver cantando no banheiro de madrugada… NÃO BATA NA PORTA
"""
from engine.dsl import S, C

TITLE = "Se a sua irmã estiver cantando no banheiro de madrugada… NÃO BATA NA PORTA"
NOITE = 4
LEAD = 2.0          # silêncio de ambiente antes da primeira fala
GAP_NAR = 0.75      # pausas de terror entre falas
PAUSA_REGRA = 2.0   # segura o cartão da regra
PAUSA_VOZ = 1.2     # respiro depois de cada voz da criatura
TAIL = 20.0
THUMB = dict(ordem='NÃO **BATA**', cena='banheiro', criatura='coisa_ep04', balao='Canta comigo?')

VOICES = {
    'nar': 'f22a680983644e699676e5b8879923c6',    # MM Narrador
    'coisa': 'e808da2329754929803c8bd98dc36857',  # Lucilene (imitando a irmã, com efeito)
    'irma': 'e808da2329754929803c8bd98dc36857',   # Lucilene (limpa)
}

# a coisa desta noite: imita a Duda de camisola, cabelo molhado cobrindo metade do rosto, cabeça torta,
# boca vertical, braços compridos; o detalhe vermelho é a xuxinha que a Duda perdeu no ralo
Q = 'coisa_ep04'
BOX = {'monstro': 'atras', 'quem': Q, 'pos': (1430, 862), 's': 0.7, 'escuro': 0.35}           # atrás do vidro embaçado
BOX_TETO = {'monstro': 'teto', 'quem': Q, 'pos': (1250, 0), 's': 0.66}                         # pendurada no teto, em cima do box
ESPELHO = {'monstro': 'janela', 'quem': Q, 'rect': (232, 252, 296, 296)}                       # no espelho embaçado
PORTA_BANHO = {'monstro': 'porta', 'quem': Q, 'rect': (820, 280, 240, 540), 'lado': 'dir', 'abre': 0.2}
PORTA_CLOSE = {'monstro': 'porta', 'quem': Q, 'rect': (640, 40, 640, 760), 'lado': 'dir', 'abre': 0.16}
PORTA_QUARTO = {'monstro': 'porta', 'quem': Q, 'rect': (760, 260, 230, 540), 'lado': 'esq', 'abre': 0.3}
TETO = {'monstro': 'teto', 'quem': Q, 'pos': (1130, 0), 's': 0.6}


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
    ('nar', "Se a sua irmã estiver cantando no banheiro de madrugada, não bata na porta. Não pergunte se vai demorar. Não cante junto. E, aconteça o que acontecer, não entregue nada pra ela.",
     S('banho', cam=dict(zoom=1.0, to=1.12), fx=['piscar', dict(BOX, surge=True)])),
    ('nar', "Eu não tô falando de quando ela entra no banho às sete da manhã, liga a caixinha de som no último volume e canta a mesma música de novela até a água acabar.",
     S('corredor_banho_manha', corredor('p3', eyes='half', mouth='frown', arms='cross', facing=-1))),
    ('nar', "Também não tô falando de quando ela canta escovando os dentes, com a boca cheia de espuma, só pra te irritar.",
     S('banho_manha', C('irma', 'pia', None, mouth='grin', eyes='happy', arms='hold', prop='escova'), C('voce', 'porta', None, eyes='half', mouth='flat', facing=-1),
       cam=dict(zoom=1.05, to=1.12, cx=520, cy=640))),
    ('nar', "Eu tô falando disso.",
     S('preto')),
    ('nar', "Os seus pais foram pra formatura de um primo em Goiânia. Voltam de ônibus, domingo de manhã. A sua irmã, a Duda, tem dezessete anos e ficou responsável por você.",
     S('sala', C('irma', 'sofa2', None, sit=True, mouth='smile', arms='hold', prop='celular'), C('voce', 'sofa', None, sit=True, mouth='smile'), cam=dict(zoom=1.0, to=1.08))),
    ('nar', "Na prática, isso quer dizer que ela fez miojo pros dois, se trancou no quarto às nove e passou a noite de fone, rindo com as amigas no celular.",
     S('cama_duda', C('irma', 'deitado', None, lie=True, eyes='happy', mouth='grin', arms='hold', prop='celular'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Na sua casa só tem um banheiro. Fica no meio do corredor, entre o quarto dela e o seu.",
     S('corredor_banho', cam=dict(zoom=1.0, to=1.1))),
    ('nar', "São três e dez da manhã.",
     S('preto', fx=[{'texto': ['03:10'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Você acorda com sede. E, antes de levantar, você ouve. Do banheiro, baixinho, a voz da Duda. Cantando.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.05, to=1.2))),
    ('coisa', "Peixinho do ralo, sobe que eu te falo... se a água esfriar, ninguém vai te achar...",
     S('banho', cam=dict(zoom=1.2, to=1.35, cx=1430, cy=520), fx=[BOX, 'zoom_punch'])),
    ('nar', "Você conhece essa música. A Duda inventou quando tinha sete anos e cantava toda vez que te dava banho, quando você era pequeno. Ela nunca mais cantou. Morre de vergonha dela.",
     S('quarto', quarto(eyes='wide', mouth='o', sweat=True), cam=dict(focus='voce', zoom=1.6, to=1.75))),
    ('nar', "Tem luz acesa por baixo da porta. Sai vapor pela fresta, como se alguém tivesse tomado um banho quente e demorado. Mas o chuveiro tá desligado. Não tem barulho de água. Nem uma gota.",
     S('banheiro_porta', cam=dict(zoom=1.0, to=1.15, cy=560), fx=['piscar'])),
    ('nar', "E a porta do quarto da Duda tá entreaberta. Na luz do celular, você vê ela. Deitada. Dormindo de boca aberta, com o fone ainda no ouvido.",
     S('cama_duda', C('irma', 'deitado', None, lie=True, eyes='closed', mouth='o'), cam=dict(zoom=1.2, to=1.35, cx=1000, cy=600))),

    # ---------------------------------------------------------------- O QUE É
    ('nar', "Presta atenção, porque isso é importante. A coisa que tá no banheiro sobe pelo ralo. Ela mora nos canos da casa. E os canos escutam tudo o que se canta no chuveiro.",
     S('banho', cam=dict(zoom=1.0, to=1.15), fx=[dict(ESPELHO, surge=True)])),
    ('nar', "Cada música, cada voz, cada desafinada. Por isso ela sabe a voz da Duda. Sabe até a música que nem você lembrava mais.",
     S('banho', cam=dict(zoom=1.35, to=1.5, cx=1430, cy=780))),
    ('nar', "Mas lá embaixo é escuro. Ela não enxerga nada. Não sabe quem tá do lado de fora da porta, nem quantos, nem onde.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'escuro': 0.65, 'surge': True}])),
    ('nar', "E ela não consegue sair sozinha. Bater na porta do banheiro é dizer: sai daí, eu tô esperando. E ela é muito obediente.",
     S('banheiro_porta', cam=dict(zoom=1.15, to=1.3, cx=960, cy=520))),

    # ---------------------------------------------------------------- GANCHO
    ('nar', "E pensa bem nisso. Quantas vezes você já cantou no chuveiro achando que tava sozinho? Alto, desafinado, sem vergonha nenhuma, porque ninguém tava ouvindo.",
     S('banho_manha', C('voce', 'pia', None, eyes='closed', mouth='grin', arms='up'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Agora lembra daquele barulho que o ralo faz de vez em quando. Aquele gorgolejo, quando ninguém deu descarga e ninguém abriu torneira nenhuma.",
     S('banho', cam=dict(zoom=1.5, to=1.7, cx=1430, cy=800))),
    ('nar', "Talvez seja só ar no cano. Talvez seja alguém aplaudindo.",
     S('banho', cam=dict(zoom=1.1, to=1.2, cx=1300, cy=520), fx=[dict(BOX, surge=True, boca='grin')])),

    # ---------------------------------------------------------------- REGRA 1
    ('nar', "Regra número um.",
     S('preto', fx=[{'regra': (1, 'NÃO **BATA** NA PORTA')}])),
    ('nar', "Não bata. Nem de leve, nem com a ponta do dedo. Não fala Duda, sai logo. Não pergunta se vai demorar.",
     S('corredor_banho', corredor('meio', arms='face'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Isso é mais difícil do que parece. Você cresceu batendo nessa porta. Toda manhã, antes da escola, alguém esmurra e grita que vai se atrasar. A sua mão vai querer ir sozinha. Enfia as duas no bolso do moletom.",
     S('corredor_banho', corredor('meio', eyes='closed', mouth='wavy', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.6))),
    ('nar', "Se ela perceber que tem alguém no corredor, a música para no meio. E ela pergunta.",
     S('banheiro_porta', cam=dict(zoom=1.1, to=1.25))),
    ('coisa', "Tem alguém aí fora?",
     S('banho', cam=dict(zoom=1.3, to=1.45, cx=1430, cy=480), fx=[dict(BOX, boca='flat')])),
    ('nar', "Fica quieto. Pra ela, uma pergunta sem resposta é um corredor vazio. E um corredor vazio não tem ninguém esperando.",
     S('corredor_banho', corredor('meio', eyes='half'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- REGRA 2
    ('nar', "Regra número dois.",
     S('preto', fx=[{'regra': (2, 'NÃO CANTE **JUNTO**')}])),
    ('nar', "A música da Duda tem uma última parte. Uma parte que só vocês dois sabem, porque era você que cantava, sentado na banheira, batendo a mão na água.",
     S('quarto', quarto(eyes='sad', mouth='flat'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Ela vai cantar tudo de novo. E vai parar logo antes do fim.",
     S('banheiro_porta', cam=dict(zoom=1.0, to=1.12))),
    ('coisa', "Peixinho do ralo, sobe que eu te falo... se a água esfriar...",
     S('banho', cam=dict(zoom=1.15, to=1.28, cx=1250, cy=400), fx=[dict(BOX_TETO, surge=True)])),
    ('nar', "E fica esperando. A sua boca vai completar sozinha, do mesmo jeito que você completa uma música no rádio. Morde a manga do moletom.",
     S('quarto', quarto(eyes='closed', mouth='wavy', arms='face', sweat=True), cam=dict(focus='voce', zoom=1.5, to=1.65))),
    ('nar', "Se você cantar, ela aprende a sua voz. E aprende que tem um maninho do lado de fora. Esperando.",
     S('quarto', quarto(eyes='wide', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Se você não cantar, ela tenta de outro jeito. Ela erra de propósito.",
     S('banho', cam=dict(zoom=1.05, to=1.15))),
    ('coisa', "...ninguém vai te achar. E a mamãe vem me buscar.",
     S('banho', cam=dict(zoom=1.4, to=1.55, cx=380, cy=400), fx=[ESPELHO])),
    ('nar', "Não é assim. Você sabe que não é. E tudo dentro de você vai querer corrigir. Quem conhece uma música não aguenta ouvir ela errada. Não corrige.",
     S('quarto', quarto(eyes='angry', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.45, to=1.55))),

    # ---------------------------------------------------------------- REGRA 3
    ('nar', "Regra número três.",
     S('preto', fx=[{'regra': (3, 'NÃO CORTE A **LUZ**')}])),
    ('nar', "Você ainda tá com sede. A cozinha fica do outro lado do corredor. Dá pra ir. Mas olha pro chão antes.",
     S('corredor_banho', corredor('p3', facing=-1), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "Aquela faixa de luz debaixo da porta é o único jeito que ela tem de saber se alguém passou. Um pé na frente da fresta faz sombra. E sombra quer dizer: tem gente aqui. Bem aqui.",
     S('banheiro_porta', cam=dict(zoom=1.5, to=1.7, cx=960, cy=700), fx=[{'olhos': (960, 785), 'surge': True}])),
    ('nar', "Anda colado na parede, do lado oposto. Devagar. De meia, nunca de chinelo. Chinelo estala.",
     S('corredor_banho', corredor('dir', eyes='half', facing=-1), cam=dict(zoom=1.15, to=1.25))),
    ('nar', "E, se você já fez sombra, não para. Volta pro quarto do mesmo jeito que saiu. Ela vai ficar com o olho na fresta até o dia clarear, tentando entender o que passou ali.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.0, to=1.12), fx=[dict(PORTA_QUARTO, abre=0.22)])),

    # ---------------------------------------------------------------- REGRA 4
    ('nar', "Regra número quatro.",
     S('preto', fx=[{'regra': (4, 'NÃO ENTREGUE A **TOALHA**')}])),
    ('nar', "Lá pelas quatro, a maçaneta do banheiro vai girar sozinha. E a porta vai abrir um dedo. Só o suficiente pra passar uma mão.",
     S('banheiro_porta', cam=dict(zoom=1.0, to=1.12), fx=['piscar'])),
    ('coisa', "Maninho? Esqueci a toalha. Pega pra mim e pendura na maçaneta?",
     S('banheiro_porta', cam=dict(zoom=1.25, to=1.4, cx=1180, cy=420), fx=[dict(PORTA_CLOSE, surge=True)])),
    ('nar', "A Duda nunca esqueceu a toalha na vida. Ela entra no banho com toalha, roupa, celular, caixinha de som, e só sai uma hora depois.",
     S('cama_duda', C('irma', 'deitado', None, lie=True, eyes='closed', mouth='flat'), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Entregar qualquer coisa por essa fresta é a mesma coisa que bater. É a sua mão dizendo: tô aqui, pode sair.",
     S('corredor_banho', corredor('dir', facing=-1, arms='point'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "E repara no que ela te chamou. Maninho. Ninguém te chama assim desde que você tinha cinco anos. Ela tá chegando perto de saber quem você é.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.1}, 'zoom_punch'])),
    ('nar', "Volta pra cama. A mão vai ficar lá, parada na fresta, esperando. A noite inteira, se precisar.",
     S('quarto', quarto(eyes='half', mouth='flat', arms='face'), cam=dict(focus='voce', zoom=1.4, to=1.5))),

    # ---------------------------------------------------------------- REGRA 5
    ('nar', "Regra número cinco.",
     S('preto', fx=[{'regra': (5, 'FIQUE LONGE DA **ÁGUA**')}])),
    ('nar', "Quando ela cansar de esperar, a água vai começar a sair por baixo da porta. Morna. Devagar. Espalhando pelo corredor, como se o chuveiro tivesse ficado ligado a noite toda.",
     S('corredor_agua', cam=dict(zoom=1.0, to=1.15))),
    ('nar', "A água é o jeito dela de tatear. Cada coisa que a água encosta, ela sente. O pé da cômoda. O tapete. A porta do seu quarto.",
     S('corredor_agua', cam=dict(zoom=1.4, to=1.6, cx=960, cy=900))),
    ('coisa', "Tá esfriando, maninho... a água tá esfriando.",
     S('corredor_agua', cam=dict(zoom=1.2, to=1.35, cx=940, cy=520), fx=[PORTA_BANHO])),
    ('nar', "Sobe na cama. Encolhe os pés. Não deixa a meia, a ponta do lençol, nem o fio do carregador encostar no chão.",
     S('quarto', quarto(eyes='wide', mouth='flat', sweat=True), cam=dict(zoom=1.05, to=1.15))),
    ('nar', "E não olha pro forro. Os canos da casa passam lá em cima, bem em cima da sua cama. Você vai ouvir um gotejar. Não é goteira.",
     S('quarto', quarto(eyes='closed', mouth='flat', arms='face'), cam=dict(zoom=1.0, to=1.12), fx=[dict(TETO, surge=True)])),

    # ---------------------------------------------------------------- REGRA 6
    ('nar', "Regra número seis.",
     S('preto', fx=[{'regra': (6, 'SEGURE A MÃO DA **DUDA**')}])),
    ('nar', "Às quatro e meia, a porta do quarto da Duda vai ranger. Ela acordou com vontade de ir ao banheiro. Meio dormindo, sem fone, descalça. Ela não sabe de nada.",
     S('corredor_agua', C('irma', 'p1', None, eyes='half', mouth='flat', facing=1), cam=dict(zoom=1.0, to=1.1))),
    ('nar', "Ela vai ver a luz. Vai ouvir a música. Vai ficar parada no meio do corredor, ouvindo a própria voz do outro lado da porta.",
     S('corredor_agua', C('irma', 'meio', None, eyes='wide', mouth='o', facing=1), cam=dict(zoom=1.2, to=1.35, cx=760, cy=600))),
    ('nar', "E aí vêm duas batidas. Lá de dentro. Toc, toc. Era o código de vocês quando você era pequeno: duas batidas queriam dizer tá tudo bem aí? E a resposta era três.",
     S('banho', cam=dict(zoom=1.15, to=1.3, cx=1300, cy=520), fx=[dict(BOX, boca='grin'), 'shake'])),
    ('nar', "A mão da Duda vai subir sozinha. Do jeito que subia todo dia. Ela já tá encostando na madeira. Segura. Segura a mão dela e puxa pra longe. Sem falar nada.",
     S('corredor_agua', C('irma', 'meio', None, eyes='half', mouth='flat', arms='point', facing=1), corredor('p1', arms='point'), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Leva ela pro seu quarto. Fecha a porta. E sobe com ela na cama.",
     S('quarto', quarto(eyes='half', mouth='flat'), C('irma', 'centro', None, eyes='wide', mouth='o', sweat=True), cam=dict(zoom=1.0, to=1.1))),
    ('coisa', "Duda... me deixa sair. Aqui dentro é tão frio.",
     S('corredor_agua', cam=dict(zoom=1.3, to=1.45, cx=940, cy=500), fx=[dict(PORTA_BANHO, abre=0.25, boca='flat')])),
    ('irma', "Essa é a minha voz. Por que essa é a minha voz?",
     S('quarto', quarto(eyes='sad', mouth='flat'), C('irma', 'centro', None, eyes='sad', mouth='o'), cam=dict(focus='irma', zoom=1.45, to=1.6))),
    ('nar', "Não responde. Abraça ela. Ela vai segurar a sua mão do jeito que segurava quando você era pequeno e tinha medo do ralo. E, pela primeira vez, é você que cuida dela.",
     S('quarto', quarto(eyes='closed', mouth='flat'), C('irma', 'centro', None, eyes='closed', mouth='flat'), cam=dict(zoom=1.05, to=1.15))),

    # ---------------------------------------------------------------- REGRA 7
    ('nar', "Regra número sete.",
     S('preto', fx=[{'regra': (7, 'ESPERE O **RALO** ENGOLIR')}])),
    ('nar', "Quando o céu ficar cinza, a luz por baixo da porta vai apagar. Não sai ainda. Silêncio não quer dizer que ela foi embora.",
     S('corredor_banho_manha', cam=dict(zoom=1.05, to=1.2, cx=940, cy=560), fx=[{'olhos': (940, 470), 'surge': True}])),
    ('nar', "Espera o sol bater no vitrô do banheiro. Espera o gorgolejo comprido do ralo, que nem um gole de água descendo. E olha a água do corredor. Ela vai voltar. Devagar. Escorrendo pra debaixo da porta, ao contrário.",
     S('preto', fx=[{'texto': ['06:15'], 'pos': 'centro', 'cor': '#E5262B'}])),
    ('nar', "Quando o chão estiver seco, aí sim. Abre a porta. De uma vez. Sem bater.",
     S('banheiro_porta', cam=dict(zoom=1.0, to=1.1))),
    ('nar', "O box tá seco. O espelho, limpo. E, em cima do ralo, tem uma xuxinha vermelha. A que a Duda perdeu no banho quando tinha nove anos e chorou a tarde inteira procurando.",
     S('banho_manha', C('voce', 'porta', None, eyes='wide', mouth='o', facing=1), cam=dict(zoom=1.3, to=1.45, cx=1200, cy=700))),
    ('irma', "Joga isso fora. E não conta nada pra mãe, tá? Ela vai achar que a gente ficou doido.",
     S('corredor_banho_manha', C('irma', 'meio', None, eyes='half', mouth='flat', arms='cross', facing=1), corredor('dir', eyes='half', facing=-1), cam=dict(zoom=1.1, to=1.2))),
    ('nar', "Você joga. No lixo da cozinha, lá fora, longe de qualquer ralo. E, quando os seus pais chegam, os dois tomam café rindo da formatura, e a casa parece a mesma de sempre.",
     S('cozinha', C('irma', 'b', None, facing=-1, mouth='smile', arms='hold', prop='caneca'), C('voce', 'a', None, eyes='half', mouth='smile'), cam=dict(zoom=1.0, to=1.1))),

    # ---------------------------------------------------------------- VIRADA
    ('nar', "Mas tem uma coisa que eu ainda não te contei.",
     S('preto', fx=['piscar'])),
    ('nar', "Naquela noite, antes de você segurar a mão da Duda, o dedo dela encostou na porta. Um toque só. Tão de leve que você achou que nem contava.",
     S('banheiro_porta', C('irma', 'esq', None, eyes='half', mouth='flat', arms='point', facing=1), cam=dict(zoom=1.4, to=1.6, cx=760, cy=520))),
    ('nar', "Contava.",
     S('preto', fx=['piscar'])),
    ('nar', "Umas semanas depois, você tá no banho sozinho, de tarde, e se pega cantarolando a música da Duda. Você para no meio. E o ralo continua. Com a sua voz.",
     S('banho', C('voce', 'box', None, eyes='wide', mouth='o', sweat=True, facing=-1), cam=dict(zoom=1.15, to=1.3, cx=1300, cy=560))),
    ('nar', "Aí, do lado de fora, alguém bate na porta. Duas vezes.",
     S('banho', C('voce', 'box', None, eyes='wide', mouth='flat', facing=-1), cam=dict(zoom=1.0, to=1.1), fx=['shake'])),
    ('coisa', "Maninho... tá demorando.",
     S('banho', C('voce', 'box', None, eyes='wide', mouth='o', sweat=True, facing=-1), cam=dict(zoom=1.0, to=1.08), fx=[{'monstro': 'lateral', 'quem': Q, 'lado': 'esq', 'y': 1120, 's': 1.2, 'surge': True}])),
    ('nar', "A Duda tá na escola. A casa tá vazia. E agora quem tá do lado de dentro do banheiro é você.",
     S('preto', fx=[{'monstro': 'rosto', 'quem': Q, 's': 3.0, 'surge': True}, 'zoom_punch'])),

    # ---------------------------------------------------------------- CTA
    ('nar', "Agora você conhece as regras. Se inscreve antes que a luz apague. E me conta nos comentários: qual música você canta no chuveiro achando que ninguém tá ouvindo?",
     S('preto', fx=[{'cta_mm': ('O QUE VOCÊ CANTA', 'NO CHUVEIRO?')}])),
]
