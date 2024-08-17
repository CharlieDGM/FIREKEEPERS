//alright, empecemos a trabajar el codigo master del proyecto
//El arduino va a servir como los "musculos" del proyecto, va a realizar lecturas analógicas de los sensores,
//va a ancender las baterias(o fuentes) de los motores y va a mandar señales PWM a los controladores
//de los motores. Mandara mensajes a la Raspberry para poder operar en conjunto y realizar tareas
//especificas

#include <HardwareSerial.h>
//no tengo idea si esto es necesario para imprimir mensajes en la consola, lo voy a dejar por si las moscas xd
#include <ESP32Servo.h>
//librerias iniciales

HardwareSerial rpi(1); // PUERTO UART 2 / / conectado a pines 16 y 17 en el setup / objeto que se usara para la comunicacion serial RPI - ESP32
int sensorPins[3] = {32, 26, 12};
//arrays que contienen a donde van conectados los componentes
//int relayPins[4] = {2, 3, 4, 5}; ELIMINAR O CAMBIAR PINOUT DE LOS RELAY EN FUTURAS VERSIONES
Servo escControl[4]; //23, 21, 18, 2 (se les coloca en esos pines en el setup)

//bool FireState = false; //ELIMINAR TODA INSTANCIA DE ESTA BANDERA EN FUTURAS VERSIONES

bool AnalogLecture(char InPin, int limit) {
  int aux = analogRead(InPin); //lee la entrada del pin analógico que le indiquemos
  if (aux > limit) {
    Serial.println("Pin Leido: " + String(InPin) + ". Lectura Obtenida: " + String(aux));
    return true; 
  } else {
    Serial.println("Pin Leido: " + String(InPin) + ". Lectura Obtenida: " + String(aux));
    return false;
  } //devuelve true o false dependiendo de la lectura
}

String rpiReading() {
  String lecture;

  if (rpi.available()) {  //comprueba si hay datos seriales disponibles4
  lecture = rpi.readStringUntil('\n');
    lecture.trim(); //ajustamos la lectura por cualquier error que pueda ocurrir
    Serial.println("Lectura de la raspberry lol xd: " + lecture);
    return lecture; //imprimimos y guardamos el valor de la lectura obtenida
  }
}

class Motor { //una clase que contiene funciones para encender y apagar las bombas de agua. Necesitamos controlar un relay y mandar una señal a los controladores
  private:
    int motorNumber;

  public:
  Motor(int m) {
    motorNumber = m;
  }

  void On(int pulseToSend) {
    //digitalWrite(relayPins[motorNumber], HIGH); A;ADIR SI SE MODIFICA LA LINEA 15
    escControl[motorNumber].write(pulseToSend); //encendemos el relay junto con el controlador del motor
    Serial.println("Se ha encendido el motor: " + String(motorNumber+1) + ". Pulso enviado: " + String(pulseToSend));
  }

  void Off() {
    //digitalWrite(relayPins[motorNumber], LOW); A;ADIR SI SE MODIFICA LA LINEA 15
    escControl[motorNumber].write(0); //apagamos el relay junto con el controlador del motor
  }
};

Motor motors[4] = {Motor(0), Motor(1), Motor(2), Motor(3)};

void setup() {
  Serial.begin(9600);
  rpi.begin(9600, SERIAL_8N1, 16, 17); 
  //iniciamos la comunicación serial de estas cosas todas horribles (conectado al 2do puerto: 16 rx, 17 tx)

  char escControlPins[4] = {23, 21, 18, 2}; //a la izquierda del controlador
  delay(2000);
  Serial.println("");
  Serial.println("Encendiendo...");
  delay(2000);
  rpi.println("start");
  for (int n = 0; n < 4; n++) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes  
    Serial.println("Se ha iniciado el motor: " + String(n+1));
    escControl[n].attach(escControlPins[n], 1000, 2000);
    escControl[n].write(0);
    delay(1000);

    //pinMode(relayPins[n], OUTPUT); AÑADIR SOLAMENTE SI SE MODIFICA LA LINEA 15
    //lo mismo, iniciamos los pines de los sensores y los relays
  }

  for (int n = 0; n < 3; n++) {
    pinMode(sensorPins[n], INPUT); //pero sensores solo son 3 >:/ (asi q hay que hacer otro ciclo for)
  }
  Serial.println("Iniciando todo pipipip...");
  delay(3000);
}

void loop() {
  motors[0].On(100);
  //REESTRUCTURAR COMPLETAMENTE EL ALGORITMO
} 

//-DemoKnight TF2
