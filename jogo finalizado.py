#Aluno: Wesley Florencio Ferreira - Curso: Analise e Desenvolvimento de sistemas
#Materia: Raciocinio Computacional
import random


# Constantes do jogo
class Constantes(object):
    FACES_DADO_VERDE: tuple = "C", "P", "C", "T", "P", "C"
    FACES_DADO_AMARELO: tuple = "T", "P", "C", "T", "P", "C"
    FACES_DADO_VERMELHO: tuple = "T", "P", "T", "C", "P", "T"

    ESTADO_JOGANDO: str = "JOGANDO"
    ESTADO_ACABAR_JOGO: str = "ACABAR_JOGO"
    ESTADO_EMPATE: str = "EMPATE"


# Objeto dados para construir os diferentes dados
class Dado(object):
    # construtor
    def __init__(self, cor, faces, face_para_cima, ja_contado):
        self.cor: str = cor
        self.faces: str = faces
        self.face_para_cima: str = face_para_cima
        self.ja_contado: bool = ja_contado

    @staticmethod
    def get_nome_face(face: str):
        if face == "P":
            return "Passos"
        elif face == "C":
            return "Cerebro"
        else:
            return "Tiro"


# Objeto jogador para construir os diferentes jogadores
class Jogador(object):
    vida: int = 3
    pontos: int = 0
    temp_pontos: int = 0
    rodada: int = 0
    ordem: int = 0
    dados: list = []

    # construtor
    def __init__(self, nome, vida, pontos, rodada_, ordem, dados):
        self.nome: str = nome
        self.vida = vida
        self.pontos = pontos
        self.rodada = rodada_
        self.ordem = ordem
        self.dados = dados

    @staticmethod
    def esta_vivo(vida):
        if vida > 0:
            return True
        else:
            return False


# Objeto mesa para guardar os dados presentes na mesa
class Mesa(object):
    dados: list = []

    # construtor
    def __init__(self, dados):
        self.dados = dados


# Configuracoes do jogo, armazenar numero de jogadores, dados disponiveis (antes de entrar no tubo), etc
class ConfiguracaoJogo(object):
    num_jogadores: int = 0
    dados_disponiveis: list = []

    # construtor
    def __init__(self, dados_disponiveis):
        self.dados_disponiveis = dados_disponiveis


# Um objeto para monitorar o estado do jogo e guardar as configuracoes
class Jogo(object):
    estado: str = Constantes.ESTADO_JOGANDO
    config: ConfiguracaoJogo = ConfiguracaoJogo([])
    mesa: Mesa = Mesa([])
    tubo_de_dados: list = []
    rodada: int = 0
    turno: int = 0
    jogadores: list = []

    def __init__(self, estado, config, jogadores, tubo_de_dados, mesa, rodada, turno):
        self.estado = estado
        self.config = config
        self.mesa = mesa
        self.tubo_de_dados = tubo_de_dados
        self.rodada = rodada
        self.turno = turno
        self.jogadores = jogadores


# Desenha 3 dados da lista de dados passada
def desenha_dados(dados: list):
    d1: str = dados[0]
    d2: str = dados[1]
    d3: str = dados[2]
    return f"\n\t  {d1.cor.upper()} \t{' ' * 12}{d3.cor.upper()}\n" \
           f"\t   _____     {d2.cor.upper().ljust(11)}_____\n" \
           f"\t  /\\  {d1.face_para_cima} \\    _____     /\\  {d3.face_para_cima} \\ \n" \
           f"\t /  \\____\\  / {d2.face_para_cima}  /\\   /  \\____\\ \n" \
           f"\t \\  /    / /____/  \\  \\  /    /\n" \
           "\t  \\/____/  \\    \\  /   \\/____/ \n" \
           f"\t {d1.get_nome_face(d1.face_para_cima).upper().ljust(11)}\\____\\/" \
           f"{d3.get_nome_face(d3.face_para_cima).upper().rjust(11, ' ')}" \
           f"\n{d2.get_nome_face(d2.face_para_cima).upper().rjust(25, ' ')}"


