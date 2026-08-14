import arcade
import serial  # Biblioteca para conversar com o Arduino Uno

from regras.configuracoes import *

from entidades.nota import Nota

from telas.resultados import TelaResultados

from sistemas.gerenciador_skin import GerenciadorSkin
from sistemas.gerenciador_notas import GerenciadorNotas
from sistemas.gerenciador_música import GerenciadorMúsica


# ==========================================
# BANDEIRA DE TESTE
# ==========================================
# True  -> Joga usando as teclas normais do computador (modo teste de mesa)
# False -> Joga batendo nos tambores físicos conectados no Arduino Uno
USAR_TECLADO = True


# ==========================================
# GAMEPLAY
# ==========================================
class TelaGameplay(arcade.View):
    
    def __init__(self, view_anterior, fase):
        
        super().__init__()
        
        self.view_anterior = view_anterior
        self.fase = fase
        
        self.notas  = GerenciadorNotas(self.fase.notas)
        self.skin   = GerenciadorSkin(self.fase.skin)
        self.música = GerenciadorMúsica(self.fase.música)
        
        self.lista_notas = arcade.SpriteList()
        
        self.notas_restantes = self.notas.data
        
        self.pontuação = 0
        self.combo = 0
        self.max_combo = 0
        self.resultado = ''
        self.tempo = 0
        
        self.cooldown_inicial = 2.0
        self.musica_iniciada = False
        
        self.indice = 0
        
        # Inicializa o Arduino apenas se NÃO for usar o teclado
        self.arduino = None
        if not USAR_TECLADO:
            try:
                # Altere 'COM3' para a porta USB correta do seu computador
                self.arduino = serial.Serial('COM3', 115200, timeout=0)
                print("CONEXÃO: Arduino Uno conectado com sucesso no modo Bateria!")
            except Exception as e:
                print(f"AVISO: Modo bateria ativo, mas o Arduino não foi encontrado. Erro: {e}")
        else:
            print("CONEXÃO: Modo Teclado ativo! Inputs do Arduino estão desligados.")
        
        self.tempo_spawn = ((ALTURA_TELA - Y_RECEPTOR) / VELOCIDADE_QUEDA)
        
        arcade.set_background_color((20, 10, 40))
        
        self.pontuação_display = arcade.Text(
            f'PONTOS: {self.pontuação}',
            20,
            560,
            arcade.color.WHITE,
            16
        )
        
        self.combo_display = arcade.Text(
            f'COMBO: {self.combo}',
            20,
            530,
            arcade.color.WHITE,
            16
        )
        
        self.resultado_display = arcade.Text(
            self.resultado,
            LARGURA_TELA / 2,
            ALTURA_TELA / 2,
            arcade.color.WHITE,
            28,
            anchor_x='center',
            bold=True
        )
        
        self.receptores = arcade.SpriteList()
        
        for i, x in enumerate(COLUNAS_X):
            receptor = arcade.Sprite(self.skin.texturas_receptor[i])
            receptor.center_x = x
            receptor.center_y = Y_RECEPTOR
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
        
        # Só escuta a porta USB se a flag estiver em modo Bateria (False)
        if not USAR_TECLADO and self.arduino and self.arduino.in_waiting > 0:
            try:
                sinal = self.arduino.readline().decode('utf-8').strip()
                
                if sinal in ["1", "2", "3", "4"]:
                    coluna_arduino = int(sinal) - 1
                    
                    for tecla_real, col_idx in TECLAS_COLUNAS.items():
                        if col_idx == coluna_arduino:
                            self.on_key_press(tecla_real, None)
                            break
            except Exception:
                pass
        
        self.tempo += delta_time
        
        self.pontuação_display.text = f'PONTOS: {self.pontuação}'
        self.combo_display.text = f'COMBO: {self.combo}'
        self.resultado_display.text = self.resultado
        
        if self.indice < len(self.notas_restantes):
            # CORREÇÃO: Acessa a posição [0] da tupla para ler o tempo numérico da nota de forma segura
            tempo_proxima_nota = self.notas_restantes[self.indice][0] + self.tempo_spawn
            print(f"Tempo Jogo: {self.tempo:.2f} | Tempo Alvo Spawn: {(tempo_proxima_nota - self.tempo_spawn):.2f} (Nota: {tempo_proxima_nota:.3f} - Spawn: {self.tempo_spawn:.2f})")
        else: print("DEBUG: Lista de notas está vazia ou o índice já chegou ao fim!")
        
        # CORREÇÃO: Acessa a posição [0] da tupla nas duas checagens matemáticas do laço while
        while (self.indice < len(self.notas_restantes) and 
            self.tempo >= ((self.notas_restantes[self.indice][0] + self.tempo_spawn) - self.tempo_spawn)):
            
            tempo_nota, coluna = (self.notas_restantes[self.indice])
            
            self.lista_notas.append(
                Nota(
                    coluna,
                    ALTURA_TELA,
                    self.skin.texturas_notas[coluna],
                    self.skin.largura_nota,
                    self.skin.altura_nota
                )
            )
            
            self.indice += 1
        
        for nota in self.lista_notas:
            
            nota.atualizar(delta_time)
            
            if nota.center_y < (Y_RECEPTOR - MARGEM_ACERTO):
                self.combo = 0
                self.resultado = 'MISS'
            
            if nota.center_y <= 0: nota.remove_from_sprite_lists()
        
        if self.indice >= len(self.notas_restantes) and len(self.lista_notas) == 0:
            
            self.música.stop()
            
            if self.arduino:
                self.arduino.close()
                
            self.window.show_view(
                TelaResultados(
                    self.pontuação,
                    self.max_combo
                    )
                )
    
    def on_draw(self):
        
        self.clear()
        
        for x in COLUNAS_X:
            
            arcade.draw_lrbt_rectangle_filled(
                x - 55,
                x + 55,
                0,
                ALTURA_TELA,
                (20, 20, 20))
        
        self.receptores.draw()
        self.lista_notas.draw()
        
        self.pontuação_display.draw()
        self.combo_display.draw()
        self.resultado_display.draw()
    
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ESCAPE:
            self.música.stop()
            
            if self.arduino:
                self.arduino.close()
                
            self.window.show_view(self.view_anterior)
            return
        
        if not USAR_TECLADO and modifiers is not None:
            return
            
        if key not in TECLAS_COLUNAS and key != arcade.key.ESCAPE:
            return
        
        coluna = TECLAS_COLUNAS[key]
        
        self.receptores[coluna].texture = (
            self.skin.texturas_receptor_clicado[coluna]
        )
        
        notas_coluna = [n for n in self.lista_notas if n.coluna == coluna]
        
        if not notas_coluna:
            return
        
        nota = min(
            notas_coluna,
            key=lambda n: abs(n.center_y - Y_RECEPTOR))
        
        distancia = abs(nota.center_y - Y_RECEPTOR)
        
        if distancia <= MARGEM_ACERTO:
            nota.remove_from_sprite_lists()
            self.combo += 1
            
            self.max_combo = max(self.max_combo, self.combo)
            
            if distancia <= (MARGEM_ACERTO / 2):
                self.pontuação += 300
                self.resultado = 'MARVELOUS'
            
            else:
                self.pontuação += 100
                self.resultado = 'GREAT'
    
    def on_key_release(self, key, modifiers):
        
        if key not in TECLAS_COLUNAS:
            return
        
        coluna = TECLAS_COLUNAS[key]
        
        self.receptores[coluna].texture = (
            self.skin.texturas_receptor[coluna]
        )
