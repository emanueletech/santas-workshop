# Santa's Workshop - standalone program for the CyberBrick receiver (ESP32-C3, MicroPython, bbl library). v2.2
# Automatic: no buttons and no remote. Switch on and the diorama runs by itself.
# Upload: connect the core to the computer with a USB-C cable (through the window in the front of the base), open it in
# Thonny (or the CyberBrick web editor) and save this file on the board as /main.py. To start it at power-on, open the board's
# boot.py, keep a copy of the original, and replace the official app call with these two lines:
#     import main
#     main.main()
#
# Wiring (receiver shield XA004, seen from the front of the base: D2 left, D1 right):
#   Servo 1 (GPIO3) -> not used (v1.9: the tree does not turn any more, it lights up from inside)
#   Servo 2 (GPIO2) -> 360 deg servo driving the ring pinion
#   Servo 3 (GPIO1) -> 180 deg servo of the elf's arm (blade)
#   LED2 / D2 (GPIO20) -> LEFT LED hub:  socket 1 = workshop, socket 2 = street lamp 1
#   LED1 / D1 (GPIO21) -> RIGHT LED hub: socket 1 = tree star (LED under the white tube), socket 2 = tree baubles (LED inside
#                         the trunk), socket 3 = sleigh lantern, socket 4 = elf's lantern (v1.9)
#   (hub sockets are numbered from the white input connector; always use the first sockets, without gaps)
#   Power: battery -> switch -> XH2.54 socket of the receiver
#
# What it does (v2.0, 31/10: the elf's arm swings in and out, Manu's option A):
#   1. Switch on with the ring EMPTY: lights start (tree star and all 6 baubles lit). The elf puts the arm across the track
#      for ALIGN_S seconds (the assembly position, check it lies on its line), then swings it out over the snow.
#   2. LOAD_S seconds to load the gifts (the two lanterns blink green): put the 6 gifts on 6 of the 7 marked spots of the
#      ring (the magnets snap them in place); leave EMPTY the spot in front of the elf (where the arm lies when it is in).
#   3. v2.2 (Manu 31/10, done 13/11): the elf works at RANDOM moments. The ring turns FIRST_DEG degrees and stops with the
#      gap in front of the elf. Then, for each of the six gifts: a random pause with the arm out (PAUSE_MIN_S..PAUSE_MAX_S);
#      sometimes the ring first parades the gifts one full turn with the arm out (PARADE_CHANCE, at most once: MAX_SPOTS)
#      and stops again with the same gap in front of the elf; then the elf swings the arm in, the ring turns one spot (one gift is pushed off and drops through the
#      sleigh into the drawer, the baubles go down one step), the ring stops, the elf swings the arm out again. The arm
#      only moves while the ring is still, and only into an empty spot with a gift right behind it.
#      There is no sensor: the ring position comes from the time, so RING_TURN_S must be measured (see CONFIG). The arm
#      finds its gap if the ring is within about 12 degrees (2 s on a 60 s turn) of where it should be (MuJoCo simulation
#      31/10). Timing errors add up with every move, so the parades are capped at MAX_SPOTS spots in total (all moves
#      together, about two turns); if the arm comes down on a gift, measure RING_TURN_S again or trim STOP_TRIM_S.
#   4. After the 6th gift the lanterns blink red: open the drawer, take the gifts, switch off. Next time start empty.
import utime
try:
    import random
except ImportError:
    import urandom as random
try:
    import os
    random.seed(int.from_bytes(os.urandom(4), 'little'))   # a different show at every switch-on
except Exception:
    pass
from bbl.servos import ServosController
from bbl.leds import LEDController

# ----------------------------------------------------------------- CONFIG
RING_SPEED = 30          # -100..100. The ring must turn COUNTER-clockwise seen from above (gifts move from the front towards
                         # the elf): flip the sign if it doesn't. Slower = more time between two gifts.
LOAD_S = 25              # seconds to load the gifts after switching on
RING_TURN_S = 60.0       # seconds for ONE full turn of the ring at RING_SPEED: time it once with a phone and write it here
                         # with the battery charged (estimate from the gears: ~60 s). The stops depend on it: measure it well.
ELF_WORK = 90            # servo 3 angle with the blade across the track (assembly: column pressed on at this angle). Fine-tune
                         # by a few degrees until the blade lies exactly on its line (see the guide).
ELF_DIR = 1              # +1 or -1: the side the arm swings OUT. Out = towards Santa and the sleigh, away from the tree.
                         # FIRST RUN: watch the arm after ALIGN_S; if it swings towards the tree, switch off at once and set -1.
