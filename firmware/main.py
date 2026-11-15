# Santa's Workshop - standalone program for the CyberBrick core (MicroPython, bbl library). v2.8
# Switch on and the diorama runs by itself. Settings below; the show, wiring, upload steps and every
# setting are explained in firmware/README.md (github.com/emanueletech/santas-workshop).
# Save this file on the core as /main.py and start it from boot.py with: import main; main.main()
import utime
try:
    import random
except ImportError:
    import urandom as random
try:
    import os
    random.seed(int.from_bytes(os.urandom(4), 'little'))  # a different show at every switch-on
except Exception:
    pass
from bbl.servos import ServosController
from bbl.leds import LEDController

# ---------------------------------------------------------------- SETTINGS
RING_SPEED = -30         # -100..100; minus = ring counter-clockwise seen from above on the real kit (-20 stalls with 6 gifts)
LOAD_S = 25              # seconds to load the gifts after switching on
RING_TURN_S = 9.46       # seconds for ONE full ring turn at RING_SPEED (measured on the real kit at -30 with 6 gifts: 2 turns 18.9 s)
ELF_WORK = 90            # elf servo angle with the arm across the track
ELF_DIR = 1              # +1 or -1: side the arm swings out (towards Santa, away from the tree)
ELF_OUT = 28             # degrees from ELF_WORK to the rest position over the snow
ELF_SWING_MS = 1600      # time for one arm swing
ALIGN_S = 3              # seconds the arm stays across the track at power-on
FIRST_DEG = 29.9         # first ring move: brings the empty spot in front of the elf
STATION_DEG = 360.0 / 7  # one spot
STOP_TRIM_S = 0.0        # added to every ring move if the stops come late or early
START_LAG_MS = 250       # extra ms per ring move: the ring starts from standstill at every stop
ELF_STEP_SPEED = 25      # arm swing speed (bbl stepping)
DROP_HOLD_MS = 1500      # arm stays across the track after the ring stops, so the gift lands before it moves
BRIGHT = 0.6             # 0..1 LED brightness (lower = longer battery)
LANTERN_BRIGHT = 0.35    # sleigh and elf lanterns, part of BRIGHT (they sit close to the eye)
WARM = (255, 140, 40)    # workshop
LAMP = (255, 200, 110)   # street lamp and lanterns
STAR = (255, 189, 49)    # tree star
BAUBLES = (255, 46, 24)  # tree baubles (red on purpose: the green tiers turn it gold)
TREE_BRIGHT = 1.0        # tree LEDs power
BAUBLE_LEVELS = (1.0, 0.82, 0.66, 0.5, 0.36, 0.24, 0.15)  # baubles after 0..6 gifts
STAR_MODE = 'twinkle'    # 'twinkle', 'blink' or 'steady'
STAR_BREATH_MS = 2400    # twinkle: one slow breath
STAR_LOW = 0.55          # twinkle: dimmest point
STAR_HIGH = 1.0          # twinkle: brightest point
STAR_SPARKLE_MS = 5300   # twinkle: a short sparkle this often
STAR_BLINK_MS = 600      # blink: on and off time
SPOTS = 7                # gift spots on the ring (6 gifts + 1 empty)
PAUSE_MIN_S = 8          # random wait before each gift, seconds (min, max)
PAUSE_MAX_S = 25
FEINT_CHANCE = 45        # % chance the elf fakes before a gift (0 = never)
FEINT_MAX = 2            # most feints before one gift
FEINT_HOLD_S = 1         # seconds the arm stays in during a feint
GIFT_FLASH_MS = 900      # baubles blink when a gift lands in the sleigh (0 = no blink)
DONE_BLINK_S = 60        # red blink when all gifts are out, then the normal lights stay on
ELF_RELEASE = True       # arm at rest: servo signal off, no holding buzz (the arm has no load there)
L_WORKSHOP, L_LAMP1 = 0, 1                        # left hub (D2): socket number - 1
L_STAR, L_BAUBLES, L_SLEIGH, L_ELF = 0, 1, 2, 3   # right hub (D1)
# --------------------------------------------------------------------------

servos = ServosController()
left = LEDController("LED2").np
right = LEDController("LED1").np
_flash = [utime.ticks_ms()]


def scale(rgb, k):
    k *= BRIGHT
    return tuple(min(255, int(c * k)) for c in rgb)


