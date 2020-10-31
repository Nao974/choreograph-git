
#include "choregraph.h"

void choregraph::init_serial()
  {
   char c;
   Serial.begin(500000);
   Serial.flush();
   c = 0;
   Serial.write(c);
   c = 255;
   Serial.write(c);
   c = 0;
   Serial.write(c);
  }
/////////////////////////////////
char choregraph::serial_getChar()
  {
   char value;
   while (Serial.available()<1);
   value = Serial.read();
   return(value);
  }

byte choregraph::serial_getByte()
  {
   byte value;
   while (Serial.available()<1);
   value = Serial.read();
   return(value);
  }
  
int choregraph::serial_getInt()
  {
   byte c1, c2; int value;
   while (Serial.available()<2);
   c1 = Serial.read(); // int on 2 bytes
   c2 = Serial.read();
   value = (c2<<8) | c1;
   return(value);
  } 

/////////////////////////////////

byte choregraph::return_position(byte servo_id)
  {
   return(servo_position[servo_id]);
  }


void choregraph::servoInit_serial()
  {
   byte pin;
   pin = serial_getByte();
   servoInit(pin);
  }

void choregraph::servoInit(byte pin)
  {
   byte servo_id;
   servo_id = nbre_servo++;
   pin_to_servo[pin]= servo_id;
   servo[servo_id].attach(pin);
   servo[servo_id].SetTrim(0);
  }  

void choregraph::servoOffset_serial()
  {
   byte servo_id;
   char offset;
   servo_id = pin_to_servo[serial_getByte()];
   offset = serial_getByte();
   offset = offset -90;
   servoOffset(servo_id, offset);
  }

void choregraph::servoOffset(byte servo_id, char offset)
  {
   
    servo[servo_id].SetTrim(offset);
  }  

void choregraph::moveSingle_serial() 
  {
   byte servo_id;
   byte pos;
   servo_id = pin_to_servo[serial_getByte()];
   pos = serial_getByte();
   moveSingle(servo_id, pos); 
  }

void choregraph::moveSingle(byte servo_id, byte pos) 
  {
   servo[servo_id].SetPosition(pos);
   servo_position[servo_id]= pos;
  }

void choregraph::moveTime_serial() 
  {
   byte servo_id;
   int pos, time;
   servo_id = pin_to_servo[serial_getByte()];
   time = serial_getInt() * 10;
   pos = serial_getInt();
   moveTime(servo_id, pos, time); 
  }

void choregraph::moveTime(byte servo_id, int pos, int time) 
  {
   unsigned long partial_time, final_time;
   float increment;

   if(time>10)
    {
     increment = (pos - servo_position[servo_id]) / (time / 10.0);
     final_time =  millis() + time;
     for (int iteration = 1; millis() < final_time; iteration++) 
      {
       partial_time = millis() + 10;
       servo[servo_id].SetPosition(servo_position[servo_id] + (iteration * increment));
       while (millis() < partial_time); //pause
     }
    }
   else servo[servo_id].SetPosition(pos);
   servo_position[servo_id] = pos;
  }

void choregraph::moveServos_serial() 
  {
   byte nbre;
   int time;
   time = serial_getInt() * 10;
   nbre = serial_getByte();

   byte servo_array[nbre], pos[nbre];   
   for (int i=0; i<nbre; i++)
     {
      servo_array[i] = pin_to_servo[serial_getByte()];
      pos[i] = serial_getByte();
     }
	moveServos(time, nbre, servo_array, pos);
   }

void choregraph::moveServos(int time, byte nbre, byte servo_array[], byte pos[]) 
  {
   unsigned long partial_time, final_time;
   float increment[nbre];
   if(time>10)
     {
      for (int i=0; i< nbre; i++) increment[i] = (pos[i] - servo_position[servo_array[i]]) / (time / 10.0);
      final_time =  millis() + time;
      for (int iteration = 1; millis() < final_time; iteration++) 
        {
         partial_time = millis() + 10;
         for (int i=0; i< nbre; i++) servo[servo_array[i]].SetPosition(servo_position[servo_array[i]] + (iteration * increment[i]));
         while (millis() < partial_time); //pause
        }
    }
   else for (int i=0; i< nbre; i++) servo[servo_array[i]].SetPosition(pos[i]);
   
   for (int i=0; i< nbre; i++)  servo_position[servo_array[i]] = pos[i];
  }

void choregraph::oscillateServos_serial()
  {
   int T; byte cycle, nbre;
   cycle = serial_getByte();
   T = serial_getInt() * 10;
   nbre = serial_getByte();
   byte servo_array[nbre];
   int A[nbre], O[nbre]; double phase_diff[nbre];
   for (int i=0; i<nbre; i++)
     {
      servo_array[i] = pin_to_servo[serial_getByte()];
      A[i] = serial_getByte() - 90;
      O[i] = serial_getByte() - 90;
      phase_diff[i]= DEG2RAD(serial_getInt() - 180);
     }
   oscillateServos(cycle, T, nbre, servo_array, A, O, phase_diff);
  }

void choregraph::oscillateServos(byte cycle, int T, byte nbre, byte servo_array[], int A[], int O[], double phase_diff[])
  {  
   for (int i=0; i<nbre; i++) 
     {
      servo[servo_array[i]].SetO(O[i]);
      servo[servo_array[i]].SetA(A[i]);
      servo[servo_array[i]].SetT(T);
      servo[servo_array[i]].SetPh(phase_diff[i]);
     }
      
   double ref=millis();
   for (double x=ref; x<=T*cycle+ref; x=millis())
     for (int i=0; i<nbre; i++)
        servo[servo_array[i]].refresh();
}
