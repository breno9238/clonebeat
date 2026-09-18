
import arcade

from configuracoes import *

from entidades.fase import Fase

from telas.tela_do_jogo import TelaGameplay

from pathlib import Path


# ==========================================
# MENU FASES
# ==========================================

class MenuFases(arcade.View):

    # Construtor responsável por preparar todos os dados necessários para o menu de fases.
    def __init__(self, view_anterior):
        super().__init__()  # Inicializa a View do Arcade para que a tela possa funcionar corretamente.

        self.view_anterior = view_anterior  # Guarda a tela anterior para poder retornar a ela com ESC.
        self.fases = []  # Lista que armazenará todas as fases encontradas.
        self.indice = 0  # Guarda o índice da fase atualmente selecionada.
        self.backgrounds = {}  # Guarda texturas já carregadas para evitar carregá-las novamente.
        self.background_selecionado = None  # Armazena a textura do background da fase selecionada.

        self.fundo_largura = 700  # Define a largura inicial do espaço destinado ao background.
        self.fundo_altura = 315  # Define a altura inicial do espaço destinado ao background.

        self.titulo = arcade.Text(
            'SELECIONE UMA FASE',
            0, 0,
            arcade.color.WHITE,
            42,
            anchor_x='center',
            bold=True
        )  # Cria o texto principal do menu e deixa seu ponto de referência centralizado.

        self.nome_fase = arcade.Text(
            '',
            0, 0,
            (220, 220, 220),
            32,
            anchor_x='center',
            bold=True
        )  # Cria o texto que mostrará o nome da fase atualmente selecionada.

        self.textos_fases = []  # Lista que armazenará os textos com os números das fases.

        # Percorre todas as pastas existentes dentro da pasta principal das fases.
        for pasta_fase in sorted(
            CAMINHO_PASTA_FASES.iterdir(),
            key=lambda pasta: pasta.name
        ):

            # Ignora qualquer item que não seja uma pasta de fase.
            if not pasta_fase.is_dir():
                continue

            nome = pasta_fase.name  # Usa o nome da pasta como nome da fase.
            notas = pasta_fase / 'notas.ini'  # Monta o caminho do arquivo que contém as notas da música.
            música = pasta_fase / 'audio.mp3'  # Monta o caminho do arquivo de áudio da fase.
            background = None  # Começa sem background até encontrar uma imagem válida.

            # Procura uma imagem de background utilizando as extensões permitidas.
            for extensao in ('.jpg', '.jpeg', '.png'):
                caminho = pasta_fase / f'background{extensao}'  # Monta o caminho possível para o background.

                # Verifica se o arquivo de imagem realmente existe.
                if caminho.is_file():
                    background = caminho  # Guarda o caminho da imagem encontrada.
                    break  # Para a busca porque já encontramos um background válido.

            # Ignora a pasta caso ela não possua o arquivo de notas necessário.
            if not notas.is_file():
                continue

            # Ignora a pasta caso ela não possua o arquivo de música necessário.
            if not música.is_file():
                continue

            pasta_skin_global = Path('skins') / skin_atual  # Monta o caminho da skin global atualmente selecionada.

            fase = Fase(
                len(self.fases) + 1,
                nome,
                notas,
                pasta_skin_global,
                música,
                background
            )  # Cria o objeto da fase reunindo todas as informações necessárias para o jogo.

            self.fases.append(fase)  # Adiciona a fase criada à lista de fases disponíveis.

        # Cria um objeto de texto para cada fase encontrada.
        for i in range(len(self.fases)):
            self.textos_fases.append(
                arcade.Text(
                    str(i + 1),
                    0, 0,
                    arcade.color.WHITE,
                    28,
                    anchor_x='center',
                    anchor_y='center',
                    bold=True
                )
            )  # Cria o número visual que será exibido dentro do botão da fase.

        # Só tenta selecionar uma fase caso pelo menos uma fase tenha sido carregada.
        if self.fases:
            self.atualizar_fase_selecionada()


    # Executado quando esta View passa a ser a tela atualmente exibida.
    def on_show_view(self):
        arcade.set_background_color((20, 10, 40))  # Define a cor de fundo do menu.


    # Atualiza todos os elementos visuais relacionados à fase selecionada.
    def atualizar_fase_selecionada(self):

        # Não faz nada caso não existam fases disponíveis.
        if not self.fases:
            return

        fase = self.fases[self.indice]  # Obtém a fase correspondente ao índice atualmente selecionado.

        self.nome_fase.text = fase.nome  # Atualiza o texto exibido com o nome da nova fase.

        # Verifica se a fase possui uma imagem de background.
        if fase.background is not None:
            caminho = Path(fase.background)  # Converte o caminho para um objeto Path.

            # Reutiliza a textura caso ela já tenha sido carregada anteriormente.
            if caminho in self.backgrounds:
                self.background_selecionado = self.backgrounds[caminho]  # Recupera a textura armazenada no dicionário.

            # Caso ainda não tenha sido carregada, lê a imagem e armazena sua textura.
            else:
                self.background_selecionado = arcade.load_texture(caminho)  # Carrega a imagem como textura do Arcade.
                self.backgrounds[caminho] = self.background_selecionado  # Guarda a textura para reutilizá-la depois.

        # Caso a fase não possua imagem, remove qualquer background anterior.
        else:
            self.background_selecionado = None

        self.atualizar_tamanho_background()  # Recalcula o tamanho do background para manter sua proporção.


    # Calcula o tamanho do background sem distorcer sua proporção original.
    def atualizar_tamanho_background(self):

        # Usa o tamanho padrão quando não existe imagem de background.
        if self.background_selecionado is None:
            self.fundo_largura = 700  # Mantém a largura padrão do espaço do background.
            self.fundo_altura = 315  # Mantém a altura padrão do espaço do background.
            return

        largura_original = self.background_selecionado.width  # Obtém a largura original da imagem.
        altura_original = self.background_selecionado.height  # Obtém a altura original da imagem.

        largura_maxima = 700  # Define o limite máximo de largura permitido para o background.
        altura_maxima = 315  # Define o limite máximo de altura permitido para o background.

        proporcao = largura_original / altura_original  # Calcula a proporção entre largura e altura da imagem.

        largura = largura_maxima  # Começa usando a largura máxima disponível.
        altura = largura / proporcao  # Calcula a altura necessária para preservar a proporção original.

        # Verifica se a altura calculada ultrapassou o limite máximo.
        if altura > altura_maxima:
            altura = altura_maxima  # Limita a altura ao máximo permitido.
            largura = altura * proporcao  # Recalcula a largura para manter a proporção da imagem.

        self.fundo_largura = largura  # Guarda a largura final calculada.
        self.fundo_altura = altura  # Guarda a altura final calculada.


    # Responsável por desenhar todos os elementos visuais do menu.
    def on_draw(self):
        self.clear()  # Limpa o conteúdo desenhado anteriormente antes de redesenhar a tela.

        largura_real = self.window.width  # Obtém a largura atual da janela, inclusive quando está em fullscreen.
        altura_real = self.window.height  # Obtém a altura atual da janela.

        self.titulo.x = largura_real / 2  # Centraliza horizontalmente o título usando a largura atual da tela.
        self.titulo.y = altura_real * 0.88  # Posiciona o título próximo ao topo da tela.
        self.titulo.draw()  # Desenha o título na tela.

        # Só exibe o nome da fase quando existem fases disponíveis.
        if self.fases:
            fundo_y = altura_real * 0.50

            self.nome_fase.x = largura_real / 2  # Centraliza horizontalmente o nome da fase.
            self.nome_fase.y = altura_real * 0.80  # Posiciona o nome abaixo do título.
            self.nome_fase.draw()  # Desenha o nome da fase selecionada.

        fundo_x = largura_real / 2  # Define o centro horizontal do background.
        fundo_y = altura_real * 0.50  # Define a posição vertical do centro do background.

        esquerda = fundo_x - self.fundo_largura / 2  # Calcula o limite esquerdo do background.
        direita = fundo_x + self.fundo_largura / 2  # Calcula o limite direito do background.
        baixo = fundo_y - self.fundo_altura / 2  # Calcula o limite inferior do background.
        cima = fundo_y + self.fundo_altura / 2  # Calcula o limite superior do background.

        # Desenha a imagem quando a fase possui um background.
        if self.background_selecionado is not None:
            arcade.draw_texture_rect(
                self.background_selecionado,
                arcade.LBWH(
                    esquerda,
                    baixo,
                    self.fundo_largura,
                    self.fundo_altura
                )
            )  # Desenha a textura dentro da área calculada anteriormente.

        # Caso não exista imagem, desenha um retângulo simples como substituição.
        else:
            arcade.draw_lrbt_rectangle_filled(
                esquerda,
                direita,
                baixo,
                cima,
                (50, 50, 50)
            )  # Cria uma área cinza para representar o background ausente.

        arcade.draw_lrbt_rectangle_outline(
            esquerda,
            direita,
            baixo,
            cima,
            (130, 130, 130),
            4
        )  # Desenha uma borda ao redor da área do background.

        # Percorre todas as fases para posicionar seus respectivos botões.
        for i in range(len(self.fases)):
            coluna = i % 5  # Calcula em qual das cinco colunas a fase ficará.
            linha = i // 5  # Calcula em qual linha a fase ficará.

            x = (largura_real / 2) - 320 + (coluna * 160)  # Calcula a posição horizontal do botão.
            y = (altura_real * 0.18) - (linha * 110)  # Calcula a posição vertical do botão.

            selecionado = i == self.indice  # Verifica se esta é a fase atualmente selecionada.

            cor = (180, 180, 180) if selecionado else (60, 60, 60)  # Usa uma cor diferente para destacar a seleção.

            arcade.draw_lrbt_rectangle_filled(
                x - 65,
                x + 65,
                y - 45,
                y + 45,
                cor
            )  # Desenha o botão visual da fase.

            # Adiciona uma borda maior para destacar visualmente a fase selecionada.
            if selecionado:
                arcade.draw_lrbt_rectangle_outline(
                    x - 67,
                    x + 67,
                    y - 47,
                    y + 47,
                    (220, 220, 220),
                    4
                )  # Desenha a borda de destaque ao redor da fase selecionada.

            self.textos_fases[i].x = x  # Posiciona o número da fase horizontalmente no centro do botão.
            self.textos_fases[i].y = y  # Posiciona o número da fase verticalmente no centro do botão.
            self.textos_fases[i].draw()  # Desenha o número da fase na tela.


    # Processa as teclas pressionadas pelo jogador.
    def on_key_press(self, key, modifiers):

        # Ignora os comandos caso não existam fases disponíveis.
        if not self.fases:
            return

        indice_anterior = self.indice  # Guarda o índice anterior para descobrir se a seleção mudou.

        # ESC retorna para a tela anterior.
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.view_anterior)  # Mostra novamente a tela que abriu o menu de fases.
            return

        # LEFT seleciona a fase anterior.
        elif key == arcade.key.LEFT:
            self.indice = (self.indice - 1) % len(self.fases)  # Diminui o índice e usa módulo para permitir voltar do início ao fim.

        # RIGHT seleciona a próxima fase.
        elif key == arcade.key.RIGHT:
            self.indice = (self.indice + 1) % len(self.fases)  # Aumenta o índice e usa módulo para permitir ir do fim ao início.

        # ENTER inicia a fase atualmente selecionada.
        elif key == arcade.key.ENTER:
            self.window.show_view(
                TelaGameplay(self, self.fases[self.indice])
            )  # Cria e abre a tela de gameplay usando a fase selecionada.
            return

        # Só atualiza a fase caso o jogador realmente tenha mudado a seleção.
        if self.indice != indice_anterior:
            self.atualizar_fase_selecionada()  # Atualiza nome e background da nova fase.