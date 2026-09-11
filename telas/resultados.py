import arcade  # Importa a biblioteca gráfica Arcade para o jogo de ritmo

from configuracoes import *  # Importa todas as variáveis de tamanho de tela e áudio do jogo


# ==========================================
# RESULTADOS
# ==========================================
# Classe responsável por gerenciar e renderizar a tela de pontuação final do jogador
class TelaResultados(arcade.View):

    # Método construtor que inicializa a tela de resultados recebendo as estatísticas da partida
    def __init__(
        self,
        pontuacao,
        combo,
        precisao=100.00,
        perfeito=0,
        bom=0,
        falha=0
    ):

        super().__init__()  # Chama o inicializador da classe base arcade.View

        self.pontuacao = pontuacao  # Armazena a pontuação total obtida pelo jogador
        self.combo = combo  # Armazena o maior combo de notas seguidas alcançado
        self.precisao = precisao  # Armazena a porcentagem de precisão dos acertos
        self.perfeito = perfection = perfeito  # Armazena a quantidade de notas com acerto perfeito
        self.bom = bom  # Armazena a quantidade de notas com acerto bom
        self.falha = falha  # Armazena a quantidade de notas perdidas ou erradas

    # Método automático do Arcade executado a cada quadro para desenhar os elementos na tela
    def on_draw(self):

        self.clear()  # Limpa a tela antes de desenhar o novo quadro para evitar rastros

        arcade.set_background_color(
            (20, 10, 40)
        )  # Define a cor de fundo da tela usando valores customizados RGB (Roxo Escuro)

        largura_real = self.window.width  # Captura a largura atual da janela gráfica do jogo
        altura_real = self.window.height  # Captura a altura atual da janela gráfica do jogo
        centro_x = largura_real / 2  # Calcula a coordenada X correspondente ao centro exato da tela
        alinhamento_esquerda = centro_x - 250  # Define uma margem de recuo para alinhar os textos à esquerda do centro

        arcade.draw_text(
            'RESULTADO',
            centro_x,
            altura_real * 0.85,
            arcade.color.CYAN,
            65,
            anchor_x='center',
            bold=True
        )  # Renderiza o título principal centralizado no topo da tela

        arcade.draw_text(
            f'PONTUAÇÃO: {self.pontuacao}',
            alinhamento_esquerda,
            altura_real * 0.70,
            arcade.color.WHITE,
            38,
            anchor_x='left',
            bold=True
        )  # Exibe o total de pontos acumulados com a cor branca

        arcade.draw_text(
            f'PRECISÃO: {self.precisao:.2f}%',
            alinhamento_esquerda,
            altura_real * 0.62,
            arcade.color.GOLD,
            38,
            anchor_x='left',
            bold=True
        )  # Exibe a porcentagem de acertos formatada com duas casas decimais em dourado

        arcade.draw_text(
            f'PERFEITO: {self.perfeito}',
            alinhamento_esquerda,
            altura_real * 0.52,
            arcade.color.LIGHT_GREEN,
            32,
            anchor_x='left',
            bold=True
        )  # Exibe a contagem de acertos excelentes na cor verde clara

        arcade.draw_text(
            f'BOM: {self.bom}',
            alinhamento_esquerda,
            altura_real * 0.44,
            arcade.color.LIGHT_BLUE,
            32,
            anchor_x='left',
            bold=True
        )  # Exibe a contagem de acertos medianos na cor azul clara

        arcade.draw_text(
            f'FALHA: {self.falha}',
            alinhamento_esquerda,
            altura_real * 0.36,
            arcade.color.RED,
            32,
            anchor_x='left',
            bold=True
        )  # Exibe a contagem de erros na cor vermelha

        arcade.draw_text(
            f'MAX COMBO: {self.combo}',
            alinhamento_esquerda,
            altura_real * 0.28,
            arcade.color.WHITE,
            32,
            anchor_x='left',
            bold=True
        )  # Exibe o maior multiplicador/combo mantido na cor branca

        arcade.draw_text(
            'APERTE ESC PARA VOLTAR AO MENU',
            centro_x,
            altura_real * 0.12,
            arcade.color.GRAY,
            24,
            anchor_x='center',
            bold=True
        )  # Desenha a instrução de navegação cinza centralizada na parte inferior

    # Método automático do Arcade invocado sempre que o jogador pressiona qualquer tecla
    def on_key_press(self, key, modifiers):
        
        # Condicional que verifica se a tecla pressionada foi a tecla ESCAPE (ESC)
        if key == arcade.key.ESCAPE:
            from telas.menu_principal import MenuPrincipal  # Importação local interna para evitar erros de importação circular
            self.window.show_view(MenuPrincipal())  # Altera a visualização atual da janela de volta para o Menu Principal
