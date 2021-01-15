#include <Servo.h>
#include <Oscillator.h>
#include <choreograph.h>

choreograph chore;

void setup() 
{
 chore.init_serial();
}
              
void loop() 
{
 char commande;  
  if (Serial.available()>0) 
    {
     commande = Serial.read();
     if (commande==SERVO_INITSINGLE) chore.servoInit_serial();
     else if (commande==SERVO_INITOFFSET) chore.servoOffset_serial();
     else if (commande==SERVO_MOVESINGLE) chore.moveSingle_serial();
     else if (commande==SERVO_MOVETIME) chore.moveTime_serial();
     else if (commande==SERVO_MOVESERVOS) chore.moveServos_serial();
     else if (commande==SERVO_MOVEOSCILLATE) chore.oscillateServos_serial();
   }
}

