import arcade

from regras.configuracoes import *

from telas.menu_fases import MenuFases
from telas.menu_configuracoes import TelaConfiguracoes


# ==========================================
# MENU PRINCIPAL
# ==========================================
class MenuPrincipal(arcade.View):
    
    def __init__(self):
        super().__init__()
        
        self.opções = [
            'INICIAR',
            'CONFIGURAÇÕES',
            'SAIR'
        ]
        
        self.indice = 0
    
    def on_draw(self):
        
        self.clear()
        
        arcade.set_background_color(
            (20, 10, 40)
        )
        
        # Pega as dimensões reais da tela cheia
        largura_real = self.window.width
        altura_real = self.window.height
        
        # Aumentei a fonte do título de 40 para 75 e subi para 82% da altura
        arcade.draw_text(
            TITULO_JOGO,
            largura_real / 2,
            altura_real * 0.82,
            arcade.color.CYAN,
            75,
            anchor_x='center',
            bold=True
        )
        
        for i, texto in enumerate(self.opções):
        
            cor = (
                arcade.color.WHITE
                if i == self.indice
                else arcade.color.GRAY
            )
            
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
            )
    
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.UP:
            self.indice = (self.indice - 1) % len(self.opções)
        
        elif key == arcade.key.DOWN:
            self.indice = (self.indice + 1) % len(self.opções)
        
        elif key == arcade.key.ENTER:
            escolha = self.opções[self.indice]
            
            if escolha == 'INICIAR': 
                self.window.show_view(MenuFases(self))
            
            elif escolha == 'CONFIGURAÇÕES':
                self.window.show_view(TelaConfiguracoes(self))
            
            elif escolha == 'SAIR':
                arcade.close_window()
