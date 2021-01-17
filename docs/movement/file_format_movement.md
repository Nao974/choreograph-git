# file: Movement

This file is used to describe a position of the robot, ie the position of some or all of the robot's motors.
The name of the proposed file is a concatenation of the category and the name.

format: **json**  
Extension: **.mov**  

```json
{
 "name": "shake_leg",
 "duration": 500,
 "functions": 
    {
     "I001":
        {
         "function": "Linear",
         "position": "shakeleg_1",
         "duration": 500,
         "nb_step": 0
        },
     "I002":
        {
         "function": "Linear",
         "position": "shakeleg_2",
         "duration": 500,
         "nb_step": 0
        }
    },
 "id": "I007",
 "file": "C:/Choregrpah_TK/PROJECTS/otto/movements/shake_leg.mov"
}
```

* **name**: name of the movement
* **duration**: unit of time of the movement
* **functions**: list of positions in object form
  * **function**: movement function
  * **position**: name of the position
  Warning, the position must be loaded and available in the list of positions
  * **duration**: duration of the movement
  * **nb_step**: number of steps according to the duration of the position and the time unit of the movement (duration)
* **id**: id of the movement in the list of movements
* **file**: path / name_of_file.mov

---

[=> All files format](../file_format.md)

---

[<= Return](../../README.md#file-format)
