# music-punch
A project in MicroyPython which controls the artwork "Just Another Beep Boop Machine"

This project was a small experiment in creating music in a simple and interactive way: the user punches cards, and feeds them into the machine. The device then reads the open holes, and plays the corresponding note.

This code is written for an [Espruino Pico](http://www.espruino.com/Pico), which has been flashed with [MicroyPython](http://micropython.org/) (a process I detail [here](http://maxlupo.com/installing-micropython-on-the-espruino-pico/)).

## Documentation

<img src=/assets/beep-boop.JPG width="700"/>

Video of use: [https://www.youtube.com/watch?v=OQMbFPYHY8g](https://www.youtube.com/watch?v=OQMbFPYHY8g)

For more pictures and and a pseudo how-to build guide, take a look at my [blog post](http://maxlupo.com/just-another-beep-boop-machine/) for this device.

### The Code

As mentioned above, the code runs on a microcontroller running **MicroPython**, and the script can be found [here](https://github.com/mlupo/music-punch/blob/master/main.py). You just need to wire up the components to the pins outlined in the code (or equivalent for different boards), and upload the main.py onto your device.

PLEASE NOTE THAT I AM NOT A PROGRAMMER, JUST AN ARTIST WHO HAPPENS TO WRITE CODE SOMETIMES...

# UPDATE

This project has been extended to include an apparatus which plays an old chord organ.

<img src=/assets/piano-player.JPG width="700"/>

 The "main-piano.py" file contains the code which reads the light sensors and outputs MIDI commands to a connected device. The MicroPython MIDI library used was this one [here](https://github.com/SpotlightKid/micropython-stm-lib/tree/master/midi) by @SpotlightKid
To see this whole crazy thing in action, you can go here: [https://www.youtube.com/watch?v=mpJQyF-S-P0](https://www.youtube.com/watch?v=mpJQyF-S-P0), or check out the [blog post](https://maxlupo.com/beep-boopatronics/) for the project.

