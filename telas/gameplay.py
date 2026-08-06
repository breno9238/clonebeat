import arcade

from regras.configuracoes import *

from entidades.nota import Nota

from telas.resultados import TelaResultados

from sistemas.gerenciador_skin import GerenciadorSkin
from sistemas.gerenciador_notas import GerenciadorNotas
from sistemas.gerenciador_música import GerenciadorMúsica


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
        
        self.indice = 0
        
        self.tempo_spawn = ((ALTURA_TELA - Y_RECEPTOR) / VELOCIDADE_QUEDA)
        
        arcade.set_background_color((25, 25, 25))
        
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
        
        self.música.play()
    
    def on_update(self, delta_time):
        
        self.tempo += delta_time
        
        self.pontuação_display.text = f'PONTOS: {self.pontuação}'
        self.combo_display.text = f'COMBO: {self.combo}'
        self.resultado_display.text = self.resultado
        
        if self.indice < len(self.notas_restantes):
            tempo_proxima_nota = self.notas_restantes[self.indice][0]
            print(f"Tempo Jogo: {self.tempo:.2f} | Tempo Alvo Spawn: {(tempo_proxima_nota - self.tempo_spawn):.2f} (Nota: {tempo_proxima_nota} - Spawn: {self.tempo_spawn:.2f})")
        else: print("DEBUG: Lista de notas está vazia ou o índice já chegou ao fim!")
        
        while (self.indice < len(self.notas_restantes) and 
            self.tempo >= (self.notas_restantes[self.indice][0] - self.tempo_spawn)):
            
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
            self.window.show_view(self.view_anterior)
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