# Changelog

## 2026-11-16

- Santa's Workshop is published on MakerWorld: [model page](https://makerworld.com/en/models/3622136-animated-santa-s-workshop-diorama-with-leds). Links added to the README and the license.

## 2026-11-15

- Firmware 3.14, the version for the published model. The ring moves in short steps (a quarter of a spot, 22 steps with random pauses of 0.6 to 2.5 s) and the arm swings towards the sleigh at every step, so ring and arm push the gift together; the gifts can sit on any free circle. A last quick turn carries in any gift left on the ring. Finale: every light swaps red and green for 10 s. Then ornament mode: the baubles breathe slowly through red, gold, green, blue and purple. Warmer lanterns that match the street lamp, brighter star. Removed: the timed stops and their settings (`FIRST_DEG`, `HOME_DEG`, `STOP_TRIM_S`, `ALIGN_S`, `ELF_NUDGE`).
- Firmware 3.6: before every gift the elf gets ready with two small 5° pushes of its arm (`ELF_NUDGE`); at the end only the sleigh lantern blinks red.
- Firmware 3.5: simpler show. The elf's arm goes across the track after loading and stays there: every gift that reaches it slides along it and drops, so the stops no longer need exact timing. No more feints or parade lap. `RING_SPEED` -50 (two turns in 17.9 s with six gifts, `RING_TURN_S` 8.94, `STOP_TRIM_S` 0.28). New `HOME_DEG`: after the sixth gift the ring finishes its turn, so the next switch-on finds a circle under the arm.
- Assembly guide: at power-on check that the arm rests over a ring circle (step 30); step 31 shows the new show.
- Firmware 2.8: shorter, steadier stops (`START_LAG_MS` 250), the arm holds for 1.5 s after the ring stops so the gift lands first (`DROP_HOLD_MS`), brighter tree (star twinkles between 55% and 100%, baubles never go below 15%).
- Firmware 2.7: `RING_SPEED` back to -30, because at -20 the real kit stalls with six gifts on the ring. `RING_TURN_S` 9.46 s, measured at -30 with six gifts (two turns in 18.9 s).

## 2026-11-14

- Firmware 2.6: quieter ring (`RING_SPEED` -20) with the turn time measured on the real kit (`RING_TURN_S` 17.7 s; the old 60 s estimate made several gifts drop at once). Dimmer lanterns, baubles blink when a gift lands, red blink for one minute at the end and then the lights stay on, elf servo released at rest so it does not buzz.
- Firmware 2.5: `RING_SPEED` is now -30, because with +30 the real kit turned the ring clockwise.
- Assembly guide now 31 steps: the lamp post is built in hand first, then set on the base; step 10 explains Thonny with screenshots; the tree base gets its LEDs first. All cables go on the receiver before it is screwed down.
- Assembly guide: cable routes redrawn so no cable passes through a part; tools named in the guide (1.5 mm hex key for the kit M2.5 × 6 screws, small Phillips screwdriver for the servo screws and the centre screw).
- Firmware 2.4 made compact (7 KB instead of 12 KB, same code): the core has little memory to compile it. The long explanations moved to firmware/README.md. Tested again on the real core.
- Firmware 2.4: one gift at a time at random moments, no parade turn. Before a gift the elf sometimes fakes once or twice: the arm swings into the empty spot and back out, the ring stays still and nothing drops. New "How it runs" animation.
- Base reprint round: the workshop LED now goes in from below into a seat in the base, held by a new white U clip (151 printed parts). The lantern and street lamp glasses have four small posts that hold their LEDs. Screw holes for the kit M2.5 screws are 2.3 mm. Guide steps 15, 16, 17, 19 and 20 updated; print time about 24.6 h and 736 g of PLA.

## 2026-11-13

- Firmware 2.2: the elf works at random moments. A random wait of 8 to 25 seconds before each gift and, now and then, a full parade turn of the ring with the arm out. A simulation of 200,000 switch-ons found no case where the arm comes down on a gift or a gift is left on the ring. Run on the real core without servos connected; still to be tested on the assembled diorama.
- New "How it runs" animation that follows firmware 2.2.
- Servos lowered: new servo brackets for the drive and the elf, fixed with screws from below; new pinion and elf arm with a round spigot through the deck hole (the real servo boss did not pass the old hole). New magnet pocket in the gift boxes. Guide steps 4, 5, 11 and 18 updated, PDFs, interactive guide and all-steps GIF regenerated.
- New README: animated banner, numbers, assembly guide card, electronics card and badges.

## 2026-11-12

- Servo brackets: notch for the servo wires in the bracket hole, so the servo goes in with its wires. Guide step 4 updated.
- Assembly guide rebuilt: 30 steps, Italian and English, interactive page and PDF, with the emanuele tech brand colours and logo.
- Guide fixes from the real assembly: battery and strap go on the lid before the lid goes on the base; on each tree tier the baubles go on after the first garland.
- Charging door and gift drawer: fronts that overlap the wall, so no gap shows; plinth on the bottom lid under the drawer.
- Charging door hooked on the two posts behind the opening, printed upright.
- Square keys print without brim.

## 2026-11-11

- Firmware 2.1: the elf servo is set to its start angle before the first slow move (2.0 stopped at the first arm move on the real core).
- All keys shorter with chamfered edges, plus a printed press tool that seats each key at the right depth.
- Pull tabs on the gift drawer and the charging door.
- Looser ring holes and deeper peg holes on the elf and Santa figures; left and right tags on the kit cards.
- Deeper logo engraving on the bottom lid; lantern and lamp glasses with more clearance.

## 2026-10-31

- Firmware 2.0: the elf's arm swings in and out while the ring is still.
- Small parts grouped on kit cards, one card per colour.
