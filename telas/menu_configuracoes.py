import arcade
from pathlib import Path

from regras.configuracoes import *

# ==========================================
# CONFIGURAÇÕES
# ==========================================
class TelaConfiguracoes(arcade.View):

    def __init__(self, view_anterior):
        super().__init__()
        
        self.view_anterior = view_anterior
        
        # Lista com as opções que o jogador pode selecionar e alterar
        self.opcoes = [
            'SKIN ATUAL',
            'VELOCIDADE',
            'VOLUME'
        ]
        self.indice_vertical = 0 # Controla qual opção está selecionada (Cima/Baixo)

        # Escaneia as pastas dentro do diretório 'skins' para listar as opções
        self.skins = []
        caminho_skins = Path("skins")
        if caminho_skins.is_dir():
            for pasta in sorted(caminho_skins.iterdir()):
                if pasta.is_dir():
                    self.skins.append(pasta.name)
        
        if not self.skins:
            self.skins.append("padrao")

        # Vincula o índice da lista ao valor que já estava salvo na configuração global
        global skin_atual
        if skin_atual in self.skins:
            self.indice_skin = self.skins.index(skin_atual)
        else:
            self.indice_skin = 0

    def on_draw(self):

        self.clear()

        # Mantém o fundo roxo padrão (20, 10, 40) de todas as telas do seu jogo
        arcade.set_background_color((20, 10, 40))

        largura_real = self.window.width
        altura_real = self.window.height
        centro_x = largura_real / 2

        # TÍTULO CENTRALIZADO (Fonte 65)
        arcade.draw_text(
            'CONFIGURAÇÕES',
            centro_x,
            altura_real * 0.82,
            arcade.color.CYAN,
            65,
            anchor_x='center',
            bold=True
        )

        # RENDERIZAÇÃO DAS OPÇÕES DE VARIÁVEIS DO JOGO
        global VELOCIDADE_QUEDA, VOLUME, skin_atual
        
        for i, opcao in enumerate(self.opcoes):
            # Define se a linha atual está selecionada pelo jogador para mudar a cor
            selecionado = (i == self.indice_vertical)
            cor_texto = arcade.color.WHITE if selecionado else arcade.color.GRAY
            cor_valor = arcade.color.YELLOW if selecionado else arcade.color.GRAY
            
            y_pos = (altura_real * 0.58) - (i * 110)
            
            # Desenha o nome da variável na esquerda
            arcade.draw_text(
                opcao,
                centro_x - 180,
                y_pos,
                cor_texto,
                32,
                anchor_x='right',
                bold=True
            )
            
            # Descobre o valor em tempo real de cada variável global para desenhar na direita
            valor_texto = ""
            if opcao == 'SKIN ATUAL':
                valor_texto = f"<  {self.skins[self.indice_skin].upper()}  >"
            elif opcao == 'VELOCIDADE':
                valor_texto = f"<  {VELOCIDADE_QUEDA}  >"
            elif opcao == 'VOLUME':
                valor_texto = f"<  {int(VOLUME * 100)}%  >"
                
            arcade.draw_text(
                valor_texto,
                centro_x + 80,
                y_pos,
                cor_valor,
                32,
                anchor_x='left',
                bold=True
            )

        # INSTRUÇÃO INFERIOR COORDENADA COM A TV
        arcade.draw_text(
            'USE AS SETAS PARA NAVEGAR E ALTERAR  |  ESC PARA VOLTAR',
            centro_x,
            altura_real * 0.15,
            arcade.color.GRAY,
            24,
            anchor_x='center',
            bold=True
        )

    def on_key_press(self, key, modifiers):
        global skin_atual, VELOCIDADE_QUEDA, VOLUME

        # Navegação Vertical (Selecionar qual variável quer mexer)
        if key == arcade.key.UP:
            self.indice_vertical = (self.indice_vertical - 1) % len(self.opcoes)
            
        elif key == arcade.key.DOWN:
            self.indice_vertical = (self.indice_vertical + 1) % len(self.opcoes)

        # Navegação Horizontal (Mudar o valor da variável selecionada de forma bruta)
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            opcao_atual = self.opcoes[self.indice_vertical]
            direcao = 1 if key == arcade.key.RIGHT else -1
            
            if opcao_atual == 'SKIN ATUAL':
                self.indice_skin = (self.indice_skin + direcao) % len(self.skins)
                skin_atual = self.skins[self.indice_skin] # Atualiza a variável global de skin
                
            elif opcao_atual == 'VELOCIDADE':
                # Altera a velocidade de queda de 100 em 100 pixels por segundo
                VELOCIDADE_QUEDA = max(400, min(3000, VELOCIDADE_QUEDA + (direcao * 100)))
                
            elif opcao_atual == 'VOLUME':
                # Altera o volume do áudio de 5% em 5%
                VOLUME = max(0.0, min(1.0, VOLUME + (direcao * 0.05)))

        # Sair e voltar ao Menu Principal
        elif key == arcade.key.ESCAPE:
            from telas.menu_principal import MenuPrincipal
            self.window.show_view(MenuPrincipal())
