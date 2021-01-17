# file: Controller

This file allows you to attach your movements to the keys of your Bluetooth controller or your keyboard.

* Attach your movements to the buttons of the controller
* Link the keys of your keyboard to the buttons of the controller

format: **json**  
Extension: **.ctl**  

```json
{
 "controller_name": 
    {
     "model": "Dualshock 3 Wireless",
     "picture": "controller_ps3.jpg",
     "adress": "localhost",
     "port": "auto",
     "sync_read": true
    },
 "movements":
    {
     "L1": "jump",
     "L2": "shake_leg",
     "R1": "flapping",
     "R2": "moonwalker",
     "LF": "turn_left_key",
     "RG": "turn_right_key",
     "UP": "walk_fd_key",
     "DW": "walk_bd_key",
     "S" : "",
     "O" : "",
     "T" : "crusaito",
     "X" : "Swing"
    }, 
 "keys":
    {
     "L1": "&",
     "L2": "é",
     "R1": ")",
     "R2": "=",
     "LF": "q",
     "RG": "d",
     "UP": "z",
     "DW": "s",
     "S" : "k",
     "O" : "m",
     "T" : "o",
     "X" : "l"
    }
}
```

* **model**: controller model
* **picture**: controller image in jpeg format
* **address**: not implemented
* **port**: not implemented
* **sync_read**: not implemented
* **movements**: list of controller buttons with associated movement:
  * "button": "movement"
* **keys**: list of controller buttons with associated keyboard key:
  * "button": "keyboard_key"

CAUTION, movements must be loaded in the list on the "Movement" tab.

---

[=> All files format](../file_format.md)

---

[<= Return](../../README.md#controller)