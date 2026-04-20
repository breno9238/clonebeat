#________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________-
import pygame                       # Motor gráfico para o jogo
import json
from functools import partial
from rules.game_widgets import Key, Note, Background, Foreground, Score, Combo, Accuracy
from rules.readers import read_settings


#_______________________________________________________________________________________________
#________MÓDULO DE EXECUÇÃO DO JOGO_________________________________________________________________
class Gameplay:
    '''
    Classe que inicia e executa a gameplay
    '''
    
    def __init__(self, difficult: dict):
        '''
        Inicializador da gameplay
        '''
        
        # Inicialização do módulo do Pygame
        pygame.init()
        
        # Inicia os módulos sonoros
        pygame.mixer.init()
        
        # Pega as dimensões do monitor do 
        info = pygame.display.Info() 
        
        # Configurações da Tela
        self.w      = info.current_w - 100                         # Largura (Monitor - 100px)
        self.h      = info.current_h - 100                         # Altura (Monitor - 100px)
        self.screen = pygame.display.set_mode((self.w, self.h))    # Define a janela
        self.clock  = pygame.time.Clock()                          # Controlador de FPS
        self.run    = True                                         # Controle do Loop
        
        # Configurações do jogo
        self.layer_group = pygame.sprite.LayeredUpdates
        self.settings    = read_settings()
        self.skin        = self.settings['skin']
        self.speed       = self.settings['speed']
        
        # Carregamento do Beatmap
        self.notes_group = pygame.sprite.Group # Grupo que gerencia todas as notas ativas
        self.keys_group  = pygame.sprite.Group # Grupo que gerencia
        self.hit_objects = difficult['HitObjects']
        self.hit_list    = sorted(self.hit_objects)
        self.next_note   = 0
        
        # Carregamento da Skin
        self.background = difficult['Background']
        self.widgets = {
            'background' :   Background(skin_path=self.skin, layer_group=self.layer_group),
            'foreground' :   Foreground(skin_path=self.skin, layer_group=self.layer_group),
            'score'      :        Score(skin_path=self.skin, layer_group=self.layer_group),
            'combo'      :        Combo(skin_path=self.skin, layer_group=self.layer_group),
            'accuracy'   :     Accuracy(skin_path=self.skin, layer_group=self.layer_group),
            'key_1'      :          Key(skin_path=self.skin, layer_group=self.layer_group),
            'key_2'      :          Key(skin_path=self.skin, layer_group=self.layer_group),
            'key_3'      :          Key(skin_path=self.skin, layer_group=self.layer_group),
            'key_4'      :          Key(skin_path=self.skin, layer_group=self.layer_group),
            'note_1'     : partial(Note(skin_path=self.skin, layer_group=self.layer_group)),
            'note_2'     : partial(Note(skin_path=self.skin, layer_group=self.layer_group)),
            'note_3'     : partial(Note(skin_path=self.skin, layer_group=self.layer_group1)),
            'note_4'     : partial(Note(skin_path=self.skin, layer_group=self.layer_group))
        }
        
        for widget in self.widgets.items():
            self.layer_group.add(widget)
        
        # Cria uma máscara de pixels para colisões perfeitas (ignora áreas transparentes)
        self.masks = {(i, pygame.mask.from_surface(self.widgets[i][0])) for i in self.widgets.keys() if 'note' in i or 'key' in i}
        
        
        # CONFIGURAÇÃO DA MÚSICA
        self.audio = difficult['AudioFilename']
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
    
    
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
            try:
                self.screen.blit(self.widgets['background'][0], self.widgets['background'][1])
                self.screen.blit(self.widgets['foreground'][0], self.widgets['foreground'][1])
            except TypeError: print(f'\n\n\n{self.widgets}\n\n\n')
            
            # 3. Processamento e Desenho das Notas
            self.time = pygame.mixer.music.get_pos()
            
            while self.next_note < len(self.hit_list):
                timestamp, pos_x = self.hit_list[self.next_note]
                
                if timestamp - self.time < 2000:
                    match pos_x:
                        case 64:  Note(self.widgets['note_1'], timestamp,  self.notes_group)
                        case 192: Note(self.widgets['note_2'], timestamp,  self.notes_group)
                        case 320: Note(self.widgets['note_3'], timestamp,  self.notes_group)
                        case 448: Note(self.widgets['note_4'], timestamp,  self.notes_group)
                    
                    self.next_note += 1
                
                else:
                    break
            
            self.notes_group.draw(self.screen,)
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