const int PIEZO_VERMELHO = A0; 
const int PIEZO_AMARELO  = A1; 
const int PIEZO_VERDE    = A2; 
const int PIEZO_AZUL     = A3; 

// Subido de 20 para para eliminar os disparos fantasmas por ruído
const int LIMITE_BATIDA = 90; 

const unsigned long TEMPO_TRAVA = 100; // Debounce ligeiramente maior para o sinal estabilizar

unsigned long ultimoTempoVermelho = 0;
unsigned long ultimoTempoAmarelo  = 0;
unsigned long ultimoTempoVerde    = 0;
unsigned long ultimoTempoAzul     = 0;

void setup() {
  Serial.begin(115200); 
}

// Função auxiliar para fazer dupla leitura e descartar o ruído da porta anterior
int lerPiezoLimpo(int pino) {
  analogRead(pino); // Primeira leitura descarta a carga residual da porta anterior
  delayMicroseconds(10); // Pequena pausa para o registrador ADC estabilizar
  return analogRead(pino); // Segunda leitura real e limpa
}

void loop() {
  unsigned long tempoAtual = millis();

  // 1. TAMBOR VERMELHO (A0)
  int batidaVermelho = lerPiezoLimpo(PIEZO_VERMELHO);
  if (batidaVermelho > LIMITE_BATIDA && (tempoAtual - ultimoTempoVermelho >= TEMPO_TRAVA)) {
    Serial.println("0"); 
    ultimoTempoVermelho = tempoAtual;   
  }

  // 2. TAMBOR AMARELO (A1)
  int batidaAmarelo = lerPiezoLimpo(PIEZO_AMARELO);
  if (batidaAmarelo > LIMITE_BATIDA && (tempoAtual - ultimoTempoAmarelo >= TEMPO_TRAVA)) {
    Serial.println("1"); 
    ultimoTempoAmarelo = tempoAtual;   
  }

  // 3. TAMBOR VERDE (A2)
  int batidaVerde = lerPiezoLimpo(PIEZO_VERDE);
  if (batidaVerde > LIMITE_BATIDA && (tempoAtual - ultimoTempoVerde >= TEMPO_TRAVA)) {
    Serial.println("2"); 
    ultimoTempoVerde = tempoAtual;   
  }

  // 4. TAMBOR AZUL (A3)
  int batidaAzul = lerPiezoLimpo(PIEZO_AZUL);
  if (batidaAzul > LIMITE_BATIDA && (tempoAtual - ultimoTempoAzul >= TEMPO_TRAVA)) {
    Serial.println("3"); 
    ultimoTempoAzul = tempoAtual;   
  }
}