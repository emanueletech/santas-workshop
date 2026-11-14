<p align="center">
  <img src="assets/banner.svg" alt="Santa's Workshop, a 3D printed Christmas diorama by emanuele tech" width="100%">
</p>

<p align="center">
  <img src="assets/badges/status.svg" height="28" alt="Status: work in progress">
  <img src="assets/badges/makerworld.svg" height="28" alt="MakerWorld exclusive">
  <img src="assets/badges/cyberbrick.svg" height="28" alt="CyberBrick, MicroPython">
  <img src="assets/badges/firmware.svg" height="28" alt="Firmware 2.6">
  <img src="assets/badges/guide.svg" height="28" alt="Guide in English and Italian">
</p>

<p align="center"><b>English</b> · <a href="README.it.md">Italiano</a></p>

<p align="center">
  <b>Switch it on and the workshop comes alive.</b><br>
  The tree lights up, the gift ring turns, and the elf pushes the gifts one by one through Santa's sleigh into a drawer. No remote, no buttons.
</p>

<p align="center">
  <a href="#-assembly-guide">Assembly guide</a> ·
  <a href="#-how-it-works">How it works</a> ·
  <a href="#-electronics">Electronics</a> ·
  <a href="#-firmware">Firmware</a> ·
  <a href="ROADMAP.md">Roadmap</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <img src="images/photos/night_full.jpg" alt="Santa's Workshop at night: the tree, the workshop, the lamp post and Santa's sleigh lit up" width="100%">
</p>

<p align="center">
  <img src="assets/stats.svg" alt="151 printed parts, 13 plates, 24.6 hours and 736 g of PLA, no glue, supports or AMS" width="100%">
</p>

## 🛠 Assembly guide

<p align="center">
  <a href="docs/pdf/Santas_Workshop_assembly_guide_EN.pdf"><img src="assets/guide_card.svg" alt="Assembly guide: 31 steps in 6 phases, English and Italian. Open the guide." width="100%"></a>
</p>

<p align="center">
  <a href="docs/pdf/Santas_Workshop_assembly_guide_EN.pdf"><img src="assets/badges/pdf_en.svg" height="28" alt="Assembly guide PDF in English"></a>
  <a href="docs/pdf/Santas_Workshop_guida_montaggio_IT.pdf"><img src="assets/badges/pdf_it.svg" height="28" alt="Guida di montaggio PDF in italiano"></a>
  <a href="docs/index.html"><img src="assets/badges/interactive.svg" height="28" alt="Interactive guide"></a>
</p>

Thirty-one steps, from snapping the keys off the kit cards to loading the first gifts. Every step has its own animation, the list of parts with the plate they come from, and the actions to tick off. The interactive guide is a single page with an English / Italian switch: download [`docs/index.html`](docs/index.html) together with the `docs/img` folder and open it in a browser.

<p align="center">
  <img src="assets/tools.svg" alt="Tools: a 1.5 mm hex key for the kit M2.5 x 6 screws, a small Phillips screwdriver for the servo and centre screws, and the key press tool printed with the model. No glue and no soldering." width="100%">
</p>

| Phase | Steps | What happens |
| :--- | :---: | :--- |
| **Preparation** | 1–3 | Keys and the press tool, magnets in the gift ring and in the gifts. |
| **Under the base** | 4–10 | Servos, switch, LED hubs and receiver, then the program and a first test. |
| **Scene on top** | 11–20 | Pinion, tree base, gift ring, snow cover, workshop, lamp post, sleigh and the elf. |
| **Lights and closing** | 21–25 | LEDs to the hubs, battery and bottom lid, gift drawer, charging door, USB plug. |
| **Figures and tree** | 26–29 | Santa, the snowman, the North Pole sign post and the tree, tier by tier. |
| **Switch on** | 30–31 | Load the gifts, switch on, and fine tune the show. |

<details>
<summary><b>Watch all 31 steps in one animation</b> (5 MB)</summary>
<br>
<p align="center"><img src="images/assembly_all_steps.gif" alt="All assembly steps in one animation" width="100%"></p>
</details>

## 🎄 How it works

<p align="center"><img src="images/how_it_runs.gif" alt="How the workshop runs (render)" width="640"></p>

