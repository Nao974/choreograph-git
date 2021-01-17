# Determine the neutral position (trim)

When you assemble your robot, you will certainly position your servomotors on their median value and then mount the lifter. But it may not be oriented exactly the way you want it to.
You will therefore be able to increment or decrement the neutral position of your servomotors in order to place it in the desired position.

1. Before assembly, position your servo motors **on the neutral position** (90 ° between [0; 180]) from a small Arduino script (available on the internet)

2. Assemble your robot by placing each lifter in the middle position

3. Configure your JSON skeleton file as below for each servo motor then launch ***Choreograph***:

    - "offset": 0
    - "default_position": 90

    <img alt="json_init.trim" width="50%" src="./img_doc1_pos_init.png" />  

4. Load the firmware into your controller card [=> firmware](../firmware/desc_firmware.md)

5. For each servo motor, refine the position with the up / down arrows of each servo motor.
    <img alt="change_position.trim" width="50%" src="./img_doc2_pos_revised.png" />

6. Start the offset recalculation

    <div align="center"><img alt="recalculate.menu" width="29%" src="./img_doc3_menu_recalculate.png" />&nbsp;<img alt="recalculed.screen" width="70%" src="./img_doc4_win_recalculate.png" /></div>  

7. Update your JSON file by modifying the "offset" parameter of your servo motors with the value indicated in the recalculation

    ```json
    "YL":
        {
         ...
         "offset" : 6,
         "angle_limit": [0, 180],
         "default_position": 90,
         ...
        }
    ```

8. Reload your skeleton file using the Squelette-> Update menu

    <img alt="updated.trim" width="50%" src="./img_doc5_updated.png" />

---
[<= Return](../../README.md#desc-trim)
