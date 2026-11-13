# Firmware

`main.py` is the standalone program for the CyberBrick core on the receiver shield (ESP32-C3, MicroPython, Bambu `bbl` library). Current version: 2.2 (run on the real core, still to be tested on the assembled diorama).

It needs no remote and no buttons: switch on and the show starts. The full description of the sequence, the wiring and every setting is in the comment block at the top of `main.py`.

## The show

1. Switch on with the ring empty. The lights start and the lanterns blink green: put the six gifts on the ring, leaving empty the spot in front of the elf.
2. The ring makes a first move and stops with the empty spot in front of the elf.
3. For each gift the elf waits a random time with its arm out. Now and then the ring first parades the gifts one full turn. Then the arm swings in, the ring moves one spot, the next gift is pushed into the sleigh and the arm swings out again.
4. After the sixth gift the lanterns blink red: open the drawer and take the gifts.

A show lasts about 2.5 to 4.5 minutes, about one minute more when the ring parades.

The randomness is set at the top of `main.py`:

| Setting | Default | What it does |
| --- | --- | --- |
| `PAUSE_MIN_S`, `PAUSE_MAX_S` | 8, 25 | Random wait before each gift, in seconds. |
| `PARADE_CHANCE` | 15 | Chance in % that the ring parades one full turn before a gift. Set 0 to turn parades off. |
| `MAX_SPOTS` | 14 | Limit on all ring moves together, in spots (two turns). |

The ring has no sensor: its position comes from the time, so measure `RING_TURN_S` well. Parades add travel, so they also add timing error. If the arm comes down on a gift after a parade, measure `RING_TURN_S` again or set `PARADE_CHANCE = 0`.

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
