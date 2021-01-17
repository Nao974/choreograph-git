# Multi-Types

In your robot description file *(skeleton.skt)*, you will define the type of your controllers as well as those of your servo-motors.
[=> format skeleton.skt] (../ skeleton / file_format_skeleton_fr.md)

## **The Controllers**

The controllers currently supported are the cards:

- arduino, arduino_uno, arduino_nano, arduino_mega
  - Only the firmware for Arduino boards is currently developed

- Raspberry Pi, Pi_b, Pi 3, Pi 4
  - Choreograph directly controls the servo-motors through its GPIOs.
  - you should therefore describe your controller with *connection: onboard*

---

## **Servo-motors**

Actuators currently supported are servo motors:

- standard PWM servo-motors (for model making)

- M-Boxe, only by Raspbery Pi
[=> Github M-Boxe project](https://github.com/Nao974/M-BOXE)

- Serial servo motors can be declared in the skeleton.skt but are not currently supported by the firmware.

---

[<= Return](../../README.md#multi-type)
