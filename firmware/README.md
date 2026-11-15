# Firmware

`main.py` is the standalone program for the CyberBrick core on the receiver shield (ESP32-C3, MicroPython, Bambu `bbl` library). Current version: 3.14.

It needs no remote and no buttons: switch on and the show starts. `main.py` is kept short on purpose, because the core has little memory to compile it: every setting has a one-line comment there, and this page explains the rest.

## The show

1. Switch on. The elf's arm goes across the track at once and stays there, waiting a few degrees towards the tree. The lanterns blink green: you have 25 seconds to put the six gifts on the free circles you can see (the circle inside the little house stays empty).
2. The ring moves in short steps, a quarter of a spot each, with a short random pause between them. At every step the arm swings a little towards the sleigh while the ring turns: ring and arm push the gift at the blade together, it slides along the arm and drops into the sleigh. Then the arm goes back towards the tree for the next gift.
3. After 22 steps the ring makes one last quick turn without pauses, which carries in any gift still on the ring.
4. Finale: every light swaps red and green for ten seconds. Then the diorama stays on as an ornament: the normal lights come back, the star twinkles and the tree baubles breathe slowly, taking a new colour at every breath (red, gold, green, blue, purple). Open the drawer and take the gifts.

The show lasts about a minute and a half after loading. The ring has no sensor and the gifts can sit on any circle: the arm stays across the track the whole time, so the timing does not need to be exact.

## All settings

They are at the top of `main.py`.

| Setting | Default | What it does |
| --- | --- | --- |
| `RING_SPEED` | -50 | Ring servo speed, -100 to 100. Seen from above the ring must turn counter-clockwise, so the gifts move from the front towards the elf: on the real kit that is a negative value. Flip the sign if it does not. At -50 the ring has enough push to pull a gift off its magnet; at -20 it stalls. |
| `LOAD_S` | 25 | Seconds to load the gifts after switching on. |
| `RING_TURN_S` | 8.94 | Seconds for one full turn of the ring at `RING_SPEED`, measured on the real kit at -50 with six gifts (two turns in 17.9 s). No precision is needed. |
| `ELF_WORK` | 90 | Elf servo angle with the arm across the track (the assembly position). |
| `ELF_DIR` | 1 | Side the arm swings out: towards Santa and the sleigh, away from the tree. |
| `ELF_OUT` | 28 | Degrees from `ELF_WORK` to the rest position over the snow, used at the end of the show. |
| `ELF_SWING_MS` | 1600 | Time for one full arm swing. |
| `STEP_DEG` | 12.9 | One ring step: a quarter of a spot (360 / 28). The gift at the blade slides a little further at every step. |
| `MOVES` | 22 | Ring steps in one show. With the gifts on the free circles they are usually all in by then. |
| `LAST_LAP_DEG` | 150 | One last quick turn without pauses, which carries in any gift still on the ring. 0 turns it off. |
| `START_LAG_MS` | 250 | Extra time for every ring move, because the ring starts from standstill at each stop. |
| `ELF_STEP_SPEED` | 25 | Arm swing speed (bbl stepping speed). |
| `ELF_BACK` | 5 | Between steps the blade waits this many degrees towards the tree, ready for the next gift. Keep it at 6 or less: the tree garland is close. |
| `ELF_PUSH` | 8 | During every ring step the blade swings this many degrees towards the sleigh, so ring and arm push the gift together. More can push a gift off the track before the sleigh. |
| `BRIGHT` | 0.6 | Brightness of the workshop, street lamp and lanterns, 0 to 1. Lower means longer battery life. |
| `WARM`, `LAMP` | | Colours of the workshop and the street lamp. |
| `LANTERN`, `LANTERN_BRIGHT` | orange, 0.45 | Colour and power of the sleigh and elf lanterns. Their small glass shows the LED whiter, so a warmer colour gives the same light as the street lamp. Too white: lower the middle number; too orange: raise it. |
| `STAR`, `BAUBLES` | | Colours of the tree star (almost white, the most light the LED gives) and of the baubles during the show (nearly red on purpose: the green tiers turn it gold). |
| `TREE_BRIGHT` | 1.0 | Power of the two tree LEDs. |
| `STAR_MODE` | `'twinkle'` | `'twinkle'` (soft blink), `'blink'` (sharp on and off) or `'steady'`. `STAR_BREATH_MS`, `STAR_LOW`, `STAR_HIGH`, `STAR_SPARKLE_MS` and `STAR_BLINK_MS` tune it. |
| `BAUBLE_COLORS` | red, gold, green, blue, purple | Ornament mode after the show: the baubles breathe slowly and take the next colour at every breath. Leave one colour for no change. `BAUBLE_BREATH_MS` and `BAUBLE_LOW` tune the breath. |
| `PAUSE_MIN_S`, `PAUSE_MAX_S` | 0.6, 2.5 | Random pause before each ring step, in seconds. |
| `DONE_MODE` | `'xmas'` | Finale when all gifts are in: `'xmas'` every light swaps red and green, `'red'` every light blinks red, `'sleigh'` only the sleigh lantern blinks red. |
| `DONE_BLINK_S`, `DONE_STEP_MS` | 10, 500 | Length of the finale in seconds, and time of one colour in milliseconds. |
| `IDLE_MOVE` | False | After the show: `False` keeps only the lights on, nothing moves and the arm rests. `True` makes the ring take a short step now and then, so a gift put back on the ring goes into the sleigh again. `IDLE_MIN_S` and `IDLE_MAX_S` set the wait. |
| `ELF_RELEASE` | True | When the arm stands still its servo signal is switched off, so it does not buzz. |

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

This folder has the two files the core needs: [`main.py`](main.py) (the show) and [`boot.py`](boot.py) (starts the show at power-on). [`santa_workshop_mpy.zip`](santa_workshop_mpy.zip) holds the same two files in one download.

1. Connect the core to a computer with a USB-C data cable, through the window in the front of the base.
2. Open the board in Thonny (or another MicroPython editor). Step 10 of the [assembly guide](https://emanueletech.github.io/santas-workshop/) shows every click.
3. Save `main.py` and `boot.py` on the core, in its main folder, with the same names. Before you overwrite `boot.py`, keep a copy of the original.
4. Switch off and on again: the show starts by itself.

To go back to the official CyberBrick app, put the original `boot.py` back on the core.

## Settings to check on the first run

- `RING_SPEED`: the ring must turn counter-clockwise seen from above. Flip the sign if it does not.
- `ELF_DIR`: at the end of the show the arm must swing out towards Santa and the sleigh. If it swings towards the tree, switch off at once and set `-1`.
- `ELF_WORK`: the angle with the arm across the track. Trim by a few degrees until it lies on its line.

## Test status

Version 3.14 runs the full show on the assembled diorama (15 November 2026). See the [roadmap](../ROADMAP.md).
