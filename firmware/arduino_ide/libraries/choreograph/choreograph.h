#pragma once

#include <arduino.h>
#include <Servo.h>
#include <Oscillator.h>

#define  NB_SERVO_MAX        12

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
  uint8_t return_position(uint8_t servo_id);
  void servoInit(uint8_t pin);
  void servoOffset(uint8_t servo_id, int8_t offset);
  void moveSingle(uint8_t servo_id, uint8_t pos);
  void moveTime(uint8_t servo_id, int16_t pos, int16_t time);
  void moveServos(int16_t time, uint8_t nbre, uint8_t servo_array[], uint8_t pos[]);
  void oscillateServos(uint8_t cycle, int16_t T, uint8_t nbre, uint8_t servo_array[], int16_t A[], int16_t O[], int32_t phase_diff[]);
  

  // calling standard functions from the serial link
  void servoInit_serial();
  void servoOffset_serial();
  void moveSingle_serial();
  void moveTime_serial();
  void moveServos_serial();
  void oscillateServos_serial();

  // basic function for exchange via serial link  
  void init_serial();
  int8_t serial_getChar();
  uint8_t serial_getByte();
  int16_t serial_getInt();

 private:
  Oscillator servo[NB_SERVO_MAX];
  uint8_t pin_to_servo[64];
  uint8_t servo_position[64];
  uint8_t nbre_servo=0;
};
