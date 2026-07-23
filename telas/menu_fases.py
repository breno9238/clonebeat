import arcade

from regras.configuracoes import *

from entidades.fase import Fase

from telas.gameplay import TelaGameplay

from pathlib import Path

from sistemas.gerenciador_skin import GerenciadorSkin

from sistemas.gerenciador_notas import GerenciadorNotas

from sistemas.gerenciador_música import GerenciadorMúsica


# ==========================================
# MENU FASES
# ==========================================
class MenuFases(arcade.View):

    def __init__(self):
        super().__init__()
        
        self.fases = []
        self.indice = 0
        
        for fase in CAMINHO_PASTA_FASES.iterdir():
            
            nome   = fase.name
            notas  = GerenciadorNotas(next(fase.glob('notas.ini'), None))
            skin   = GerenciadorSkin(next(fase.glob('skin/'), None))
            música = GerenciadorMúsica(next(fase.glob('música.mp3'), None))
            
            if fase.is_dir:
                fase = Fase(
                    self.indice+1,
                    nome,
                    notas.data,
                    skin.data,
                    música.data,
                    True
                    )
                
                self.fases.append(fase)
    
    def on_draw(self):
        
        self.clear()
        arcade.set_background_color((25, 10, 45))
        
        arcade.draw_text(
            'SELECIONE UMA FASE',
            LARGURA_TELA / 2,
            520,
            arcade.color.WHITE,
            26,
            anchor_x='center',
            bold=True
        )
        
        for i, fase in enumerate(self.fases):
            
            coluna = i % 5
            linha = i // 5
            
            x = 170 + (coluna * 110)
            y = 370 - (linha * 120)
            
            selecionado = (i == self.indice)
            
            cor = (arcade.color.CYAN if selecionado else arcade.color.DARK_BLUE)
            
            arcade.draw_lrbt_rectangle_filled(
                x - 45,
                x + 45,
                y - 45,
                y + 45,
                cor
            )
            
            arcade.draw_text(
                fase.nome,
                x,
                y,
                arcade.color.WHITE,
                20,
                anchor_x='center',
                anchor_y='center',
                bold=True
            )
    
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT and self.indice > 0:
            self.indice -= 1
        
        elif key == arcade.key.RIGHT and self.indice < 9:
            self.indice += 1
        
        elif key == arcade.key.UP and self.indice >= 5:
            self.indice -= 5
        
        elif key == arcade.key.DOWN and self.indice <= 4:
            self.indice += 5
        
        elif key == arcade.key.ENTER:
            
            fase = self.fases[self.indice]
            self.window.show_view(TelaGameplay(fase))