# Choreograph (beta) v0.9

<a id="up"> </a>

[![Video Presentation](docs/video_presentation.png)](https://youtu.be/9EAe0ReYfHI)

[Version française](./README_fr.md)

[Quickstart](#quickstart)

---

Software environment allowing the parameterization of servo-motor-based robots.

<a id="format-skeleton"> </a>

## Choreograph allows you

- A **Structured Description** of your robots  
On the basis of a JSON file, you will be able to describe each controller, each servo motor and group them to form the members of your robot.

<div align="center"><img alt="skeleton.json" width="50%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="skeleton.screen" width="40%" src="docs/skeleton/img_skeleton_screen.png" /></div>  

[=> learn more](docs/skeleton/file_format_skeleton.md)

---
<a id="desc-trim"> </a>

- Determine the **neutral position (trim)** of each servo.  
Once the skeleton file has been loaded, you will be able to find the initial position of each servo motor and recalculate their offset.

<div align="center"><img alt="recalculate.trim" width="100%" src="docs/trim/img_recalculate_trim.png" /></div>  

[=> learn more](docs/trim/desc_trim.md)

---
<a id="position"> </a>

- Control in **real time** each servo motor independently and record **SnapShot** positions.

<div align="center"><img alt="position.screen" width="60%" src="docs/position/img_position_screen.png" />&nbsp;<img alt="position.screen" width="30%" src="docs/position/img_position_screen2.png" /></div>  

[=> learn more](docs/position/desc_position.md)

---
<a id="movement"> </a>

- **Create movements** by chaining previously recorded positions, thanks to configurable transitions.

<div align="center"><img alt="movement.screen" width="90%" src="docs/movement/img_movement.png" /></div>  

[=> learn more](docs/movement/desc_movement.md)

---
<a id="export-c"> </a>

- **Export in C language** the description of the skeleton and movements for direct integration into your source codes.

<div align="center"><img alt="skeleton.json" width="49%" src="docs/skeleton/img_skeleton_json.png" />&nbsp;<img alt="export_c.screen" width="49%" src="docs/export_c/img_export_c.png" /></div>  

[=> learn more](docs/export_c/desc_export_c.md)

---
<a id="multi-type"> </a>

- Support for **several types** of controllers (Arduino Uno, Nano, Mega, Raspberry) and servo motors (pwm, series). It suffices to declare them in the description of the skeleton.

<div align="center"><img alt="multi_type.screen" width="75%" src="docs/multi_type/img_multi_type.png" /></div>  

[=> learn more](docs/multi_type/desc_multi_type.md)

---
<a id="controller"> </a>

- **Pilot your robot** by attaching the configured movements to the keys of the keyboard or your Bluetooth controller.

<div align="center"><img alt="controller.screen" width="75%" src="docs/controller/img_controller.png" /></div>  

[=> learn more](docs/controller/desc_controller.md)

---
<a id="firmware"> </a>

- The **Firmware** must be loaded into your robot.
Available for Arduino boards, it is to be loaded from the Arduino IDE.
VSCode PIO support is under development along with other Micro Controller cards.

<div align="center"><img alt="lang.screen" width="75%" src="docs/firmware/img_doc1_firmware_arduino.png" /></div>  

[=> learn more](docs/firmware/desc_firmware.md)

---
<a id="multi-lang"> </a>

- **Multi languages**, available in English and French, the languages ​​are stored in the form of an easily modifiable dictionary.

<div align="center"><img alt="lang.screen" width="50%" src="docs/lang/img_lang.png" /></div>  

---
<a id="file-format"> </a>

- All the setting formats are described in the following link.

[=> learn more](docs/file_format.md)

---

## Quick Start

<a id="quickstart"> </a>

OK, you have assembled your robot and carried out some good functioning tests on the various servo-motors, now it's time for Movements !!!

**Everything happens in the *. / Data folder***

- duplicate the *.data/_default_project* folder
  - rename it with the name of your project
- duplicate the file *. / data / _defaut_project.pjt
  - rename it with the name of your project
  - open it is to modify the following tags at least
    - **description**: with the previously of your robot
    - **filepath**: modify the path with the name of the previously renamed folder
    - [=> full format of the project file](docs/projet/file_format_project.md)
- in your project folder, replace the **view.jpg** file with an image of your robot, it will be displayed each time your project is loaded.

---

Now let's modify the description file of your robot by opening the *skeleton.skt* file

- At a minimum, you should modify
  - on the *controller* node
    - the type of your card
    - connection and port
  - describe each servo motor
  - you can now group the servomotors of each member in the *motorgroups* node
  - and finally attach these *motorgroups* to the right controller
- All the details can be found in the documentation [=> complete format squeleton.skt](docs/skeleton/file_format_skeleton.md)

---

Load the firmware *Choreograph* into your card [=> firmware documentation](docs/firmware/desc_firmware.md)

---

- You can now save your own positions
  - [=> documentation on positions](docs/position/desc_position.md)
- Then chain them in the form of movements
  - [=> documentation on movements](docs/movement/desc_movement.md)
- Control your robot from your keyboard or BT controller
  - [=> documentation on controllers](docs/controller/desc_controller.md)

---

[=> Top](#up)
