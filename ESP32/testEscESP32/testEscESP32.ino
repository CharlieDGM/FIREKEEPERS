#include <ESP32Servo.h>
int pinA = 23;
int pinB = 21;
int pinC = 18;

Servo esc;
void setup() {
  // put your setup code here, to run once:
  esc.attach(pinA, 1000, 2000);
  esc.write(0);
  delay(3000);
}

void loop() {
  // put your main code here, to run repeatedly:
  esc.write(70);
}
