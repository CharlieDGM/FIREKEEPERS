//alright, empecemos a trabajar el codigo master del proyecto
//El arduino va a servir como los "musculos" del proyecto, va a realizar lecturas analógicas de los sensores,
//va a ancender las baterias(o fuentes) de los motores y va a mandar señales PWM a los controladores
//de los motores. Mandara mensajes a la Raspberry para poder operar en conjunto y realizar tareas
//especificas
#include <WiFi.h>
#include <ESP32Servo.h>
//librerias iniciales

WiFiServer server(80); //Servidor local en el puerto 80. Utilizado para conectarse con la Raspberry

int sensorPins[3] = {32, 26, 12};
//arrays que contienen a donde van conectados los componentes
Servo escControl[4]; //23, 21, 18, 2 (se les coloca en esos pines en el setup)

bool AnalogLecture(int InPin, int limit) {
  int aux = analogRead(InPin); //lee la entrada del pin analógico que le indiquemos
  if (aux > limit) {
    Serial.println("Pin Leido: " + String(InPin) + ". Lectura Obtenida: " + String(aux));
    return true; 
  } else {
    Serial.println("Pin Leido: " + String(InPin) + ". Lectura Obtenida: " + String(aux));
    return false;
  } //devuelve true o false dependiendo de la lectura
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
  }
};

Motor motors[4] = {Motor(0), Motor(1), Motor(2), Motor(3)};

void setup() {
  Serial.begin(9600); 
  //iniciamos la comunicación serial de estas cosas todas horribles (conectado al 2do puerto: 16 (cable negro) rx, 17 (cable blanco) tx)

  char escControlPins[4] = {23, 21, 18, 2}; //a la izquierda del controlador (Motores A, B, C, D)
  delay(2000);
  Serial.println("");
  Serial.println("Encendiendo...");
  delay(2000);
  for (int n = 0; n < 4; n++) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes  
    Serial.println("Encendiendo el motor: " + String(n+1));
    escControl[n].attach(escControlPins[n], 1000, 2000);
    escControl[n].write(0);
    delay(1000);
  }

  for (int n = 0; n < 3; n++) {
    pinMode(sensorPins[n], INPUT); //pero sensores solo son 3 >:/ (asi q hay que hacer otro ciclo for)
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

void loop() {
  //REESTRUCTURAR COMPLETAMENTE EL ALGORITMO
} 

//-DemoKnight TF2
