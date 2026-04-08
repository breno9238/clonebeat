#________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________-
import pygame                       # Motor gráfico para o jogo
import json
from rules.note import Note        # Classe das notas musicais
from rules.key import Key
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
        info = pygame.display.Info()        # Pega as notecs do monitor do usuário
        
        
        # Configurações de Skin e Grupos de Sprites
        self.skin = skin
        self.notes = 4
        self.notes_group = pygame.sprite.Group() # Grupo que gerencia todas as notas ativas
        self.keys_group = pygame.sprite.Group()
        self.hit_objects = hit_objects
        self.hit_list = sorted(self.hit_objects.items())
        self.next_note = 0
        
        # Configuração da Música
        self.audio = audio_file_name
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play()
        
        #___________________________________________________________________________________________
        #__CONFIGURAÇÕES DE TELA____________________________________________________________________
        self.w      = info.current_w - 100                         # Largura (Monitor - 100px)
        self.h      = info.current_h - 100                         # Altura (Monitor - 100px)
        self.screen = pygame.display.set_mode((self.w, self.h))    # Define a janela
        self.clock  = pygame.time.Clock()                          # Controlador de FPS
        self.run    = True                                         # Controle do Loop
        
        
        
        #___________________________________________________________________________________________
        #__CARREGAMENTO DE SKIN_____________________________________________________________________
        
        self.pad = pygame.image.load(f'skins/{skin}/esteira.png').convert_alpha()
        
        # Carrega a imagem e otimiza para transparência (Alpha)
        self.pre_render_notes = {
            'blue': pygame.image.load(f'skins/{skin}/blue_note.png').convert_alpha(),
            'red': pygame.image.load(f'skins/{skin}/red_note.png').convert_alpha()
        }
        
        self.pre_render_notes = {
            'blue': pygame.transform.scale(self.pre_render_notes['blue'], (80, 80)),
            'red': pygame.transform.scale(self.pre_render_notes['red'], (80, 80))
        }
        
        # Cria uma máscara de pixels para colisões perfeitas (ignora áreas transparentes)
        self.masks = {
            'blue': pygame.mask.from_surface(self.pre_render_notes['blue']),
            'red': pygame.mask.from_surface(self.pre_render_notes['red'])
        }
        print("loop")
        self.keys = {
            pygame.K_a:   Key('skins/padrão/key.png', 64, self.h-400, self.keys_group),
            pygame.K_s:   Key('skins/padrão/key.png', 192, self.h-400, self.keys_group),
            pygame.K_KP4: Key('skins/padrão/key.png', 320, self.h-400, self.keys_group),
            pygame.K_KP5: Key('skins/padrão/key.png', 448, self.h-400, self.keys_group)
        }
        
        self.hit_line = pygame.rect.Rect(0, self.h-100, self.w, 2)
    
    def start(self):
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
            
            # impact = pygame.sprite.groupcollide(self.keys_group, self.notes_group, False, True)
            # all_notes_impacted: dict[Note, dict[int, int]] = {}
            
            # for key, notes_impacted in impact.items():
            #     for note in notes_impacted:
            #         note.kill()
            #         all_notes_impacted[note] = [note.timestamp, note.pos_x, note.rect.y]
            
            # for note_impact in all_notes_impacted.items:
            #     note_impact: list[int]
            #     for note_timestamp, note_pos_x, note_pos_y in note_impact:
            #         if self.h-100-note_pos_y > 20:
                        
                    
            #         if self.h-100-note_pos_y > 192:
                        
                    
            #         if self.h-100-note_pos_y > 320:
                        
                    
            #         if self.h-100-note_pos_y > 448:
                        
            
            
            
            #_______________________________________________________________________________________
            #__LIMPEZA DA TELA______________________________________________________________________
            self.screen.fill('#5E5B8B')           # Fundo sólido roxo acinzentado
            
            #_______________________________________________________________________________________
            #__RENDERIZAÇÃO DE OBJETOS______________________________________________________________
            
            # 1. Desenho da Esteira
            self.screen.blit(self.pad, (self.w/2 - (self.pad.get_height()/4), 0))
            
            # 3. Processamento e Desenho das Notas
            self.time = pygame.mixer.music.get_pos()
            
            while self.next_note < len(self.hit_list):
                timestamp, pos_x = self.hit_list[self.next_note]
                
                if timestamp - self.time < 2000:
                    match pos_x:
                        case 64:  Note(self.pre_render_notes['blue'], timestamp, self.w*0.35, self.h*0.9, self.notes_group)
                        case 192: Note(self.pre_render_notes['red'], timestamp, self.w*0.45, self.h*0.9, self.notes_group)
                        case 320: Note(self.pre_render_notes['red'], timestamp, self.w*0.55, self.h*0.9, self.notes_group)
                        case 448: Note(self.pre_render_notes['blue'], timestamp, self.w*0.65, self.h*0.9, self.notes_group)
                    
                    self.next_note += 1
                else:
                    break
            
            self.notes_group.draw(self.screen)
            self.notes_group.update(self.time, 20) # Atualiza a posição de todas as notas
            # 4. Notas Longas (Slider/Hold)
            
            #_______________________________________________________________________________________
            #__ATUALIZAÇÃO DA TELA__________________________________________________________________
            pygame.display.flip()                 # Envia o frame renderizado para o monitor
            
            #_______________________________________________________________________________________
            #__CONTROLE DE FPS______________________________________________________________________
            self.fps = self.clock.tick(60)        # Limita o jogo a 60 quadros por segundo
        
        
        # Finalização Segura do Pygame
        pygame.quit()