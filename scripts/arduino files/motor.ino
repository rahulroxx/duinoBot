// The following is the basic Arduino code which runs a loop that makes the Robot go straight forward.

int INBYTE = 0;
int LeftMotorForward = 10; // Pin 10 has Left Motor connected on Arduino boards.
int LeftMotorReverse = 9; // Pin 9 has Left Motor connected on Arduino boards.

int RightMotorForward = 12; // Pin 12 has Right Motor connected on Arduino boards.
int RightMotorReverse = 13; // Pin 13 has Right Motor connected on Arduino boards.


void setup()
{
  Serial.begin(9600);
  pinMode(LeftMotorForward, OUTPUT);  // initialize the  pin as an output.
  pinMode(RightMotorForward, OUTPUT);  // initialize the  pin as an output.
  pinMode(LeftMotorReverse, OUTPUT);  // initialize the  pin as an output.
  pinMode(RightMotorReverse, OUTPUT);  // initialize the  pin as an output.
}

// The following Loop is to make the Robot go staright
void loop(){
  Serial.println("Press 1 to turn Arduino pin 13 LED ON or 0 to turn it OFF:");
  while (!Serial.available());
    INBYTE = Serial.read();        // read next available byte
  if( INBYTE == '1' ){
   digitalWrite(RightMotorForward, HIGH);   // turn the Right Motor ON
   digitalWrite(LeftMotorForward, HIGH);   // turn the Left Motor ON
   delay(100);               // wait for  10 seconds
 
   digitalWrite(RightMotorForward,LOW);   // turn the Right Motor OFF
   digitalWrite(LeftMotorForward, LOW);   // turn the Left Motor OFF    // tell servo to go to position in variable 'pos'
                       // waits 15ms for the servo to reach the position
  }
 delay(5);            // wait for  10 seconds
}
