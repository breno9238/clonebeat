#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física

#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Note(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(self, data: list[pygame.surface.Surface, tuple[int, int], int], timestamp: int, pos_x: int, group: pygame.sprite.Group):
        '''
        Inicializa um objeto de nota musical que desce pela tela.
        
        Args:
        png_path: Caminho da imagem da nota (ex: 'assets/note.png')
        speed_val: Velocidade de queda em pixels por frame
        pos_x/pos_y: Coordenadas iniciais de spawn
        '''
        
        # Inicialização da Classe Pai (Sprite)
        super().__init__(group)
        
        self.image = data[0]
        self.pos = data[1]
        self._layer = data[2]
        
        # Configurações de Movimento
        self.timestamp = timestamp
        self.pos_x = pos_x
        
        # Define o retângulo de colisão (Hitbox) baseado no tamanho da imagem
        self.rect: pygame.Rect = self.image.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.rect.x = pos_x
        self.rect.y = 0
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self, current_time, speed, hit_line=None):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        self.rect.y += speed