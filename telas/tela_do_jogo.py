
import arcade  # Importa a biblioteca gráfica Arcade para o jogo de ritmo
import serial  # Importa a biblioteca serial para comunicação com hardware (Arduino)

from configuracoes import *  # Importa todas as constantes globais do jogo
from entidades.nota import Nota  # Importa a classe que representa cada nota musical
from telas.resultados import TelaResultados  # Importa a tela final que exibe os resultados
from sistemas.gerenciador_skin import GerenciadorSkin  # Importa o sistema que carrega os elements visuais
from sistemas.gerenciador_notas import GerenciadorNotas  # Importa o leitor do mapa de notas musicais
from sistemas.gerenciador_música import GerenciadorMúsica  # Importa o controlador do áudio da fase

USAR_TECLADO = True  # Define se os comandos do jogo virão pelo teclado por padrão

# Classe que gerencia a tela principal de jogabilidade da partida
class TelaGameplay(arcade.View):
    
    # Método construtor que inicializa a tela de jogabilidade com a fase selecionada
    def __init__(self, view_anterior, fase):
        super().__init__()  # Inicializa a classe base view do Arcade
        self.view_anterior = view_anterior  # Guarda a referência do menu anterior para retorno
        self.fase = fase  # Guarda as informações da fase que será jogada
        
        pasta_skin_atual = Path('skins') / skin_atual  # Monta o caminho dinâmico com a skin selecionada
        self.notas  = GerenciadorNotas(self.fase.notas)  # Instancia o gerenciador com o arquivo de notas da fase
        self.skin   = GerenciadorSkin(pasta_skin_atual)  # Instancia o carregador de texturas com a pasta da skin
        self.música = GerenciadorMúsica(self.fase.música)  # Instancia o reprodutor musical com o áudio da fase
        
        self.lista_notas = arcade.SpriteList()  # Cria a lista controladora de sprites para as notas em movimento
        self.notas_restantes = self.notas.data  # Extrai a lista ordenada com os tempos e colunas das notas
        
        self.pontuação = 0  # Inicializa os pontos do jogador zerados
        self.combo = 0  # Inicializa o combo atual de notas consecutivas zerado
        self.max_combo = 0  # Inicializa o registro de maior combo atingido na partida zerado
        self.resultado = ''  # Inicializa o texto de feedback de acerto vazio
        self.tempo = 0  # Inicializa o cronômetro interno do gameplay zerado
        
        self.notas_processadas = 0  # Conta quantas notas passaram do receptor ou foram clicadas
        self.notas_acertadas = 0  # Conta quantas notas o jogador conseguiu acertar
        self.precisao = 100.00  # Inicializa o indicador de precisão em cem por cento
        
        self.cont_perfeito = 0  # Conta a quantidade de acertos no tempo perfeito
        self.cont_bom = 0  # Conta a quantidade de acertos no tempo aceitável
        self.cont_falha = 0  # Conta a quantidade de notas perdidas ou erradas
        
        self.cooldown_inicial = 2.0  # Temporizador de espera em segundos antes da música iniciar
        self.musica_iniciada = False  # Controle booleano para garantir que a música inicie uma única vez
        self.indice = 0  # Ponteiro seletor para acompanhar a leitura da lista de notas restantes
        self.arduino = None  # Inicializa a variável do dispositivo de hardware como nula
        
        # Condicional que tenta estabelecer comunicação USB caso o teclado esteja desligado
        if not USAR_TECLADO:
            # Estrutura de tratamento para evitar travamento do jogo se o dispositivo falhar
            try:
                self.arduino = serial.Serial('COM6', 115200, timeout=0)  # Abre a porta COM3 na frequência configurada
                print("CONEXÃO: Arduino Uno conectado com sucesso")  # Exibe aviso de sucesso no console
            # Bloco capturador executado se o hardware não estiver conectado na porta
            except Exception as e:
                print(f"AVISO: Arduino não encontrado: {e}")  # Exibe o erro de hardware sem interromper o jogo
        
        self.largura_real = self.window.width  # Armazena a largura atual da janela do jogo
        self.altura_real = self.window.height  # Armazena a altura atual da janela do jogo
        
        self.largura_total_pista = 800  # Define a dimensão horizontal total do fundo da pista de notas
        self.centro_da_tela = self.largura_real / 2  # Calcula a metade horizontal da área visível da tela
        
        self.colunas_gigantes = [
            self.centro_da_tela - 300,
            self.centro_da_tela - 100,
            self.centro_da_tela + 100,
            self.centro_da_tela + 300
        ]  # Mapeia a posição X fixa das quatro faixas de queda centralizadas na tela
        
        self.tempo_spawn = ((self.altura_real - Y_RECEPTOR) / VELOCIDADE_QUEDA)  # Calcula a antecipação necessária para instanciar a nota
        
        self.pontuação_display = arcade.Text(
            f'PONTOS: {self.pontuação}',
            50, self.altura_real - 80,
            arcade.color.WHITE, 38, bold=True
        )  # Instancia o elemento gráfico de texto para exibir os pontos no canto superior esquerdo
        
        self.precisao_display = arcade.Text(
            f'PRECISÃO:\n{self.precisao:.2f}%',
            50, self.altura_real - 220,
            arcade.color.YELLOW, 38, anchor_x='left', multiline=True, width=400, bold=True
        )  # Instancia o elemento gráfico formatado para exibir a taxa de precisão abaixo dos pontos
        
        self.combo_display = arcade.Text(
            f'COMBO: {self.combo}',
            self.centro_da_tela, (self.altura_real / 2) - 60,
            arcade.color.WHITE, 38, anchor_x='center', bold=True
        )  # Instancia o texto centralizado para exibir o combo atual no meio da pista
        
        self.resultado_display = arcade.Text(
            self.resultado,
            self.centro_da_tela, (self.altura_real / 2) + 20,
            arcade.color.WHITE, 32, anchor_x='center', bold=True
        )  # Instancia o indicador de acertos que flutua acima do texto de combo
    
        self.receptores = arcade.SpriteList()  # Inicializa a lista de elementos visuais para os botões receptores fixos
        # Laço para gerar individualmente cada um dos quatro receptores nas posições horizontais correspondentes
        for i, x in enumerate(self.colunas_gigantes):
            receptor = arcade.Sprite(self.skin.texturas_receptor[i])  # Cria o objeto de sprite carregando a imagem neutra da skin
            receptor.center_x = x  # Aplica a coordenada horizontal da coluna atual no receptor
            receptor.center_y = Y_RECEPTOR  # Posiciona o receptor verticalmente na linha de acerto definida globalmente
            receptor.width = 130  # Ajusta a largura padrão do receptor para cento e trinta pixels
            receptor.height = 130  # Ajusta a altura padrão do receptor para cento e trinta pixels
            self.receptores.append(receptor)  # Armazena o sprite construído dentro da lista coletora de receptores
        
    # Método automático do Arcade que processa os cálculos lógicos e atualizações do jogo a cada quadro
    def on_update(self, delta_time):
        # Condicional que decrementa o contador de preparação da partida
        if self.cooldown_inicial > 0:
            self.cooldown_inicial -= delta_time  # Subtrai o tempo decorrido do cronômetro de início
            return  # Interrompe o método prematuramente para paralisar o jogo até zerar a espera
            
        # Condicional executada uma vez quando o jogo sai do estado de cooldown inicial
        if not self.musica_iniciada:
            self.música.play()  # Ativa o reprodutor de áudio para tocar o som principal da fase
            self.musica_iniciada = True  # Modifica a flag para impedir que o áudio seja reiniciado no próximo loop
            # Condicional que limpa dados acumulados na porta USB do controle físico
            if self.arduino:
                self.arduino.reset_input_buffer()  # Esvazia mensagens antigas do buffer serial para evitar cliques fantasmas
            return   # Interrompe a atualização atual para sincronizar o início das ações
        
        # Condicional que gerencia a entrada de dados do controle Arduino externo se ativo
        if not USAR_TECLADO and self.arduino and self.arduino.in_waiting > 0:
            # Estrutura de prevenção para isolar erros de leitura e decodificação na transmissão serial
            try:
                # Laço que esvazia as mensagens recebidas na fila do buffer USB
                while self.arduino.in_waiting > 0:
                    sinal = self.arduino.readline().decode('utf-8', errors='ignore').strip().lower()  # Trata a mensagem serial em texto limpo
                    
                    mapa_teclas = {
                        "d": arcade.key.D, "0": arcade.key.D,
                        "f": arcade.key.F, "1": arcade.key.F,
                        "j": arcade.key.J, "2": arcade.key.J,
                        "k": arcade.key.K, "3": arcade.key.K
                    }  # Associa caracteres vindos do microcontrolador às constantes de teclado do Arcade
                    
                    # Condicional que verifica se a string recebida coincide com os botões mapeados
                    if sinal in mapa_teclas:
                        print(f"Tecla detectada: {sinal.upper()}")  # Exibe no terminal a tecla identificada no sinal
                        tecla_pressionada = mapa_teclas[sinal]  # Captura o identificador da tecla correspondente ao sinal
                        self.on_key_press(tecla_pressionada, None)  # Dispara manualmente o método de pressionamento do jogo
                        arcade.schedule(lambda dt, k=tecla_pressionada: self.on_key_release(k, None), 0.08)  # Agenda a liberação automática congelando a tecla atual
            # Captura falhas de hardware ocorridas durante o processamento de laço interno
            except Exception as e:
                print(f"Erro ao ler serial: {e}")  # Reporta a mensagem de erro da leitura física no console do programador
        
        self.tempo += delta_time  # Avança o cronômetro do jogo somando a fração de segundo atual
        
        self.pontuação_display.text = f'PONTOS: {self.pontuação}'  # Sincroniza a string visível de pontos com o valor real
        self.combo_display.text = f'COMBO: {self.combo}'  # Sincroniza a string visível de combo com o multiplicador real
        self.precisao_display.text = f'PRECISÃO:\n{self.precisao:.2f}%'  # Sincroniza o painel visível de precisão formatando as decimais
        self.resultado_display.text = self.resultado  # Sincroniza o feedback visual com o texto de classificação atualizado
        
        # Laço que gera novas notas enquanto o tempo da música alcançar o instante do arquivo de notas
        while (self.indice < len(self.notas_restantes) and 
                self.tempo + (self.tempo_spawn /2) >= self.notas_restantes[self.indice][0]):
            
            tempo_nota, coluna = self.notas_restantes[self.indice]  # Desempacota o instante e a pista em que a nota deve surgir
            
            # Instancia um novo objeto Nota definindo sua coluna inicial e posição de surgimento
            nova_nota = Nota(
                coluna,
                self.altura_real + 50,
                self.skin.texturas_notas[coluna],
                self.skin.largura_nota,
                self.skin.altura_nota
            )
            nova_nota.center_x = self.colunas_gigantes[coluna]  # Posiciona a nova nota na coordenada horizontal correta de sua trilha
            nova_nota.width = 130  # Define a largura visual da nota em movimento para cento e trinta pixels
            nova_nota.height = 130  # Define a altura visual da nota em movimento para cento e trinta pixels
            
            self.lista_notas.append(nova_nota)  # Insere o elemento instanciado na lista ativa para começar a renderização e movimento
            self.indice += 1  # Move o ponteiro para analisar a próxima linha sequencial do mapa de notas
        
        # Laço de repetição que move e verifica a situação de todas as notas que estão descendo na tela
        for nota in self.lista_notas:
            nota.center_y -= (VELOCIDADE_QUEDA * delta_time)  # Subtrai a coordenada Y proporcionalmente à velocidade para criar a queda
            
            # Condicional que checa se a nota ultrapassou o receptor sem clique e ainda não registrou falha
            if nota.center_y < (Y_RECEPTOR - 150) and not hasattr(nota, 'computou_miss'):
                self.combo = 0  # Reseta o multiplicador de combo atual do jogador
                self.resultado = 'MISS'  # Define a string de feedback visual da tela para indicar erro
                self.resultado_display.color = arcade.color.RED  # Altera a cor do texto flutuante para vermelho
                nota.computou_miss = True  # Marca o sprite para que ele não compute múltiplas falhas no mesmo loop
                
                self.cont_falha += 1  # Incrementa a contagem de erros no painel de estatísticas finais
                self.notas_processadas += 1  # Incrementa o totalizador de notas registradas na avaliação geral
                # Condicional interna de segurança contra divisão por zero no cálculo da precisão
                if self.notas_processadas > 0:
                    self.precisao = (self.notas_acertadas / self.notas_processadas) * 100  # Atualiza a porcentagem de precisão geral do jogador
            
            # Condicional que detecta se o sprite saiu totalmente da base inferior da janela de jogo
            if nota.center_y <= -50: 
                nota.remove_from_sprite_lists()  # Exclui o sprite definitivamente do jogo para liberar memória RAM
        
        # Condicional que verifica se todas as notas do arquivo acabaram e não há mais nenhuma caindo na tela
        if self.indice >= len(self.notas_restantes) and len(self.lista_notas) == 0:
            self.música.stop()  # Desliga o reprodutor de áudio para finalizar a trilha sonora
            # Condicional que encerra a conexão do hardware físico
            if self.arduino:
                self.arduino.close()  # Fecha o canal de transmissão USB com o Arduino de forma limpa
            # Transiciona a janela gráfica do jogo direcionando o jogador para o relatório final
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
    
    # Método automático do Arcade executado a cada quadro para renderizar os elementos visuais
    def on_draw(self):
        self.clear()  # Limpa o quadro anterior para evitar duplicações ou rastros visuais na janela
        
        esquerda_pista = self.centro_da_tela - (self.largura_total_pista / 2)  # Calcula a coordenada X da borda esquerda da pista de dança
        direita_pista = self.centro_da_tela + (self.largura_total_pista / 2)  # Calcula a coordenada X da borda direita da pista de dança
        
        arcade.draw_lrbt_rectangle_filled(
            esquerda_pista, direita_pista,
            0, self.altura_real, (24, 22, 33)
        )  # Desenha o retângulo de fundo cinza escuro para delimitar a área da pista de notas
        
        # Laço que percorre os eixos horizontais para desenhar as linhas verticais divisórias
        for x in self.colunas_gigantes:
            arcade.draw_line(x, 0, x, self.altura_real, (38, 35, 53), 3)  # Renderiza as linhas das colunas separadoras da pista
        
        self.receptores.draw()  # Renderiza na tela os quatro botões receptores de notas fixas
        self.lista_notas.draw()  # Renderiza na tela todas as notas musicais que estão em movimento ativo
        self.pontuação_display.draw()  # Renderiza o elemento de texto que exibe o placar de pontos atual do jogador
        self.combo_display.draw()  # Renderiza o elemento de texto do contador de combos no centro do jogo
        self.precisao_display.draw()  # Renderiza o painel textual que mostra a porcentagem de precisão calculada
        self.resultado_display.draw()  # Renderiza o texto flutuante com a classificação do último acerto obtido
    
    # Método automático do Arcade invocado sempre que o jogador pressiona qualquer tecla do dispositivo
    def on_key_press(self, key, modifiers):
        # Condicional que checa se a tecla acionada foi a tecla ESCAPE (ESC) para sair do jogo
        if key == arcade.key.ESCAPE:
            self.música.stop()  # Para a reprodução da música da fase de forma imediata
            # Condicional que verifica se a porta serial de hardware externo está ligada
            if self.arduino:
                self.arduino.close()  # Fecha a conexão serial de dados com o circuito externo do Arduino
            self.window.show_view(self.view_anterior)  # Altera a visualização atual para redirecionar o usuário à tela anterior
            return True  # Retorna verdadeiro para encerrar o tratamento do evento de clique atual
        
        # Condicional que barra entradas paralelas caso o teclado esteja configurado para ignorar
        if not USAR_TECLADO and modifiers is not None:
            return True  # Retorna verdadeiro para ignorar o input do teclado do computador
        
        # Condicional que valida se a tecla pressionada faz parte dos botões ativos de jogo
        if key not in TECLAS_COLUNAS:
            return True  # Interrompe a execução caso o botão não corresponda a nenhuma coluna mapeada
        
        coluna = TECLAS_COLUNAS[key]  # Busca no dicionário global o índice numérico da coluna ativada
        self.receptores[coluna].texture = self.skin.texturas_receptor_clicado[coluna]  # Transiciona a textura do botão para o estado visual de clicado
        self.receptores[coluna].width = 130  # Mantém fixo o tamanho de largura em pixels após a troca de imagem
        self.receptores[coluna].height = 130  # Mantém fixo o tamanho de altura em pixels após a troca de imagem
        
        notas_coluna = [n for n in self.lista_notas if n.coluna == coluna]  # Varre a pista coletando apenas as notas que pertencem a essa coluna
        # Condicional que verifica se a pista de notas desta coluna está totalmente vazia
        if not notas_coluna:
            return True  # Encerra o processamento por não haver notas para interceptar ou pontuar
        
        nota = min(notas_coluna, key=lambda n: abs(n.center_y - Y_RECEPTOR))  # Seleciona da trilha a nota que está fisicamente mais próxima da linha de acerto
        distancia = abs(nota.center_y - Y_RECEPTOR)  # Calcula a distância absoluta em pixels entre os centros da nota e do receptor
        
        # Condicional que valida se o jogador acionou o comando dentro da margem de acerto tolerada
        if distancia <= 150:
            nota.remove_from_sprite_lists()  # Deleta o sprite da nota das listas do jogo para fazê-la desaparecer
            self.combo += 1  # Incrementa o multiplicador de acertos seguidos do usuário
            self.max_combo = max(self.max_combo, self.combo)  # Compara e grava se este foi o maior combo atingido na partida
            
            self.notas_processadas += 1  # Adiciona uma nota à contagem de elementos respondidos no gameplay
            self.notas_acertadas += 1  # Adiciona uma nota à contagem de acertos válidos computados
            # Condicional de controle matemático para blindar a equação contra divisão por zero
            if self.notas_processadas > 0:
                self.precisao = (self.notas_acertadas / self.notas_processadas) * 100  # Recalcula a taxa de acertos em formato percentual
            
            # Condicional que verifica se a nota estava perfeitamente alinhada ao receptor
            if distancia <= 75:
                self.pontuação += 300  # Concede a pontuação máxima de trezentos pontos pelo tempo exato
                self.resultado = 'MARVELOUS'  # Modifica a string de feedback para indicar uma classificação perfeita
                self.resultado_display.color = arcade.color.LIGHT_GREEN  # Configura a cor do indicador em verde claro
                self.cont_perfeito += 1  # Incrementa a contagem de notas excelentes nas estatísticas
            # Caso a nota tenha sido acertada dentro do limite periférico externo do receptor
            else:
                self.pontuação += 100  # Concede a pontuação reduzida de cem pontos pelo acerto bom
                self.resultado = 'GREAT'  # Modifica a string de feedback para indicar uma classificação mediana
                self.resultado_display.color = arcade.color.LIGHT_BLUE  # Configura a cor do indicador em azul claro
                self.cont_bom += 1  # Incrementa a contagem de notas boas nas estatísticas
        
        return True  # Retorna verdadeiro para informar ao sistema que o evento de teclado foi resolvido
                
    # Método automático do Arcade invocado sempre que o jogador solta qualquer tecla ativa
    def on_key_release(self, key, modifiers):
        # Condicional que checa se o botão liberado pertence ao mapeamento de colunas do jogo
        if key in TECLAS_COLUNAS:
            coluna = TECLAS_COLUNAS[key]  # Descobre o índice correspondente à faixa de notas do botão liberado
            self.receptores[coluna].texture = self.skin.texturas_receptor[coluna]  # Restaura a textura do botão para a imagem de estado neutro
            self.receptores[coluna].width = 130  # Restabelece a largura original estável do receptor em pixels
            self.receptores[coluna].height = 130  # Restabelece a altura original estável do receptor em pixels
