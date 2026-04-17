#________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________-
import pygame                       # Motor gráfico para o jogo
import json
from rules.note import Note        # Classe das notas musicais
from rules.key import Key
from pathlib import Path
from rules.beatmap_reader import Beatmap



#________MÓDULO DE EXECUÇÃO DO JOGO_________________________________________________________________
class Gameplay:
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E INICIALIZAÇÃO DO PYGAME_________________________________________________________
    def __init__(self, difficult: dict):
        
        # Inicialização do Pygame e Coleta de Dados do Monitor
        pygame.init()                       # Inicia os módulos internos
        pygame.mixer.init()                 # inicia os módulos sonoros
        info = pygame.display.Info()        # Pega as notecs do monitor do usuário
        
        # Configurações do Jogo
        with open('settings.json', 'r', encoding='utf-8') as settings:
            setting = json.load(settings)
            self.skin = setting['skin']
        
        self.background = difficult['Background']
        
        # Grupos de Sprites
        self.notes_group = pygame.sprite.Group() # Grupo que gerencia todas as notas ativas
        self.keys_group = pygame.sprite.Group()
        self.hit_objects = difficult['HitObjects']
        self.hit_list = sorted(self.hit_objects)
        self.next_note = 0
        
        # Configuração da Música
        self.audio = difficult['AudioFilename']
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.set_volume(0.05)
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
        
        def load_widget(widget: str, index=None):
            try:
                if index:
                    texture = pygame.transform.scale(
                        pygame.image.load(f'skins/{self.skin}/'+str(widget[index]['texture'])).convert_alpha(),
                        (self.w*widget[index]['width'], 
                        self.h*widget[index]['height'])
                    )
                    position = (widget[index]['pos_x'], widget[index]['pos_y'])
                    texture.set_alpha(widget[index]['opacity'])
                    zindex = widget[index]['zindex']
                
                else:
                    texture = pygame.transform.scale(
                        pygame.image.load(f'skins/{self.skin}/'+str(widget['texture'])).convert_alpha(),
                        (self.w*widget['width'],
                        self.h*widget['height'])
                    )
                    texture.set_alpha(widget['opacity'])
                    zindex = widget['zindex']
                    position = (widget['pos_x'], widget['pos_y'])
                return [texture, position, zindex]
            
            except FileNotFoundError as error:
                try:
                    if f'{self.skin}/0' in str(error) and widget == 'background': 
                        texture = pygame.transform.scale(
                            pygame.image.load(self.background),
                            (self.w*widget['width'], 
                            self.h*widget['height'])
                        )
                        texture.set_alpha(widget['opacity'])
                        zindex = widget['zindex']
                        position = (widget['pos_x'], widget['pos_y'])
                        return [texture, position, zindex]
                
                except TypeError: 
                    print(f'\n\n{self.background}\n\n')
        
        def extract_apparence(data_req):
            with open(f'skins/{self.skin}/apparence_4k.json', 'r', encoding='utf-8') as apparence:
                data = json.load(apparence)
                return data[data_req]
        
        self.widgets = {
            'background': load_widget(widget=extract_apparence('background')),
            'foreground': load_widget(widget=extract_apparence('foreground')),
            'note_1':     load_widget(widget=extract_apparence('notes'), index='note_1'),
            'note_2':     load_widget(widget=extract_apparence('notes'), index='note_2'),
            'note_3':     load_widget(widget=extract_apparence('notes'), index='note_3'),
            'note_4':     load_widget(widget=extract_apparence('notes'), index='note_4'),
            'key_1':      load_widget(widget=extract_apparence('keys'),  index='key_1'),
            'key_2':      load_widget(widget=extract_apparence('keys'),  index='key_2'),
            'key_3':      load_widget(widget=extract_apparence('keys'),  index='key_3'),
            'key_4':      load_widget(widget=extract_apparence('keys'),  index='key_4')
        }
        
        # Cria uma máscara de pixels para colisões perfeitas (ignora áreas transparentes)
        self.masks = {(i, pygame.mask.from_surface(self.widgets[i][0])) for i in self.widgets.keys() if 'note' in i or 'key' in i}
        
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
                        case 64:  Note(self.widgets['note_1'], timestamp, 64, self.notes_group)
                        case 192: Note(self.widgets['note_2'], timestamp, 192, self.notes_group)
                        case 320: Note(self.widgets['note_3'], timestamp, 320, self.notes_group)
                        case 448: Note(self.widgets['note_4'], timestamp, 448, self.notes_group)
                    
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