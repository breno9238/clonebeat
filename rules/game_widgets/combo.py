import json
import pygame
from pathlib import Path
from game_widgets._widget import Widget

class Combo(Widget):
    
    def __init__(self, skin_path: str, layer_group: pygame.sprite.LayeredUpdates):
        '''
        Inicializa um objeto do fundo decorativo.
        '''
        
        # Leitura do apparence_4k.json pra extração das definições e configurações da skin
        with open(f'{skin_path}/apparence.json', 'r', encoding='utf-8') as apparence_4k:
            
            # Transformação texto json -> dicionário do python
            self.ui = json.load(apparence_4k)
        
        # Carregamento da imagem
        self.image = pygame.image.load(self.ui['texture']).convert_alpha()
        
        # Tamanho da imagem
        self.image = pygame.transform.scale(self.image, (self.ui['width'], self.ui['height']))
        
        # Posição da imagem na tela
        self.rect = self.image.get_rect(midtop=(self.ui['pos_x'], self.ui['pos_y']))
        
        # Transparência da imagem
        self.image.set_alpha(self.ui['opacity'])
        
        # Camada de sobreposção da imagem
        self._layer = self.ui['pos_z']
        
        # Grupo de sprites do jogo
        super().__init__(layer_group)