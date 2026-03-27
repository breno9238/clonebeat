#________IMPORTAÇÃO DE DEPENDÊNCIAS________________________________________________________________-
import pygame                       # Motor gráfico para o jogo
from rules.note import Notes        # Classe das notas musicais



#________MÓDULO DE EXECUÇÃO DO JOGO_________________________________________________________________
class Gameplay:
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E INICIALIZAÇÃO DO PYGAME_________________________________________________________
    def __init__(
        self, 
        skin: str,
        audio_file_name: str,
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
        info = pygame.display.Info()        # Pega as specs do monitor do usuário
        
        # Configurações de Skin e Grupos de Sprites
        self.skin = 'padrão'
        self.notes = Notes
        self.notes_group = pygame.sprite.Group() # Grupo que gerencia todas as notas ativas
        
        
        
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
            
            # 2. Chaves de Entrada
            self.screen
            
            # 3. Processamento e Desenho das Notas
            for note in self.notes:
                
                # Instanciação da Nota (Caminho fixo temporário)
                note = Notes('beatmaps/2484096 DETRO - volcanic (Short Ver.)7/Menphiss (1).png', 5, 1, 50)
                self.notes_group.add(note)
                
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

if __name__ == '__main__':
    
    test = Gameplay(
        'padrão', 
            'C:\Users\Mecanica\OneDrive\Desktop\clonebeat\beatmaps\2484096 DETRO - volcanic (Short Ver.)\D#5.wav',)