import arcade

class Gameplay(arcade.Window):
    
    def __init__(self, difficult, width = 1280, height = 720, title = "Arcade Window", fullscreen = False, resizable = False):
        
        super().__init__(width, height, title, fullscreen, resizable)
        
        arcade.set_background_color(arcade.color.AMAZON)
    
    def setup(self):
        """Configura o jogo aqui (carregar mapas, sons, etc.)"""
        pass
    
    def on_draw(self):
        """Renderiza tudo na tela"""
        self.clear()
    
    def on_update(self, delta_time):
        """Toda a lógica de movimento e física fica aqui"""
        pass