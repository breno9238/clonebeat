import arcade  # Importa a biblioteca gráfica Arcade para herdar a estrutura de Sprites

from configuracoes import *  # Importa constantes globais (como as colunas e velocidade de queda)


# ==========================================
# NOTA
# ==========================================
# Classe que representa individualmente cada nota musical que desce pela pista do jogo
class Nota(arcade.Sprite):

    # Método construtor que inicializa o objeto de sprite da nota com tamanho e posição originais
    def __init__(
        self,
        coluna,
        y_inicial,
        textura,
        largura,
        altura
    ):
        
        super().__init__(textura)  # Inicializa a classe pai Sprite injetando a textura visual da nota
        
        self.width = largura  # Define a largura final do sprite com base na configuração da skin
        self.height = altura  # Define a altura final do sprite com base na configuração da skin
        self.coluna = coluna  # Armazena o índice da trilha vertical (0 a 3) em que a nota se encontra
        self.center_x = COLUNAS_X[coluna]  # Define a posição X fixa buscando a coordenada horizontal no vetor global
        self.center_y = y_inicial  # Define a posição Y inicial no topo da tela para iniciar a descida
    
    # Método interno de atualização da nota com base na fração de tempo do jogo
    def atualizar(self, delta_time):
        
        self.center_y -= (VELOCIDADE_QUEDA * delta_time)  # Subtrai a altura do sprite dinamicamente para fazê-lo descer
