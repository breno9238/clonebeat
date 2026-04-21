import yaml
import pygame
from pathlib import Path

class Accuracy(pygame.sprite.Sprite):
    '''
    Cria um objeto do contador de precisão.
    '''
    
    def __init__(
            self, 
            settings: dict, 
            sprite_group: pygame.sprite.Group
        ):
        
        # Carregamento da imagem
        self.image = pygame.image.load(self.accuracy['texture']).convert_alpha()
        
        # Tamanho da imagem
        self.image = pygame.transform.scale(self.image, (self.accuracy['width'], self.accuracy['height']))
        
        # Posição da imagem na tela
        self.rect = self.image.get_rect(midtop=(self.accuracy['pos_x'], self.accuracy['pos_y']))
        
        # Camada de sobreposção da imagem
        self._layer = self.accuracy['pos_z']
        
        # Grupo de sprites do jogo
        super().__init__(sprite_group)
        
        # Transparência da imagem
        self.image.set_alpha(self.accuracy['opacity'])
    
    def update(self, *args, **kwargs):
        pass