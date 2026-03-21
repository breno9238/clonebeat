#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import pygame
from rules.note import Note



#________MÓDULO DE EXECUÇÃO DO JOGO___________________________
class Gameplay:
    
    #__CONSTRUTOR E INICIALIZAÇÃO DO PYGAME_____________
    def __init__(self, skin, beatmap):
        
        pygame.init()                   # Inicializa os módulos do Pygame
        info = pygame.display.Info()    # Coleta informações do monitor
        
        
        
        #_____________________________________________________________
        #__CONFIGURAÇÕES DE TELA____________________________
        self.largura = info.current_w - 100                             # Largura da janela (Monitor - 100px)
        self.altura = info.current_h - 100                              # Altura da janela (Monitor - 100px)
        self.tela = pygame.display.set_mode((self.largura, self.altura))    # Cria a janela do jogo
        self.relogio = pygame.time.Clock()                                  # Controlador de tempo/FPS
        self.run = True                                                 # Variável de controle do loop
        
        
        
        #_____________________________________________________________
        #__CARREGAMENTO DE SKIN_____________________________
        esteira = pygame.image.load('assets/skins/&&&/esteira.png'.replace('&&&', skin)).convert_alpha()    # Carrega a imagem com transparência
        
        
        
        #_____________________________________________________________
        #__LOOP PRINCIPAL DO JOGO___________________________
        while self.run:
            
            
            #__EVENTOS DE ENTRADA_______________________________
            for events in pygame.event.get():
                if events.type == pygame.QUIT:    # Se fechar a janela
                    self.run = False          # Para o loop do jogo
                    self.menu.destroy()       # Fecha a instância do app
            
            
            
            #_____________________________________________________________
            #__LÓGICA DO JOGO__________________________________
            
            
            
            #_____________________________________________________________
            #__LIMPEZA DA TELA__________________________________
            self.tela.fill('#5E5B8B')    # Preenchimento de fundo sólido
            
            
            
            #_____________________________________________________________
            #__RENDERIZAÇÃO DE OBJETOS__________________________
            # esteira
            self.tela.blit(esteira, (self.largura/2 - (esteira.get_height()/4), 0))
            
            # chaves
            
            
            # notas
            
            for note in beatmap:
                note = Note()
            
            # notas longas
            
            
            
            #_____________________________________________________________
            #__ATUALIZAÇÃO DA TELA______________________________
            # Mostra o frame renderizado
            pygame.display.flip()
            
            
            
            #_____________________________________________________________
            #__CONTROLE DE FPS__________________________________
            # Trava o jogo em 60 FPS
            self.fps = self.relogio.tick(60)
        
        
        # Encerra o Pygame ao sair do loop
        pygame.quit()
