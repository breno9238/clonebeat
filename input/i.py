import serial # Importa a biblioteca para comunicação serial
import time

# Configure a porta correta (ex: 'COM3' no Windows ou '/dev/ttyUSB0' no Linux)
# A velocidade (9600) deve ser a mesma do código C++
porta_serial = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2) # Espera a conexão estabilizar

while True:
    if porta_serial.in_waiting > 0:
        # Lê a linha enviada, decodifica de bytes para string e limpa espaços
        linha = porta_serial.readline().decode('utf-8').strip()
        print(f"Valor recebido do C++: {linha}")
