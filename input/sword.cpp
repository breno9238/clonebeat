void setup() {
  Serial.begin(9600); // Inicia a comunicação a 9600 bps
}

void loop() {
  int valorProcessado = 42; // Exemplo de valor
  Serial.println(valorProcessado); // Envia o valor para o PC
  delay(1000); // Espera 1 segundo para não sobrecarregar
}