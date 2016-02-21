# music-punch
A project in MicroyPython which controls the artwork "Just Another Beep Boop Machine"

This project was a small experiment in creating music in a simple and interactive way: the user punches cards, and feeds them into the machine. The device then reads the open holes, and plays the corresponding note.

This code is written for an [Espruino Pico](http://www.espruino.com/Pico), which has been flashed with [MicroyPython](http://micropython.org/) (a process I detail [here](http://maxlupo.com/installing-micropython-on-the-espruino-pico/)).

## Documentation

<img src=/assets/beep-boop.JPG width="600"/>

Video of use: [https://www.youtube.com/watch?v=OQMbFPYHY8g](https://www.youtube.com/watch?v=OQMbFPYHY8g)

##How To
I can not promise that this will be a comprehensive guide, but it should be a good foundation for you to try a similar project.

First some preliminary steps:
1. Grab all of the project's 3D models and assets from [Thingiverse](http://www.thingiverse.com/thing:1305712)
2. Get the source code for the project [here](https://github.com/mlupo/music-punch)
3. Review how to wire up a photo-resistor to a micocontroller from [this post](http://bildr.org/2012/11/photoresistor-arduino/) (though that code example is for an Arduino)

The 3D model file `LED-holder.stl` is the top mount for the LEDs, and will need to be 3D printed. For this project I used something similar to [these](https://www.adafruit.com/products/300) (which were actually just a bit too bright). The LEDs just need to be mounted into this holder, and then wired in series to the microcontroller.

The file `sensor-holder.stl`, as you can guess, will hold the [light sensors](https://www.adafruit.com/products/161). Each needs to be mounted, and then wired to a specific pin on your microcontroller. For this project, the sensors are being used as a simple on-off switch, instead of sending analogue information. This makes the project a bit more flexible, as it does not require a crazy amount of analogue pins. The `sensor-holder.stl` and `LED-holder.stl` need to be connected with a 4-40 bolt on each side.

The servo is held in place by `servo-mount-no-holes.stl`, but the 3D-printable file does not have holes to bolt the servo in place, and so those will have to be drilled in later (...or you can just affix the servo to the mount with some tape, while you are adjusting its placement). The exact servo I used was [this one](https://www.creatroninc.com/product/full-rotation-micro-servo-motor-15kgcm/), but just about any continuous rotation servo of a similar size should work. Once in place, attach the `ring.stl` to a servo disc, and then slide on an elastic band for some grip. The one sort of tricky thing is that you will have to find a way to put some pressure on the wheel, in order to drive the card through.

###The Code
As mentioned above, the code runs on a microcontroller running MicroPython, and the script can be found [here](https://github.com/mlupo/music-punch/blob/master/main.py). You just need to wire up the components to the pins outlined in the code (or equivalent for different boards), and upload the main.py onto your device.

Really though, this project can be done on almost any microcontroller, as long as you write a script with similar logic. Basically, the main.py script just does this:

1. Initialize the pins corresponding to the light sensors as inputs.
2. Set up a PWM pin to output to a speaker or piezo buzzer.
3. Create a function which takes the pin receiving light, and then activates the piezo to play the corresponding note.
4. Wrap this all up in a loop that checks to see which pins are full of light, and then act accordingly.

PLEASE NOTE THAT I AM NOT A PROGRAMMER, JUST AN ARTIST WHO HAPPENS TO WRITE CODE SOMETIMES... so I am always a little embarrassed over the quality of my coding.

