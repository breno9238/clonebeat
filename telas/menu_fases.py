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
        
        self.fundo_largura = 400
        self.fundo_altura = 180
        
        self.titulo = arcade.Text(
            'SELECIONE UMA FASE',
            LARGURA_TELA / 2,
            540,
            arcade.color.WHITE,
            26,
            anchor_x='center',
            bold=True
        )
        
        self.nome_fase = arcade.Text(
            '',
            LARGURA_TELA / 2,
            500,
            (190, 190, 190),
            20,
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
            skin = pasta_fase / 'skin'
            música = pasta_fase / 'audio.mp3'
            background = None
            
            for extensao in ('.jpg', '.jpeg', '.png'):
                caminho = pasta_fase / f'background{extensao}'
                
                if caminho.is_file():
                    background = caminho
                    break
            
            if not notas.is_file():
                continue
            
            if not skin.is_dir():
                continue
            
            if not música.is_file():
                continue
            
            fase = Fase(
                len(self.fases) + 1,
                nome,
                notas,
                skin,
                música,
                background
            )
            
            self.fases.append(fase)
        
        # CRIAR TEXTOS DOS NÚMEROS
        for i in range(len(self.fases)):
            coluna = i % 5
            linha = i // 5
            
            x = 80 + coluna * 110
            y = 155 - linha * 75
            
            self.textos_fases.append(
                arcade.Text(
                    str(i + 1),
                    x,
                    y,
                    arcade.color.WHITE,
                    16,
                    anchor_x='center',
                    anchor_y='center',
                    bold=True
                )
            )
        
        if self.fases:
            self.atualizar_fase_selecionada()
            
    # ==========================================
    # EVENTO AO MOSTRAR A TELA
    # ==========================================
    def on_show_view(self):
        # ALTERADO APENAS AQUI: Aplica a mesma cor (20, 10, 40) do seu Menu Principal
        arcade.set_background_color((20, 10, 40)) 
        
        if self.fases and self.preview is None:
            fase = self.fases[self.indice]
            self.preview = GerenciadorMúsica(fase.música)
            self.preview.play()
    
    
    # ==========================================
    # ATUALIZAR FASE SELECIONADA
    # ==========================================
    def atualizar_fase_selecionada(self):
        if not self.fases:
            return
        
        fase = self.fases[self.indice]
        
        # PARAR PREVIEW ANTERIOR
        if self.preview is not None:
            self.preview.stop()
            self.preview = None
        
        # NOME DA FASE
        self.nome_fase.text = fase.nome
        
        # BACKGROUND
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
        
        # PREVIEW DA MÚSICA
        self.preview = GerenciadorMúsica(fase.música)
        self.preview.play()
    
    
    # ==========================================
    # ATUALIZAR TAMANHO DO BACKGROUND
    # ==========================================
    def atualizar_tamanho_background(self):
        if self.background_selecionado is None:
            self.fundo_largura = 400
            self.fundo_altura = 180
            
            return
        
        largura_original = self.background_selecionado.width
        altura_original = self.background_selecionado.height
        
        largura_maxima = 400
        altura_maxima = 180
        
        proporcao = largura_original / altura_original
        
        largura = largura_maxima
        altura = largura / proporcao
        
        if altura > altura_maxima:
            altura = altura_maxima
            largura = altura * proporcao
        
        self.fundo_largura = largura
        self.fundo_altura = altura
    
    
    # ==========================================
    # DESENHAR
    # ==========================================
    def on_draw(self):
        self.clear()
        
        self.titulo.draw()
        
        if self.fases:
            self.nome_fase.draw()
        
        fundo_x = LARGURA_TELA / 2
        fundo_y = 365
        
        esquerda = fundo_x - self.fundo_largura / 2
        direita = fundo_x + self.fundo_largura / 2
        baixo = fundo_y - self.fundo_altura / 2
        cima = fundo_y + self.fundo_altura / 2
        
        # BACKGROUND
        if self.background_selecionado is not None:
            arcade.draw_texture_rect(
                self.background_selecionado,
                arcade.LBWH(
                    esquerda,
                    baixo,
                    self.fundo_largura,
                    self.fundo_altura
                )
            )
        else:
            arcade.draw_lrbt_rectangle_filled(
                esquerda,
                direita,
                baixo,
                cima,
                (50, 50, 50)
            )
        
        # BORDA
        arcade.draw_lrbt_rectangle_outline(
            esquerda,
            direita,
            baixo,
            cima,
            (130, 130, 130),
            3
        )
        
        # QUADRADOS DAS FASES
        for i in range(len(self.fases)):
            coluna = i % 5
            linha = i // 5
            
            x = 80 + coluna * 110
            y = 155 - linha * 75
            
            selecionado = i == self.indice
            
            if selecionado:
                cor = (180, 180, 180)
            else:
                cor = (60, 60, 60)
            
            arcade.draw_lrbt_rectangle_filled(
                x - 40,
                x + 40,
                y - 25,
                y + 25,
                cor
            )
            
            if selecionado:
                arcade.draw_lrbt_rectangle_outline(
                    x - 42,
                    x + 42,
                    y - 27,
                    y + 27,
                    (220, 220, 220),
                    3
                )
            
            self.textos_fases[i].draw()
    
    
    # ==========================================
    # TECLAS
    # ==========================================
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
            
        # ENTER / SPACE (Gatilho para iniciar a música selecionada)
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.preview is not None:
                self.preview.stop()
                self.preview = None
            fase_selecionada = self.fases[self.indice]
            self.window.show_view(TelaGameplay(self, fase_selecionada))
            return
        
        # ESQUERDA
        if key == arcade.key.LEFT:
            if self.indice > 0:
                self.indice -= 1
        
        # DIREITA
        elif key == arcade.key.RIGHT:
            if self.indice < len(self.fases) - 1:
                self.indice += 1
        
        # CIMA
        elif key == arcade.key.UP:
            if self.indice >= 5:
                self.indice -= 5
        
        # BAIXO
        elif key == arcade.key.DOWN:
            if self.indice + 5 < len(self.fases):
                self.indice += 5
                
        if self.indice != indice_anterior:
            self.atualizar_fase_selecionada()
