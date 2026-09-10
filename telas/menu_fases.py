import arcade

from regras.configuracoes import *

from entidades.fase import Fase

from telas.gameplay import TelaGameplay

from pathlib import Path

from sistemas.gerenciador_música import GerenciadorMúsica


# ==========================================
# MENU FASES
# ==========================================
class MenuFases(arcade.View):
    
    def __init__(self, view_anterior):
        super().__init__()
        
        self.view_anterior = view_anterior
        
        self.fases = []
        self.indice = 0
        self.preview = None
        
        self.backgrounds = {}
        self.background_selecionado = None
        
        self.fundo_largura = 700
        self.fundo_altura = 315
        
        self.titulo = arcade.Text(
            'SELECIONE UMA FASE',
            0, 0,
            arcade.color.WHITE,
            42,
            anchor_x='center',
            bold=True
        )
        
        self.nome_fase = arcade.Text(
            '',
            0, 0,
            (220, 220, 220),
            32,
            anchor_x='center',
            bold=True
        )
        
        self.textos_fases = []
        
        # CARREGAR FASES
        for pasta_fase in sorted(
            CAMINHO_PASTA_FASES.iterdir(),
            key=lambda pasta: pasta.name
        ):
            if not pasta_fase.is_dir():
                continue
            
            nome = pasta_fase.name
            notas = pasta_fase / 'notas.ini'
            música = pasta_fase / 'audio.mp3'
            background = None
            
            for extensao in ('.jpg', '.jpeg', '.png'):
                caminho = pasta_fase / f'background{extensao}'
                
                if caminho.is_file():
                    background = caminho
                    break
            
            if not notas.is_file():
                continue
            
            if not música.is_file():
                continue
            
            # 🚀 ALTERADO BRUTAMENTE: Agora aponta para a pasta global de skins na raiz usando a skin_atual do menu
            pasta_skin_global = Path('skins') / skin_atual
            
            fase = Fase(
                len(self.fases) + 1,
                nome,
                notas,
                pasta_skin_global,
                música,
                background
            )
            
            self.fases.append(fase)
        
        for i in range(len(self.fases)):
            self.textos_fases.append(
                arcade.Text(
                    str(i + 1),
                    0, 0,
                    arcade.color.WHITE,
                    28,
                    anchor_x='center',
                    anchor_y='center',
                    bold=True
                )
            )
        
        if self.fases:
            self.atualizar_fase_selecionada()
            
    def on_show_view(self):
        arcade.set_background_color((20, 10, 40)) 
        
        if self.fases and self.preview is None:
            fase = self.fases[self.indice]
            self.preview = GerenciadorMúsica(fase.música)
            self.preview.play()
    
    def atualizar_fase_selecionada(self):
        if not self.fases:
            return
        
        fase = self.fases[self.indice]
        
        if self.preview is not None:
            self.preview.stop()
            self.preview = None
        
        self.nome_fase.text = fase.nome
        
        if fase.background is not None:
            caminho = Path(fase.background)
            
            if caminho in self.backgrounds:
                self.background_selecionado = self.backgrounds[caminho]
            else:
                self.background_selecionado = arcade.load_texture(caminho)
                self.backgrounds[caminho] = self.background_selecionado
        else:
            self.background_selecionado = None
        
        self.atualizar_tamanho_background()
        
        self.preview = GerenciadorMúsica(fase.música)
        self.preview.play()
    
    def atualizar_tamanho_background(self):
        if self.background_selecionado is None:
            self.fundo_largura = 700
            self.fundo_altura = 315
            return
        
        largura_original = self.background_selecionado.width
        altura_original = self.background_selecionado.height
        
        largura_maxima = 700
        altura_maxima = 315
        
        proporcao = largura_original / altura_original
        largura = largura_maxima
        altura = largura / proporcao
        
        if altura > altura_maxima:
            altura = altura_maxima
            largura = altura * proporcao
        
        self.fundo_largura = largura
        self.fundo_altura = altura
    
    def on_draw(self):
        self.clear()
        
        largura_real = self.window.width
        altura_real = self.window.height
        
        self.titulo.x = largura_real / 2
        self.titulo.y = altura_real * 0.88
        self.titulo.draw()
        
        if self.fases:
            self.nome_fase.x = largura_real / 2
            self.nome_fase.y = altura_real * 0.80
            self.nome_fase.draw()
        
        fundo_x = largura_real / 2
        fundo_y = altura_real * 0.50
        
        esquerda = fundo_x - self.fundo_largura / 2
        direita = fundo_x + self.fundo_largura / 2
        baixo = fundo_y - self.fundo_altura / 2
        cima = fundo_y + self.fundo_altura / 2
        
        if self.background_selecionado is not None:
            arcade.draw_texture_rect(
                self.background_selecionado,
                arcade.LBWH(esquerda, baixo, self.fundo_largura, self.fundo_altura)
            )
        else:
            arcade.draw_lrbt_rectangle_filled(esquerda, direita, baixo, cima, (50, 50, 50))
        
        arcade.draw_lrbt_rectangle_outline(esquerda, direita, baixo, cima, (130, 130, 130), 4)
        
        for i in range(len(self.fases)):
            coluna = i % 5
            linha = i // 5
            
            x = (largura_real / 2) - 320 + (coluna * 160)
            y = (altura_real * 0.18) - (linha * 110)
            
            selecionado = i == self.indice
            cor = (180, 180, 180) if selecionado else (60, 60, 60)
            
            arcade.draw_lrbt_rectangle_filled(x - 65, x + 65, y - 45, y + 45, cor)
            
            if selecionado:
                arcade.draw_lrbt_rectangle_outline(x - 67, x + 67, y - 47, y + 47, (220, 220, 220), 4)
            
            self.textos_fases[i].x = x
            self.textos_fases[i].y = y
            self.textos_fases[i].draw()
    
    def on_key_press(self, key, modifiers):
        if not self.fases:
            return
        
        indice_anterior = self.indice
        
        if key == arcade.key.ESCAPE:
            if self.preview is not None:
                self.preview.stop()
                self.preview = None
            self.window.show_view(self.view_anterior)
            return

        elif key == arcade.key.LEFT:
            self.indice = (self.indice - 1) % len(self.fases)
        
        elif key == arcade.key.RIGHT:
            self.indice = (self.indice + 1) % len(self.fases)
            
        elif key == arcade.key.ENTER:
            if self.preview is not None:
                self.preview.stop()
                self.preview = None
            self.window.show_view(TelaGameplay(self, self.fases[self.indice]))
            return

        if self.indice != indice_anterior:
            self.atualizar_fase_selecionada()