1. **Lights on.** The tree, the workshop, the street lamp and both lanterns light up from six LEDs.
2. **Load the gifts.** Six gifts snap onto the magnets of the ring while the lanterns blink green.
3. **The elf picks its moment.** It waits a random time, from 8 to 25 seconds, and now and then it fakes: the arm swings into the empty spot and back out, and nothing drops. Then the elf swings its arm across the track for real, a 360° servo turns the 100-tooth ring one spot through a 12-tooth pinion, and the arm pushes the next gift off.
4. **Into the drawer.** The sleigh has no floor, so each gift drops into a drawer in the front of the base. Each time a gift lands, the tree baubles blink and then dim one step. After the sixth gift the lanterns blink red for a minute, then the lights stay on.

Every switch-on gives a different show.

## ⚡ Electronics

<p align="center">
  <img src="assets/electronics.svg" alt="Electronics: CyberBrick core with receiver shield, 360 and 180 degree servos, two LED hubs, six LEDs, battery and switch" width="100%">
</p>

Everything comes from the Bambu Lab CyberBrick range and is plugged with the kit cables, no soldering. The parts are held by press fits, snap fits and the kit screws: no glue and no supports. The plates are laid out for a 330 × 320 mm bed (Bambu Lab H2C), one colour per plate, so no AMS is needed.

## 💾 Firmware

[`firmware/main.py`](firmware/main.py) is a standalone MicroPython program for the CyberBrick core. It runs the whole show on its own: light scenes, ring stops and the elf's arm at random moments, with every timing in one settings block at the top. Version 2.6 is still to be tested on the assembled diorama. Wiring and loading steps are in [`firmware/README.md`](firmware/README.md).

## 📸 The printed diorama

<p align="center">
  <img src="images/photos/workshop.jpg" alt="The workshop with its snowy roof and a gift on the ring" width="32%">
  <img src="images/photos/santa_sleigh.jpg" alt="Santa waving next to his sleigh" width="32%">
  <img src="images/photos/tree_detail.jpg" alt="The tree with its baubles and the workshop" width="32%">
</p>

<p align="center">
  <img src="images/photos/night_lamp.jpg" alt="The lamp post and the tree lit at night" width="32%">
  <img src="images/photos/night_red.jpg" alt="The sleigh glowing red at the end of the show" width="32%">
  <img src="images/photos/day_full.jpg" alt="The whole diorama in daylight" width="32%">
</p>

### From the workbench

<p align="center">
  <img src="images/assembly/key_press_tool_in_hand_IMG_5712.jpeg" alt="The key press tool" width="32%">
  <img src="images/assembly/sleigh_underside_two_flat_keys_first_2026-11-12.jpeg" alt="Two flat keys pressed into the sleigh underside first" width="32%">
  <img src="images/assembly/base_third_flat_key_then_santa_key_2026-11-12.jpeg" alt="The third flat key in the base, then Santa's key" width="32%">
</p>

<p align="center"><sub>Real photos from the first full assembly.</sub></p>

## 📁 In this repository

| Folder | Content |
| :--- | :--- |
| [`docs/`](docs/) | Interactive assembly guide (`index.html`) and its images. |
| [`docs/pdf/`](docs/pdf/) | The same guide as printable PDF, one file per language. |
| [`firmware/`](firmware/) | MicroPython program for the CyberBrick core and how to load it. |
| [`images/`](images/) | Renders, animations, photos of the printed diorama and of the assembly. |
| [`assets/`](assets/) | Banner, logo and the graphics of this page. |

> [!NOTE]
> The printable files (STL, 3MF, STEP) are not in this repository. Santa's Workshop will be a MakerWorld exclusive, so they will be available only there. The link will be added here when the model is online.

## 📜 License

The guide, images, firmware and documentation in this repository are released under [CC BY-NC-SA 4.0](LICENSE): you can share and adapt them for non-commercial use, with credit to emanuele tech. Selling prints, kits or assembled dioramas needs a commercial license, available on MakerWorld.

---

<p align="center">
  <img src="assets/logo_light.svg#gh-light-mode-only" alt="emanuele tech" width="160">
  <img src="assets/logo_dark.svg#gh-dark-mode-only" alt="emanuele tech" width="160">
  <br>
  <sub>Design, prints and photos by <a href="https://github.com/emanueletech">emanuele tech</a>. CyberBrick is a product of Bambu Lab; this project is not affiliated with Bambu Lab.</sub>
</p>