# Metodo para desenhar um trofeu com o nome do jogador
def desenha_trofeu(jogador: Jogador):
    return "\t .-=========-." \
           "\n\t \\'-=======-'/" \
           "\n\t _|   .=.   |_" \
           "\n\t((|   {#1}  |))" \
           "\n\t \\|   /|\\   |/" \
           "\n\t  \\__ '`' __/" \
           "\n\t    _`) (`_" \
           "\n\t  _/_______\\_" \
           "\n\t /___________\\" \
           f"\n [Parabéns {jogador.nome}]"


# Funcao para evitar repeticao de confirmacoes
def dialogo_confirmacao(mensagem: str):
    opcao = '?'
    while opcao.upper() != 'N' and opcao.upper() != 'S':
        print(f"\n{monta_titulo_secao('pergunta')}")
        opcao = input("\t" + mensagem + "\n\t[S]im [N]ão: ")
    return True if opcao.upper() == 'S' else False


# Define numero de jogadores e chama metodo para os demais outros atributos
def definir_jogadores():
    print(monta_titulo_secao("CONF. INICIAL") + "\n└───Vamos configurar o jogo!──────────────────────────│")
    try:
        num_jogadores = int(input(f"──── Defina o número de jogadores (minimo 2):"))
        if num_jogadores < 2:
            print(f"No minimo 2 jogadores são necessarios")
        else:
            if dialogo_confirmacao(f"Você selecionou {num_jogadores} jogadores, confirma?"):
                return nomear_jogadores(dialogo_confirmacao(f"Deseja nomear os {num_jogadores} jogadores?"),
                                        num_jogadores)
    except ValueError:
        print(f"Tem de ser um numero inteiro!!")
    return definir_jogadores()


# Metodo para atribuir nome para os jogadores, caso o jogador nao deseje atribuir um nome o padrao é setado como
# "Jogador #", retorna uma lista de jogadores
def nomear_jogadores(deseja_nomear: bool, num_jogadores: int):
    i = 0
    jogadores: list = []
    while i < num_jogadores:
        i += 1
        nome = f"Jogador {i}"
        if deseja_nomear:
            nome = input(f"──── Qual o nome Nome do Jogador {i}: ")
            # Se não foi digitado nenhum nome, atribui "Jogador #"
            nome = f"Jogador {i}" if len(nome) == 0 else nome
            # Verifica duplicidade se existe adicionar pos-fixo [#]
            dup: int = sum(x.nome == nome for x in jogadores)
            if dup:
                print(f"Nome duplicado, adicionando pos-fixo")
                nome = nome + f" [{dup + 1}]"
        jogador = Jogador(nome, 3, 0, 0, 0, [])
        if deseja_nomear and dialogo_confirmacao(f"O nome do jogador: {nome}, esta correto ?") or not deseja_nomear:
            jogadores.append(jogador)
        else:
            i -= 1
    return jogadores


# Verifica se uma das condições de finalização do jogo foram atingidas
def verificar_estado_jogo(jogo: Jogo):
    # Conta todos jogadores vivos
    #jogadores_vivos = list(filter(lambda x: x.vida > 0, jogo.jogadores))
    #if len(jogadores_vivos) == 0:
    #    print("Todos jogadores morreram, não houve vencedores nessa partida")
    #if len(jogadores_vivos) == 1:
    #    print("\tSomente 1 jogador vivo, ele é o vencedor")
    #    print(desenha_trofeu(jogadores_vivos[0]))
    #    jogo.estado = Constantes.ESTADO_ACABAR_JOGO

    # Verifica todos jogadores que atingiram 13 pontos ou mais
    jogadores_pontuacao = list(filter(lambda x: x.pontos >= 13 and x.vida > 0, jogo.jogadores))
    if len(jogadores_pontuacao) == 1:
        print(f"\tO jogador {jogadores_pontuacao[0].nome} atingiu 13 pontos, ele é o vencedor")
        print(desenha_trofeu(jogadores_pontuacao[0]))
        jogo.estado = Constantes.ESTADO_ACABAR_JOGO
        input("\n Pressione ENTER para ver o placar...\n")
        print(get_placar(jogo.jogadores, jogadores_pontuacao[0]))
    elif len(jogadores_pontuacao) > 1:
        print("\tMais de 1 jogador atingiu a pontuacao necessaria para vitoria, irão para uma rodada de desempate")
        jogo.estado = Constantes.ESTADO_EMPATE


