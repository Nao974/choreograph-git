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

/*
 * Defines for 16 bit timers used with  Servo library
 *
 * If _useTimerX is defined then TimerX is a 16 bit timer on the current board
 * timer16_Sequence_t enumerates the sequence that the timers should be allocated
 * _Nbr_16timers indicates how many 16 bit timers are available.
 */

/**
 * SAM Only definitions
 * --------------------
 */

// For SAMD21G:
#define _useTimer0
#define _useTimer1
#define _useTimer2




#if defined (_useTimer0)
#define TC_FOR_TIMER0       TCC0
#define CHANNEL0_FOR_TIMER0  0
#define CHANNEL1_FOR_TIMER0  1
#define CHANNEL2_FOR_TIMER0  2
#define CHANNEL3_FOR_TIMER0  3
//#define ID_TC_FOR_TIMER1    ID_TC3   //forse non serve

#endif
#if defined (_useTimer1)
#define TC_FOR_TIMER1       TCC1
#define CHANNEL0_FOR_TIMER1  0
#define CHANNEL1_FOR_TIMER1  1
//#define ID_TC_FOR_TIMER2    ID_TC4   //forse non serve
#endif


#if defined (_useTimer2)
#define TC_FOR_TIMER2       TCC2
#define CHANNEL_FOR_TIMER2  0
#define CHANNEL_FOR_TIMER2  1
//#define ID_TC_FOR_TIMER3    ID_TC5      //forse non serve

#endif

#endif

//typedef enum { _timer1, _timer2, _timer3, _timer4, _timer5, _Nbr_16timers } timer16_Sequence_t ;    // forse non serve

