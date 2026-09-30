import arcade
import serial
import configuracoes

from pathlib import Path
from entidades.nota import Nota
from telas.tela_resultados import TelaResultados
from sistemas.gerenciador_skin import GerenciadorSkin
from sistemas.gerenciador_notas import GerenciadorNotas
from sistemas.gerenciador_música import GerenciadorMúsica


# ==========================================
# TELA GAMEPLAY
# ==========================================
# Classe que gerencia a tela principal de jogabilidade da partida.
class TelaGameplay(arcade.View):
    
    # Método construtor que inicializa a tela de jogabilidade com a fase selecionada.
    def __init__(self, view_anterior, fase):
        super().__init__()
        self.view_anterior = view_anterior
        self.fase = fase
        
        # ------------------------------------------
        # CARREGAMENTO DE RECURSOS
        # ------------------------------------------
        # Monta o caminho dinâmico com a skin selecionada globalmente.
        pasta_skin_atual = Path('skins') / configuracoes.skin_atual
        
        # Instancia os gerenciadores usando as propriedades dinâmicas da fase.
        self.notas = GerenciadorNotas(self.fase.notas)
        self.skin = GerenciadorSkin(pasta_skin_atual)
        self.música = GerenciadorMúsica(self.fase.música)
        
        # ------------------------------------------
        # ESTRUTURA DE DADOS DAS NOTAS
        # ------------------------------------------
        self.lista_notas = arcade.SpriteList()
        self.notas_restantes = self.notas.data
        
        # ------------------------------------------
        # REQUISITOS DE PONTUAÇÃO E PLACAR
        # ------------------------------------------
        self.pontuação = 0
        self.combo = 0
        self.max_combo = 0
        self.resultado = ''
        self.tempo = 0
        
        # ------------------------------------------
        # INDICADORES DE PRECISÃO
        # ------------------------------------------
        self.notas_processadas = 0
        self.notas_acertadas = 0
        self.precisao = 100.00
        
        self.cont_perfeito = 0
        self.cont_bom = 0
        self.cont_falha = 0
        
        # ------------------------------------------
        # TEMPORIZADORES DE INÍCIO E FIM
        # ------------------------------------------
        self.cooldown_inicial = 2.0
        self.musica_iniciada = False
        self.indice = 0
        self.arduino = None
        self.tempo_fim_partida = 0.0  # Cronômetro para controlar o delay de encerramento.
        
        # Condicional de segurança: tenta o Arduino. Se falhar, força o modo TECLADO em tempo real.
        if not configuracoes.USAR_TECLADO:
            try:
                self.arduino = serial.Serial('COM3', 115200, timeout=0)
                print("CONEXÃO: Arduino Uno conectado com sucesso.")
            except Exception as e:
                configuracoes.USAR_TECLADO = True
                print(f"AVISO: Arduino não encontrado. Chaveando para modo TECLADO automaticamente: {e}")
        
        # ------------------------------------------
        # GEOMETRIA E POSICIONAMENTO DA PISTA
        # ------------------------------------------
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
        
        self.tempo_spawn = ((self.altura_real - configuracoes.Y_RECEPTOR) / configuracoes.velocidade_queda)
        
        # ------------------------------------------
        # RELATÓRIOS VISUAIS EM TEXTO
        # ------------------------------------------
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
    
        # ------------------------------------------
        # CONSTRUÇÃO DOS RECEPTORES FIXOS
        # ------------------------------------------
        self.receptores = arcade.SpriteList()
        for i, x in enumerate(self.colunas_gigantes):
            receptor = arcade.Sprite(self.skin.texturas_receptor[i])
            receptor.center_x = x
            receptor.center_y = configuracoes.Y_RECEPTOR
            receptor.width = 130
            receptor.height = 130
            self.receptores.append(receptor)
    # ==========================================
    # ATUALIZAÇÃO LÓGICA
    # ==========================================
    # Método automático do Arcade que processa os cálculos lógicos e atualizações do jogo a cada quadro.
    def on_update(self, delta_time):
        # Condicional que decrementa o contador de preparação da partida.
        if self.cooldown_inicial > 0:
            self.cooldown_inicial -= delta_time
            return
            
        # Condicional executada uma vez quando o jogo sai do estado de cooldown inicial.
        if not self.musica_iniciada:
            self.música.play()
            self.musica_iniciada = True
            # Condicional que limpa dados acumulados na porta USB do controle físico.
            if self.arduino:
                self.arduino.reset_input_buffer()
            return
        
        # Condicional que gerencia a entrada de dados do controle Arduino externo se ativo.
        if not configuracoes.USAR_TECLADO and self.arduino and self.arduino.in_waiting > 0:
            try:
                # Laço que esvazia as mensagens recebidas na fila do buffer USB.
                while self.arduino.in_waiting > 0:
                    sinal = self.arduino.readline().decode('utf-8', errors='ignore').strip().lower()
                    
                    # Associa caracteres vindos do microcontrolador às constantes de teclado do Arcade.
                    mapa_teclas = {
                        "d": arcade.key.D, "0": arcade.key.D,
                        "f": arcade.key.F, "1": arcade.key.F,
                        "j": arcade.key.J, "2": arcade.key.J,
                        "k": arcade.key.K, "3": arcade.key.K
                    }
                    
                    # Condicional que verifica se a string recebida coincide com os botões mapeados.
                    if sinal in mapa_teclas:
                        print(f"Tecla detectada: {sinal.upper()}")
                        tecla_pressionada = mapa_teclas[sinal]
                        self.on_key_press(tecla_pressionada, None)
                        arcade.schedule(lambda dt, k=tecla_pressionada: self.on_key_release(k, None), 0.08)
            except Exception as e:
                print(f"Erro ao ler serial: {e}")
        
        # Sincroniza o cronômetro interno acumulando o tempo passado.
        self.tempo += delta_time
        
        # Atualiza os dados exibidos nos textos informativos da tela.
        self.pontuação_display.text = f'PONTOS: {self.pontuação}'
        self.combo_display.text = f'COMBO: {self.combo}'
        self.precisao_display.text = f'PRECISÃO:\n{self.precisao:.2f}%'
        self.resultado_display.text = self.resultado
        
        # ------------------------------------------
        # GERAÇÃO DE NOVAS NOTAS (SPAWN)
        # ------------------------------------------
        # Laço corrigido adicionando [0] para comparar o float do tempo com o float da tupla.
        while (self.indice < len(self.notas_restantes) and self.tempo >= self.notas_restantes[self.indice][0]):
            tempo_nota, coluna = self.notas_restantes[self.indice]
            
            # Instancia a nota delegando as texturas lidas do gerenciador de skin do jogo.
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

        
        # ------------------------------------------
        # MOVIMENTAÇÃO E DECAIMENTO DAS NOTAS
        # ------------------------------------------
        # Laço de repetição que move e verifica a situação de todas as notas que estão descendo.
        for nota in self.lista_notas:
            # Invoca a descida física automatizada utilizando a velocidade de queda do arquivo de configurações.
            nota.atualizar(delta_time)
            
            # Condicional que checa se a nota ultrapassou o receptor sem clique.
            if nota.center_y < (configuracoes.Y_RECEPTOR - 150) and not hasattr(nota, 'computou_miss'):
                self.combo = 0
                self.resultado = 'FALHA'
                self.resultado_display.color = arcade.color.RED
                nota.computou_miss = True
                
                self.cont_falha += 1
                self.notas_processadas += 1
                # Condicional interna de segurança contra divisão por zero no cálculo da precisão.
                if self.notas_processadas > 0:
                    self.precisao = (self.notas_acertadas / self.notas_processadas) * 100
            
            # Condicional que detecta se o sprite saiu totalmente da base inferior da janela.
            if nota.center_y <= -50: 
                nota.remove_from_sprite_lists()
        
        # ------------------------------------------
        # CONCLUSÃO DA PARTIDA (COM DELAY DE 2s)
        # ------------------------------------------
        # Condicional que verifica se todas as notas acabaram e saíram da tela de gameplay.
        if self.indice >= len(self.notas_restantes) and len(self.lista_notas) == 0:
            
            # Acumula as frações de segundo para criar a janela de espera de dois segundos.
            self.tempo_fim_partida += delta_time
            
            # Condicional executada apenas quando o tempo de delay estipulado é atingido.
            if self.tempo_fim_partida >= 2.0:
                self.música.stop()
                
                # Condicional que encerra de forma limpa a conexão do hardware.
                if self.arduino:
                    self.arduino.close()
                
                # Transiciona direcionando o jogador para os relatórios de resultados sem salvar nada ainda.
                self.window.show_view(
                    TelaResultados(
                        self.fase.nome,
                        self.fase.dificuldade_atual,
                        self.pontuação,
                        self.max_combo,
                        self.precisao,
                        self.cont_perfeito,
                        self.cont_bom,
                        self.cont_falha
                    )
                )
    # ==========================================
    # RENDERIZAÇÃO GRÁFICA
    # ==========================================
    # Método automático do Arcade executado a cada quadro para renderizar os elementos visuais.
    def on_draw(self):
        self.clear()
        
        # Calcula as delimitações laterais para centralizar a área da pista de dança.
        esquerda_pista = self.centro_da_tela - (self.largura_total_pista / 2)
        direita_pista = self.centro_da_tela + (self.largura_total_pista / 2)
        
        # Desenha o retângulo de fundo cinza escuro para delimitar a pista.
        arcade.draw_lrbt_rectangle_filled(esquerda_pista, direita_pista, 0, self.altura_real, (24, 22, 33))
        
        # Laço que percorre os eixos horizontais para desenhos das linhas verticais divisórias.
        for x in self.colunas_gigantes:
            arcade.draw_line(x, 0, x, self.altura_real, (38, 35, 53), 3)
        
        # Renderiza os coletores fixos, as notas móveis e as interfaces textuais na janela.
        self.receptores.draw()
        self.lista_notas.draw()
        self.pontuação_display.draw()
        self.combo_display.draw()
        self.precisao_display.draw()
        self.resultado_display.draw()


    # ==========================================
    # TRATAMENTO DE INPUTS (PRESSIONAR)
    # ==========================================
    # Método automático do Arcade invocado sempre que o jogador pressiona qualquer tecla do dispositivo.
    def on_key_press(self, key, modifiers):
        # Condicional que checa se a tecla acionada foi a tecla ESCAPE (ESC) para sair do jogo.
        if key == arcade.key.ESCAPE:
            self.música.stop()
            if self.arduino:
                self.arduino.close()
                
            # Importação local para evitar importações circulares no motor de visualização.
            from telas.menu_fases import MenuFases
            
            # ALTERADO: Força o jogo a voltar sempre para a tela de seleção de fases, passando o menu inicial como retorno.
            from telas.menu_principal import MenuPrincipal
            self.window.show_view(MenuFases(MenuPrincipal()))
            return True
        
        # Condicional que barra entradas paralelas caso o teclado esteja configurado para ignorar.
        if not configuracoes.USAR_TECLADO:
            return True
        
        # Condicional que valida se a tecla pressionada faz parte dos botões ativos de jogo.
        if key not in configuracoes.TECLAS_COLUNAS:
            return True
        
        coluna = configuracoes.TECLAS_COLUNAS[key]
        self.receptores[coluna].texture = self.skin.texturas_receptor_clicado[coluna]
        self.receptores[coluna].width = 130
        self.receptores[coluna].height = 130
        
        # Varre a pista coletando apenas as notas que pertencem a essa coluna.
        notas_coluna = [n for n in self.lista_notas if n.coluna == coluna]
        if not notas_coluna:
            return True
        
        # Seleciona da trilha a nota que está fisicamente mais próxima da linha de acerto.
        nota = min(notas_coluna, key=lambda n: abs(n.center_y - configuracoes.Y_RECEPTOR))
        distancia = abs(nota.center_y - configuracoes.Y_RECEPTOR)
        
        # Condicional que valida se o jogador acionou o comando dentro da margem de acerto tolerada.
        if distancia <= 150:
            nota.remove_from_sprite_lists()
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            
            self.notas_processadas += 1
            self.notas_acertadas += 1
            if self.notas_processadas > 0:
                self.precisao = (self.notas_acertadas / self.notas_processadas) * 100
            
            # Condicional que verifica se a nota estava perfeitamente alinhada ao receptor.
            if distancia <= 75:
                self.pontuação += 300
                self.resultado = 'PERFEITO'
                self.resultado_display.color = arcade.color.LIGHT_GREEN
                self.cont_perfeito += 1
            # Caso a nota tenha sido acertada dentro do limite periférico externo do receptor.
            else:
                self.pontuação += 100
                self.resultado = 'BOM'
                self.resultado_display.color = arcade.color.LIGHT_BLUE
                self.cont_bom += 1
        
        return True


    # ==========================================
    # TRATAMENTO DE INPUTS (SOLTAR)
    # ==========================================
    # Método automático do Arcade invocado sempre que o jogador solta qualquer tecla ativa.
    def on_key_release(self, key, modifiers):
        # Condicional que checa se o botão liberado pertence ao mapeamento de colunas do jogo.
        if key in configuracoes.TECLAS_COLUNAS:
            coluna = configuracoes.TECLAS_COLUNAS[key]
            self.receptores[coluna].texture = self.skin.texturas_receptor[coluna]
            self.receptores[coluna].width = 130
            self.receptores[coluna].height = 130