# Sorteia ordem dos jogadores, embaralhando a lista e definindo o valor do atributo "ordem" para facilidade de
# comparacao e exibicao
def sorteia_ordem(jogadores: list):
    input("\n Pressione ENTER para sortear a ordem dos jogadores...\n")
    print(monta_titulo_secao("Sorteio Ordem") + f"\n\t{monta_titulo_secao('Ordem definida', max_=18)}")
    random.shuffle(jogadores)
    for i in range(0, len(jogadores)):
        jogadores[i].ordem = i + 1
        print(f"\t{i + 1} - {jogadores[i].nome}")
    print(f"\t{monta_rodape_secao(max_=18)}\n{monta_rodape_secao()}")
    if not dialogo_confirmacao("Jogadores sorteados, deseja manter essa ordem?"):
        sorteia_ordem(jogadores)


# Metodo chamado apos definicoes iniciais de dados e jogadores, sorteia a ordem, e inicia uma nova rodada
# executado ate ter um vencedor
def inicia_jogo(jogo: Jogo):
    sorteia_ordem(jogo.jogadores)
    adiciona_dados_tubo(jogo.tubo_de_dados, jogo.config.dados_disponiveis)
    inicia_nova_rodada(jogo)


# Espera uma lista de dados, adiciona eles no tubo para serem sorteados pelo jogador e mistura
# Tambem seta o atributo como "ja contato" como false, para garantir que os dados de cerebro serao contados
# quando sorteados novamente
def adiciona_dados_tubo(tubo_de_dados: list, dados: list):
    for dado in dados:
        dado.ja_contado = False
        tubo_de_dados.append(dado)
    random.shuffle(tubo_de_dados)


# Inicia uma nova rodada, uma rodada termina quando todos jogadores tiverem jogados ao menos 1 turno
def inicia_nova_rodada(jogo):
    while jogo.estado != Constantes.ESTADO_ACABAR_JOGO:
        jogo.rodada += 1
        print(f"\n{monta_titulo_secao(f'Rodada #{jogo.rodada}')}")
        for jogador in jogo.jogadores:
            verificar_estado_jogo(jogo)
            #if not jogador.esta_vivo(jogador.vida):
            #    continue
            if jogo.estado == Constantes.ESTADO_ACABAR_JOGO:
                break
            jogador.rodada = jogo.rodada
            jogador.temp_pontos = 0
            jogador.vida = 3
            inicia_novo_turno(jogo, jogador)
        print(monta_rodape_secao())
        if jogo.estado == Constantes.ESTADO_ACABAR_JOGO:
            break
        verificar_estado_jogo(jogo)
    else:
        print(f"\tAcabou o jogo!! Obrigado por jogar ")


# Inicia um novo turno, passando a vez para o proximo jogador
def inicia_novo_turno(jogo: Jogo, jogador: Jogador):
    jogo.turno += 1
    # Reseta a vida
    jogador.vida = 3
    # Retorna todos dados da mesa para o tubo, se houver e limpa a mesa
    if len(jogo.mesa.dados) > 0:
        adiciona_dados_tubo(jogo.tubo_de_dados, jogo.mesa.dados)
        jogo.mesa.dados = []

    print(f"\t{monta_titulo_secao(f'Turno #{jogo.turno}', max_=45)}")
    print(f"\t ── É a vez de {jogador.nome} jogar")
    print(f"{get_status_jogador(jogador)}")
    deseja_continuar: int = 5
    # O turno continua ate uma das condições serem atingidas
    # Jogador possui mais que 0 de vida (ou seja nao possui 3 dados com a face de tiro virada para cima)
    # Jogador faz 13 pontos
    # Jogador possui dados com a face cerebro ou passos na mesa E deseja continuar
    preparado: int = 0
    while preparado != 5:
        preparado = fase_preparacao(jogo, jogador, e_novo_turno=True)
        deseja_continuar = preparado
    while deseja_continuar != 6 and jogador.esta_vivo(jogador.vida) and jogador.pontos < 13:
        if deseja_continuar == 5:
            jogar_dados(jogo, jogador)
        if jogador.vida > 0 and jogador.pontos < 13 and jogo.estado != Constantes.ESTADO_ACABAR_JOGO:
            deseja_continuar = fase_preparacao(jogo, jogador, False)
    else:
        if deseja_continuar == 6:
            print(f"\t{jogador.nome} > [Passou a vez]")
            jogador.pontos += jogador.temp_pontos
        elif not jogador.esta_vivo(jogador.vida):
            print(f"\t {jogador.nome} > [Esta morto]")
            print(f"\t Dessa vez esse zumbi morreu de vez")
            input("\n\t Pressione ENTER para continuar...\n")
    print(f"\t{monta_rodape_secao(max_=45)}")


