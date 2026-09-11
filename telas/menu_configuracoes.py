import arcade  # Importa a biblioteca gráfica Arcade para o jogo de ritmo
from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos

from configuracoes import *  # Importa todas as variáveis de tamanho de tela e áudio do jogo

# ==========================================
# CONFIGURAÇÕES
# ==========================================
# Classe que gerencia e renderiza a tela onde o usuário altera opções do jogo
class TelaConfiguracoes(arcade.View):

    # Método construtor que inicializa a tela de configurações recebendo a referência da tela anterior
    def __init__(self, view_anterior):
        super().__init__()  # Chama o inicializador da classe base arcade.View
        
        self.view_anterior = view_anterior  # Armazena a janela que chamou as configurações para poder retornar
        
        self.opcoes = [
            'SKIN ATUAL',
            'VELOCIDADE',
            'VOLUME'
        ]  # Lista com as opções que o jogador pode selecionar e alterar
        self.indice_vertical = 0  # Controla qual opção está selecionada (Cima/Baixo)

        self.skins = []  # Inicializa uma lista vazia para armazenar os nomes visuais disponíveis
        caminho_skins = Path("skins")  # Define o caminho para a pasta que contém os pacotes estéticos
        
        # Condicional que valida se a pasta de skins realmente existe no sistema
        if caminho_skins.is_dir():
            # Laço que percorre de forma ordenada todos os arquivos e pastas do diretório skins
            for pasta in sorted(caminho_skins.iterdir()):
                # Condicional que assegura que apenas subdiretórios sejam considerados skins
                if pasta.is_dir():
                    self.skins.append(pasta.name)  # Adiciona o nome da pasta à lista de skins disponíveis
        
        # Condicional que adiciona uma skin padrão de segurança caso nenhuma pasta seja encontrada
        if not self.skins:
            self.skins.append("padrao")  # Adiciona o identificador fallback "padrao" à lista

        global skin_atual  # Informa ao interpretador que o código utilizará a variável externa global skin_atual
        
        # Condicional que verifica se a skin ativa globalmente existe no mapeamento de pastas escaneadas
        if skin_atual in self.skins:
            self.indice_skin = self.skins.index(skin_atual)  # Descobre o índice correspondente da skin ativa na lista
            
        # Caso a skin global ativa não esteja mapeada nas pastas existentes
        else:
            self.indice_skin = 0  # Reseta o ponteiro seletor para a primeira skin encontrada

    # Método automático do Arcade executado a cada quadro para desenhar os elementos na tela
    def on_draw(self):

        self.clear()  # Limpa os elementos gráficos do quadro anterior antes de redesenhar

        arcade.set_background_color((20, 10, 40))  # Mantém o fundo roxo padrão (20, 10, 40) de todas as telas do seu jogo

        largura_real = self.window.width  # Captura a largura atual da janela gráfica do jogo
        altura_real = self.window.height  # Captura a altura atual da janela gráfica do jogo
        centro_x = largura_real / 2  # Calcula a coordenada X correspondente ao centro exato da tela

        arcade.draw_text(
            'CONFIGURAÇÕES',
            centro_x,
            altura_real * 0.82,
            arcade.color.CYAN,
            65,
            anchor_x='center',
            bold=True
        )  # TÍTULO CENTRALIZADO (Fonte 65)

        global VELOCIDADE_QUEDA, VOLUME, skin_atual  # Puxa o escopo das variáveis globais para renderizar seus valores reais
        
        # Laço de repetição que varre as opções disponíveis para desenhá-las linha por linha
        for i, opcao in enumerate(self.opcoes):
            selecionado = (i == self.indice_vertical)  # Define se a linha atual está selecionada pelo jogador para mudar a cor
            cor_texto = arcade.color.WHITE if selecionado else arcade.color.GRAY  # Define texto branco para o ativo e cinza para inativo
            cor_valor = arcade.color.YELLOW if selecionado else arcade.color.GRAY  # Define valor amarelo para o ativo e cinza para inativo
            
            y_pos = (altura_real * 0.58) - (i * 110)  # Calcula o espaçamento vertical entre as linhas de menu
            
            arcade.draw_text(
                opcao,
                centro_x - 180,
                y_pos,
                cor_texto,
                32,
                anchor_x='right',
                bold=True
            )  # Desenha o nome da variável na esquerda
            
            valor_texto = ""  # Inicializa uma string vazia para construir a exibição gráfica do valor
            
            # Condicional que monta a formatação da linha caso seja a seleção de skin
            if opcao == 'SKIN ATUAL':
                valor_texto = f"<  {self.skins[self.indice_skin].upper()}  >"  # Formata o nome em maiúsculas com setas laterais
                
            # Condicional que monta a formatação da linha caso seja o ajuste de velocidade
            elif opcao == 'VELOCIDADE':
                valor_texto = f"<  {VELOCIDADE_QUEDA}  >"  # Adiciona setas visuais ao redor do valor bruto de pixels por segundo
                
            # Condicional que monta a formatação da linha caso seja o controle do áudio
            elif opcao == 'VOLUME':
                valor_texto = f"<  {int(VOLUME * 100)}%  >"  # Transforma o float decimal em uma porcentagem inteira legível de 0 a 100
                
            arcade.draw_text(
                valor_texto,
                centro_x + 80,
                y_pos,
                cor_valor,
                32,
                anchor_x='left',
                bold=True
            )  # Descobre o valor em tempo real de cada variável global para desenhar na direita

        arcade.draw_text(
            'USE AS SETAS PARA NAVEGAR E ALTERAR  |  ESC PARA VOLTAR',
            centro_x,
            altura_real * 0.15,
            arcade.color.GRAY,
            24,
            anchor_x='center',
            bold=True
        )  # INSTRUÇÃO INFERIOR COORDENADA COM A TV

    # Método automático do Arcade invocado sempre que o jogador pressiona qualquer tecla
    def on_key_press(self, key, modifiers):
        global skin_atual, VELOCIDADE_QUEDA, VOLUME  # Acessa as variáveis globais para que as teclas alterem os valores de fato

        # Navegação Vertical (Selecionar qual variável quer mexer)
        if key == arcade.key.UP:
            self.indice_vertical = (self.indice_vertical - 1) % len(self.opcoes)  # Desloca o ponteiro seletor para cima de forma circular
            
        # Condicional que verifica se a tecla pressionada foi a seta para baixo
        elif key == arcade.key.DOWN:
            self.indice_vertical = (self.indice_vertical + 1) % len(self.opcoes)  # Desloca o ponteiro seletor para baixo de forma circular

        # Navegação Horizontal (Mudar o valor da variável selecionada de forma bruta)
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            opcao_atual = self.opcoes[self.indice_vertical]  # Captura o identificador em string do que está selecionado na vertical
            direcao = 1 if key == arcade.key.RIGHT else -1  # Define valor positivo para soma na direita ou negativo para subtração na esquerda
            
            # Condicional interna que altera especificamente o ponteiro de skins do diretório
            if opcao_atual == 'SKIN ATUAL':
                self.indice_skin = (self.indice_skin + direcao) % len(self.skins)  # Aplica o deslocamento horizontal de forma circular na lista
                skin_atual = self.skins[self.indice_skin]  # Atualiza a variável global de skin
                
            # Condicional interna que altera especificamente a física de queda das notas do jogo
            elif opcao_atual == 'VELOCIDADE':
                VELOCIDADE_QUEDA = max(400, min(3000, VELOCIDADE_QUEDA + (direcao * 100)))  # Altera a velocidade de queda de 100 em 100 pixels por segundo
                
            # Condicional interna que altera a constante matemática de ganho de som do Mixer
            elif opcao_atual == 'VOLUME':
                VOLUME = max(0.0, min(1.0, VOLUME + (direcao * 0.05)))  # Altera o volume do áudio de 5% em 5%

        # Sair e voltar ao Menu Principal
        elif key == arcade.key.ESCAPE:
            from telas.menu_principal import MenuPrincipal  # Importação local interna para evitar erros de importação circular
            self.window.show_view(MenuPrincipal())  # Altera a visualização atual para redirecionar o usuário ao menu principal
