import arcade

from configuracoes import *

from sistemas.gerenciador_resultados import carregar_ranking, salvar_no_ranking


# ==========================================
# RESULTADOS E RANKING DINÂMICO
# ==========================================
# Classe responsável por gerenciar e renderizar a tela de pontuação final e o ranking de jogadores.
class TelaResultados(arcade.View):

    # Método construtor que inicializa a tela recebendo as estatísticas e identificadores da fase.
    def __init__(
        self,
        nome_fase,
        dificuldade,
        pontuacao,
        combo,
        precisao=100.00,
        perfeito=0,
        bom=0,
        falha=0
    ):
        super().__init__()

        # ------------------------------------------
        # IDENTIFICADORES DA FASE
        # ------------------------------------------
        self.nome_fase = nome_fase  # Guarda o nome da fase atual para gravação e busca.
        self.dificuldade = dificuldade  # Guarda a dificuldade jogada para segmentação do ranking.

        # ------------------------------------------
        # ESTATÍSTICAS DA PARTIDA
        # ------------------------------------------
        self.pontuacao = pontuacao  # Armazena a pontuação total obtida pelo jogador.
        self.combo = combo  # Armazena o maior combo de notas seguidas alcançado.
        self.precisao = precisao  # Armazena a porcentagem de precisão dos acertos.
        self.perfeito = perfeito  # Armazena a quantidade de notas com acerto perfeito.
        self.bom = bom  # Armazena a quantidade de notas com acerto bom.
        self.falha = falha  # Armazena a quantidade de notas perdidas ou erradas.

        # ------------------------------------------
        # CONTROLE DA CAIXA DE TEXTO (INPUT DE NOME)
        # ------------------------------------------
        self.nome_jogador = ""  # String mutável que armazena os caracteres digitados pelo usuário.
        self.score_salvo = False  # Flag booleana para travar novas gravações após salvar uma vez.
        self.piscar_cursor = 0  # Temporizador incremental para controlar o efeito visual do cursor.

        # ------------------------------------------
        # ESTRUTURA DO RANKING DINÂMICO AUTOMÁTICO
        # ------------------------------------------
        # Carrega a lista completa de registros guardados no arquivo JSON sem travar limites.
        self.ranking = carregar_ranking(self.nome_fase, self.dificuldade)
        
        self.indice_rolagem = 0  # Controla em qual posição da lista a exibição visual deve começar.
        self.tempo_rolagem = 0.0  # Acumulador de tempo para gerenciar a velocidade da animação.
        self.direcao_rolagem = 1  # Controla o sentido da movimentação (1 para baixo, -1 para retornar ao topo).
    # ==========================================
    # RENDERIZAÇÃO GRÁFICA
    # ==========================================
    # Método automático do Arcade executado a cada quadro para desenhar os elementos na tela.
    def on_draw(self):
        self.clear()
        arcade.set_background_color((20, 10, 40))

        largura_real = self.window.width
        altura_real = self.window.height
        centro_x = largura_real / 2

        # Incrementa o temporizador para fazer o cursor de digitação piscar.
        self.piscar_cursor += 1

        # ------------------------------------------
        # ATUALIZAÇÃO DA ROLAGEM DINÂMICA
        # ------------------------------------------
        # Condicional que gerencia a movimentação da lista se houver mais de 10 recordes gravados.
        if len(self.ranking) > 10:
            self.tempo_rolagem += 1 / 60  # Incrementa o tempo aproximado baseado na taxa de frames.
            
            # Condicional que executa o passo de rolagem a cada 2.5 segundos de intervalo.
            if self.tempo_rolagem >= 2.5:
                self.tempo_rolagem = 0.0
                
                # Desloca a exibição vertical seguindo o sentido da direção ativa.
                self.indice_rolagem += self.direcao_rolagem
                
                # Condicional que detecta o fim da lista e inverte o sentido para subir.
                if self.indice_rolagem >= len(self.ranking) - 10:
                    self.indice_rolagem = len(self.ranking) - 10
                    self.direcao_rolagem = -1
                    
                # Condicional que detecta o retorno ao topo e inverte para descer de novo.
                elif self.indice_rolagem <= 0:
                    self.indice_rolagem = 0
                    self.direcao_rolagem = 1

        # ------------------------------------------
        # TÍTULO PRINCIPAL
        # ------------------------------------------
        arcade.draw_text(
            f'RESULTADO - {self.nome_fase.upper()} ({self.dificuldade})',
            centro_x, altura_real * 0.90,
            arcade.color.CYAN, 48, anchor_x='center', bold=True
        )

        # ==========================================
        # PAINEL ESQUERDO: ESTATÍSTICAS DO JOGADOR
        # ==========================================
        x_painel_esquerdo = centro_x - 580

        arcade.draw_text(f'PONTUAÇÃO: {self.pontuacao}', x_painel_esquerdo, altura_real * 0.75, arcade.color.WHITE, 34, bold=True)
        arcade.draw_text(f'PRECISÃO: {self.precisao:.2f}%', x_painel_esquerdo, altura_real * 0.67, arcade.color.GOLD, 34, bold=True)
        arcade.draw_text(f'PERFEITO: {self.perfeito}', x_painel_esquerdo, altura_real * 0.59, arcade.color.LIGHT_GREEN, 28, bold=True)
        arcade.draw_text(f'BOM: {self.bom}', x_painel_esquerdo, altura_real * 0.52, arcade.color.LIGHT_BLUE, 28, bold=True)
        arcade.draw_text(f'FALHA: {self.falha}', x_painel_esquerdo, altura_real * 0.45, arcade.color.RED, 28, bold=True)
        arcade.draw_text(f'COMBO MAXIMO: {self.combo}', x_painel_esquerdo, altura_real * 0.38, arcade.color.WHITE, 28, bold=True)

        # ------------------------------------------
        # CAIXA DE TEXTO (DIGITAR NOME)
        # ------------------------------------------
        if not self.score_salvo:
            arcade.draw_text('REGISTRE SEU NOME:', x_painel_esquerdo, altura_real * 0.28, arcade.color.CYAN, 24, bold=True)
            
            # Renderiza o fundo do campo mantendo a proporção correta com o menor valor no bottom.
            arcade.draw_lrbt_rectangle_filled(x_painel_esquerdo, x_painel_esquerdo + 420, altura_real * 0.19, altura_real * 0.25, (50, 40, 80))
            arcade.draw_lrbt_rectangle_outline(x_painel_esquerdo, x_painel_esquerdo + 420, altura_real * 0.19, altura_real * 0.25, arcade.color.WHITE, 2)
            
            cursor = "_" if (self.piscar_cursor // 30) % 2 == 0 else ""
            arcade.draw_text(f"{self.nome_jogador}{cursor}", x_painel_esquerdo + 15, altura_real * 0.205, arcade.color.YELLOW, 24, bold=True)
            arcade.draw_text('Aperte ENTER para salvar no ranking', x_painel_esquerdo, altura_real * 0.15, arcade.color.GRAY, 16, bold=True)
        else:
            arcade.draw_text('RECORDE REGISTRADO!', x_painel_esquerdo, altura_real * 0.23, arcade.color.GREEN, 24, bold=True)

        # ==========================================
        # PAINEL DIREITO: TABELA DO RANKING REDESENHADA
        # ==========================================
        x_painel_direito = centro_x - 90
        y_ranking_inicial = altura_real * 0.75

        arcade.draw_text('RANKING DE JOGADORES', x_painel_direito, y_ranking_inicial, arcade.color.CYAN, 34, bold=True)
        arcade.draw_line(x_painel_direito, y_ranking_inicial - 15, x_painel_direito + 680, y_ranking_inicial - 15, arcade.color.GRAY, 3)

        # Cabeçalho da tabela com espaçamentos otimizados para nomes longos.
        y_cabecalho = y_ranking_inicial - 50
        arcade.draw_text('POS  NOME', x_painel_direito, y_cabecalho, arcade.color.GRAY, 20, bold=True)
        arcade.draw_text('SCORE', x_painel_direito + 320, y_cabecalho, arcade.color.GRAY, 20, bold=True)
        arcade.draw_text('PRECISÃO', x_painel_direito + 470, y_cabecalho, arcade.color.GRAY, 20, bold=True)
        arcade.draw_text('ERROS', x_painel_direito + 610, y_cabecalho, arcade.color.GRAY, 20, bold=True)

        # Filtra a lista extraindo o pedaço visível dinâmico de 10 posições baseado na rolagem.
        fatia_visivel = self.ranking[self.indice_rolagem : self.indice_rolagem + 10]

        # Laço que percorre a fatia ativa e desenha as linhas da tabela.
        for idx, entrada in enumerate(fatia_visivel):
            pos_real = self.indice_rolagem + idx
            y_linha = y_cabecalho - 42 - (idx * 45)
            
            # Aplica a cor dourada de destaque se for o líder absoluto (posição 0).
            cor_linha = arcade.color.GOLD if pos_real == 0 else arcade.color.WHITE
            
            # Formata os dados textuais da linha atual aceitando o novo teto de 16 letras.
            texto_pos_nome = f"#{pos_real + 1:02d}  {entrada.get('nome', 'ANÔNIMO')[:16]}"
            texto_score = f"{entrada.get('pontuacao', 0)}"
            texto_prec = f"{entrada.get('precisao', 0.0):.2f}%"
            texto_erros = f"{entrada.get('falha', 0)}"

            # Renderiza as colunas perfeitamente tabeladas.
            arcade.draw_text(texto_pos_nome, x_painel_direito, y_linha, cor_linha, 20, bold=True)
            arcade.draw_text(texto_score, x_painel_direito + 320, y_linha, cor_linha, 20, bold=True)
            arcade.draw_text(texto_prec, x_painel_direito + 470, y_linha, cor_linha, 20, bold=True)
            arcade.draw_text(texto_erros, x_painel_direito + 610, y_linha, cor_linha, 20, bold=True)

        # ------------------------------------------
        # INSTRUÇÕES DE NAVEGAÇÃO
        # ------------------------------------------
        arcade.draw_text(
            'APERTE ESC PARA VOLTAR AO MENU',
            centro_x, altura_real * 0.06,
            arcade.color.GRAY, 22, anchor_x='center', bold=True
        )
    # ==========================================
    # CAPTURA DE INPUTS (TECLADO)
    # ==========================================
    # Método automático executado quando o usuário pressiona teclas de controle ou de texto.
    def on_key_press(self, key, modifiers):
        # Condicional que retorna ao menu de seleção de fases se o ESC for acionado.
        if key == arcade.key.ESCAPE:
            
            # Importação local interna para evitar falhas circulares na inicialização.
            from telas.menu_fases import MenuFases
            from telas.menu_principal import MenuPrincipal
            
            # ALTERADO: Define o redirecionamento gráfico para carregar de volta o menu de fases.
            self.window.show_view(MenuFases(MenuPrincipal()))
            return

        # Condicional que processa a gravação de dados ao pressionar ENTER.
        if key == arcade.key.ENTER and not self.score_salvo:
            # Invoca a inserção no arquivo JSON através do gerenciador de scores.
            salvar_no_ranking(
                self.nome_fase, self.dificuldade, self.nome_jogador,
                self.pontuacao, self.precisao, self.perfeito, self.bom, self.falha
            )
            self.score_salvo = True
            
            # Recarrega e atualiza instantaneamente a lista na tela refletindo o novo nome.
            self.ranking = carregar_ranking(self.nome_fase, self.dificuldade)
            return

        # Condicional que remove o último caractere caso o Backspace seja pressionado.
        if key == arcade.key.BACKSPACE and not self.score_salvo:
            self.nome_jogador = self.nome_jogador[:-1]
            return


    # ==========================================
    # DIGITAÇÃO DE TEXTO ACUMULADA
    # ==========================================
    # Método nativo do Arcade que captura a entrada de caracteres brutos (Unicode) de forma estável.
    def on_text(self, text):
        # Bloqueia a inserção de novos caracteres caso já tenha salvado ou estourado o limite de 16 letras.
        if self.score_salvo or len(self.nome_jogador) >= 16:
            return

        # Ignora caracteres de controle que entram como texto no buffer do pyglet.
        if text in ('\r', '\n', '\t', '\b'):
            return

        # Acumula o caractere em maiúsculo na string identificadora de nome.
        self.nome_jogador += text.upper()