ELF_OUT = 28             # degrees from ELF_WORK to the rest position over the snow (model: free from 0 to +34)
ELF_SWING_MS = 1600      # time allowed for one swing in or out (ring always still meanwhile)
ALIGN_S = 3              # seconds the arm stays across the track at power-on (to check the assembly angle)
FIRST_DEG = 29.9         # ring degrees from the loading position to the first stop (gap in front of the elf)
STATION_DEG = 360.0 / 7  # one spot
STOP_TRIM_S = 0.0        # seconds added to every ring move (negative = shorter) if the stops come late or early
START_LAG_MS = 0         # extra milliseconds per move to make up for the servo's start, if the stops drift behind
ELF_STEP_SPEED = 25      # bbl stepping speed for the slow, gentle swing
BRIGHT = 0.6             # 0..1, overall LED brightness (lower = longer battery life)
WARM = (255, 140, 40)    # workshop
LAMP = (255, 200, 110)   # street lamps and lanterns
STAR = (255, 189, 49)    # tree star: warm white through the white tube and the translucent star (light simulation 29/10)
BAUBLES = (255, 46, 24)  # tree baubles (all six share one LED): nearly red on purpose, the green tiers tint the light green,
                         # so this comes out warm gold on the translucent baubles (light simulation 29/10)
TREE_BRIGHT = 1.0        # the two tree LEDs run at full power (only 2 LEDs: little battery)
BAUBLE_LEVELS = (1.0, 0.63, 0.36, 0.18, 0.08, 0.02, 0.0)   # brightness after 0..6 gifts: equal steps for the eye (CIE L*)
STAR_MODE = 'twinkle'    # 'twinkle' (Manu 30/10: slow breathing + a short sparkle every few seconds), 'blink' (on/off), 'steady'
STAR_BREATH_MS = 2400    # twinkle: one slow breath (dim -> bright -> dim)
STAR_LOW = 0.35          # twinkle: dimmest point of the breath (0..1)
STAR_SPARKLE_MS = 5300   # twinkle: a short full-power sparkle this often
STAR_BLINK_MS = 600      # blink: on and off times
SPOTS = 7                # gift spots on the ring (6 gifts + the empty one under the blade)
PAUSE_MIN_S = 3          # v2.2: random pause with the arm out before each gift (seconds, min and max)
PAUSE_MAX_S = 12
PARADE_CHANCE = 15       # v2.2: % chance, before each gift, that the ring first parades the gifts one full turn (arm out)
MAX_SPOTS = 14           # v2.2: cap on all ring moves together, in spots (14 = two turns): timing errors add up with travel
# LED index on each hub (socket number - 1)
L_WORKSHOP, L_LAMP1 = 0, 1                 # left hub  (D2 / LED2)
L_STAR, L_BAUBLES, L_SLEIGH, L_ELF = 0, 1, 2, 3   # right hub (D1 / LED1), v1.9 order
# --------------------------------------------------------------------------

servos = ServosController()
left = LEDController("LED2").np
right = LEDController("LED1").np


def scale(rgb, k):
    k *= BRIGHT
    return (int(rgb[0] * k), int(rgb[1] * k), int(rgb[2] * k))


