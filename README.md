# music-punch
A project in MicroyPython which controls the artwork "Just Another Beep Boop Machine"

This project was a small experiment in creating music in a simple and interactive way: the user punches cards, and feeds them into the machine. The device then reads the open holes, and plays the corresponding note.

This code is written for an [Espruino Pico](http://www.espruino.com/Pico), which has been flashed with [MicroyPython](http://micropython.org/) (a process I detail [here](http://maxlupo.com/installing-micropython-on-the-espruino-pico/)).

## Documentation

<img src=/assets/beep-boop.JPG width="600"/>

Video of use: [https://www.youtube.com/watch?v=OQMbFPYHY8g](https://www.youtube.com/watch?v=OQMbFPYHY8g)

For more pictures and and a pseudo how-to build guide, take a look at my [blog post](http://maxlupo.com/just-another-beep-boop-machine/) for this device.

###The Code
As mentioned above, the code runs on a microcontroller running MicroPython, and the script can be found [here](https://github.com/mlupo/music-punch/blob/master/main.py). You just need to wire up the components to the pins outlined in the code (or equivalent for different boards), and upload the main.py onto your device.

Really though, this project can be done on almost any microcontroller, as long as you write a script with similar logic. Basically, the main.py script just does this:

1. Initialize the pins corresponding to the light sensors as inputs.
2. Set up a PWM pin to output to a speaker or piezo buzzer.
3. Create a function which takes the pin receiving light, and then activates the piezo to play the corresponding note.
4. Wrap this all up in a loop that checks to see which pins are full of light, and then act accordingly.

PLEASE NOTE THAT I AM NOT A PROGRAMMER, JUST AN ARTIST WHO HAPPENS TO WRITE CODE SOMETIMES... so I am always a little embarrassed over the quality of my coding.
