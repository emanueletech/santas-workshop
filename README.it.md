<p align="center">
  <img src="assets/banner.svg" alt="Santa's Workshop, a 3D printed Christmas diorama by emanuele tech" width="100%">
</p>

<p align="center">
  <img src="assets/badges/status.svg" height="28" alt="Status: work in progress">
  <img src="assets/badges/makerworld.svg" height="28" alt="MakerWorld exclusive">
  <img src="assets/badges/cyberbrick.svg" height="28" alt="CyberBrick, MicroPython">
  <img src="assets/badges/firmware.svg" height="28" alt="Firmware 3.14">
  <img src="assets/badges/guide.svg" height="28" alt="Guide in English and Italian">
</p>

<p align="center"><a href="README.md">English</a> · <b>Italiano</b></p>

<p align="center">
  <b>Accendilo e il laboratorio prende vita.</b><br>
  L'albero si illumina, l'anello dei regali gira e l'elfo spinge i pacchi uno alla volta nella slitta di Babbo Natale, fino al cassetto. Niente telecomando, niente pulsanti.
</p>

<p align="center">
  <a href="#-guida-di-montaggio">Guida di montaggio</a> ·
  <a href="#-come-funziona">Come funziona</a> ·
  <a href="#-elettronica">Elettronica</a> ·
  <a href="#-firmware">Firmware</a> ·
  <a href="ROADMAP.md">Roadmap</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <img src="images/photos/night_full.jpg" alt="Il Laboratorio di Babbo Natale di notte: albero, officina, lampione e slitta illuminati" width="100%">
</p>

<p align="center">
  <img src="assets/stats_it.svg" alt="151 pezzi stampati, 13 piatti, 24,6 ore e 736 g di PLA, niente colla, supporti o AMS" width="100%">
</p>

## 🎬 Video di montaggio

<p align="center"><a href="https://youtu.be/pzDiji6TK0Q"><img src="images/video_thumbnail.jpg" alt="Guarda il video del montaggio 3D del Laboratorio di Babbo Natale su YouTube" width="100%"></a></p>
<p align="center"><sub>Tutti i passi del montaggio in animazione 3D, su YouTube.</sub></p>

## 🛠 Guida di montaggio

<p align="center">
  <a href="docs/pdf/Santas_Workshop_guida_montaggio_IT.pdf"><img src="assets/guide_card_it.svg" alt="Guida di montaggio: 31 passi animati, in italiano e inglese. Apri la guida." width="100%"></a>
</p>

<p align="center">
  <a href="docs/pdf/Santas_Workshop_guida_montaggio_IT.pdf"><img src="assets/badges/pdf_it.svg" height="28" alt="Guida di montaggio PDF in italiano"></a>
  <a href="docs/pdf/Santas_Workshop_assembly_guide_EN.pdf"><img src="assets/badges/pdf_en.svg" height="28" alt="Assembly guide PDF in English"></a>
  <a href="docs/index.html"><img src="assets/badges/interactive.svg" height="28" alt="Guida interattiva"></a>
</p>

Trentuno passi, dallo staccare le chiavette dalle kit card fino a caricare i primi regali. Ogni passo ha la sua animazione, l'elenco dei pezzi con il piatto da cui vengono e le azioni da spuntare. La guida interattiva è una pagina unica con il cambio italiano / inglese: scarica [`docs/index.html`](docs/index.html) insieme alla cartella `docs/img` e aprila nel browser.

<p align="center">
  <img src="assets/tools_it.svg" alt="Attrezzi: brugola da 1,5 mm per le viti M2,5 x 6 del kit, piccolo cacciavite a croce per le viti dei servo e la vite centrale, e lo strumento per le chiavette stampato con il modello. Niente colla e niente saldature." width="100%">
</p>

| Fase | Passi | Cosa succede |
| :--- | :---: | :--- |
| **Preparazione** | 1–3 | Chiavette e strumento, magneti nell'anello e nei regali. |
| **Sotto la base** | 4–10 | Servo, interruttore, hub dei LED e ricevitore, poi il programma e una prima prova. |
| **Scena sopra la base** | 11–20 | Pignone, base dell'albero, anello, copertura di neve, officina, lampione, slitta ed elfo. |
| **Luci e chiusura** | 21–25 | LED agli hub, batteria e coperchio, cassetto dei regali, sportello della ricarica, tappo USB. |
| **Figure e albero** | 26–29 | Babbo Natale, il pupazzo di neve, il palo del Polo Nord e l'albero, un piano alla volta. |
| **Accensione** | 30–31 | Carica i regali, accendi e regola lo spettacolo. |

<details>
<summary><b>Guarda tutti i 31 passi in un'unica animazione</b> (5 MB)</summary>
<br>
<p align="center"><img src="images/assembly_all_steps.gif" alt="Tutti i passi di montaggio in un'animazione" width="100%"></p>
</details>

## 🎄 Come funziona

<p align="center"><img src="images/how_it_runs.gif" alt="Come gira il laboratorio (render)" width="640"></p>

