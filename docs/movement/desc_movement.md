# Movements

A movement is a sequence of positions using predefined functions.

## Creating a movement

1. Under the bank of movements, click on **New**

    - Indicate the name of your movement

    - The default time base

2. Select the position to insert by simple click in the bank of positions

3. Choose the transformation function

4. Configure the function according to your needs, then click on **insert**

5. repair these operations to insert a new position

6. Click on **Save as** to save your movement

    - You must click on **save as** in order to save it in the movement bank, you can cancel saving the file if you wish.

<img alt="new_movement.win" width="60%" src="./img_doc1_new_movement.png" />

---

## The different transformation functions

### Direct (x)

Direct application of the position without any notion of duration.

Setting:

- No.

### Linear (x)

Movement to the position in x ms. Calculates the *pitch* of each servo motor so that all servo motors arrive at the same time.

Setting:

- The Duration in ms

### Oscillator (A, O, T, Ph)

Sinusoidal oscillator based on the oscillator.h library

Settings:

- Duration: Period in milliseconds
- Cycle: Number of loops
- A: Amplitude in degrees
- O: Offset in degrees
- Phase Diff: Phase shift

<img alt="oscillator.win" width="50%" src="./img_doc2_oscillator.png" />

---

## Actions on movements

Select your movement in the bank, the details of the positions and transformation function is displayed below with the following buttons:

<img alt="manage_movement.win" width="50%" src="./img_doc3_manage_movement.png" />

- Delete Line: deletes the selected position line
- Play One: Play only the selected position
- Up: Move the position one line above
- Down: Move the position one line down
- Play All: Play the whole movement
- Save as: Save your movement
- Export to C: Transform your movement into C code
    <img alt="export to C" width="100%" src="./img_doc4_export_c.png" />

---

## Movement management

Select your movement in the bank:

- New: Creation of a new movement
- Remove: Removes the transaction from the bank, but not the file
- Delete file: Deletes the file and the movement in the bank

<img alt="manage_bank" width="50%" src="./img_doc5_manage_bank.png" />

---

## Format of the movement.json file

[=> file_format_movement](./file_format_movement.md)

---

[<= Return](../../README.md#movement)
