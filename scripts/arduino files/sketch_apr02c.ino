#include <Servo.h>
Servo myservo;
Servo myservo1;
char INBYTE;
int  pos = 0; // LED on pin 13

void setup() {
  myservo.attach(9);
  Serial.begin(9600);
  myservo1.attach(10);
}

void loop() {
  Serial.println("Press 1 to turn Arduino pin 13 LED ON or 0 to turn it OFF:");
  while (!Serial.available());   // stay here so long as COM port is empty   
  INBYTE = Serial.read();        // read next available byte
  if( INBYTE == '1' ){
   for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  }
    }  // if it's a 0 (zero) tun LED off
  if( INBYTE == '2' ){
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  }
    } // if it's a 1 (one) turn LED on
    ///
  if( INBYTE == '3' ){
   for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  }
    }  // if it's a 0 (zero) tun LED off
  if( INBYTE == '4' ){
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  }
    } // if it's a 1 (one) turn LED on
  delay(5);
}
