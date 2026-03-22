#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import pygame
from rules.note import Notes



#________MÓDULO DE EXECUÇÃO DO JOGO___________________________
class Gameplay:
    
    #__CONSTRUTOR E INICIALIZAÇÃO DO PYGAME_____________
    def __init__(self, skin, music, title, artist, creator, version, od, keys, map_id, preview, notes):
        
        pygame.init()                   # Inicializa os módulos do Pygame
        info = pygame.display.Info()    # Coleta informações do monitor
        
        self.music = music
        self.title = title
        self.artist = artist
        self.creator = creator
        self.version = version
        self.od = od
        self.key = keys
        self.id = map_id
        self.preview = preview
        
        self.skin = 'padrão'
        self.notes = notes
        self.notes_group = pygame.sprite.Group()
        
        
        
        #_____________________________________________________________
        #__CONFIGURAÇÕES DE TELA____________________________
        self.w = info.current_w - 100                             # Largura da janela (Monitor - 100px)
        self.h = info.current_h - 100                              # Altura da janela (Monitor - 100px)
        self.screen = pygame.display.set_mode((self.w, self.h))    # Cria a janela do jogo
        self.clock = pygame.time.Clock()                                  # Controlador de tempo/FPS
        self.run = True                                                 # Variável de controle do loop
        
        
        
        #_____________________________________________________________
        #__CARREGAMENTO DE SKIN_____________________________
        pad = pygame.image.load('skins/&&&/esteira.png'.replace('&&&', skin)).convert_alpha()    # Carrega a imagem com transparência
        
        
        
        #_____________________________________________________________
        #__LOOP PRINCIPAL DO JOGO___________________________
        while self.run:
            
            
            #__EVENTOS DE ENTRADA_______________________________
            for events in pygame.event.get():
                if events.type == pygame.QUIT:    # Se fechar a janela
                    self.run = False          # Para o loop do jogo
            
            
            
            #_____________________________________________________________
            #__LÓGICA DO JOGO__________________________________
            
            
            
            #_____________________________________________________________
            #__LIMPEZA DA TELA__________________________________
            self.screen.fill('#5E5B8B')    # Preenchimento de fundo sólido
            
            
            
            #_____________________________________________________________
            #__RENDERIZAÇÃO DE OBJETOS__________________________
            # esteira
            self.screen.blit(pad, (self.w/2 - (pad.get_height()/4), 0))
            
            # chaves
            self.screen
            
            # notas
            for note in self.notes:
                
                note = Notes('beatmaps/2484096 DETRO - volcanic (Short Ver.)7/Menphiss (1).png', 5, 1, 50)
                self.notes_group.add(note)
            self.notes_group.update()
            
            # notas longas
            
            
            
            #_____________________________________________________________
            #__ATUALIZAÇÃO DA TELA______________________________
            # Mostra o frame renderizado
            pygame.display.flip()
            
            
            
            #_____________________________________________________________
            #__CONTROLE DE FPS__________________________________
            # Trava o jogo em 60 FPS
            self.fps = self.clock.tick(60)
        
        
        # Encerra o Pygame ao sair do loop
        pygame.quit()
