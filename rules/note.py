#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física



#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Note(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(self, png_img: pygame.Surface, speed_val: float, timestamp: int, pos_x: int, end: int, group: pygame.sprite.Group):
        '''
        Inicializa um objeto de nota musical que desce pela tela.
        
        Args:
        png_path: Caminho da imagem da nota (ex: 'assets/note.png')
        speed_val: Velocidade de queda em pixels por frame
        pos_x/pos_y: Coordenadas iniciais de spawn
        '''
        
        # Inicialização da Classe Pai (Sprite)
        super().__init__(group)
        
        # Configurações de Movimento
        self.speed: float = speed_val      # Define a cadência da queda
        self.timestamp = timestamp
        self.pos_x = pos_x
        #___________________________________________________________________________________________
        #__PROCESSAMENTO VISUAL E COLISÃO___________________________________________________________
        
        self.image = png_img
        
        # Define o retângulo de colisão (Hitbox) baseado no tamanho da imagem
        self.rect: pygame.Rect = png_img.get_rect()
        
        self.rect.x = pos_x
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self, base_y: int, current_time, hit_line: pygame.sprite.Sprite):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        self.rect.y = 600 - (self.timestamp - current_time) * self.speed          # Incrementa a posição Y com base na velocidade
        if self.rect.colliderect(hit_line):
            self.kill()