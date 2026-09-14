import arcade  # Importa a biblioteca gráfica Arcade para o jogo de ritmo

from configuracoes import *  # Importa todas as variáveis de tamanho de tela e áudio do jogo

from telas.menu_fases import MenuFases  # Importa a tela de seleção de fases do jogo
from telas.menu_configuracoes import TelaConfiguracoes  # Importa a tela de ajustes e configurações


# ==========================================
# MENU PRINCIPAL
# ==========================================
# Classe que gerencia e renderiza o menu inicial do jogo
class MenuPrincipal(arcade.View):
    
    # Método construtor que inicializa a estrutura do menu principal
    def __init__(self):
        super().__init__()  # Chama o inicializador da classe base arcade.View
        
        self.opções = [
            'INICIAR',
            'CONFIGURAÇÕES',
            'SAIR'
        ]  # Define a lista de textos que compõem as opções selecionáveis do menu
        
        self.indice = 0  # Controla qual opção do menu está selecionada no momento (começa na primeira)
    
    # Método automático do Arcade executado a cada quadro para desenhar os elementos na tela
    def on_draw(self):
        
        self.clear()  # Limpa o quadro anterior para evitar duplicidade visual na tela
        
        arcade.set_background_color(
            (20, 10, 40)
        )  # Define a cor de fundo da tela usando valores customizados RGB (Roxo Escuro)
        
        # Pega as dimensões reais da tela cheia
        largura_real = self.window.width  # Captura a largura atual da janela gráfica do jogo
        altura_real = self.window.height  # Captura a altura atual da janela gráfica do jogo
        
        # Aumentei a fonte do título de 40 para 75 e subi para 82% da altura
        arcade.draw_text(
            TITULO_JOGO,
            largura_real / 2,
            altura_real * 0.82,
            arcade.color.CYAN,
            75,
            anchor_x='center',
            bold=True
        )  # Desenha o título estilizado centralizado na parte superior da tela
        
        # Laço de repetição que percorre e renderiza todas as opções da lista na tela
        for i, texto in enumerate(self.opções):
        
            # Condicional que define uma cor diferente caso a opção seja a que está selecionada
            cor = (
                arcade.color.WHITE
                if i == self.indice
                else arcade.color.GRAY
            )  # Aplica cor branca para o item ativo e cinza para os itens inativos
            
            # Aumentei a fonte dos botões de 24 para 42 
            # Aumentei o espaçamento entre eles de 60 para 95 pixels para ver melhor de longe
            arcade.draw_text(
                texto,
                largura_real / 2,
                (altura_real * 0.48) - (i * 95),
                cor,
                42,
                anchor_x='center',
                bold=True
            )  # Desenha cada opção textual com distanciamento vertical proporcional
    
    # Método automático do Arcade invocado sempre que o jogador pressiona qualquer tecla
    def on_key_press(self, key, modifiers):
        
        # Condicional que verifica se o jogador pressionou a tecla direcional para CIMA
        if key == arcade.key.UP:
            self.indice = (self.indice - 1) % len(self.opções)  # Desloca a seleção para cima de forma circular
        
        # Condicional que verifica se o jogador pressionou a tecla direcional para BAIXO
        elif key == arcade.key.DOWN:
            self.indice = (self.indice + 1) % len(self.opções)  # Desloca a seleção para baixo de forma circular
        
        # Condicional que verifica se o jogador pressionou a tecla ENTER para confirmar
        elif key == arcade.key.ENTER:
            escolha = self.opções[self.indice]  # Captura o texto correspondente à opção selecionada
            
            # Condicional que checa se a escolha confirmada foi a opção de iniciar o jogo
            if escolha == 'INICIAR': 
                self.window.show_view(MenuFases(self))  # Muda a visualização da tela para o menu de fases
            
            # Condicional que checa se a escolha confirmada foi a opção de abrir configurações
            elif escolha == 'CONFIGURAÇÕES':
                self.window.show_view(TelaConfiguracoes(self))  # Muda a visualização da tela para o painel de configurações
            
            # Condicional que checa se a escolha confirmada foi a opção de sair do jogo
            elif escolha == 'SAIR':
                arcade.close_window()  # Encerra o jogo e fecha a janela ativa imediatamente
