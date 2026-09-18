import arcade

from pathlib import Path

import configuracoes


# ==========================================
# CONFIGURAÇÕES
# ==========================================

# Classe que gerencia e renderiza a tela onde o usuário altera opções do jogo.
class TelaConfiguracoes(arcade.View):

    # Método construtor que inicializa a tela de configurações
    # recebendo a referência da tela anterior.
    def __init__(self, view_anterior):

        super().__init__()  # Inicializa a classe base arcade.View.

        self.view_anterior = view_anterior  # Guarda a tela anterior para poder retornar.

        # Lista com as opções que o jogador pode selecionar e alterar.
        self.opcoes = [
            'SKIN ATUAL',
            'VELOCIDADE',
            'VOLUME'
        ]

        # Controla qual opção está selecionada.
        self.indice_vertical = 0

        # Lista que armazenará os nomes das skins disponíveis.
        self.skins = []

        # Define o caminho para a pasta que contém as skins.
        caminho_skins = Path("skins")

        # Verifica se a pasta de skins realmente existe.
        if caminho_skins.is_dir():

            # Percorre todas as pastas dentro do diretório skins em ordem.
            for pasta in sorted(caminho_skins.iterdir()):

                # Considera somente diretórios como skins.
                if pasta.is_dir():

                    # Adiciona o nome da pasta à lista de skins.
                    self.skins.append(pasta.name)

        # Caso nenhuma skin seja encontrada, cria uma opção padrão.
        if not self.skins:
            self.skins.append("padrao")

        # Verifica se a skin atualmente configurada existe na lista.
        if configuracoes.skin_atual in self.skins:

            # Encontra o índice da skin atualmente selecionada.
            self.indice_skin = self.skins.index(
                configuracoes.skin_atual
            )

        # Caso a skin atual não exista mais.
        else:

            # Seleciona a primeira skin disponível.
            self.indice_skin = 0

            # Atualiza a configuração global para a primeira skin.
            configuracoes.skin_atual = self.skins[0]


    # ==========================================
    # DESENHO
    # ==========================================

    # Método executado pelo Arcade para desenhar a tela.
    def on_draw(self):

        # Limpa os elementos gráficos do quadro anterior.
        self.clear()

        # Define o fundo roxo padrão.
        arcade.set_background_color((20, 10, 40))

        # Obtém o tamanho real da janela.
        largura_real = self.window.width
        altura_real = self.window.height

        # Calcula o centro horizontal da tela.
        centro_x = largura_real / 2


        # ==========================================
        # TÍTULO
        # ==========================================

        arcade.draw_text(
            'CONFIGURAÇÕES',
            centro_x,
            altura_real * 0.82,
            arcade.color.CYAN,
            65,
            anchor_x='center',
            bold=True
        )


        # ==========================================
        # OPÇÕES
        # ==========================================

        # Percorre todas as opções do menu.
        for i, opcao in enumerate(self.opcoes):

            # Verifica se essa é a opção atualmente selecionada.
            selecionado = (i == self.indice_vertical)

            # Define a cor do nome da opção.
            cor_texto = (
                arcade.color.WHITE
                if selecionado
                else arcade.color.GRAY
            )

            # Define a cor do valor da opção.
            cor_valor = (
                arcade.color.YELLOW
                if selecionado
                else arcade.color.GRAY
            )

            # Calcula a posição vertical da opção.
            y_pos = (altura_real * 0.58) - (i * 110)


            # ==========================================
            # NOME DA OPÇÃO
            # ==========================================

            arcade.draw_text(
                opcao,
                centro_x - 180,
                y_pos,
                cor_texto,
                32,
                anchor_x='right',
                bold=True
            )


            # ==========================================
            # VALOR DA OPÇÃO
            # ==========================================

            valor_texto = ""


            # ------------------------------------------
            # SKIN
            # ------------------------------------------

            if opcao == 'SKIN ATUAL':

                valor_texto = (
                    f"<  {self.skins[self.indice_skin].upper()}  >"
                )


            # ------------------------------------------
            # VELOCIDADE
            # ------------------------------------------

            elif opcao == 'VELOCIDADE':

                valor_texto = (
                    f"<  {configuracoes.VELOCIDADE_QUEDA}  >"
                )


            # ------------------------------------------
            # VOLUME
            # ------------------------------------------

            elif opcao == 'VOLUME':

                valor_texto = (
                    f"<  {int(configuracoes.VOLUME * 100)}%  >"
                )


            # Desenha o valor da opção.
            arcade.draw_text(
                valor_texto,
                centro_x + 80,
                y_pos,
                cor_valor,
                32,
                anchor_x='left',
                bold=True
            )


        # ==========================================
        # INSTRUÇÕES
        # ==========================================

        arcade.draw_text(
            'USE AS SETAS PARA NAVEGAR E ALTERAR  |  ESC PARA VOLTAR',
            centro_x,
            altura_real * 0.15,
            arcade.color.GRAY,
            24,
            anchor_x='center',
            bold=True
        )


    # ==========================================
    # TECLADO
    # ==========================================

    # Método executado quando o jogador pressiona uma tecla.
    def on_key_press(self, key, modifiers):


        # ==========================================
        # NAVEGAÇÃO VERTICAL
        # ==========================================

        # Seta para cima.
        if key == arcade.key.UP:

            # Move a seleção uma posição para cima.
            self.indice_vertical = (
                self.indice_vertical - 1
            ) % len(self.opcoes)


        # Seta para baixo.
        elif key == arcade.key.DOWN:

            # Move a seleção uma posição para baixo.
            self.indice_vertical = (
                self.indice_vertical + 1
            ) % len(self.opcoes)


        # ==========================================
        # ALTERAÇÃO HORIZONTAL
        # ==========================================

        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:

            # Descobre qual opção está selecionada.
            opcao_atual = self.opcoes[self.indice_vertical]

            # Define a direção da alteração.
            #
            # RIGHT = +1
            # LEFT  = -1
            direcao = (
                1
                if key == arcade.key.RIGHT
                else -1
            )


            # ==========================================
            # SKIN
            # ==========================================

            if opcao_atual == 'SKIN ATUAL':

                # Move para a próxima ou para a skin anterior.
                self.indice_skin = (
                    self.indice_skin + direcao
                ) % len(self.skins)

                # ALTERA A VARIÁVEL REAL DO MÓDULO
                # configuracoes.py.
                configuracoes.skin_atual = (
                    self.skins[self.indice_skin]
                )


            # ==========================================
            # VELOCIDADE
            # ==========================================

            elif opcao_atual == 'VELOCIDADE':

                # Altera diretamente a variável
                # existente em configuracoes.py.
                configuracoes.VELOCIDADE_QUEDA = max(
                    400,
                    min(
                        3000,
                        configuracoes.VELOCIDADE_QUEDA
                        + (direcao * 100)
                    )
                )


            # ==========================================
            # VOLUME
            # ==========================================

            elif opcao_atual == 'VOLUME':

                # Altera diretamente a variável
                # existente em configuracoes.py.
                configuracoes.VOLUME = max(
                    0.0,
                    min(
                        1.0,
                        configuracoes.VOLUME
                        + (direcao * 0.05)
                    )
                )


        # ==========================================
        # VOLTAR
        # ==========================================

        elif key == arcade.key.ESCAPE:

            # Importação local para evitar possível
            # importação circular com o MenuPrincipal.
            from telas.menu_principal import MenuPrincipal

            # Retorna para o menu principal.
            self.window.show_view(MenuPrincipal())