# Um menu de preparacao antes de lancar os dados
# Recebe o objeto jogador da vez, e um identificador se é novo turno ou nao
def fase_preparacao(jogo: Jogo, jogador: Jogador, e_novo_turno=False):
    opcao = 0
    try:
        # Se for novo turno, nao existe aw opção da passar a vez
        if e_novo_turno:
            opcao = int(input(
                f"[1] Ver meus status [2] Ver dados no tubo [3] Ver dados na mesa [4] Ver placar [5] Jogar dados "))
        else:
            opcao = int(input(
                f"[1] Ver meus status [2] Ver dados no tubo [3] Ver dados na mesa [4] Ver placar [5] Continuar a jogar dados [6] Passar a vez "))
        if opcao < 0 or ((opcao > 5 and e_novo_turno) or opcao > 6 and not e_novo_turno):
            print("\tSelecione uma opção valida")
        elif opcao == 1:
            print(get_status_jogador(jogador))
        elif opcao == 2:
            print(get_dados_tubo(jogo.tubo_de_dados))
        elif opcao == 3:
            print(get_dados_mesa(jogo.mesa))
        elif opcao == 4:
            print(get_placar(jogo.jogadores, jogador))
    except ValueError:
        print(f"\t\tTem de ser um numero inteiro!!")
    return opcao


# Metodo para retornar um texto com o status do jogador, vida, pontos e se ainda esta vivo
def get_status_jogador(jogador: Jogador):
    texto_retorno: str = f"\t{monta_titulo_secao('Status', max_=35)}"
    texto_retorno = texto_retorno + f"\n\t {jogador.nome}"
    texto_retorno = texto_retorno + f"\n\t ♥ Vida {jogador.vida}/3"
    texto_retorno = texto_retorno + f"\n\t ♦ Pontos {jogador.pontos}/13"
    texto_retorno = texto_retorno + f"\n\t ♦ Pontos do Turno {jogador.temp_pontos}/13"
    texto_retorno = texto_retorno + f"\n\t{monta_rodape_secao(max_=35)}"
    return texto_retorno


# Exibe uma lista com os dados atualmente no tubo de dados
def get_dados_tubo(tubo_de_dados):
    texto_retorno: str = f"\t{monta_titulo_secao('DADOS TUBO', max_=30)}"
    for cor in sorted({x.cor for x in tubo_de_dados}):
        texto_retorno = texto_retorno + f"\n\t Dado(s) {cor}(s): {sum(x.cor == cor for x in tubo_de_dados)} "
    texto_retorno = texto_retorno + f"\n\t Total: {len(tubo_de_dados)} "
    texto_retorno = texto_retorno + f"\n\t{monta_rodape_secao(max_=30)}"
    return texto_retorno


# Exibe uma lista com os dados atualmente na mesa e as respectivas faces
def get_dados_mesa(mesa: Mesa):
    texto_retorno: str = f"\t{monta_titulo_secao('DADOS NA MESA')}"
    if len(mesa.dados) > 0:
        for cor in sorted({x.cor for x in mesa.dados}):
            texto_retorno = texto_retorno + f"\n\t Dado(s) {cor}(s): {sum(x.cor == cor for x in mesa.dados)}"  # Soma os dados de suas respectivas cores
            faces: list = list(x.face_para_cima if x.cor == cor else None for x in
                               mesa.dados)  # Filtra os dados pela cor e monta uma lista com as faces
            texto_retorno = texto_retorno + f"\n\t ─ Face(s): {', '.join(filter(None, faces))}"
        texto_retorno = texto_retorno + f"\n\t Total: {len(mesa.dados)} "
    else:
        texto_retorno = texto_retorno + f"\n\t Nenhum dado presente na mesa"
    texto_retorno = texto_retorno + f"\n\t{monta_rodape_secao(max_=50)}"
    return texto_retorno


