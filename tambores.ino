// Definição dos pinos analógicos onde as moedinhas piezo estão ligadas
const int PIEZO_VERMELHO = A0; // Coluna 1
const int PIEZO_AMARELO  = A1; // Coluna 2
const int PIEZO_VERDE    = A2; // Coluna 3
const int PIEZO_AZUL     = A3; // Coluna 4

// Força da batida necessária para o jogo aceitar o comando (Filtro de ruído)
const int LIMITE_BATIDA = 120; // Subi ligeiramente para isolar melhor o azul

// Tempo em milissegundos de trava para evitar cliques duplos falsos
const unsigned long TEMPO_TRAVA = 80; // Aumentado para dar tempo da energia escoar pro GND

// Armazena o tempo da última batida de cada tambor de forma isolada
unsigned long ultimoTempoVermelho = 0;
unsigned long ultimoTempoAmarelo  = 0;
unsigned long ultimoTempoVerde    = 0;
unsigned long ultimoTempoAzul     = 0;

void setup() {
  // Inicializa a porta serial na velocidade configurada no seu novo gameplay.py
  Serial.begin(115200); 
}

void loop() {
  unsigned long tempoAtual = millis();

  // 1. PROCESSAMENTO DO TAMBOR VERMELHO (A0)
  int batidaVermelho = analogRead(PIEZO_VERMELHO);
  if (batidaVermelho > LIMITE_BATIDA && (tempoAtual - ultimoTempoVermelho >= TEMPO_TRAVA)) {
    Serial.println("1"); 
    ultimoTempoVermelho = tempoAtual;   
  }

  // 2. PROCESSAMENTO DO TAMBOR AMARELO (A1)
  int batidaAmarelo = analogRead(PIEZO_AMARELO);
  if (batidaAmarelo > LIMITE_BATIDA && (tempoAtual - ultimoTempoAmarelo >= TEMPO_TRAVA)) {
    Serial.println("2"); 
    ultimoTempoAmarelo = tempoAtual;   
  }

  // 3. PROCESSAMENTO DO TAMBOR VERDE (A2)
  int batidaVerde = analogRead(PIEZO_VERDE);
  if (batidaVerde > LIMITE_BATIDA && (tempoAtual - ultimoTempoVerde >= TEMPO_TRAVA)) {
    Serial.println("3"); 
    ultimoTempoVerde = tempoAtual;   
  }

  // 4. PROCESSAMENTO DO TAMBOR AZUL (A3)
  int batidaAzul = analogRead(PIEZO_AZUL);
  if (batidaAzul > LIMITE_BATIDA && (tempoAtual - ultimoTempoAzul >= TEMPO_TRAVA)) {
    Serial.println("4"); 
    ultimoTempoAzul = tempoAtual;   
  }
}
