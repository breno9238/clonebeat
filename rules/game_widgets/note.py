#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física
import yaml

#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Note(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(
            self, 
            settings: dict, 
            sprite_group: pygame.sprite.Group
):
        '''
        Inicializa um objeto da nota musical que desce pela tela.
        '''
        
        # Carregamento da imagem
        self.image = pygame.image.load(self.ui['texture']).convert_alpha()
        
        # Tamanho da imagem
        self.image = pygame.transform.scale(self.image, (self.ui['width'], self.ui['height']))
        
        # Posição da imagem na tela
        self.rect = self.image.get_rect(midtop=(self.ui['pos_x'], self.ui['pos_y']))
        
        # Camada de sobreposção da imagem
        self._layer = self.ui['pos_z']
        
        # Grupo de sprites do jogo
        super().__init__(layer_group)
        
        # Transparência da imagem
        self.image.set_alpha(self.ui['opacity'])
        
        if timestamp:
            # Tempo de spawn da nota
            self.timestamp = timestamp
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self, delta_time: int, speed: int):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        self.rect.y += speed * delta_time
        if self.rect.top > 900:
            self.kill()