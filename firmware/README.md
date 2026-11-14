# Firmware

`main.py` is the standalone program for the CyberBrick core on the receiver shield (ESP32-C3, MicroPython, Bambu `bbl` library). Current version: 2.6 (ring speed and turn time measured on the real kit, still to be tested as a full show on the assembled diorama).

It needs no remote and no buttons: switch on and the show starts. `main.py` is kept short on purpose, because the core has little memory to compile it: every setting has a one-line comment there, and this page explains the rest.

## The show

1. Switch on with the ring empty. The lights start and the lanterns blink green: put the six gifts on the ring, leaving empty the spot in front of the elf.
2. The ring makes a first move and stops with the empty spot in front of the elf.
3. For each gift the elf waits a random time with its arm out. Now and then it fakes once or twice: the arm swings into the empty spot and back out while the ring stays still, so nothing drops. Then the arm swings in for real, the ring moves one spot, the next gift is pushed into the sleigh and the arm swings out again. The ring always stops with the gifts on their magnets.
4. Each time a gift lands the tree baubles blink, then dim one step. After the sixth gift the lanterns blink red for a minute, then the normal lights stay on: open the drawer and take the gifts.

A show lasts about 2.5 to 4 minutes.

The randomness is set at the top of `main.py`:

| Setting | Default | What it does |
| --- | --- | --- |
| `PAUSE_MIN_S`, `PAUSE_MAX_S` | 8, 25 | Random wait before each gift, in seconds. |
| `FEINT_CHANCE` | 45 | Chance in % that the elf fakes before a gift. Set 0 to turn the feints off. |
| `FEINT_MAX` | 2 | Most feints before one gift. |
| `FEINT_HOLD_S` | 1 | Seconds the arm stays in during a feint. |

The ring has no sensor: its position comes from the time, so measure `RING_TURN_S` well. The whole show is only six spots of travel, less than one turn, and a feint never moves the ring. The gifts always drop in the order they sit on the ring: a truly random order would need the arm to land between two gifts, and with a timed ring that is not reliable.

## All settings

They are at the top of `main.py`.

| Setting | Default | What it does |
| --- | --- | --- |
| `RING_SPEED` | -20 | Ring servo speed, -100 to 100. Seen from above the ring must turn counter-clockwise, so the gifts move from the front towards the elf: on the real kit that is a negative value. Flip the sign if it does not. Lower is quieter. Slower means more time between two gifts. |
| `LOAD_S` | 25 | Seconds to load the gifts after switching on. |
| `RING_TURN_S` | 17.7 | Seconds for one full turn of the ring at `RING_SPEED`, measured on the real kit at -20 (two turns in 35.4 s). Every stop depends on it: if you change `RING_SPEED`, time two turns with a phone and a charged battery and write half here. |
| `ELF_WORK` | 90 | Elf servo angle with the arm across the track (the assembly position). |
| `ELF_DIR` | 1 | Side the arm swings out: towards Santa and the sleigh, away from the tree. |
| `ELF_OUT` | 28 | Degrees from `ELF_WORK` to the rest position over the snow. The model is free from 0 to 34. |
| `ELF_SWING_MS` | 1600 | Time for one arm swing. The ring is always still meanwhile. |
| `ALIGN_S` | 3 | Seconds the arm stays across the track at power-on, to check the assembly angle. |
| `FIRST_DEG` | 29.9 | First ring move, from the loading position to the stop with the empty spot in front of the elf. |
| `STOP_TRIM_S`, `START_LAG_MS` | 0 | Small corrections added to every ring move if the stops come early or late. |
| `ELF_STEP_SPEED` | 25 | Arm swing speed (bbl stepping speed, about 39 degrees per second). |
| `BRIGHT` | 0.6 | Overall LED brightness, 0 to 1. Lower means longer battery life. |
| `LANTERN_BRIGHT` | 0.35 | Sleigh and elf lanterns, as a part of `BRIGHT`: they sit close to the eye. |
| `WARM`, `LAMP`, `STAR`, `BAUBLES` | | Colours of the workshop, lamps and lanterns, tree star and baubles. The bauble colour is nearly red on purpose: the green tree tiers tint it, and it comes out warm gold. |
| `TREE_BRIGHT` | 1.0 | Power of the two tree LEDs. |
| `BAUBLE_LEVELS` | | Bauble brightness after 0 to 6 gifts, in equal steps for the eye. |
| `STAR_MODE` | `'twinkle'` | `'twinkle'` (slow breathing with a short sparkle), `'blink'` or `'steady'`. `STAR_BREATH_MS`, `STAR_LOW`, `STAR_SPARKLE_MS` and `STAR_BLINK_MS` tune it. |
| `PAUSE_MIN_S`, `PAUSE_MAX_S` | 8, 25 | Random wait before each gift, in seconds. |
| `FEINT_CHANCE`, `FEINT_MAX`, `FEINT_HOLD_S` | 45, 2, 1 | The elf's feints, see above. |
| `GIFT_FLASH_MS` | 900 | The baubles blink when a gift lands in the sleigh. 0 turns it off. |
| `DONE_BLINK_S` | 60 | Seconds of red blinking after the last gift, then the normal lights stay on. |
| `ELF_RELEASE` | True | At rest the elf servo signal is switched off, so it does not buzz. The arm has no load over the snow. |

The arm finds the empty spot if the ring stops within about 12 degrees of where it should, which is about 0.6 seconds on a 17.7-second turn: that is why `RING_TURN_S` must be measured.

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

Version 2.4 ran on the real core from memory (14 November 2026), without servos and LEDs connected, with no errors. The ring speed and turn time of 2.6 were measured on the real kit. Saving it on the board with the `boot.py` change and a full show on the assembled diorama are still to be done. See the [roadmap](../ROADMAP.md).
