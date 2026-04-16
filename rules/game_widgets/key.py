#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física



#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Key(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(self, png_path: str, pos_x: int, pos_y: int, group: pygame.sprite.Group):
        '''
        '''
        
        # Inicialização da Classe Pai (Sprite)
        super().__init__(group)
        
        # Configurações de Movimento
        self.pos_x = pos_x
        self.pos_y = pos_y
        #___________________________________________________________________________________________
        #__PROCESSAMENTO VISUAL E COLISÃO___________________________________________________________
        
        self.full_image = pygame.image.load(png_path).convert_alpha()
        
        # Carrega a imagem e otimiza para transparência (Alpha)
        self.image: pygame.Surface = pygame.transform.scale(self.full_image, (80, 80))
        
        # Define o retângulo de colisão (Hitbox) baseado no tamanho da imagem
        self.rect: pygame.Rect = self.image.get_rect()
        
        # Cria uma máscara de pixels para colisões perfeitas (ignora áreas transparentes)
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)
        
        self.rect.x = pos_x
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self, current_time):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        
        self.rect.y = 600 - (self.timestamp - current_time) * self.speed          # Incrementa a posição Y com base