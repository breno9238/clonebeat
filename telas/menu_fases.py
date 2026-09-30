import arcade
import configuracoes

from pathlib import Path
from entidades.fase import Fase
from telas.tela_jogo import TelaGameplay
from sistemas.gerenciador_resultados import carregar_melhor_score, apagar_ranking_fase

# ==========================================
# MENU FASES
# ==========================================
# Classe responsável por gerenciar a renderização e controles da seleção de fases.
class MenuFases(arcade.View):

    # Construtor responsável por preparar todos os dados necessários para o menu de fases.
    def __init__(self, view_anterior):
        super().__init__()
        self.view_anterior = view_anterior
        self.fases = []
        self.indice = 0
        self.backgrounds = {}
        self.background_selecionado = None

        self.fundo_largura = 700
        self.fundo_altura = 315

        # ------------------------------------------
        # CONFIGURAÇÃO DOS ELEMENTOS VISUAIS
        # ------------------------------------------
        self.titulo = arcade.Text(
            'SELECIONE UMA FASE',
            0, 0,
            arcade.color.WHITE, 42,
            anchor_x='center', bold=True
        )
        self.nome_fase = arcade.Text(
            '',
            0, 0,
            (220, 220, 220), 32,
            anchor_x='center', bold=True
        )
        self.texto_dificuldade = arcade.Text(
            '',
            0, 0,
            arcade.color.YELLOW, 26,
            anchor_x='center', bold=True
        )
        self.texto_highscore = arcade.Text(
            '',
            0, 0,
            arcade.color.GOLD, 24,
            anchor_x='center', bold=True
        )

        self.textos_fases = []

        # Percorre todas as pastas existentes dentro da pasta principal das fases.
        for pasta_fase in sorted(configuracoes.CAMINHO_PASTA_FASES.iterdir(), key=lambda pasta: pasta.name):
            if not pasta_fase.is_dir():
                continue

            nome = pasta_fase.name
            música = pasta_fase / 'audio.mp3'
            fundo = None

            # Procura uma imagem de fundo utilizando as extensões permitidas.
            for extensao in ('.jpg', '.jpeg', '.png'):
                caminho = pasta_fase / f'fundo{extensao}'
                if caminho.is_file():
                    fundo = caminho
                    break

            if not música.is_file():
                continue

            # Carrega de forma dinâmica a skin ativa direto do arquivo de configurações globais.
            pasta_skin_global = Path('skins') / configuracoes.skin_atual

            # Cria o objeto da fase passando o diretório completo para mapear as dificuldades.
            fase = Fase(
                len(self.fases) + 1,
                nome,
                pasta_fase,
                pasta_skin_global,
                música,
                fundo
            )
            self.fases.append(fase)

        # Cria um objeto de texto para cada fase encontrada na varredura.
        for i in range(len(self.fases)):
            self.textos_fases.append(
                arcade.Text(
                    str(i + 1),
                    0, 0,
                    arcade.color.WHITE, 28,
                    anchor_x='center', anchor_y='center', bold=True
                )
            )

        if self.fases:
            self.atualizar_fase_selecionada()

    # Método automático executado quando esta View passa a ser a tela ativa.
    def on_show_view(self):
        arcade.set_background_color((20, 10, 40))

    # ==========================================
    # ATUALIZAÇÃO DE INTERFACE
    # ==========================================
    # Atualiza todos os elementos visuais e de texto relacionados à fase e dificuldade.
    def atualizar_fase_selecionada(self):
        if not self.fases:
            return

        fase = self.fases[self.indice]
        self.nome_fase.text = fase.nome
        self.texto_dificuldade.text = f"< DIFICULDADE: {fase.dificuldade_atual} >"
        
        # Sincroniza dinamicamente a cor do texto usando o RGB lido do nome do arquivo físico.
        self.texto_dificuldade.color = fase.cor_dificuldade_atual
        
        # Carrega o dicionário com os dados completos do melhor score gravado.
        dados_recorde = carregar_melhor_score(fase.nome, fase.dificuldade_atual)
        
        # Condicional que checa se existe um recorde válido associado (score maior que zero).
        if dados_recorde.get("pontuacao", 0) > 0:
            nome = dados_recorde.get("nome", "ANÔNIMO")
            pts = dados_recorde.get("pontuacao", 0)
            prec = dados_recorde.get("precisao", 0.0)
            self.texto_highscore.text = f"RECORDE: {pts} pts ({prec:.2f}%) por {nome}"
        else:
            self.texto_highscore.text = "RECORDE: NENHUM REGISTRO"

        if fase.fundo is not None:
            caminho = Path(fase.fundo)
            if caminho in self.backgrounds:
                self.background_selecionado = self.backgrounds[caminho]
            else:
                self.background_selecionado = arcade.load_texture(caminho)
                self.backgrounds[caminho] = self.background_selecionado
        else:
            self.background_selecionado = None

        self.atualizar_tamanho_background()

    # Calcula o tamanho do fundo preservando a proporção original da imagem.
    def atualizar_tamanho_background(self):
        if self.background_selecionado is None:
            self.fundo_largura = 700
            self.fundo_altura = 315
            return

        largura_original = self.background_selecionado.width
        altura_original = self.background_selecionado.height
        largura_maxima, altura_maxima = 700, 315
        proporcao = largura_original / altura_original

        largura = largura_maxima
        altura = largura / proporcao

        if altura > altura_maxima:
            altura = altura_maxima
            largura = altura * proporcao

        self.fundo_largura = largura
        self.fundo_altura = altura

    # ==========================================
    # RENDERIZAÇÃO GRÁFICA (TELA DE SELEÇÃO)
    # ==========================================
    # Desenha todos os componentes visuais, menus e overlays na janela.
    def on_draw(self):
        self.clear()
        largura_real = self.window.width
        altura_real = self.window.height
        centro_x = largura_real / 2

        # ------------------------------------------
        # DISTRIBUIÇÃO VERTICAL DE CIMA PARA BAIXO
        # ------------------------------------------
        # Titulo reposicionado mais alto, mantendo um respiro elegante até o topo.
        self.titulo.x = centro_x
        self.titulo.y = altura_real * 0.92
        self.titulo.draw()

        if self.fases:
            # Nome da fase deslocado simetricamente para cima.
            self.nome_fase.x = centro_x
            self.nome_fase.y = altura_real * 0.85
            self.nome_fase.draw()
            
            # Texto identificador da dificuldade ativa com espaçamento confortável.
            self.texto_dificuldade.x = centro_x
            self.texto_dificuldade.y = altura_real * 0.79
            self.texto_dificuldade.draw()

            # Placar de recordes posicionado logo abaixo da dificuldade correspondente.
            self.texto_highscore.x = centro_x
            self.texto_highscore.y = altura_real * 0.74
            self.texto_highscore.draw()

        # Centro da foto do mapa subiu ligeiramente para 0.51.
        fundo_x = centro_x
        fundo_y = altura_real * 0.51
        esquerda = fundo_x - self.fundo_largura / 2
        direita = fundo_x + self.fundo_largura / 2
        baixo = fundo_y - self.fundo_altura / 2
        cima = fundo_y + self.fundo_altura / 2

        if self.background_selecionado is not None:
            arcade.draw_texture_rect(self.background_selecionado, arcade.LBWH(esquerda, baixo, self.fundo_largura, self.fundo_altura))
        else:
            arcade.draw_lrbt_rectangle_filled(esquerda, direita, baixo, cima, (50, 50, 50))

        arcade.draw_lrbt_rectangle_outline(esquerda, direita, baixo, cima, (130, 130, 130), 4)

        # ==========================================
        # BOTÃO MODO INVISÍVEL (QUADRADO BRANCO DINÂMICO)
        # ==========================================
        # Posicionado de forma simétrica no meio da tela verticalmente.
        bx = largura_real - 160
        by = altura_real * 0.51
        
        # ALTERADO: Inverte as cores de fundo e do texto dinamicamente com base no estado ativo.
        if configuracoes.MODO_INVISIVEL:
            cor_fundo_quadrado = (255, 255, 255)       # Branco puro quando ativado.
            cor_borda_quadrado = (200, 200, 200)       # Cinza claro para a borda ativa.
            cor_texto_quadrado = (20, 10, 40)          # Texto escuro para dar contraste no fundo branco.
        else:
            cor_fundo_quadrado = (40, 35, 55)          # Cinza-escuro original quando desativado.
            cor_borda_quadrado = (100, 100, 110)       # Borda opaca discreta.
            cor_texto_quadrado = (255, 255, 255)       # Texto branco puro.
        
        # ALTERADO: Recuos simétricos de 60px para criar um QUADRADO perfeito de 120x120px.
        arcade.draw_lrbt_rectangle_filled(bx - 60, bx + 60, by - 60, by + 60, cor_fundo_quadrado)
        arcade.draw_lrbt_rectangle_outline(bx - 62, bx + 62, by - 62, by + 62, cor_borda_quadrado, 3)
        
        # Renderiza as linhas textuais dentro do bloco quadrado com quebra de linha.
        arcade.draw_text(
            "MODO\nINVISÍVEL\n[ TECLA I ]",
            bx - 60, by + 20,
            cor_texto_quadrado, 15,
            align='center', bold=True,
            multiline=True, width=120
        )






        # ==========================================
        # MATRIZ DE BOTÕES ORIGINAIS GRANDES
        # ==========================================
        # Laço que desenha as duas linhas de caixas respeitando a proporção inicial.
        for i in range(len(self.fases)):
            coluna = i % 5  # MANTIDO: Fixa exatamente 5 botões por fileira horizontal.
            linha = i // 5  # MANTIDO: Quebra para a segunda fileira a partir da 6ª fase (índice 5).
            
            # Subi a base do eixo Y para o multiplicador 0.22 para dar mais distância do rodapé.
            x = (centro_x) - 320 + (coluna * 160)
            y = (altura_real * 0.22) - (linha * 110)

            selecionado = (i == self.indice)
            cor = (180, 180, 180) if selecionado else (60, 60, 60)
            
            # MANTIDO: Tamanho físico original de 130px de largura e 90px de altura.
            arcade.draw_lrbt_rectangle_filled(x - 65, x + 65, y - 45, y + 45, cor)

            if selecionado:
                arcade.draw_lrbt_rectangle_outline(x - 67, x + 67, y - 47, y + 47, (220, 220, 220), 4)

            self.textos_fases[i].x = x
            self.textos_fases[i].y = y
            self.textos_fases[i].draw()


    # ==========================================
    # CONTROLE DE ENTRADAS (TECLADO)
    # ==========================================
    # Processa as interações do teclado para navegar pelas fases e dificuldades.
    def on_key_press(self, key, modifiers):
        if not self.fases:
            return

        fase_atual = self.fases[self.indice]

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.view_anterior)
            return
        
        elif key == arcade.key.LEFT:
            self.indice = (self.indice - 1) % len(self.fases)
            self.atualizar_fase_selecionada()
            
        elif key == arcade.key.RIGHT:
            self.indice = (self.indice + 1) % len(self.fases)
            self.atualizar_fase_selecionada()

        # Condicional que altera a dificuldade selecionada movendo para cima na lista interna.
        elif key == arcade.key.UP:
            fase_atual.indice_dificuldade = (fase_atual.indice_dificuldade - 1) % len(fase_atual.lista_dificuldades)
            self.atualizar_fase_selecionada()

        # Condicional que altera a dificuldade selecionada movendo para baixo na lista interna.
        elif key == arcade.key.DOWN:
            fase_atual.indice_dificuldade = (fase_atual.indice_dificuldade + 1) % len(fase_atual.lista_dificuldades)
            self.atualizar_fase_selecionada()

        # Condicional que limpa o ranking da dificuldade atual caso a tecla DELETE seja pressionada.
        elif key == arcade.key.DELETE:
            apagar_ranking_fase(fase_atual.nome, fase_atual.dificuldade_atual)
            self.atualizar_fase_selecionada()
        
        # Condicional que confirma a seleção e inicia a partida na fase correspondente.
        elif key == arcade.key.ENTER:
            self.window.show_view(TelaGameplay(self, fase_atual))
            return

        # Condicional que liga ou desliga o modificador do Modo Invisível ao pressionar a tecla I.
        elif key == arcade.key.I:
            configuracoes.MODO_INVISIVEL = not configuracoes.MODO_INVISIVEL
            return