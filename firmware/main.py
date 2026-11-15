# Santa's Workshop - standalone program for the CyberBrick core (MicroPython, bbl library). v3.14
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
RING_SPEED = -50         # -100..100; minus = ring counter-clockwise seen from above on the real kit (-50: enough push to pull a gift off its magnet; -20 stalls)
LOAD_S = 25              # seconds to load the gifts after switching on
RING_TURN_S = 8.94       # seconds for ONE full ring turn at RING_SPEED (measured on the real kit at -50 with 6 gifts: 2 turns 17.9 s; no precision needed)
ELF_WORK = 90            # elf servo angle with the arm across the track
ELF_DIR = 1              # +1 or -1: side the arm swings out (towards Santa, away from the tree)
ELF_OUT = 28             # degrees from ELF_WORK to the rest position over the snow
ELF_SWING_MS = 1600      # time for one arm swing
STEP_DEG = 360.0 / 28    # one ring step = a quarter of a spot: the gift at the blade slides a little further at every step
MOVES = 22               # ring steps per show: with the gifts loaded on the free circles they are usually all in by now
LAST_LAP_DEG = 150       # then one last quick turn without pauses: it carries in any gift still on the ring (0 = no last turn)
START_LAG_MS = 250       # extra ms per ring move: the ring starts from standstill at every stop
ELF_STEP_SPEED = 25      # arm swing speed (bbl stepping)
ELF_BACK = 5             # between ring steps the blade waits this many degrees towards the tree, ready for the next gift (max 6: the tree garland is close)
ELF_PUSH = 8             # during every ring step the blade swings this many degrees towards the sleigh: ring and arm push the gift together
                         # (computed on the parts: more can push a gift off the track before the sleigh)
BRIGHT = 0.6             # 0..1 brightness of workshop, street lamp and lanterns (lower = longer battery)
WARM = (255, 140, 40)    # workshop
LAMP = (255, 200, 110)   # street lamp
LANTERN = (255, 105, 20)  # sleigh and elf lanterns: their small glass shows the LED whiter, so a warmer colour gives the same light as the lamp
                         # (still too white: lower the middle number; too orange: raise it)
LANTERN_BRIGHT = 0.45    # lanterns, part of BRIGHT (small glass, close to the eye: full power looks white)
STAR = (255, 255, 150)   # tree star (almost white: the most light the LED can give)
BAUBLES = (255, 60, 30)  # tree baubles during the show (red on purpose: the green tiers turn it gold)
BAUBLE_COLORS = ((255, 60, 30), (255, 170, 20), (30, 255, 40), (30, 90, 255), (190, 40, 255))
                         # ornament mode after the show: the baubles breathe slowly and take the next colour at every breath
                         # (red, gold, green, blue, purple; leave one colour only for no change)
BAUBLE_BREATH_MS = 5000  # ornament: one slow bauble breath
BAUBLE_LOW = 0.06        # ornament: dimmest point of the breath (the colour changes here)
TREE_BRIGHT = 1.0        # tree LEDs power: star and baubles always at full power
STAR_MODE = 'twinkle'    # 'twinkle' (soft blink), 'blink' (sharp on and off) or 'steady'
STAR_BREATH_MS = 1400    # twinkle: one blink, dim to bright and back
STAR_LOW = 0.1           # twinkle: dimmest point
STAR_HIGH = 1.0          # twinkle: brightest point
STAR_SPARKLE_MS = 5300   # twinkle: a short sparkle this often
STAR_BLINK_MS = 600      # blink: on and off time
PAUSE_MIN_S = 0.6        # random wait before each ring step, seconds (min, max)
PAUSE_MAX_S = 2.5
DONE_MODE = 'xmas'       # lights when all gifts are in: 'xmas' = every light swaps red and green, 'red' = every light blinks red,
                         # 'sleigh' = only the sleigh lantern blinks red
DONE_BLINK_S = 10        # seconds of that finale, then the normal lights come back and stay on
DONE_STEP_MS = 500       # finale: time of one colour
IDLE_MOVE = False        # after the show the diorama stays on as an ornament. False = lights only, nothing moves, arm at rest;
                         # True = the ring keeps making a short step now and then with the elf arm (a gift put back on the ring goes into the sleigh again)
IDLE_MIN_S = 8           # ornament: random wait between two ring steps, seconds (min, max)
IDLE_MAX_S = 20
ELF_RELEASE = True       # arm standing still: servo signal off, no holding buzz (the arm has no load there)
L_WORKSHOP, L_LAMP1 = 0, 1                        # left hub (D2): socket number - 1
L_STAR, L_BAUBLES, L_SLEIGH, L_ELF = 0, 1, 2, 3   # right hub (D1)
# --------------------------------------------------------------------------

servos = ServosController()
left = LEDController("LED2").np
right = LEDController("LED1").np
RED, GREEN, OFF = (255, 0, 0), (0, 255, 0), (0, 0, 0)


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


