import json
import pygame
from pathlib import Path

class Widget(pygame.sprite.Sprite):
    
    def __init__(self, skin_path: str, sprite_group: pygame.sprite.Group, raw_widget):
        '''
        Inicializa um objeto do fundo decorativo.
        '''
        
        # Leitura do apparence_4k.json pra extração das definições e configurações da skin
        with open(f'assets/skins/{skin_path}/apparence.json', 'r', encoding='utf-8') as apparence_4k:
            
            # Transformação texto json -> dicionário do python
            ui = json.load(apparence_4k)
            self.widget = ui[raw_widget]
        
        # Carregamento da imagem
        self.image = pygame.image.load(self.background['texture']).convert_alpha()
        
        # Tamanho da imagem
        self.image = pygame.transform.scale(self.image, (self.background['width'], self.background['height']))
        
        # Posição da imagem na tela
        self.rect = self.image.get_rect(midtop=(self.background['pos_x'], self.background['pos_y']))
        
        # Camada de sobreposção da imagem
        self._layer = self.background['pos_z']
        
        # Grupo de sprites do jogo
        super().__init__(sprite_group)
        
        # Transparência da imagem
        self.image.set_alpha(self.background['opacity'])