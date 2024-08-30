//alright, empecemos a trabajar el codigo master del proyecto
//El arduino va a servir como los "musculos" del proyecto, va a realizar lecturas analógicas de los sensores,
//va a ancender las baterias(o fuentes) de los motores y va a mandar señales PWM a los controladores
//de los motores. Mandara mensajes a la Raspberry para poder operar en conjunto y realizar tareas
//especificas
#include <WiFi.h>
#include <ESP32Servo.h>
//librerias iniciales

WiFiServer server(80); //Servidor local en el puerto 80. Utilizado para conectarse con la Raspberry

int sensorPins[3] = {32,26,14}; // sensores 1, 2, 3
//arrays que contienen a donde van conectados los componentes
Servo escControl[4]; //23, 21, 18, 2 (se les coloca en esos pines en el setup)
int pulsos[4] = {50, 75, 70, 60}; //pulsos de las bombas: A, B, C, D

bool AnalogLecture(int InPin, int limit, bool inverted) {
  int aux = analogRead(InPin); 
  Serial.println("Pin Leido: " + String(InPin) + ". Lectura Obtenida: " + String(aux));
  return inverted ? aux < limit : aux > limit;
}

class Motor { //una clase que contiene funciones para encender y apagar las bombas de agua. Necesitamos controlar un relay y mandar una señal a los controladores
  private:
    int motorNumber;

  public:
  Motor(int m) {
    motorNumber = m;
  }

  void On(int pulseToSend) {
    escControl[motorNumber].write(pulseToSend); //encendemos el relay junto con el controlador del motor
    Serial.println("Motor: " + String(motorNumber+1) + ". Pulso enviado: " + String(pulseToSend));
  }

  void Off() {
    //digitalWrite(relayPins[motorNumber], LOW); A;ADIR SI SE MODIFICA LA LINEA 15
    escControl[motorNumber].write(0); //apagamos el relay junto con el controlador del motor
    //Serial.println("Motor: " + String(motorNumber+1) + " Apagado");
  }
};

Motor motors[4] = {Motor(0), Motor(1), Motor(2), Motor(3)};

void encender(int direccion) {
  switch (direccion) { //nomas anadimos esta funcion porque necesitamos una manera de activar los motores frontales con una sola iteracion de un ciclo for. Entonces agrupamos las funciones correspondientes dentro de este switch case.
    case 0:
      motors[0].On(pulsos[0]);
      break;
    case 1:
      motors[1].On(pulsos[1]);
      motors[2].On(pulsos[2]);
      break;
    case 2:
      motors[3].On(pulsos[3]);
      break;
  }
}

bool controlarMotores(int lecturaSensor) {
  int limite = 300;

  if (lecturaSensor > limite) {
    for (int n = 0; n < 4; n++) {
      motors[n].On(pulsos[n]);
    }
    return true;
  } else {
    for (int n = 0; n < 4; n++) {
      motors[n].Off();
    }
    return false;
  }
}

void setup() {
  Serial.begin(9600); 
  //iniciamos la comunicación serial de estas cosas todas horribles (conectado al 2do puerto: 16 (cable negro) rx, 17 (cable blanco) tx)

  int escControlPins[4] = {23, 21, 18, 2}; //a la izquierda del controlador (Motores A, B, C, D)
  delay(2000);
  Serial.println("");
  Serial.println("Encendiendo...");
  delay(4000);
  for (int n = 0; n < 3; n++) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes  
    Serial.println("Encendiendo el motor: " + String(n+1));
    escControl[n].attach(escControlPins[n], 1000, 2000);
    escControl[n].write(0);
    delay(3000);
  }
  escControl[2].write(0);
  Serial.println("Re-encendiendo el tercer motor...");
  delay(3000);

  for (int n = 0; n < 3; n++) {
    pinMode(sensorPins[n], INPUT);
    int lecturaInicial = analogRead(sensorPins[n]); //pero sensores solo son 3 >:/ (asi q hay que hacer otro ciclo for)
    Serial.println("Sensor iniciado: " + String(n+1) + ". Lectura inicial: " + String(lecturaInicial));
    delay(500);
  }

  WiFi.begin("CLARO_193EC7", "22FC83B7F3"); //Nos conectamos al internet con las credenciales de la red
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); //Esperamos que se realice la conexion a la red.
    Serial.println("Espera wachin, me estoy conectando al internet...");
  }
  Serial.println("Ya me conecte al internet xd");

  server.begin(); //iniciamos el servidor local
  Serial.println("Servidor iniciado");
  Serial.print("Direccion IP del servidor: ");
  Serial.println(WiFi.localIP()); //no tengo idea porque no me deja concatenar esta linea con la anterior.
  delay(2000);

  Serial.println("Esperando conexion del cliente/raspberryPi xddd...");
  while (!server.available()) {
    delay(750);
    Serial.print("."); //Esperamos a que se conecte la raspberry pi.
  }
  Serial.println("\nSe ha conectado el cliente.\n");

  Serial.println("=======================================================");
  Serial.println("Iniciando todo pipipipipi... (3.14 3.14 3.14 3.14 3.14)");
  delay(3000);
}

String mensajesRPI[3] = {"derecha", "frente", "izquierda"}; 

void loop() {
  WiFiClient cliente = server.available(); // Acepta una conexión del cliente
  
  if (cliente) { // Verifica si hay un cliente conectado
    Serial.println("Cliente conectado.");
    while (cliente.connected()) { // Mientras el cliente esté conectado
    String mensaje;
      if (cliente.available()) { // Si hay datos disponibles del cliente
        mensaje = cliente.readStringUntil('\n');
        Serial.println("Mensaje recibido: " + mensaje);
        cliente.flush(); // Limpia la entrada del cliente para evitar sobrecarga
      }
      
      int lecturaSensor = analogRead(sensorPins[0]);
      //Serial.println(lecturaSensor);
      if (controlarMotores(lecturaSensor)) {
        cliente.println("encendido");
        delay(3000);
      } else {
        cliente.println("apagado");
        delay(1000);
      }

      for (int n = 0; n < 3; n++) {
        if (mensaje == mensajesRPI[n]) {
          encender(n);
          Serial.println("Se ha detectado fuego en la camara: " + String(n+1));
          delay(6000);
        }
      }
    }
    
    // Cuando se desconecta el cliente
    Serial.println("Cliente desconectado.");
    cliente.stop(); // Cierra la conexión del cliente adecuadamente
  }
}
//-DemoKnight TF2
