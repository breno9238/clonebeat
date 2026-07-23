import configparser

from regras.configuracoes import *

from pathlib import Path

import arcade

class GerenciadorMúsica:
    
    def __init__(self, arquivo_música):
        
        self.música_crua = Path(arquivo_música)
        self.música = arcade.load_sound(self.música_crua)
        self.player = arcade.play_sound(self.música, 1, 0, False, 1)