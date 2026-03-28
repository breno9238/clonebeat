#________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________-
import pygame                       # Motor gráfico para o jogo
from rules.note import Note        # Classe das notas musicais
from pathlib import Path



#________MÓDULO DE EXECUÇÃO DO JOGO_________________________________________________________________
class Gameplay:
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E INICIALIZAÇÃO DO PYGAME_________________________________________________________
    def __init__(
        self, 
        skin: str,
        audio_file_name: Path,
        map_title: str,
        artist: str,
        creator: str,
        version: str,
        overall_difficulty: str,
        beatmap_id: str,
        circle_size: str,
        preview_time: str,
        hit_objects: dict[int, int]):
        
        # Inicialização do Pygame e Coleta de Dados do Monitor
        pygame.init()                       # Inicia os módulos internos
        pygame.mixer.init()
        info = pygame.display.Info()        # Pega as specs do monitor do usuário
        
        
        # Configurações de Skin e Grupos de Sprites
        self.skin = 'padrão'
        self.notes = 4
        self.notes_group = pygame.sprite.Group() # Grupo que gerencia todas as notas ativas
        
        # Configuração da Música
        self.audio = audio_file_name
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play()
        
        #___________________________________________________________________________________________
        #__CONFIGURAÇÕES DE TELA____________________________________________________________________
        self.w = info.current_w - 100                             # Largura (Monitor - 100px)
        self.h = info.current_h - 100                             # Altura (Monitor - 100px)
        self.screen = pygame.display.set_mode((self.w, self.h))    # Define a janela
        self.clock = pygame.time.Clock()                          # Controlador de FPS
        self.run = True                                           # Controle do Loop
        
        
        
        #___________________________________________________________________________________________
        #__CARREGAMENTO DE SKIN_____________________________________________________________________
        # Caminho dinâmico para a textura da esteira
        pad = pygame.image.load('skins/&&&/esteira.png'.replace('&&&', skin)).convert_alpha()
        
        for timestamp, pos_x in hit_objects.items():
            
            match pos_x:
                case 64:  note: Note = Note('skins/padrão/blue_note.jpeg', 5, timestamp, pos_x, 0)
                case 192: note: Note = Note('skins/padrão/red_note.jpeg', 5, timestamp, pos_x, 0)
                case 320: note: Note = Note('skins/padrão/red_note.jpeg', 5, timestamp, pos_x, 0)
                case 448: note: Note = Note('skins/padrão/blue_note.jpeg', 5, timestamp, pos_x, 0)
            
            self.notes_group.add(note)
        
        #___________________________________________________________________________________________
        #__LOOP PRINCIPAL DO JOGO___________________________________________________________________
        while self.run:
            
            
            #_______________________________________________________________________________________
            #__EVENTOS DE ENTRADA___________________________________________________________________
            for events in pygame.event.get():
                if events.type == pygame.QUIT:    # Clique no 'X' da janela
                    self.run = False              # Encerra o loop
            
            
            
            #_______________________________________________________________________________________
            #__LÓGICA DO JOGO_______________________________________________________________________
            # (Espaço reservado para cálculos de tempo e pontuação)
            
            
            
            #_______________________________________________________________________________________
            #__LIMPEZA DA TELA______________________________________________________________________
            self.screen.fill('#5E5B8B')           # Fundo sólido roxo acinzentado
            
            
            
            #_______________________________________________________________________________________
            #__RENDERIZAÇÃO DE OBJETOS______________________________________________________________
            
            # 1. Desenho da Esteira
            self.screen.blit(pad, (self.w/2 - (pad.get_height()/4), 0))
            
            # 3. Processamento e Desenho das Notas
            self.time = pygame.mixer.music.get_pos()
            
            for note in self.notes_group:
                note: Note
                if self.time > note.timestamp + 200:
                    note.kill()
            self.notes_group.draw(self.screen)
            self.notes_group.update() # Atualiza a posição de todas as notas
            # 4. Notas Longas (Slider/Hold)
            
            
            #_______________________________________________________________________________________
            #__ATUALIZAÇÃO DA TELA__________________________________________________________________
            pygame.display.flip()                 # Envia o frame renderizado para o monitor
            
            
            
            #_______________________________________________________________________________________
            #__CONTROLE DE FPS______________________________________________________________________
            self.fps = self.clock.tick(60)        # Limita o jogo a 60 quadros por segundo
        
        
        # Finalização Segura do Pygame
        pygame.quit()