def flicker(t_ms, period, seed):
    return 0.72 + 0.28 * ((t_ms // period) * seed % 100) / 100.0


def star_level(t_ms):
    """0..1 brightness of the star at time t_ms (STAR_MODE)."""
    if STAR_MODE == 'steady':
        return 1.0
    if STAR_MODE == 'blink':
        return 1.0 if (t_ms // STAR_BLINK_MS) % 2 == 0 else 0.0
    ph = (t_ms % STAR_BREATH_MS) / STAR_BREATH_MS
    tri = 1.0 - abs(2.0 * ph - 1.0)
    k = STAR_LOW + (STAR_HIGH - STAR_LOW) * tri * tri * (3 - 2 * tri)
    sp = t_ms % STAR_SPARKLE_MS
    if sp < 90 or 180 <= sp < 260:
        k = 1.0
    return k


def leds(t_ms, state, done=0):
    left[L_WORKSHOP] = scale(WARM, flicker(t_ms, 90, 7919))
    left[L_LAMP1] = scale(LAMP, 1.0)
    right[L_STAR] = scale(STAR, star_level(t_ms) * TREE_BRIGHT / BRIGHT)
    k = BAUBLE_LEVELS[done]
    if utime.ticks_diff(_flash[0], utime.ticks_ms()) > 0 and (t_ms // 150) % 2:
        k = 0.0
    right[L_BAUBLES] = scale(BAUBLES, k * TREE_BRIGHT / BRIGHT)
    lantern = scale(LAMP, flicker(t_ms, 110, 104729) * LANTERN_BRIGHT)
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
        servos.timing_proc()
        now = utime.ticks_ms()
        leds(utime.ticks_diff(now, t0), state, 6 if state == 'done' else done)
        utime.sleep_ms(10)


def ring_turn(deg, t0, done):
    """Turns the ring by deg degrees (timed) and stops it."""
    servos.set_speed(2, RING_SPEED)
    wait(int(deg / 360.0 * RING_TURN_S * 1000 + STOP_TRIM_S * 1000 + START_LAG_MS), t0, 'show', done)
    servos.stop(2)
    wait(300, t0, 'show', done)


def arm(angle, t0, state, done):
    servos.set_angle_stepping(3, angle, ELF_STEP_SPEED)
    wait(ELF_SWING_MS, t0, state, done)


def arm_rest(rest, t0, state, done):
    arm(rest, t0, state, done)
    if ELF_RELEASE:
        servos.stop(3)                           # quiet: no holding torque needed over the snow


def rand_ms(lo, hi):
    return int((lo + (hi - lo) * random.getrandbits(10) / 1023.0) * 1000)


def main():
    t0 = utime.ticks_ms()
    rest = ELF_WORK + ELF_DIR * ELF_OUT
    servos.stop(1)
    servos.stop(2)
    try:
        servos.set_angle(3, ELF_WORK)            # arm across the track; bbl needs set_angle before stepping
        wait(ELF_SWING_MS, t0, 'load', 0)
        wait(ALIGN_S * 1000, t0, 'load')
        arm_rest(rest, t0, 'load', 0)            # arm out: load the gifts (green lanterns)
        wait(LOAD_S * 1000, t0, 'load')
        ring_turn(FIRST_DEG, t0, 0)              # empty spot in front of the elf
        for done in range(1, 7):
            pause = rand_ms(PAUSE_MIN_S, PAUSE_MAX_S)
            feints = 0
            while feints < FEINT_MAX and random.getrandbits(7) < FEINT_CHANCE * 128 // 100:
                feints += 1
            for _ in range(feints):              # feint: arm into the empty spot and out, ring still
                wait(pause // (feints + 1), t0, 'show', done - 1)
                arm(ELF_WORK, t0, 'show', done - 1)
                wait(FEINT_HOLD_S * 1000, t0, 'show', done - 1)
                arm_rest(rest, t0, 'show', done - 1)
            wait(pause // (feints + 1), t0, 'show', done - 1)
            arm(ELF_WORK, t0, 'show', done - 1)
            ring_turn(STATION_DEG, t0, done - 1) # one gift drops into the sleigh
            _flash[0] = utime.ticks_add(utime.ticks_ms(), GIFT_FLASH_MS)
            wait(DROP_HOLD_MS, t0, 'show', done - 1)
            arm_rest(rest, t0, 'show', done)
        wait(DONE_BLINK_S * 1000, t0, 'done')   # red: all gifts are in the sleigh
        while True:
            wait(1000, t0, 'show', 6)            # then the normal lights stay on
    finally:
        servos.stop(1); servos.stop(2); servos.stop(3)
        left.fill((0, 0, 0)); right.fill((0, 0, 0)); left.write(); right.write()


if __name__ == "__main__":
    main()
