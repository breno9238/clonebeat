import configparser

import configuracoes

import arcade

from pathlib import Path


# ==========================================
# GERENCIADOR DE MÚSICA
# ==========================================

# Classe responsável por gerenciar a reprodução e interrupção do áudio das fases.
class GerenciadorMúsica:
    
    # Método construtor que recebe o caminho do áudio e o armazena na classe.
    def __init__(self, arquivo_música):
        
        self.arquivo_música = Path(arquivo_música)  # Converte o caminho recebido em um objeto Path do sistema.
    
    # ==========================================
    # CONTROLE DE ÁUDIO
    # ==========================================

    # Método responsável por carregar o áudio na memória e iniciar a reprodução.
    def play(self):
        
        self.música = arcade.load_sound(self.arquivo_música)  # Carrega o arquivo de som da fase na memória do jogo.
        self.player = arcade.play_sound(self.música, volume=configuracoes.volume)  # Inicia a reprodução do som aplicando o volume global em tempo real.
    
    # Método responsável por interromper imediatamente a reprodução do áudio.
    def stop(self):
        
        arcade.stop_sound(self.player)  # Interrompe o player de áudio ativo para silenciar a música.
