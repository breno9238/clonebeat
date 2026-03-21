import pygame

class Note(pygame.sprite.Sprite):
    
    def __init__(self, png, speed, x, y):
        
        self.speed = speed
        
        super().__init__()
        
        # carrega a imagem e remove o fundo (se necessário)
        self.image = pygame.image.load(png).convert_alpha()
        
        # define o retângulo de colisão baseado no tamanho da imagem
        self.rect = self.image.get_rect()
        
        # desconsidera a colisão de areas transparentes no retangulo, apenas pixels coloridos
        self.mask = pygame.mask.from_surface(self.image)
        
        # posiciona a nota na tela
        self.rect.topleft = (x, y)
    
    def gravity(self):
        
        self.rect.y += self.speed