// Definição dos pinos analógicos onde as moedinhas piezo estão ligadas
const int PIEZO_VERMELHO = A0; // Coluna 1
const int PIEZO_AMARELO  = A1; // Coluna 2
const int PIEZO_VERDE    = A2; // Coluna 3
const int PIEZO_AZUL     = A3; // Coluna 4

// Força da batida necessária para o jogo aceitar o comando (Filtro de ruído)
const int LIMITE_BATIDA = 100; 

// Tempo em milissegundos de trava para evitar cliques duplos falsos
const int TEMPO_TRAVA = 40; 

void setup() {
  // Inicializa a porta serial em alta velocidade para garantir atraso zero (sem lag)
  Serial.begin(115200); 
}

void loop() {
  // 1. LEITURA E PROCESSAMENTO DO TAMBOR VERMELHO (Coluna 1)
  int batidaVermelho = analogRead(PIEZO_VERMELHO);
  if (batidaVermelho > LIMITE_BATIDA) {
    Serial.println("1"); // Manda o texto "1" que o seu Python vai ler e converter na Tecla D
    delay(TEMPO_TRAVA);   
  }

  // 2. LEITURA E PROCESSAMENTO DO TAMBOR AMARELO (Coluna 2)
  int batidaAmarelo = analogRead(PIEZO_AMARELO);
  if (batidaAmarelo > LIMITE_BATIDA) {
    Serial.println("2"); // Manda o texto "2" que o seu Python vai ler e converter na Tecla F
    delay(TEMPO_TRAVA);   
  }

  // 3. LEITURA E PROCESSAMENTO DO TAMBOR VERDE (Coluna 3)
  int batidaVerde = analogRead(PIEZO_VERDE);
  if (batidaVerde > LIMITE_BATIDA) {
    Serial.println("3"); // Manda o texto "3" que o seu Python vai ler e converter na Tecla J
    delay(TEMPO_TRAVA);   
  }

  // 4. LEITURA E PROCESSAMENTO DO TAMBOR AZUL (Coluna 4)
  int batidaAzul = analogRead(PIEZO_AZUL);
  if (batidaAzul > LIMITE_BATIDA) {
    Serial.println("4"); // Manda o texto "4" que o seu Python vai ler e converter na Tecla K
    delay(TEMPO_TRAVA);   
  }
}