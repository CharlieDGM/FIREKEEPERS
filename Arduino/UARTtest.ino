#include <SoftwareSerial.h>

SoftwareSerial rpi(11, 12); //declaramos en donde vamos a tener nuestra conexión

char LedPin = 2;
char InPin = A1;
//variables de uso general

bool AnalogLecture(int limit) {
  int aux = analogRead(InPin); //lee la entrada del pin analógico
  Serial.println(aux);
  if (aux > limit) {
    return true; 
  } else {
    return false;
  } //devuelve true o false dependiendo de la lectura
}

String rpiReading() {
  String lecture;

  if (rpi.available()) {  
    while (rpi.available() > 0) {
      rpi.read();
    }

    lecture = rpi.readStringUntil('\n');
    lecture.trim();
    Serial.println(lecture);
    return lecture;
  }
}

void setup() {
  pinMode(LedPin, OUTPUT);
  pinMode(InPin, INPUT);
  Serial.begin(9600);
  rpi.begin(9600); //nomas declaraciones iniciales del setup
}

void loop() {
  if (!AnalogLecture(85)) {
    rpi.println("LOW");
  } else {
    rpi.println("HIGH");
  }

  if (rpiReading().equals("encender")) {
    digitalWrite(LedPin, HIGH);
    delay(3000);
  } else {
    digitalWrite(LedPin, LOW);
  }
}