# Exibe uma lista com os jogadores, sua pontuacao e status se vivo ou nao
def get_placar(jogadores: list, jogador_da_vez: Jogador):
    # Soma os dados de suas respectivas cores
    texto_retorno: str = f"\t{monta_titulo_secao('PLACAR')}"
    for jogador in jogadores:
        indicador: str = ""
        status: str = "VIVO"
        nome: str = jogador.nome
        pontos: int = jogador.pontos
        if jogador.nome == jogador_da_vez.nome:
            indicador = ">>"
        if not jogador.esta_vivo(jogador.vida):
            nome = jogador.nome = '\u0336'.join(jogador.nome) + '\u0336'  # Riscar o nome dos jogadores mortos
            status = "MORTO"
        texto_retorno = texto_retorno + f"\n\t {indicador} {nome} \t\t Pontos: {str(pontos).rjust(2, '0')} \t\t {status}"
    texto_retorno = texto_retorno + F"\n\t{monta_rodape_secao()}"
    return texto_retorno


# Espera um jogador com uma lista de dados para jogar
def jogar_dados(jogo: Jogo, jogador: Jogador):
    print(f"\t{monta_titulo_secao('ACAO', max_=65)}")
    pegar_dados(jogo, jogador)
    print("\t ────Cores dos dados que possui:", end=" ")
    cores: list = []
    for dado in jogador.dados:
        cores.append(dado.cor)
    print(', '.join(cores))  # Somente para imprimir a lista de cores sem a virgula no final
    print(f'\t ──{jogador.nome} > [Jogou os dados]:')
    print(f'\t ────Resultado:', end=" ")
    # Para cada dado em posse do jogador, usamos um "random.choice" para obter a face virada para cima e imprimimos ela
    for dado in jogador.dados:
        dado.face_para_cima = random.choice(dado.faces)
        jogo.mesa.dados.append(dado)
        print(f"{dado.cor} : {dado.face_para_cima}", end=" / ")
    # Limpa os dados da mao do jogador, ja que ja jogou todos
    print("\n" + desenha_dados(jogador.dados))
    definir_score(jogo.mesa, jogador)
    print(f"\n\t{monta_rodape_secao(max_=65)}")
    jogador.dados = []


# Pega dados virado com face de passos se tiver, e completa com os dados do tubo, se nao tiver ao menos 3 dados
# recolhe os dados da mesa com a face diferente de tiro e coloca novamente no tubo e entao pega 3 dados do tubo
def pegar_dados(jogo: Jogo, jogador: Jogador):
    # Verifica se existem dados disponiveis na mesa para serem pegos (com a face passos)
    quantidade_passos: int = 0
    if len(jogo.mesa.dados) > 0:  # Se existir algum dado
        # Verificamos a quantidade de passos, somando a quantidade de elementos que atendem o criterio
        quantidade_passos = sum(x.face_para_cima == "P" for x in jogo.mesa.dados)
        print(
            f"\t -Há {quantidade_passos} dado(s) com a face de passos na mesa.")
        if quantidade_passos > 0:  # Se a quantidade de passos for maior que 0 removemos da mesa damos para o jogador
            indice: int = len(jogo.mesa.dados) - 1
            while indice >= 0:  # removendo os dados da mesa de tras para frente para evitar erros de index out of bound
                if jogo.mesa.dados[indice].face_para_cima == 'P':
                    jogador.dados.append(jogo.mesa.dados[indice])
                    jogo.mesa.dados.pop(indice)
                indice -= 1

    quantidade_pegar_do_tubo: int = 3 - quantidade_passos
    # Caso não houver dados suficientes no tubo para serem pegos, adiciona todos dados com cerebro na mesa para o tubo
    if len(jogo.tubo_de_dados) < quantidade_pegar_do_tubo:
        print("\n\t Não há dados suficientes, vamos adicionar os dados com a face de cerebro no tubo")
        for indice, dado in sorted(enumerate(jogo.mesa.dados), reverse=True):
            jogo.tubo_de_dados.append(dado) if dado.face_para_cima == "C" else None
            jogo.mesa.dados.pop(indice)
        print(f"\n\t Dados adicionados. Dados disponiveis no tubo {len(jogo.tubo_de_dados)}")

    # Se houver uma quantidade suficiente para pegar do tubo, pega
    if quantidade_pegar_do_tubo <= 0:
        print(f"\t Não precisa pegar do tubo, pegou {quantidade_passos} dado(s) da mesa e ira re-rolar os mesmos")
    else:
        print(f"\n\t ──{jogador.nome} > [Pegou {quantidade_pegar_do_tubo} dado(s) do tubo]")
        # Retorna 3 indices randomicos da lista de tubo de dados, os indices sao obtidos passando a funcao list e enumerate
        # o ultimo parametro representa quantos resultados eu desejo obter, usando sample para evitar resultados repetidos
        dado_indice: list = random.sample(list(enumerate(jogo.tubo_de_dados)), quantidade_pegar_do_tubo)
        # Mostra lista de dados obtidos e retira os mesmos do tubo
        # Fazendo o for de tras para frente pois uma vez que o elemento é removido da lista seus indices sao alterados
        for i in sorted(dado_indice, reverse=True):
            dado = jogo.tubo_de_dados[i[0]]  # Pega o dado de indice equivalente do tubo
            jogador.dados.append(dado)  # Adiciona ao jogador
            jogo.tubo_de_dados.pop(i[0])