1. **Luci accese.** L'albero, l'officina, il lampione e le due lanterne si accendono con sei LED.
2. **Carica i regali.** L'elfo mette il braccio di traverso sulla pista e sei regali si agganciano ai magneti dei cerchi liberi mentre le lanterne lampeggiano verdi.
3. **L'elfo al lavoro.** Un servo a 360° fa girare l'anello da 100 denti con un pignone da 12, a piccoli passi con una pausa casuale fra uno e l'altro. A ogni passo l'elfo spinge il braccio verso la slitta: anello e braccio spingono insieme il regalo, che scivola lungo il braccio e cade.
4. **Nel cassetto.** La slitta non ha fondo, quindi ogni regalo cade in un cassetto sul davanti della base. Un ultimo giro veloce porta dentro i regali rimasti sull'anello. Poi tutte le luci si alternano rosse e verdi per qualche secondo e il diorama resta acceso come decorazione: la stella brilla e le palline respirano piano passando per rosso, oro, verde, blu e viola.

Ogni accensione è uno spettacolo diverso.

## ⚡ Elettronica

<p align="center">
  <img src="assets/electronics_it.svg" alt="Elettronica: core CyberBrick con ricevitore, servo da 360 e da 180 gradi, due hub LED, sei LED, batteria e interruttore" width="100%">
</p>

Tutto viene dalla linea Bambu Lab CyberBrick e si collega con i cavi del kit, senza saldare. I pezzi stanno insieme a incastro, a scatto e con le viti del kit: niente colla e niente supporti. I piatti sono pensati per un piano da 330 × 320 mm (Bambu Lab H2C), un colore per piatto, quindi l'AMS non serve.

## 💾 Firmware

[`firmware/main.py`](firmware/main.py) è un programma MicroPython autonomo per il core CyberBrick. Gestisce da solo tutto lo spettacolo: luci, passi dell'anello con pause casuali e braccio dell'elfo, con tutti i tempi in un unico blocco di impostazioni in cima al file. La versione 3.14 fa lo spettacolo completo sul diorama montato. Collegamenti e caricamento sono in [`firmware/README.md`](firmware/README.md) (in inglese).

## 📸 Il diorama stampato

<p align="center">
  <img src="images/photos/workshop.jpg" alt="L'officina con il tetto innevato e un regalo sull'anello" width="32%">
  <img src="images/photos/santa_sleigh.jpg" alt="Babbo Natale che saluta accanto alla slitta" width="32%">
  <img src="images/photos/tree_detail.jpg" alt="L'albero con le palline e l'officina" width="32%">
</p>

<p align="center">
  <img src="images/photos/night_lamp.jpg" alt="Il lampione e l'albero accesi di notte" width="32%">
  <img src="images/photos/night_red.jpg" alt="La slitta che si illumina di rosso a fine spettacolo" width="32%">
  <img src="images/photos/day_full.jpg" alt="Il diorama intero alla luce del giorno" width="32%">
</p>

### Dal banco di lavoro

<p align="center">
  <img src="images/assembly/key_press_tool_in_hand_IMG_5712.jpeg" alt="Lo strumento per le chiavette" width="32%">
  <img src="images/assembly/sleigh_underside_two_flat_keys_first_2026-11-12.jpeg" alt="Prima le due chiavette piatte sotto la slitta" width="32%">
  <img src="images/assembly/base_third_flat_key_then_santa_key_2026-11-12.jpeg" alt="La terza chiavetta piatta nella base, poi quella di Babbo Natale" width="32%">
</p>

<p align="center"><sub>Foto vere del primo montaggio completo.</sub></p>

## 📁 Cosa c'è in questa repository

| Cartella | Contenuto |
| :--- | :--- |
| [`docs/`](docs/) | Guida di montaggio interattiva (`index.html`) e le sue immagini. |
| [`docs/pdf/`](docs/pdf/) | La stessa guida in PDF da stampare, un file per lingua. |
| [`firmware/`](firmware/) | Programma MicroPython per il core CyberBrick (`main.py` e `boot.py`, anche in un unico zip) e come caricarlo. |
| [`images/`](images/) | Render, animazioni, foto del diorama stampato e del montaggio. |
| [`assets/`](assets/) | Banner, logo e grafiche di questa pagina. |

> [!NOTE]
> I file da stampare (STL, 3MF, STEP) non sono in questa repository. Il Laboratorio di Babbo Natale sarà un modello esclusivo MakerWorld, quindi saranno disponibili solo lì. Il link verrà aggiunto qui quando il modello sarà online.

## 📜 Licenza

Guida, immagini, firmware e documentazione di questa repository sono rilasciati con licenza [CC BY-NC-SA 4.0](LICENSE): puoi condividerli e modificarli per uso non commerciale, citando emanuele tech. Per vendere stampe, kit o diorami montati serve una licenza commerciale, disponibile su MakerWorld.

---

<p align="center">
  <img src="assets/logo_light.svg#gh-light-mode-only" alt="emanuele tech" width="160">
  <img src="assets/logo_dark.svg#gh-dark-mode-only" alt="emanuele tech" width="160">
  <br>
  <sub>Progetto, stampe e foto di <a href="https://github.com/emanueletech">emanuele tech</a>. CyberBrick è un prodotto di Bambu Lab; questo progetto non è affiliato a Bambu Lab.</sub>
</p>
