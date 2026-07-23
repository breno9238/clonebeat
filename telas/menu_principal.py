import arcade

from regras.configuracoes import *

from telas.menu_fases import MenuFases
from telas.configuracoes import TelaConfiguracoes


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
        
        arcade.draw_text(
            TITULO_JOGO,
            LARGURA_TELA / 2,
            470,
            arcade.color.CYAN,
            40,
            anchor_x='center',
            bold=True
        )
        
        for i, texto in enumerate(self.opções):
        
            cor = (
                arcade.color.WHITE
                if i == self.indice
                else arcade.color.GRAY
            )
            
            arcade.draw_text(
                texto,
                LARGURA_TELA / 2,
                300 - (i * 60),
                cor,
                24,
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
                self.window.show_view(MenuFases())
            
            elif escolha == 'CONFIGURAÇÕES':
                self.window.show_view(TelaConfiguracoes())
            
            elif escolha == 'SAIR':
                arcade.close_window()