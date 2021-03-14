#include "choreograph.h"

void choreograph::init_serial()
  {
   int8_t c;
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
int8_t choreograph::serial_getChar()
  {
   int8_t value;
   while (Serial.available()<1);
   value = Serial.read();
   return(value);
  }

uint8_t choreograph::serial_getByte()
  {
   uint8_t value;
   while (Serial.available()<1);
   value = Serial.read();
   return(value);
  }
  
int16_t choreograph::serial_getInt()
  {
   uint8_t c1, c2; int16_t value;
   while (Serial.available()<2);
   c1 = Serial.read(); // int16_t on 2 bytes
   c2 = Serial.read();
   value = (c2<<8) | c1;
   return(value);
  } 

/////////////////////////////////

uint8_t choreograph::return_position(uint8_t servo_id)
  {
   return(servo_position[servo_id]);
  }


void choreograph::servoInit_serial()
  {
   uint8_t pin;
   pin = serial_getByte();
   servoInit(pin);
  }

void choreograph::servoInit(uint8_t pin)
  {
   uint8_t servo_id;
   servo_id = nbre_servo++;
   pin_to_servo[pin]= servo_id;
   servo[servo_id].attach(pin);
   servo[servo_id].SetTrim(0);
  }  

void choreograph::servoOffset_serial()
  {
   uint8_t servo_id;
   int8_t offset;
   servo_id = pin_to_servo[serial_getByte()];
   offset = serial_getByte();
   offset = offset -90;
   servoOffset(servo_id, offset);
  }

void choreograph::servoOffset(uint8_t servo_id, int8_t offset)
  {
    servo[servo_id].SetTrim(offset);
  }  

void choreograph::moveSingle_serial() 
  {
   uint8_t servo_id;
   uint8_t pos;
   servo_id = pin_to_servo[serial_getByte()];
   pos = serial_getByte();
   moveSingle(servo_id, pos); 
  }

void choreograph::moveSingle(uint8_t servo_id, uint8_t pos) 
  {
   servo[servo_id].SetPosition(pos);
   servo_position[servo_id]= pos;
  }

void choreograph::moveTime_serial() 
  {
   uint8_t servo_id;
   int16_t pos, time;
   servo_id = pin_to_servo[serial_getByte()];
   time = serial_getInt() * 10;
   pos = serial_getInt();
   moveTime(servo_id, pos, time); 
  }

void choreograph::moveTime(uint8_t servo_id, int16_t pos, int16_t time) 
  {
   unsigned long partial_time, final_time;
   float increment;

   if(time>10)
    {
     increment = (pos - servo_position[servo_id]) / (time / 10.0);
     final_time =  millis() + time;
     for (int16_t iteration = 1; millis() < final_time; iteration++) 
      {
       partial_time = millis() + 10;
       servo[servo_id].SetPosition(servo_position[servo_id] + (iteration * increment));
       while (millis() < partial_time); //pause
     }
    }
   else servo[servo_id].SetPosition(pos);
   servo_position[servo_id] = pos;
  }

void choreograph::moveServos_serial() 
  {
   uint8_t nbre;
   int16_t time;
   time = serial_getInt() * 10;
   nbre = serial_getByte();

   uint8_t servo_array[nbre], pos[nbre];   
   for (int16_t i=0; i<nbre; i++)
     {
      servo_array[i] = pin_to_servo[serial_getByte()];
      pos[i] = serial_getByte();
     }
	moveServos(time, nbre, servo_array, pos);
   }

void choreograph::moveServos(int16_t time, uint8_t nbre, uint8_t servo_array[], uint8_t pos[]) 
  {
   unsigned long partial_time, final_time;
   float increment[nbre];
   if(time>10)
     {
      for (int16_t i=0; i< nbre; i++) increment[i] = (pos[i] - servo_position[servo_array[i]]) / (time / 10.0);
      final_time =  millis() + time;
      for (int16_t iteration = 1; millis() < final_time; iteration++) 
        {
         partial_time = millis() + 10;
         for (int16_t i=0; i< nbre; i++) servo[servo_array[i]].SetPosition(servo_position[servo_array[i]] + (iteration * increment[i]));
         while (millis() < partial_time); //pause
        }
    }
   else for (int16_t i=0; i< nbre; i++) servo[servo_array[i]].SetPosition(pos[i]);
   
   for (int16_t i=0; i< nbre; i++)  servo_position[servo_array[i]] = pos[i];
  }

void choreograph::oscillateServos_serial()
  {
   int16_t T; uint8_t cycle, nbre;
   cycle = serial_getByte();
   T = serial_getInt() * 10;
   nbre = serial_getByte();
   uint8_t servo_array[nbre];
   int16_t A[nbre], O[nbre]; int32_t phase_diff[nbre];
   for (int16_t i=0; i<nbre; i++)
     {
      servo_array[i] = pin_to_servo[serial_getByte()];
      A[i] = serial_getByte() - 90;
      O[i] = serial_getByte() - 90;
      phase_diff[i]= DEG2RAD(serial_getInt() - 180);
     }
   oscillateServos(cycle, T, nbre, servo_array, A, O, phase_diff);
  }

void choreograph::oscillateServos(uint8_t cycle, int16_t T, uint8_t nbre, uint8_t servo_array[], int16_t A[], int16_t O[], int32_t phase_diff[])
  {  
   for (int16_t i=0; i<nbre; i++) 
     {
      servo[servo_array[i]].SetO(O[i]);
      servo[servo_array[i]].SetA(A[i]);
      servo[servo_array[i]].SetT(T);
      servo[servo_array[i]].SetPh(phase_diff[i]);
     }
      
   int32_t ref=millis();
   for (int32_t x=ref; x<=T*cycle+ref; x=millis())
     for (int16_t i=0; i<nbre; i++)
        servo[servo_array[i]].refresh();
}
