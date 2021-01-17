# file: Position

This file is used to describe a position of the robot, ie the position of some or all of the robot's motors.
The name of the proposed file is a concatenation of the category and the name.

format: **json**  
Extension: **.pos**  

```JSON
    {
     "category": "default",
     "name": "init",
     "description": "Initial position.\n The robot is standing.",
     "motors":
        {
         "YL": "90",
         "YR": "90",
         "RL": "90",
         "RR": "90"
        }
    }
```

* **category**: family of the position
* **name**: name of the position
* **description**: description of the position. Line breaks are done by "\n"
* **motors**: list of motors with:
"name": "position"

---

[=> All file formats](../file_format.md)

---

[<= Return](../../README.md#file-format)
