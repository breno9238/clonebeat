import json
import pygame
from pathlib import Path
from _widget import Widget

class Accuracy(Widget):
    '''
    Cria um objeto do contador de precisão.
    '''
    def __init__(self, skin_path: str, layer_group: pygame.sprite.Group):
        
        # Extrai e define os atributos do widget.
        super().__init__(skin_path, pygame.sprite.Group, 'accuracy')
la = pygame.sprite.LayeredUpdates()
a = Accuracy('padrão', la)
print(a, la)
