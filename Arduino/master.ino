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
int sensorPins[3] = {32, 26, 13};
//arrays que contienen a donde van conectados los componentes
int relayPins[4] = {2, 3, 4, 5};
Servo escControl[4]; //23, 3, 18, 15 (se les coloca en esos pines en el setup)

bool FireState = false; //ELIMINAR TODA INSTANCIA DE ESTA BANDERA EN FUTURAS VERSIONES
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

Motor motors[4] = {Motor(0), Motor(1), Motor(2), Motor(3)};

  void setup() {
    Serial.begin(9600);
    rpi.begin(9600, SERIAL_8N1, 16, 17); 
  //iniciamos la comunicación serial de estas cosas todas horribles (conectado al 2do puerto: 16 rx, 17 tx)

    pinMode(resetBoton, INPUT_PULLUP);

    char escControlPins[4] = {23, 3, 18, 15}; //a la derecha del controlador

    for (int n = 0; n < 4; n++) { //aprovechando que de todo tenemos 4 metemos todo en un ciclo for para iniciar sus protocolos correspondientes  
      escControl[n].attach(escControlPins[n], 1000, 2000);
      escControl[n].write(0);

      pinMode(relayPins[n], OUTPUT);
      //lo mismo, iniciamos los pines de los sensores y los relays
    }

    for (int n = 0; n < 3; n++) {
      pinMode(sensorPins[n], INPUT); //pero sensores solo son 3 >:/
    }
  }

  void loop() {
    int butonState = digitalRead(resetBoton);
    if (butonState==LOW) { //Para el algoritmo: BOTON DE RESETEO, AGREGAR TODA FUNCION QUE SEA NECESARIA PARA DEJAR EN UN ESTADO NEUTRO EL PROYECTO
        FireState = false;
        for (int n = 0; n < 4; n++) {
          motors[n].Off();
        } 
        rpi.println("reset");
        Serial.println("Sistema Reseteado");
      }

    if (FireState==false) {
      //Para el algoritmo: AQUI VAN LAS LECTURAS (Seriales y Analogicas) QUE VAN A CAMBIAR EL ESTADO DE LA BANDERA FireState A true
    } else {
      //Para el algoritmo: AQUI VAN LAS FUNCIONES QUE SE VAN A EJECUTAR LUEGO DE PASAR EL ESTADO DE LA BANDERA A true (sin tomar en cuenta funcion para devolver su estado a false)

    }
  } 

  //-DemoKnight TF2
