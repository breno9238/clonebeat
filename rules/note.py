#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import pygame                       # Motor de jogo para manipulação de sprites e física



#________CLASSE DE NOTAS MUSICAIS (SPRITES)_________________________________________________________
class Notes(pygame.sprite.Sprite):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DA NOTA___________________________________________________________________________
    def __init__(self, png_path: str, speed_val: float, pos_x: int, pos_y: int):
        '''
        Inicializa um objeto de nota musical que desce pela tela.
        png_path: Caminho da imagem da nota (ex: 'assets/note.png')
        speed_val: Velocidade de queda em pixels por frame
        pos_x/pos_y: Coordenadas iniciais de spawn
        '''
        
        # Inicialização da Classe Pai (Sprite)
        super().__init__()
        
        # Configurações de Movimento
        self.speed: float = speed_val      # Define a cadência da queda
        
        #___________________________________________________________________________________________
        #__PROCESSAMENTO VISUAL E COLISÃO___________________________________________________________
        
        # Carrega a imagem e otimiza para transparência (Alpha)
        self.image: pygame.Surface = pygame.image.load(png_path).convert_alpha()
        
        # Define o retângulo de colisão (Hitbox) baseado no tamanho da imagem
        self.rect: pygame.Rect = self.image.get_rect()
        
        # Cria uma máscara de pixels para colisões perfeitas (ignora áreas transparentes)
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)
        
        # Define o ponto de spawn inicial (Canto superior esquerdo)
        self.rect.topleft = (pos_x, pos_y)
    
    
    
    #_______________________________________________________________________________________________
    #__ATUALIZAÇÃO DE FRAME_________________________________________________________________________
    def update(self):
        '''
        Executa a lógica de movimento a cada ciclo do loop principal.
        Faz a nota descer verticalmente somando a velocidade ao eixo Y.
        '''
        
        # Movimento Vertical Descendente
        self.rect.y += self.speed          # Incrementa a posição Y com base na velocidade