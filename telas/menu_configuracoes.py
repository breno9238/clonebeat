import arcade
import serial

from pathlib import Path

import configuracoes


# ==========================================
# CONFIGURAÇÕES
# ==========================================

# Classe que gerencia e renderiza a tela onde o usuário altera opções do jogo.
class TelaConfiguracoes(arcade.View):

    # Método construtor que inicializa a tela de configurações recebendo a referência da tela anterior.
    def __init__(self, view_anterior):
        super().__init__()
        self.view_anterior = view_anterior  # Guarda a tela anterior para poder retornar.

        # Lista com as opções que o jogador pode selecionar e alterar.
        self.opcoes = [
            'SKIN ATUAL',
            'VELOCIDADE',
            'VOLUME',
            'CONTROLE'
        ]

        # Controla qual opção está selecionada verticalmente.
        self.indice_vertical = 0

        # Lista que armazenará os nomes das skins disponíveis.
        self.skins = []

        # Atributo que armazena a string de feedback caso ocorra falha de hardware.
        self.mensagem_erro = ""

        # Define o caminho para a pasta que contém as skins.
        caminho_skins = Path("skins")

        # Verifica se a pasta de skins realmente existe.
        if caminho_skins.is_dir():
            # Percorre todas as pastas dentro do diretório skins em ordem.
            for pasta in sorted(caminho_skins.iterdir()):
                if pasta.is_dir():
                    self.skins.append(pasta.name)

        # Caso nenhuma skin seja encontrada, cria uma opção padrão.
        if not self.skins:
            self.skins.append("padrao")

        # Verifica se a skin atualmente configurada existe na lista.
        if configuracoes.skin_atual in self.skins:
            self.indice_skin = self.skins.index(configuracoes.skin_atual)
        else:
            self.indice_skin = 0
            configuracoes.skin_atual = self.skins[0]

    # ==========================================
    # DESENHO
    # ==========================================

    # Método executado pelo Arcade para desenhar a tela.
    def on_draw(self):
        self.clear()
        arcade.set_background_color((20, 10, 40))

        # Obtém o tamanho real da janela gráfica.
        largura_real = self.window.width
        altura_real = self.window.height
        centro_x = largura_real / 2

        # ------------------------------------------
        # TÍTULO
        # ------------------------------------------
        arcade.draw_text(
            'CONFIGURAÇÕES',
            centro_x, altura_real * 0.82,
            arcade.color.CYAN, 65,
            anchor_x='center', bold=True
        )

        # ------------------------------------------
        # OPÇÕES DO MENU
        # ------------------------------------------
        for i, opcao in enumerate(self.opcoes):
            selecionado = (i == self.indice_vertical)

            cor_texto = (arcade.color.WHITE if selecionado else arcade.color.GRAY)
            cor_valor = (arcade.color.YELLOW if selecionado else arcade.color.GRAY)
            y_pos = (altura_real * 0.58) - (i * 85)

            arcade.draw_text(opcao, centro_x - 180, y_pos, cor_texto, 32, anchor_x='right', bold=True)

            valor_texto = ""

            if opcao == 'SKIN ATUAL':
                valor_texto = f"<  {self.skins[self.indice_skin].upper()}  >"

            elif opcao == 'VELOCIDADE':
                valor_texto = f"<  {configuracoes.velocidade_queda}  >"

            elif opcao == 'VOLUME':
                valor_texto = f"<  {int(configuracoes.volume * 100)}%  >"

            elif opcao == 'CONTROLE':
                valor_texto = "<  TECLADO  >" if configuracoes.USAR_TECLADO else "<  ARDUINO  >"

            arcade.draw_text(valor_texto, centro_x + 80, y_pos, cor_valor, 32, anchor_x='left', bold=True)

        # ------------------------------------------
        # MENSAGEM DE ERRO DO HARDWARE
        # ------------------------------------------
        # Condicional que renderiza o aviso visual em vermelho caso a mensagem não esteja vazia.
        if self.mensagem_erro:
            arcade.draw_text(
                self.mensagem_erro,
                centro_x, altura_real * 0.22,
                arcade.color.RED, 22,
                anchor_x='center', bold=True
            )

        # ------------------------------------------
        # INSTRUÇÕES DE NAVEGAÇÃO
        # ------------------------------------------
        arcade.draw_text(
            'USE AS SETAS PARA NAVEGAR E ALTERAR  |  ESC PARA VOLTAR',
            centro_x, altura_real * 0.15,
            arcade.color.GRAY, 24,
            anchor_x='center', bold=True
        )

    # ==========================================
    # TECLADO
    # ==========================================

    # Método executado quando o jogador pressiona uma tecla.
    def on_key_press(self, key, modifiers):
        # Seta para cima.
        if key == arcade.key.UP:
            self.indice_vertical = (self.indice_vertical - 1) % len(self.opcoes)

        # Seta para baixo.
        elif key == arcade.key.DOWN:
            self.indice_vertical = (self.indice_vertical + 1) % len(self.opcoes)

        # Modificações nas opções laterais através das setas esquerda e direita.
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            opcao_atual = self.opcoes[self.indice_vertical]
            direcao = (1 if key == arcade.key.RIGHT else -1)

            # Limpa qualquer erro antigo assim que o usuário mexe em qualquer opção.
            self.mensagem_erro = ""

            if opcao_atual == 'SKIN ATUAL':
                self.indice_skin = (self.indice_skin + direcao) % len(self.skins)
                configuracoes.skin_atual = self.skins[self.indice_skin]

            elif opcao_atual == 'VELOCIDADE':
                configuracoes.velocidade_queda = max(
                    400,
                    min(
                        3000,
                        configuracoes.velocidade_queda + (direcao * 100)
                    )
                )

            elif opcao_atual == 'VOLUME':
                configuracoes.volume = max(
                    0.0,
                    min(
                        1.0,
                        configuracoes.volume + (direcao * 0.05)
                    )
                )

            elif opcao_atual == 'CONTROLE':
                # Se o estado for Teclado, o usuário tenta ativar o Arduino.
                if configuracoes.USAR_TECLADO:
                    try:
                        # Realiza um teste físico tentando abrir a porta serial COM3.
                        teste_serial = serial.Serial('COM3', 115200, timeout=0)
                        teste_serial.close()
                        
                        # Permite a mudança caso o hardware esteja conectado.
                        configuracoes.USAR_TECLADO = False
                    except Exception:
                        # Mantém em modo teclado e injeta a string vermelha de aviso na tela.
                        configuracoes.USAR_TECLADO = True
                        self.mensagem_erro = "ERRO: O ARDUINO NÃO FOI CONECTADO!"
                else:
                    configuracoes.USAR_TECLADO = True

        # Retorna para a visualização do menu principal do jogo.
        elif key == arcade.key.ESCAPE:
            from telas.menu_principal import MenuPrincipal
            self.window.show_view(MenuPrincipal())