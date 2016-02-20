import pyb

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

# set up the on board switch, and itial volume
SW = pyb.Switch()
volume = 4

# each pin on the board is connected to a photo-resistor
# which are mounted left-to-right in the device
ONE = pyb.Pin('A8', pyb.Pin.IN)
TWO = pyb.Pin('B7', pyb.Pin.IN)
THREE = pyb.Pin('B6', pyb.Pin.IN)
FOUR = pyb.Pin('B5', pyb.Pin.IN)
STOP_PIN = pyb.Pin('A7', pyb.Pin.IN)
FIVE = pyb.Pin('B13', pyb.Pin.IN)
SIX = pyb.Pin('B14', pyb.Pin.IN)
SEVEN = pyb.Pin('B15', pyb.Pin.IN)
OCTAVE_UP = pyb.Pin('B3', pyb.Pin.IN)

PIN_LIST = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN]

# all leds are powered from this pin
LED = pyb.Pin("B1", pyb.Pin.OUT_PP)

# the photo-resistors are simple on-off switches, instead of
# using them to recieve analogue input. This is due to a lack
# ADC pins, previously LIGHT = 1800 and DARK = 2200 were used
ON = 0
OFF = 1

# set up pin PWM timer for output to buzzer or speaker
# Pin B10 with timer 2 Channel 3
BUZZER = pyb.Pin("B10")
TIMER = pyb.Timer(2, freq=3000)
CHANNEL = TIMER.channel(3, pyb.Timer.PWM_INVERTED,
                        pin=BUZZER)

C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784
A5 = 880
B5 = 988
C6 = 1047
D6 = 1175
E6 = 1319
F6 = 1397
G6 = 1568
A6 = 1760
B6 = 1976

NOTE_LIST = [C5, D5, E5, F5, G5, A5, B5]


def play_note_digi(pin, note, vol=4, other_pins=PIN_LIST):
    ''' This function will play the note associated with
    a specific photo-resistor recieving light'''
    # the selected note's frequency is selected
    TIMER.freq(note)
    start = pyb.millis()
    if STOP_PIN.value() == ON:
        # make sure the servo doesn't move
        servo.speed(0)
    while pyb.elapsed_millis(start) < 475:
        # for the next 475 millis, we will check to see if
        # the note needs to stop, and otherwise play the tune
        halt_value = STOP_PIN.value()
        light_value = pin.value()
        if STOP_PIN.value() == OFF:
            servo.speed(-11)
        else:
            servo.speed(0)
        if (halt_value == OFF) and (light_value == ON):
            # this is the only condition resulting in a played note
            CHANNEL.pulse_width_percent(vol)
            # print("playing")
        elif light_value == OFF:
            CHANNEL.pulse_width_percent(0)
            break
        elif halt_value == OFF:
            CHANNEL.pulse_width_percent(0)
            # print ("HALT has no light")
            break
        else:
            CHANNEL.pulse_width_percent(0)
            # print("nothing")
            break
            # print("off")
    # pyb.delay(250)


def pitch_shift(note):
    ''' function to shift the pitch od ntoes up'''
    if note == C5:
        note = C6
    elif note == E5:
        note = E6
    elif note == D5:
        note = D6
    elif note == F5:
        note = F6
    elif note == G5:
        note = G6
    elif note == A5:
        note = A6
    elif note == B5:
        note = B6
    else:
        return note
    return note


# PROGRAM START ##########################

LED.high()
pyb.delay(100)

while True:
    pyb.delay(2)
    for pins, notes in zip(PIN_LIST, NOTE_LIST):
        # iterate over the pins, and play the corresponding note
        if OCTAVE_UP.value() == ON:
            play_note_digi(pins, pitch_shift(notes), volume)
        elif pins.value() == ON:
            # print(pins, notes)
            play_note_digi(pins, notes, volume)

    if SW() == True:
        volume += 1
        pyb.delay(200)
        if volume > 8:
            volume = 1
        print(volume)

