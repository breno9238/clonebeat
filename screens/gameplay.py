# ________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________- 
import pygame
import yaml
from functools import partial
from rules.game_widgets import Key, Note, Background, Foreground, Score, Combo, Accuracy
from rules.readers import read_settings

# ________MÓDULO DE EXECUÇÃO DO JOGO_________________________________________________________________ 
class Gameplay:
    ''' Classe que inicia e executa a gameplay '''
    
    def __init__(self, difficult: dict):
        ''' Inicializador da gameplay '''
        
        # --- Inicialização do Sistema ---
        pygame.init()
        pygame.mixer.init()
        
        # --- Configurações de Janela ---
        info = pygame.display.Info()
        self.w = info.current_w - 100
        self.h = info.current_h - 100
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.run = True
        
        # --- Configurações de Jogo e Usuário ---
        self.layer_group = pygame.sprite.LayeredUpdates
        self.settings = read_settings()
        self.skin = self.settings['skin']
        self.speed = self.settings['speed']
        
        # --- Gerenciamento de Sprites e Beatmap ---
        self.notes_group = pygame.sprite.Group()
        self.keys_group = pygame.sprite.Group()
        self.hit_objects = difficult['HitObjects']
        self.background = difficult['Background']
        self.hit_list = sorted(self.hit_objects)
        self.next_note = 0
        
        # --- Carregamento de Áudio ---
        self.audio = difficult['AudioFilename']
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        
        # --- Carregamento da Skin (YAML) ---
        skin_path = f'assets/skins/{self.skin}/apparence_4k.yaml'
        with open(skin_path, 'r', encoding='utf-8') as apparence_4k:
            self.ui = yaml.safe_load(apparence_4k)
        
        # --- Instanciação dos Elementos da Skin ---
        self.skin_elements = {
            'background': Background(ui=self.ui['background'], layer_group=self.layer_group),
            'foreground': Foreground(ui=self.ui['track_lane'], layer_group=self.layer_group),
            'score':      Score(ui=self.ui['score'], layer_group=self.layer_group),
            'combo':      Combo(ui=self.ui['combo'], layer_group=self.layer_group),
            'accuracy':   Accuracy(ui=self.ui['accuracy'], layer_group=self.layer_group)
        }
        
        # Gerando Keys e Notes via loop
        self.skin_elements['keys'] = {
            f'key_{i}': Key(ui=self.ui['keys'][f'key_{i}'], layer_group=self.layer_group) 
            for i in range(1, 5)
        }
        self.skin_elements['notes'] = {
            f'note_{i}': partial(Note, ui=self.ui['notes'][f'note_{i}'], layer_group=self.layer_group) 
            for i in range(1, 5)
        }
        
        # --- Geração de Máscaras para Colisão ---
        self.masks = {}
        # Unindo dicionários para gerar máscaras de keys e templates de notas
        elementos_colisao = {**self.skin_elements['keys'], **self.skin_elements['notes']} 
        
        for k, v in elementos_colisao.items():
            self.masks[k] = pygame.mask.from_surface(v.image)
    
    def start(self):
        # Loop principal
        while self.run:
            # --- Entrada do Usuário ---
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.run = False
            
            # --- Lógica e Renderização ---
            self.screen.fill("#5E5B8B") # Fundo sólido
            
            # 1. Desenho da Esteira (Widgets estáticos)
            # Nota: Verifique se 'self.widgets' foi definido ou se deve usar 'self.skin_elements'
            self.screen.blit(self.widgets['background'][0], self.widgets['background'][1])
            self.screen.blit(self.widgets['foreground'][0], self.widgets['foreground'][1])
            
            # 2. Spawn e Atualização das Notas
            self.time = pygame.mixer.music.get_pos()
            
            while self.next_note < len(self.hit_list):
                timestamp, pos_x = self.hit_list[self.next_note]
                
                if timestamp - self.time < 2000:
                    match pos_x:
                        case 64:  Note(self.widgets['note_1'], timestamp, self.notes_group)
                        case 192: Note(self.widgets['note_2'], timestamp, self.notes_group)
                        case 320: Note(self.widgets['note_3'], timestamp, self.notes_group)
                        case 448: Note(self.widgets['note_4'], timestamp, self.notes_group)
                    self.next_note += 1
                else:
                    break
            
            # 3. Desenho e Update dos Grupos
            self.layer_group.draw(self.screen)
            self.layer_group.update()
            
            # --- Atualização da Janela ---
            pygame.display.flip()
            
            # --- Controle de Framerate ---
            fps_target = self.settings.get('fps', 60)
            self.fps = self.clock.tick(fps_target)
        
        # Finalização
        pygame.quit()