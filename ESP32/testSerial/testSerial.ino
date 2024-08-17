void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Espera a que se establezca la conexión
  }
  Serial.println("Iniciando ESP32...");
}

void loop() {
  Serial.println("Loop ejecutándose...");
  delay(1000); // Espera un segundo entre mensajes
}