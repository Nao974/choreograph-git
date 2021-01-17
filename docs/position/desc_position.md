# Real-time control and posture recording

Once your robot is assembled, your skeleton description file created, the firmware loaded in your robot and the initial positions configured, we will be able to start doing interesting things :)

## Real-time control

Nothing could be simpler, from the **Interactive** tab modify the current position either by entering a position manually, or by using the up and down arrows ==> the servo motor moves accordingly.

<img alt="change_pos" width="50%" src="./img_doc1_change_pos.png" />

If you do not want the servomotors to move with each change, you can uncheck "Real-Time Inferface Writing", then once all the positions have been entered, click on the "Position-> Robot" button to send them to your robot in one go.

<img alt="not_real_time" width="25%" src="./img_doc2_not_real_time.png" />

---

## Posture recording

Thanks to the real-time control of your servo-motors, your robot is now in the position you are looking for, you just have to click on **"SnapShot"** of the *"Tools"* window in order to save this posture.

<img alt="SnapShot" width="25%" src="./img_doc10_snapshoot.png" />

By default, all servomotors are taken into account, you can uncheck those that do not interest you, indicate:

- the category that will serve as a heading in the position bank
- the name of the posture
- a description of it

By clicking on save, this will place your new posture in the bank and offer to save it on your disk.

<div align="center"><img alt="SnapShoot.win" width="30%" src="./img_doc11_snapshoot_win.png" />&nbsp;<img alt="positions.Bank" width="50%" src="./img_doc12_positions_bank.png" /></div>

---

## The Bank of Positions

It is loaded from the folder containing the **.pos** files, either when opening the project, or after having separately opened the skeleton file then by the menu *Movement-> Load Position (s)*.
*The creation of a description file of your project is strongly recommended ([.pjt format](../project/file_format_project.md))*.

<img alt="positions.Bank" width="50%" src="./img_doc20_positions_bank.png" />

It allows you to list and categorize the recorded postures.

- **-> Robot** allows you to send the selected position directly to your robot, and updates the interactive tab

- **Remove** removes the selected position from the list but does not remove the file

- **Delete file** deletes the selected position from the list as well as the file

- **Interactive <-** send the position to the *Interactive* tab but not to the robot

---

## File format position.json

[=> file_format_position](./file_format_position.md)

---

[<= Return](../../README_fr.md#position)
