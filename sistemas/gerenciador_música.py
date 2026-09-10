import configparser  # Importa o leitor de arquivos de configuração no formato .ini

from configuracoes import *  # Importa todas as constantes globais do jogo (como o VOLUME)

from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos

import arcade  # Importa a biblioteca gráfica e de áudio Arcade para o jogo de ritmo

# Classe responsável por gerenciar a reprodução e interrupção do áudio das fases
class GerenciadorMúsica:
    
    # Método construtor que recebe o caminho do áudio e o armazena na classe
    def __init__(self, arquivo_música):
        
        self.arquivo_música = Path(arquivo_música)  # Converte o caminho recebido em um objeto Path do sistema
    
    # Método responsável por carregar o áudio na memória e iniciar a reprodução
    def play(self):
        
        self.música = arcade.load_sound(self.arquivo_música)  # Carrega o arquivo de som da fase na memória do jogo
        self.player = arcade.play_sound(self.música, volume=VOLUME)  # Inicia a reprodução do som aplicando o volume global
    
    # Método responsável por interromper imediatamente a reprodução do áudio
    def stop(self):
        arcade.stop_sound(self.player)  # Interrompe o player de áudio ativo para silenciar a música