# Verifica a mesa e atualiza os atributos do jogador (pontos e vida)
def definir_score(mesa: Mesa, jogador: Jogador):
    cerebros: int = 0
    tiros: int = 0
    for dado in mesa.dados:
        if dado.face_para_cima == "C" and not dado.ja_contado:
            cerebros += 1
            dado.ja_contado = True
        tiros += 1 if dado.face_para_cima == "T" else 0
    jogador.temp_pontos += cerebros
    jogador.vida = 3 - tiros
    if 3 - tiros == 0:
        print("\n\n\t☠OUCH!! 3 tiros, você morreu pra valer!!☠")
    print(f"\n{get_status_jogador(jogador)}")


# Espera uma lista de dados, com a quantidade, cores e faces, adiciona esses a lista de dados disponiveis no jogo
def definir_dados(lista_dados):
    dados_em_jogo: list = []
    for i in range(0, len(lista_dados)):
        contador: int = lista_dados[i]["quantidade"]
        while contador > 0:
            dado = Dado(lista_dados[i]["cor"], lista_dados[i]["faces"], None, False)
            contador -= 1
            dados_em_jogo.append(dado)
    return dados_em_jogo


# Funcao para montar um titulo formatado de uma secao, para evitar repeticao e poluicao de codigo
# Se desejar um tamanho max customizado, passar o valor de max_
# Exemplo: ┌──EXEMPLO ──────────────────────────────────┐
def monta_titulo_secao(text: str, max_=None):
    max_: int = 50 if max_ is None else max_
    return f"┌───{text.upper().ljust(max_, '─')}" + "┐"


# Funcao para montar um rodape formatado de uma secao, para evitar repeticao e poluicao de codigo
# Se desejar um tamanho max customizado, passar o valor de max_
# Exemplo: └──────────────────────────────────┘
def monta_rodape_secao(max_=None):
    max_: int = 50 if max_ is None else max_
    return f"└───" + "─" * max_ + "┘"


def inicio():
    print(monta_titulo_secao("Zombie Dice"))
    print("\tWesley Florencio Ferreira")
    print(monta_rodape_secao())
    print("")
    # Configuracao inicial dos dados, para facilitar futuras customizacoes
    dados_iniciais = [
        {
            "quantidade": 6,
            "cor": "verde",
            "faces": Constantes.FACES_DADO_VERDE
        },
        {
            "quantidade": 4,
            "cor": "amarelo",
            "faces": Constantes.FACES_DADO_AMARELO
        },
        {
            "quantidade": 3,
            "cor": "vermelho",
            "faces": Constantes.FACES_DADO_VERMELHO
        }
    ]
    # Define os dados, espera uma lista/dicionario com os atributos, quantidade, cor e faces
    config: ConfiguracaoJogo = ConfiguracaoJogo(definir_dados(dados_iniciais))
    # Definicao inicial dos jogadores (quantidade, nomes, etc)
    jogadores: list = definir_jogadores()
    # Inicia objeto do jogo, com estado Jogando, configuracoes, jogadores, tubo de dados vazio, uma nova mesa rodada 1
    # e turno 1
    mesa = Mesa([])
    jogo = Jogo(Constantes.ESTADO_JOGANDO, config, jogadores, [], mesa, 0, 0)
    inicia_jogo(jogo)


if __name__ == '__main__':
    inicio()