def flicker(t_ms, period, seed):
    return 0.72 + 0.28 * ((t_ms // period) * seed % 100) / 100.0


def star_level(t_ms):
    """0..1 brightness of the star at time t_ms (STAR_MODE)."""
    if STAR_MODE == 'steady':
        return 1.0
    if STAR_MODE == 'blink':
        return 1.0 if (t_ms // STAR_BLINK_MS) % 2 == 0 else 0.0
    ph = (t_ms % STAR_BREATH_MS) / STAR_BREATH_MS              # triangle wave, eased: soft breathing
    tri = 1.0 - abs(2.0 * ph - 1.0)
    k = STAR_LOW + (0.8 - STAR_LOW) * tri * tri * (3 - 2 * tri)
    sp = t_ms % STAR_SPARKLE_MS
    if sp < 90 or 180 <= sp < 260:                              # double flash, like a glint
        k = 1.0
    return k


def leds(t_ms, state, done=0):
    left[L_WORKSHOP] = scale(WARM, flicker(t_ms, 90, 7919))          # fire in the workshop
    left[L_LAMP1] = scale(LAMP, 1.0)
    right[L_STAR] = scale(STAR, star_level(t_ms) * TREE_BRIGHT / BRIGHT)   # the star is always on (twinkling: STAR_MODE)
    right[L_BAUBLES] = scale(BAUBLES, BAUBLE_LEVELS[done] * TREE_BRIGHT / BRIGHT)   # one step down for every gift in the sleigh
    lantern = scale(LAMP, flicker(t_ms, 110, 104729))
    if state == 'load':
        g = scale((0, 255, 0), 1.0) if (t_ms // 400) % 2 else (0, 0, 0)
        right[L_ELF] = g; right[L_SLEIGH] = g
    elif state == 'done':
        red = scale((255, 0, 0), 1.0) if (t_ms // 500) % 2 else (0, 0, 0)
        right[L_ELF] = red; right[L_SLEIGH] = red
    else:
        right[L_ELF] = lantern; right[L_SLEIGH] = lantern
    left[2] = left[3] = (0, 0, 0)
    left.write(); right.write()


def wait(ms, t0, state, done=0):
    """Runs servos and lights for ms milliseconds."""
    end = utime.ticks_add(utime.ticks_ms(), ms)
    while utime.ticks_diff(end, utime.ticks_ms()) > 0:
        servos.timing_proc()                     # drives the stepping moves (call at ~100 Hz)
        now = utime.ticks_ms()
        leds(utime.ticks_diff(now, t0), state, 6 if state == 'done' else done)
        utime.sleep_ms(10)


def ring_turn(deg, t0, done):
    """Turns the ring by deg degrees (timed) and stops it."""
    servos.set_speed(2, RING_SPEED)
    wait(int(deg / 360.0 * RING_TURN_S * 1000 + STOP_TRIM_S * 1000 + START_LAG_MS), t0, 'show', done)
    servos.stop(2)
    wait(300, t0, 'show', done)                  # let the ring settle before the arm moves


def arm(angle, t0, state, done):
    servos.set_angle_stepping(3, angle, ELF_STEP_SPEED)
    wait(ELF_SWING_MS, t0, state, done)


def rand_ms(lo, hi):
    return int((lo + (hi - lo) * random.getrandbits(10) / 1023.0) * 1000)


def plan():
    """v2.2: list of 6 parades, one per gift, in spots (0 = no parade). Spots are numbered in the order they reach the elf:
    spot 0 is the empty one in front of the elf after FIRST_DEG, spots 1..6 carry the gifts. Before each delivery the spot
    in front must be empty and the next one must hold a gift. Total travel (parades + the 6 delivery moves) <= MAX_SPOTS."""
    gift = [False] + [True] * 6
    front, budget, out = 0, MAX_SPOTS - 6, []
    for left in range(6, 0, -1):
        good = [k for k in range(0, SPOTS + 1) if not gift[(front + k) % SPOTS] and gift[(front + k + 1) % SPOTS]]
        ok = [k for k in good if k <= budget] or good[:1]   # over budget: take the shortest move that works
        k = ok[0]
        far = [j for j in ok if j > 0]           # the gifts sit together, so in practice this is one full turn (7 spots)
        if far and random.getrandbits(7) < PARADE_CHANCE * 128 // 100:
            k = far[0]
        budget -= k
        front = (front + k + 1) % SPOTS          # the delivery move: the next spot comes in front, its gift drops
        gift[front] = False
        out.append(k)
    return out


def main():
    t0 = utime.ticks_ms()
    rest = ELF_WORK + ELF_DIR * ELF_OUT
    servos.stop(1)                               # v1.9: no tree servo
    servos.stop(2)                               # the ring only turns with the arm in
    try:
        servos.set_angle(3, ELF_WORK)            # assembly position: check the arm lies across the track. Direct move on
        wait(ELF_SWING_MS, t0, 'load', 0)        # purpose (v2.1): bbl needs set_angle once before set_angle_stepping works
        wait(ALIGN_S * 1000, t0, 'load')
        arm(rest, t0, 'load', 0)                 # out over the snow while loading
        wait(LOAD_S * 1000, t0, 'load')
        ring_turn(FIRST_DEG, t0, 0)              # gap in front of the elf
        for done, k in enumerate(plan(), 1):
            wait(rand_ms(PAUSE_MIN_S, PAUSE_MAX_S), t0, 'show', done - 1)   # the elf waits a random time, arm out
            if k:
                ring_turn(k * STATION_DEG, t0, done - 1)   # parade with the arm out: stops with a gap in front of the elf
                wait(rand_ms(1, 3), t0, 'show', done - 1)
            arm(ELF_WORK, t0, 'show', done - 1)  # swing in through the gap
            ring_turn(STATION_DEG, t0, done - 1) # one gift is pushed into the sleigh
            arm(rest, t0, 'show', done)          # swing out; baubles one step down
        while True:
            wait(1000, t0, 'done')
    finally:
        servos.stop(1); servos.stop(2); servos.stop(3)
        left.fill((0, 0, 0)); right.fill((0, 0, 0)); left.write(); right.write()


if __name__ == "__main__":
    main()
