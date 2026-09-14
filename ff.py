import arcade
import serial

class RhythmGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Jogo de Ritmo - Teste de Sinais")
        arcade.set_background_color(arcade.color.BLACK)
        
        # Conecta à porta do Arduino
        try:
            self.arduino = serial.Serial('COM6', 115200, timeout=0.01)
            print("Arduino conectado na COM6 com sucesso!")
        except Exception as e:
            print(f"Erro ao abrir a porta COM6: {e}")
            self.arduino = None

    def on_update(self, delta_time):
        # Lê a porta serial se estiver disponível
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                # Lê a linha enviada pelo Arduino
                linha = self.arduino.readline().decode('utf-8', errors='ignore').strip()
                
                # Processa os sinais '1', '2', '3' ou '4'
                if linha in ['1', '2', '3', '4']:
                    print(f"Sinal recebido: Tambor {linha}")
                    self.processar_batida(int(linha))
            except Exception as e:
                print(f"Erro na leitura serial: {e}")

    def processar_batida(self, tambor):
        # Aqui entra a lógica para acertar/destruir as notas na tela
        # Exemplo: tambor 1 = coluna 1, tambor 2 = coluna 2, etc.
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_text("Bata nos piezos para testar os sinais...", 200, 300, arcade.color.WHITE, 16)

if __name__ == "__main__":
    app = RhythmGame()
    arcade.run()