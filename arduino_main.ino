#include <Stepper.h>
#include <Servo.h>

uint8_t SERVO_PIN {7U};

const uint16_t step_per_revolution = 2048U;
uint8_t deg = 0;

class Stepper stepping(step_per_revolution, 52, 48, 50, 46);
class Servo servo = Servo();

void setup() {
  Serial.begin(9600U);
  stepping.setSpeed(14L);
  servo.attach(SERVO_PIN);
  delay(100UL);
}

void loop() {
  String str = "0";

  if(Serial.available() > 0)
  {
    str = Serial.readStringUntil('\n');
  }

  if(str.equals("feed"))
  {
    for(;deg < 90; deg += 10) {
    servo.write(deg);
    delay(100UL);
    }

    delay(500UL);

    for(;deg > 0; deg -= 10) {
    servo.write(deg);
    delay(100UL);
    }
  }
  else if(str.equals("clean")) {
    stepping.step(step_per_revolution);
    delay(100UL);
  }
}
