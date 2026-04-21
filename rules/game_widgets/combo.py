import yaml
import pygame
from pathlib import Path


class Combo(pygame.sprite.Sprite):
    
    def __init__(
            self, 
            settings: dict, 
            sprite_group: pygame.sprite.Group
):
        '''
        Inicializa um objeto do fundo decorativo.
        '''
        
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
    
    def update(self, *args, **kwargs):
            pass