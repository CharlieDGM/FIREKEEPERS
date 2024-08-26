#include <WiFi.h>

WiFiServer server(80);  // Puerto 80 para el servidor

void setup() {
  delay(2000);
  Serial.begin(9600);
  Serial.println("");

  //Credenciales para conectarse a la red wifi
  WiFi.begin("CLARO_193EC7", "22FC83B7F3");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); //Espera a que se realice la conexion a la red.
    Serial.println("Conectando a WiFi... (Radahn, consort of Miquella)");
  }
  Serial.println("Conectado a WiFi (Malenia, blade of Miquella)");

  // Iniciar servidor
  server.begin();
  Serial.println("Servidor iniciado");
  Serial.print("Dirección IP del ESP32: ");
  Serial.println(WiFi.localIP()); //no entiendo porque no me deja concatenar esta linea con la anterior...?
}

void loop() {
  WiFiClient client = server.available();  // Esperar por un cliente

  if (client) {
    Serial.println("Cliente conectado");

    while (client.connected()) {
      if (client.available()) {
        String message = client.readStringUntil('\n');
        Serial.print("Mensaje recibido: ");
        Serial.println(message);

        // Enviar respuesta al cliente
        client.println("ESP32 recibió tu mensaje");
      }
    }

    // Cerrar la conexión
    client.stop();
    Serial.println("Cliente desconectado");
  }
}