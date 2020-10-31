#pragma once

#include <arduino.h>
#include <Servo.h>
#include <Oscillator.h>

#define  NB_SERVO_MAX  12

#define SERVO_INITSINGLE     10
#define SERVO_INITOFFSET     11
#define SERVO_INITSKELETON   15
#define SERVO_MOVESINGLE     20
#define SERVO_MOVETIME       21
#define SERVO_MOVESERVOS     30
#define SERVO_MOVEOSCILLATE  31

class choregraph
{
 public:
  // standard functions
  byte return_position(byte servo_id);
  void servoInit(byte pin);
  void servoOffset(byte servo_id, char offset);
  void moveSingle(byte servo_id, byte pos);
  void moveTime(byte servo_id, int pos, int time);
  void moveServos(int time, byte nbre, byte servo_array[], byte pos[]);
  void oscillateServos(byte cycle, int T, byte nbre, byte servo_array[], int A[], int O[], double phase_diff[]);
  

  // calling standard functions from the serial link
  void servoInit_serial();
  void servoOffset_serial();
  void moveSingle_serial();
  void moveTime_serial();
  void moveServos_serial();
  void oscillateServos_serial();

  // basic function for exchange via serial link  
  void init_serial();
  char serial_getChar();
  byte serial_getByte();
  int serial_getInt();

 private:
  Oscillator servo[NB_SERVO_MAX];
  byte pin_to_servo[64];
  byte servo_position[64];
  byte nbre_servo=0;
};
