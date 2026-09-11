import serial
import time

PORTA_SERIAL = 'COM4'  # Ajuste conforme seu sistema
BAUD_RATE = 9600

try:
    arduino = serial.Serial(port=PORTA_SERIAL, baudrate=BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Monitorando força dos Piezos na porta {PORTA_SERIAL}...\n")

    while True:
        if arduino.in_waiting > 0:
            dados_raw = arduino.readline()
            linha = dados_raw.decode('utf-8', errors='ignore').strip()

            # Processa apenas se a linha contiver o caractere ':'
            if ':' in linha:
                tecla, forca_str = linha.split(':')
                try:
                    forca = int(forca_str)
                    
                    # Normaliza a força para uma porcentagem (0 a 100%)
                    porcentagem = int((forca / 1023) * 100)
                    
                    # Exemplo de visualização gráfica simples no terminal
                    barra = "█" * (porcentagem // 5)
                    print(f"Tecla: [{tecla.upper()}] | Força (0-1023): {forca:<4} | Intensidade: {porcentagem:<3}% {barra}")
                
                except ValueError:
                    pass

except serial.SerialException:
    print(f"Erro ao abrir a porta {PORTA_SERIAL}.")
except KeyboardInterrupt:
    print("\nEncerrado.")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()