def leds(t_ms, state):
    lamp = scale(LANTERN, LANTERN_BRIGHT)        # the two lanterns: steady, tuned to look like the street lamp
    left[L_WORKSHOP] = scale(WARM, flicker(t_ms, 90, 7919))
    left[L_LAMP1] = scale(LAMP, 1.0)
    right[L_STAR] = scale(STAR, star_level(t_ms) * TREE_BRIGHT / BRIGHT)
    if state == 'idle':                          # ornament: slow breath, a new colour at every breath
        ph = (t_ms % BAUBLE_BREATH_MS) / BAUBLE_BREATH_MS
        tri = 1.0 - abs(2.0 * ph - 1.0)
        k = BAUBLE_LOW + (1.0 - BAUBLE_LOW) * tri * tri * (3 - 2 * tri)
        col = BAUBLE_COLORS[(t_ms // BAUBLE_BREATH_MS) % len(BAUBLE_COLORS)]
        right[L_BAUBLES] = scale(col, k * TREE_BRIGHT / BRIGHT)
    else:
        right[L_BAUBLES] = scale(BAUBLES, TREE_BRIGHT / BRIGHT)
    right[L_ELF] = lamp; right[L_SLEIGH] = lamp
    if state == 'load':                          # green lanterns: load the gifts
        g = scale(GREEN, 1.0) if (t_ms // 400) % 2 else OFF
        right[L_ELF] = g; right[L_SLEIGH] = g
    elif state == 'done':                        # all gifts are in
        ph = (t_ms // DONE_STEP_MS) % 2
        if DONE_MODE == 'sleigh':
            right[L_SLEIGH] = scale(RED, 1.0) if ph else OFF
        else:
            if DONE_MODE == 'red':
                a = b = RED if ph else OFF
            else:
                a, b = (RED, GREEN) if ph else (GREEN, RED)
            left[L_WORKSHOP] = scale(a, 1.0); left[L_LAMP1] = scale(b, 1.0)
            right[L_SLEIGH] = scale(a, 1.0); right[L_ELF] = scale(b, 1.0)
            right[L_STAR] = scale(a, TREE_BRIGHT / BRIGHT); right[L_BAUBLES] = scale(b, TREE_BRIGHT / BRIGHT)
    left[2] = left[3] = OFF
    left.write(); right.write()


def wait(ms, t0, state):
    """Runs servos and lights for ms milliseconds."""
    end = utime.ticks_add(utime.ticks_ms(), int(ms))
    while utime.ticks_diff(end, utime.ticks_ms()) > 0:
        servos.timing_proc()
        now = utime.ticks_ms()
        leds(utime.ticks_diff(now, t0), state)
        utime.sleep_ms(10)


def ring_turn(deg, t0, push=ELF_PUSH, state='show'):
    """Turns the ring by about deg degrees (timed) and stops it; the elf arm swings towards the sleigh in the same moment."""
    servos.set_speed(2, RING_SPEED)
    servos.set_angle_stepping(3, ELF_WORK + ELF_DIR * push, ELF_STEP_SPEED)
    wait(int(deg / 360.0 * RING_TURN_S * 1000 + START_LAG_MS), t0, state)
    servos.stop(2)
    wait(300, t0, state)


def arm(angle, t0, state):
    servos.set_angle_stepping(3, angle, ELF_STEP_SPEED)
    wait(ELF_SWING_MS, t0, state)


def arm_rest(rest, t0, state):
    arm(rest, t0, state)
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
        servos.set_angle(3, ELF_WORK)            # arm across the track at once, and it stays there: the ring can start anywhere
        servos.set_angle_stepping(3, ELF_WORK - ELF_DIR * ELF_BACK, ELF_STEP_SPEED)   # waiting a little towards the tree
        wait(LOAD_S * 1000, t0, 'load')          # green lanterns: put the gifts on the free circles
        for move in range(MOVES):
            wait(rand_ms(PAUSE_MIN_S, PAUSE_MAX_S), t0, 'show')   # a different wait every time
            ring_turn(STEP_DEG, t0)              # ring and arm together: the gift slides along the blade and drops into the sleigh
            servos.set_angle_stepping(3, ELF_WORK - ELF_DIR * ELF_BACK, ELF_STEP_SPEED)   # the arm goes back towards the tree for the next gift
            wait(500, t0, 'show')
        if LAST_LAP_DEG:
            wait(int(PAUSE_MIN_S * 1000), t0, 'show')
            ring_turn(LAST_LAP_DEG, t0, 0)       # last quick turn, blade straight across: any gift still on the ring goes in
            servos.set_angle_stepping(3, ELF_WORK - ELF_DIR * ELF_BACK, ELF_STEP_SPEED)
            wait(500, t0, 'show')
        if not IDLE_MOVE:
            arm_rest(rest, t0, 'show')
        wait(DONE_BLINK_S * 1000, t0, 'done')   # finale: all gifts are in the sleigh
        while True:                              # ornament: the lights stay on, the baubles breathe and change colour
            if not IDLE_MOVE:
                wait(1000, t0, 'idle')
                continue
            if ELF_RELEASE:
                servos.stop(3)                   # quiet while waiting; the arm stays across the track
            wait(rand_ms(IDLE_MIN_S, IDLE_MAX_S), t0, 'idle')
            ring_turn(STEP_DEG, t0, ELF_PUSH, 'idle')   # a slow carousel: a gift put back on the ring goes into the sleigh again
            servos.set_angle_stepping(3, ELF_WORK - ELF_DIR * ELF_BACK, ELF_STEP_SPEED)
            wait(500, t0, 'idle')
    finally:
        servos.stop(1); servos.stop(2); servos.stop(3)
        left.fill((0, 0, 0)); right.fill((0, 0, 0)); left.write(); right.write()


if __name__ == "__main__":
    main()
