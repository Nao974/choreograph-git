/*
  Copyright (c) 2013 Arduino LLC. All right reserved.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
*/

#if defined(ARDUINO_ARCH_SAMD)

#include <Arduino.h>
#include <Servo.h>

static servo_t servos[MAX_SERVOS];                          // static array of servo structures

uint8_t ServoCount = 0;                                     // the total number of attached servos
Tcc* TCCx;
uint8_t Channelx = 0;

// convenience macros

#define SERVO_MIN() (MIN_PULSE_WIDTH_SAMD)  // minimum value in uS for this servo
#define SERVO_MAX() (MAX_PULSE_WIDTH_SAMD)  // maximum value in uS for this servo

/************ static functions common to all instances ***********************/

//------------------------------------------------------------------------------
/// Interrupt handler for the TC0 channel 1.
//------------------------------------------------------------------------------


/****************** end of static functions ******************************/

Servo::Servo()
{
  if (ServoCount < MAX_SERVOS) {
    this->servoIndex = ServoCount++;                    // assign a servo index to this instance
  } else {                                                  //su questo costruttore forse si deve tornare
    this->servoIndex = INVALID_SERVO;  // too many servos
  }
}

uint8_t Servo::attach(int pin)
{
  return this->attach(pin, MIN_PULSE_WIDTH_SAMD, MAX_PULSE_WIDTH_SAMD);
}

uint8_t Servo::attach(int pin, int min, int max)
{
  

  if (this->servoIndex < MAX_SERVOS) {
    pinMode(pin, OUTPUT);                                   // set servo pin to output
    servos[this->servoIndex].Pin.nbr = pin;
    if(min > MIN_PULSE_WIDTH_SAMD) min = MIN_PULSE_WIDTH_SAMD;
	if (max > MAX_PULSE_WIDTH_SAMD) max = MAX_PULSE_WIDTH_SAMD;
	this->min  = min;
    this->max  = max;
	
	switch(pin)
	{
		case 2:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC0;
			Channelx=0;
		}
		break;
		
		case 3:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC0;
			Channelx=1;
		}
		break;
		
		case 6:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC0;
			Channelx=2;
		}
		break;
		
		case 7:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC0;
			Channelx=3;
		}
		break;
		
		case 8:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC1;
			Channelx=0;
		}
		break;
		
		case 9:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC1;
			Channelx=1;
		}
		break;
		
		case 11:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC2;
			Channelx=0;
		}
		break;
		
		case 13:
		{
			pinPeripheral(pin, g_APinDescription[pin].ulPinType);
			TCCx=TCC2;
			Channelx=1;
		}
		break;
		
		default:
		break;
		
	}
	
	if ((TCCx==TCC0) | (TCCx==TCC1)) GCLK->CLKCTRL.reg = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK3 | GCLK_CLKCTRL_ID( GCM_TCC0_TCC1 )) ;
	else if(TCCx==TCC2) GCLK->CLKCTRL.reg = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK3 | GCLK_CLKCTRL_ID( GCM_TCC2_TC3 )) ;
	else;
		
	if(servos[this->servoIndex].Pin.isActive == false)
	{	
		TCCx->CTRLA.reg &=~(TCC_CTRLA_ENABLE);        //disable TCC module
		TCCx->CTRLA.reg |=TCC_CTRLA_PRESCALER_DIV8;   //setting prescaler to divide by 8
		TCCx->WAVE.reg |= TCC_WAVE_WAVEGEN_NPWM;      //Set TCCx as normal PWM
		TCCx->CC[Channelx].reg=1500;                  //default value for servo position
		TCCx->PER.reg=20000;                          // setting servo frequency (50 hz) 
		TCCx->CTRLA.reg |= TCC_CTRLA_ENABLE ;	      //ENABLE TCCx
		servos[this->servoIndex].Pin.isActive = true; 
	}	
    
    //servos[this->servoIndex].Pin.isActive = true;  // this must be set after the check for isTimerActive
  }
  return this->servoIndex;
}

void Servo::detach()
{
  
	
  servos[this->servoIndex].Pin.isActive = false;
  if((servos[this->servoIndex].Pin.nbr == 2) | (servos[this->servoIndex].Pin.nbr == 3) | (servos[this->servoIndex].Pin.nbr == 6) | (servos[this->servoIndex].Pin.nbr == 7)) TCC0->CTRLA.reg &=~(TCC_CTRLA_ENABLE); 
  else if((servos[this->servoIndex].Pin.nbr == 8) | (servos[this->servoIndex].Pin.nbr == 9)) TCC1->CTRLA.reg &=~(TCC_CTRLA_ENABLE);
  else if ((servos[this->servoIndex].Pin.nbr == 11) | (servos[this->servoIndex].Pin.nbr == 13)) TCC2->CTRLA.reg &=~(TCC_CTRLA_ENABLE);	
}

void Servo::write(int value)
{
  // treat values less than 544 as angles in degrees (valid values in microseconds are handled as microseconds)
  if (value < MIN_PULSE_WIDTH)
  {
    if (value < 0)
      value = 0;
    else if (value > 180)
      value = 180;

    value = map(value, 0, 180, SERVO_MIN(), SERVO_MAX());
  }
  writeMicroseconds(value);
}

void Servo::writeMicroseconds(int value)
{
  // calculate and store the values for the given channel
  byte channel = this->servoIndex;
  if( (channel < MAX_SERVOS) )   // ensure channel is valid
  {
    if (value < SERVO_MIN())          // ensure pulse width is valid
      value = SERVO_MIN();
    else if (value > SERVO_MAX())
      value = SERVO_MAX();
    servos[this->servoIndex].ticks = value;   //da sistemare
	switch(servos[this->servoIndex].Pin.nbr)
	{
		case 2:
			TCC0->CC[0].reg=value;
			break;
			
		case 3:
			TCC0->CC[1].reg=value;
			break;
			
		case 6:
			TCC0->CC[2].reg=value;
			break;
			
		case 7:
			TCC0->CC[3].reg=value;
			break;

		case 8:
			TCC1->CC[0].reg=value;
			break;			
		
		case 9:
			TCC1->CC[1].reg=value;
			break;
			
		case 11:
			TCC2->CC[0].reg=value;
			break;

		case 13:
			TCC2->CC[1].reg=value;
			break;

		default:
		break;
		
	}
    
    //servos[this->servoIndex].ticks = value;   //da sistemare
	//servos[channel].ticks = value;
  }
}

int Servo::read() // return the value as degrees
{
  return map(readMicroseconds(), SERVO_MIN(), SERVO_MAX(), 0, 180);
}

int Servo::readMicroseconds()
{
  unsigned int pulsewidth;
  if (this->servoIndex != INVALID_SERVO)
    pulsewidth = servos[this->servoIndex].ticks;
  else
    pulsewidth  = 0;

  return pulsewidth;
}

bool Servo::attached()
{
  return servos[this->servoIndex].Pin.isActive;
}

#endif // ARDUINO_ARCH_SAM

