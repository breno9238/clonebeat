import arcade  # Importa a biblioteca Arcade para desenvolvimento de jogos 2D

from configuracoes import *  # Importa constantes globais (largura, altura, título)
from telas.menu_fases import MenuFases  # Importa a tela de seleção de fases
from telas.menu_principal import MenuPrincipal  # Importa a tela do menu principal

# Função principal que configura e inicia o ciclo de vida do jogo
def main():
    janela = arcade.Window(  # Cria a janela principal do jogo
        width=LARGURA_TELA,  # Define a largura da janela com a constante
        height=ALTURA_TELA,  # Define a altura da janela com a constante
        title=TITULO_JOGO,  # Define o título da janela do jogo
        update_rate=1/144,  # Define a taxa de atualização da lógica para 144 FPS
        draw_rate=1/144,  # Define a taxa de renderização da tela para 144 FPS
        fullscreen=True  # Ativa o modo tela cheia bruto
    )
    
    janela.show_view(MenuPrincipal())  # Define o MenuPrincipal como a primeira tela ativa
    arcade.run()  # Inicia o loop do jogo, mantendo a janela aberta e ativa

# Garante que o jogo só rode se este arquivo for executado diretamente
if __name__ == '__main__':
    main()
