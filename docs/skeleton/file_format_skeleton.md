# file: Skeleton

This file is used to describe all the configuration of the robot.
Servo motors are defined and then integrated into "motor groups", themselves attached to a controller.
A robot can have several controllers.

format: **json**  
Extension: **.skt**  

```json
{
 "controller":
   {
    "Name_of_controller 1":
        {
         "type": "arduino_nano",
         "connection": "serial",
         "address": ["COM5",500000],
         "port": "pin",
         "sync_read": true,
         "attached_motorgroups": ["left_leg", "right_leg"],
         "mg_alignment" : "h"
        }
    },
 "motorgroups":
    {
     "left_leg": ["YL", "RL"],
     "right_leg": ["YR", "RR"]
    },
 "motors":
    {
     "YL":
        {
         "id": 5,
         "type": "servo_pwm",
         "orientation" : "direct",
         "offset" : 19,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [2, 1, 1]
        },
     "YR":
        {
         "id": 10,
         "type": "servo_pwm",
         "orientation" : "indirect",
         "offset" : -15,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [0, 1, -1]
        },
     "RL":
        {
         "id": 6,
         "type": "servo_pwm",
         "orientation" : "direct",
         "offset" : -18,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [2, 2, 1]
        },
     "RR":
        {
         "id": 11,
         "type": "servo_pwm",
         "orientation" : "indirect",
         "offset" : 5,
         "angle_limit": [0, 180],
         "default_position": 90,
         "skeleton_position": [0, 2, -1]
        }
    }
}
```

## "controller"

Used to configure the servo-motor controller card (s).
This section can include several objects corresponding to different servo motor controller boards.

* **type**: type of card between:
arduino, arduino_uno, arduino_nano, arduino_mega, pi, pi_b, pi_3, pi_4
* **connection**: type of connection to the card:
serial, lan, onboard
* **address**: list with the information required for connection
  * **serial**: [port_com, baudrate]
  * **lan**: [@_ip, port_ip]
  * **onboard**: [nop]
* **sync_read**: not implemented
* **attached_motorgroups**: List of "motorgroups" attached to this controller
* **mg_alignment**: motor alignment by "motorgroup" in the "Skeleton" tab:
"h" for horizontal, "v" for vertical

***Currently, only the "serial" connections for Arduino and "onboard" for Py are operational.***

## "motorgroups"

A "motorgroup" is a logical grouping of servo-motors corresponding for example to an articulation or a member.
This section is used to list the "motorgroups" and define for each the servomotors that compose it.

* **"name_du_motorgroup1"**: ["servo1", "servo2"]
* **"name_du_motorgroup2"**: ["servo3", "servo24]

## motors

Used to define all the robot's servo-motors. This will be dispatched in the "motorgroups".

* **id**: GPIO on the controller board
* **type**: type of motor between:
servo_pwm, servo_serial, mboxe_a, mboxe_b
* **orientation**: used to define the direction of motor rotation:
direct, indirect
* **offset**: start-up offset to adjust the default position
* **angle_limit**: limit in min and max position of the motor not to be exceeded: [pos_min, pos_max]
* **default_position**: position at startup
* **skeleton_position**: used to define in the interactive tab, the position of the motor:
[column, row, alignment] note that the column and row numbers start at 0

---

[=> All file formats](../file_format.md)

---

[<= Return](../../README.md#format-skeleton)