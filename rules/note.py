#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física

#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Note(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(
            self,
            data: list[pygame.surface.Surface, tuple[int, int], int], 
            timestamp: int, 
            group: pygame.sprite.LayeredUpdates
            ):
        '''
        Inicializa um objeto de nota musical que desce pela tela.
        '''
        
        # Descompactação das informações e armazenamento
        self.image  = data[0]
        self.pos    = data[1]
        self._layer = data[2]
        super().__init__(group)
        
        # Tempo de spawn da nota
        self.timestamp = timestamp
        
        # Define o retângulo de colisão (Hitbox) baseado no tamanho da imagem
        self.rect = self.image.get_rect(midtop=self.pos)
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self, current_time, speed, hit_line=None):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        self.rect.y += speed
        if self.rect.top > 900:
            self.kill()