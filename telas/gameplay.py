import arcade
import serial

from regras.configuracoes import *
from entidades.nota import Nota
from telas.resultados import TelaResultados
from sistemas.gerenciador_skin import GerenciadorSkin
from sistemas.gerenciador_notas import GerenciadorNotas
from sistemas.gerenciador_música import GerenciadorMúsica

USAR_TECLADO = True

class TelaGameplay(arcade.View):
    
    def __init__(self, view_anterior, fase):
        super().__init__()
        self.view_anterior = view_anterior
        self.fase = fase
        
        # 🚀 ALTERADO BRUTAMENTE: Atualiza o Gerenciador de Skins para ler da raiz skins/ + a skin_atual escolhida
        pasta_skin_atual = Path('skins') / skin_atual
        self.notas  = GerenciadorNotas(self.fase.notas)
        self.skin   = GerenciadorSkin(pasta_skin_atual)
        self.música = GerenciadorMúsica(self.fase.música)
        
        self.lista_notas = arcade.SpriteList()
        self.notas_restantes = self.notas.data
        
        self.pontuação = 0
        self.combo = 0
        self.max_combo = 0
        self.resultado = ''
        self.tempo = 0
        
        self.notas_processadas = 0
        self.notas_acertadas = 0
        self.precisao = 100.00
        
        self.cont_perfeito = 0
        self.cont_bom = 0
        self.cont_falha = 0
        
        self.cooldown_inicial = 2.0
        self.musica_iniciada = False
        self.indice = 0
        self.arduino = None
        
        if not USAR_TECLADO:
            try:
                self.arduino = serial.Serial('COM3', 115200, timeout=0)
                print("CONEXÃO: Arduino Uno conectado com sucesso")
            except Exception as e:
                print(f"AVISO: Arduino não encontrado: {e}")
        
        self.largura_real = self.window.width
        self.altura_real = self.window.height
        
        self.largura_total_pista = 800  
        self.centro_da_tela = self.largura_real / 2
        
        self.colunas_gigantes = [
            self.centro_da_tela - 300,
            self.centro_da_tela - 100,
            self.centro_da_tela + 100,
            self.centro_da_tela + 300
        ]
        
        self.tempo_spawn = ((self.altura_real - Y_RECEPTOR) / VELOCIDADE_QUEDA)
        
        self.pontuação_display = arcade.Text(
            f'PONTOS: {self.pontuação}',
            50, self.altura_real - 80,
            arcade.color.WHITE, 38, bold=True
        )
        
        self.precisao_display = arcade.Text(
            f'PRECISÃO:\n{self.precisao:.2f}%',
            50, self.altura_real - 220,
            arcade.color.YELLOW, 38, anchor_x='left', multiline=True, width=400, bold=True
        )
        
        self.combo_display = arcade.Text(
            f'COMBO: {self.combo}',
            self.centro_da_tela, (self.altura_real / 2) - 60,
            arcade.color.WHITE, 38, anchor_x='center', bold=True
        )
        
        self.resultado_display = arcade.Text(
            self.resultado,
            self.centro_da_tela, (self.altura_real / 2) + 20,
            arcade.color.WHITE, 32, anchor_x='center', bold=True
        )
        
        self.receptores = arcade.SpriteList()
        for i, x in enumerate(self.colunas_gigantes):
            receptor = arcade.Sprite(self.skin.texturas_receptor[i])
            receptor.center_x = x
            receptor.center_y = Y_RECEPTOR
            receptor.width = 130
            receptor.height = 130
            self.receptores.append(receptor)
        
    def on_update(self, delta_time):
        if self.cooldown_inicial > 0:
            self.cooldown_inicial -= delta_time
            return
            
        if not self.musica_iniciada:
            self.música.play()
            self.musica_iniciada = True
            if self.arduino:
                self.arduino.reset_input_buffer()
            return 
        
        if not USAR_TECLADO and self.arduino and self.arduino.in_waiting > 0:
            try:
                while self.arduino.in_waiting > 0:
                    sinal = self.arduino.readline().decode('utf-8', errors='ignore').strip().lower()
                    
                    mapa_teclas = {
                        "d": arcade.key.D, "1": arcade.key.D,
                        "f": arcade.key.F, "2": arcade.key.F,
                        "j": arcade.key.J, "3": arcade.key.J,
                        "k": arcade.key.K, "4": arcade.key.K
                    }
                    
                    if sinal in mapa_teclas:
                        tecla_pressionada = mapa_teclas[sinal]
                        self.on_key_press(tecla_pressionada, None)
                        arcade.schedule(lambda dt: self.on_key_release(tecla_pressionada, None), 0.08)
            except Exception as e:
                print(f"Erro ao ler serial: {e}")
        
        self.tempo += delta_time
        
        self.pontuação_display.text = f'PONTOS: {self.pontuação}'
        self.combo_display.text = f'COMBO: {self.combo}'
        self.precisao_display.text = f'PRECISÃO:\n{self.precisao:.2f}%'
        self.resultado_display.text = self.resultado
        
        while (self.indice < len(self.notas_restantes) and 
               self.tempo >= self.notas_restantes[self.indice][0]):
            
            tempo_nota, coluna = self.notas_restantes[self.indice]
            
            nova_nota = Nota(
                coluna,
                self.altura_real + 50,
                self.skin.texturas_notas[coluna],
                self.skin.largura_nota,
                self.skin.altura_nota
            )
            nova_nota.center_x = self.colunas_gigantes[coluna]
            nova_nota.width = 130
            nova_nota.height = 130
            
            self.lista_notas.append(nova_nota)
            self.indice += 1
        
        for nota in self.lista_notas:
            nota.center_y -= (VELOCIDADE_QUEDA * delta_time)
            
            if nota.center_y < (Y_RECEPTOR - 150) and not hasattr(nota, 'computou_miss'):
                self.combo = 0
                self.resultado = 'MISS'
                self.resultado_display.color = arcade.color.RED
                nota.computou_miss = True
                
                self.cont_falha += 1
                self.notas_processadas += 1
                if self.notas_processadas > 0:
                    self.precisao = (self.notas_acertadas / self.notas_processadas) * 100
            
            if nota.center_y <= -50: 
                nota.remove_from_sprite_lists()
        
        if self.indice >= len(self.notas_restantes) and len(self.lista_notas) == 0:
            self.música.stop()
            if self.arduino:
                self.arduino.close()
            self.window.show_view(
                TelaResultados(
                    self.pontuação,
                    self.max_combo,
                    self.precisao,
                    self.cont_perfeito,
                    self.cont_bom,
                    self.cont_falha
                )
            )
    
    def on_draw(self):
        self.clear()
        
        esquerda_pista = self.centro_da_tela - (self.largura_total_pista / 2)
        direita_pista = self.centro_da_tela + (self.largura_total_pista / 2)
        
        arcade.draw_lrbt_rectangle_filled(
            esquerda_pista, direita_pista,
            0, self.altura_real, (24, 22, 33)
        )
        
        for x in self.colunas_gigantes:
            arcade.draw_line(x, 0, x, self.altura_real, (38, 35, 53), 3)
        
        self.receptores.draw()
        self.lista_notas.draw()
        self.pontuação_display.draw()
        self.combo_display.draw()
        self.precisao_display.draw()
        self.resultado_display.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.música.stop()
            if self.arduino:
                self.arduino.close()
            self.window.show_view(self.view_anterior)
            return True
        
        if not USAR_TECLADO and modifiers is not None:
            return True
        
        if key not in TECLAS_COLUNAS:
            return True
        
        coluna = TECLAS_COLUNAS[key]
        self.receptores[coluna].texture = self.skin.texturas_receptor_clicado[coluna]
        self.receptores[coluna].width = 130
        self.receptores[coluna].height = 130
        
        notas_coluna = [n for n in self.lista_notas if n.coluna == coluna]
        if not notas_coluna:
            return True
        
        nota = min(notas_coluna, key=lambda n: abs(n.center_y - Y_RECEPTOR))
        distancia = abs(nota.center_y - Y_RECEPTOR)
        
        if distancia <= 150:
            nota.remove_from_sprite_lists()
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            
            self.notas_processadas += 1
            self.notas_acertadas += 1
            if self.notas_processadas > 0:
                self.precisao = (self.notas_acertadas / self.notas_processadas) * 100
            
            if distancia <= 75:
                self.pontuação += 300
                self.resultado = 'MARVELOUS'
                self.resultado_display.color = arcade.color.LIGHT_GREEN
                self.cont_perfeito += 1
            else:
                self.pontuação += 100
                self.resultado = 'GREAT'
                self.resultado_display.color = arcade.color.LIGHT_BLUE
                self.cont_bom += 1
        
        # 🚀 FIX NOTIFICAÇÃO WINDOWS: Diz pro sistema operacional engolir o clique
        return True
                
    def on_key_release(self, key, modifiers):
        if key in TECLAS_COLUNAS:
            coluna = TECLAS_COLUNAS[key]
            self.receptores[coluna].texture = self.skin.texturas_receptor[coluna]
            self.receptores[coluna].width = 130
            self.receptores[coluna].height = 130
            
