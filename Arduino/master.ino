//alright, empecemos a trabajar el codigo master del proyecto
//El arduino va a servir como los "musculos" del proyecto, va a realizar lecturas analógicas de los sensores,
//va a ancender las baterias(o fuentes) de los motores y va a mandar señales PWM a los controladores
//de los motores. Mandara mensajes a la Raspberry para poder operar en conjunto y realizar tareas
//especificas

#include <HardwareSerial.h>
 //no tengo idea si esto es necesario para imprimir mensajes en la consola, lo voy a dejar por si las moscas xd
#include <ESP32Servo.h>
//librerias iniciales

HardwareSerial rpi(1); // PUERTO UART 2 / objeto que se usara para la comunicacion serial RPI - ESP32
int sensorPins[4] = {A0, A1, A2, A3};
//arrays que contienen a donde van conectados los componentes
int relayPins[4] = {2, 3, 4, 5};
Servo escControl[4]; //A4, A5, A6 y A7 (se les coloca en esos pines en el setup)

bool FireState = false; //bandera que nos indicara si se ha detectado fuego lol xdxxdxdxd
int resetBoton = 6; //boton de reseteo, i guess lol

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
    digitalWrite(relayPins[motorNumber], HIGH);
    escControl[motorNumber].write(pulseToSend); //encendemos el relay junto con el controlador del motor
  }

  void Off() {
    digitalWrite(relayPins[motorNumber], LOW);
    escControl[motorNumber].write(0); //apagamos el relay junto con el controlador del motor
  }
};

void setup() {
  Motor motor1(0); //creamos los 4 objetos de los motores, mandandole a cada una una variable de 0 - 3 (es mas facil esto porque ya estan declarados
  Motor motor2(1); //los pines de los objetos, entonces al llamar a la funcion de cada objeto se van a activar con la asignacion realizada (ni yo me entendi lol)
  Motor motor3(2);
  Motor motor4(3);

  Serial.begin(9600);
  rpi.begin(9600, SERIAL_8N1, 16, 17); 
//iniciamos la comunicación serial de estas cosas todas horribles (conectado al 2do puerto: 16 rx, 17 tx)

  pinMode(resetBoton, INPUT_PULLUP);

  char escControlPins[4] = {A4, A5, A6, A7};

  for (int n = 0; n < 4; n++) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes  
    escControl[n].attach(escControlPins[n], 1000, 2000);
    escControl[n].write(0);

    pinMode(sensorPins[n], INPUT);
    pinMode(relayPins[n], OUTPUT);
    //lo mismo, iniciamos los pines de los sensores y los relays
  }
}

void loop() {
  int butonState = digitalRead(resetBoton);
  if (butonState==LOW) {
      FireState = false;
      rpi.println("reset");
      Serial.println("Sistema Reseteado");
    }

  if (FireState==false) {
    
  } else {
    rpi.println("norte");

  }
} 

//-DemoKnight TF2
