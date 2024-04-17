//alright, empecemos a trabajar el codigo master del proyecto
//El arduino va a servir como los "musculos" del proyecto, va a realizar lecturas analógicas de los sensores,
//va a ancender las baterias(o fuentes) de los motores y va a mandar señales PWM a los controladores
//de los motores. Mandara mensajes a la Raspberry para poder operar en conjunto y realizar tareas
//especificas

#include <SoftwareSerial.h>
#include <Servo.h>
//librerias iniciales

SoftwareSerial rpi(11, 12); //donde va a ir conectado el raspberry
char sensorPins[4] = {A0, A1, A2, A3};
//arrays que contienen a donde van conectados los componentes
int relayPins[4] = {2, 3, 4, 5};
Servo escControl[4]; //A4, A5, A6 y A7 (se les coloca en esos pines en el setup)

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

  if (rpi.available()) {  //comprueba si hay datos seriales disponibles
    while (rpi.available() > 0) {//mientras estan disponibles los lee
      rpi.read();
    }

    lecture = rpi.readStringUntil('\n');
    lecture.trim(); //ajustamos la lectura por cualquier error que pueda ocurrir
    Serial.println(lecture);
    return lecture; //imprimimos y guardamos el valor de la lectura obtenida
  }
}

class motor { //una clase que contiene funciones para encender y apagar las bombas de agua. Necesitamos controlar un relay y mandar una señal a los controladores
  void On(int motor) {
    int pulseToSend = 20;

    digitalWrite(relayPins[motor], HIGH);
    escControl[motor].write(0);
    delay(2000);
    escControl[motor].write(pulseToSend); //encendemos el relay junto con el controlador del motor
  }

  void Off(int motor) {
    digitalWrite(relayPins[motor], LOW);
    escControl[motor].write(0); //apagamos el relay junto con el controlador del motor
  }
};

void setup() {
  Serial.begin(9600);
  rpi.begin(9600);
//iniciamos la comunicación serial de estas cosas todas horribles

  for (int n = 0; n < 4, n++;) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes
    char escControlPins[4] = {A4, A5, A6, A7};
    escControl[n].attach(escControlPins[n], 1000, 2000);
    escControl[n].write(0);

    pinMode(sensorPins[n], INPUT);
    pinMode(relayPins[n], OUTPUT);
    //lo mismo, iniciamos los pines de los sensores y los relays
  }
}

//-DemoKnight TF2