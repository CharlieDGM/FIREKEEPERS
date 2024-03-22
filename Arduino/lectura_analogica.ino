#include <SoftwareSerial.h>

char InPin = A1;
char ledPin = 2;

bool AnalogLecture() {
  int aux = analogRead(InPin);
  Serial.println(aux);
  if (aux > 72) {
    return true;
  } else {
    return false;
  }
}

void setup() {
  pinMode(InPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (!AnalogLecture()) {
    digitalWrite(ledPin, LOW);
  } else {
    Serial.println("Señal Suficiente, enciendiendo led");
    digitalWrite(ledPin, HIGH);
    delay(3000);
  }
}