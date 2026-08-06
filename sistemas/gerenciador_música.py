import configparser

from regras.configuracoes import *

from pathlib import Path

import arcade

class GerenciadorMúsica:
    
    def __init__(self, arquivo_música):
        
        self.arquivo_música = Path(arquivo_música)
    
    def play(self):
        
        self.música = arcade.load_sound(self.arquivo_música)
        self.player = arcade.play_sound(self.música, volume=VOLUME)
    
    def stop(self):
        arcade.stop_sound(self.player)