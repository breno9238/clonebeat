import json
import pygame
from pathlib import Path
from game_widgets._widget import Widget

class Hit(Widget):
    
    def __init__(self, skin_path: str, layer_group: pygame.sprite.LayeredUpdates):
        '''
        Inicializa um objeto do fundo decorativo.
        '''
        super().__init__()
        