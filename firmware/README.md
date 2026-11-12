# Firmware

`main.py` is the standalone program for the CyberBrick core on the receiver shield (ESP32-C3, MicroPython, Bambu `bbl` library). Current version: 2.1.

It needs no remote and no buttons: switch on and the show starts. The full description of the sequence, the wiring and every setting is in the comment block at the top of `main.py`.

## Wiring

| Receiver port | Goes to |
| --- | --- |
| Servo 2 | 360° servo that drives the gift ring |
| Servo 3 | 180° servo of the elf's arm |
| LED2 / D2 | Left LED hub: socket 1 workshop, socket 2 street lamp |
| LED1 / D1 | Right LED hub: socket 1 tree star, socket 2 tree baubles, socket 3 sleigh lantern, socket 4 elf's lantern |
| Power | Battery, then switch, then the XH socket of the receiver |

Hub sockets are numbered from the white input connector.

## Loading the program

1. Connect the core to a computer with a USB-C data cable, through the window in the front of the base.
2. Open the board in Thonny (or another MicroPython editor) and save `main.py` on the board as `/main.py`.
3. To start it at power-on, open the board's `boot.py`, keep a copy of the original, and replace the call to the official app with:

   ```python
   import main
   main.main()
   ```

To go back to the official CyberBrick app, restore the original `boot.py`.

## Settings to check on the first run

- `RING_TURN_S`: seconds for one full turn of the ring. There is no sensor, so the stops depend on this value. Time one turn with a charged battery and write it here.
- `RING_SPEED`: the ring must turn counter-clockwise seen from above. Flip the sign if it does not.
- `ELF_DIR`: the arm must swing out towards Santa and the sleigh. If it swings towards the tree, switch off at once and set `-1`.
- `ELF_WORK`: the angle with the arm across the track. Trim by a few degrees until it lies on its line.

## Test status

Version 2.1 ran on a real core from memory, without servos and LEDs connected, with no errors. Saving it on the board with the `boot.py` change, and a run with the whole diorama connected, are still to be done. See the [roadmap](../ROADMAP.md).
