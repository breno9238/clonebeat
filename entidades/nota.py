import arcade

from regras.configuracoes import *


# ==========================================
# NOTA
# ==========================================
class Nota(arcade.Sprite):

    def __init__(
        self,
        coluna,
        y_inicial,
        textura,
        largura,
        altura
    ):
        
        super().__init__(textura)
        
        self.width = largura
        self.height = altura
        self.coluna = coluna
        self.center_x = COLUNAS_X[coluna]
        self.center_y = y_inicial
    
    def atualizar(self, delta_time):
        
        self.center_y -= (VELOCIDADE_QUEDA * delta_time)