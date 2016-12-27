import pyb

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

# set up the on board switch, and itial volume
SW = pyb.Switch()
volume = 5

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

NOTE_LIST = [C5, D5, E5, F5, G5, A5, B5, C6, D6, E6, F6, G6, A6, B6]

#NOTE_DICT = {ONE:[C5,C6], TWO:[D5, D6], THREE:[E5, E6], FOUR:[F5, F6],
#             FIVE: [G5, G6], SIX: [A5, A6], SEVEN: [B5, B6]}

def pin_check():
    if OCTAVE_UP.value() == ON:
        scale = 7
    else:
        scale = 0
    for number, pins in enumerate(PIN_LIST):
        if pins.value() == ON:
            return NOTE_LIST[number + scale]

# PROGRAM START ##########################

LED.high()
pyb.delay(100)
playing_notes = []
play_times = []


while True:
    pyb.delay(45)
    playing = STOP_PIN.value()
    if playing == OFF:
        servo.speed(-10)
        note = pin_check()
        if (note not in playing_notes) and (note in NOTE_LIST):
            start = pyb.millis()
            playing_notes.append(note)
            play_times.append(start)
            pyb.delay(25)
            if note == pin_check():
                TIMER.freq(note)
                CHANNEL.pulse_width_percent(volume)
        for times, notes in zip(play_times, playing_notes):
            elapsed = pyb.elapsed_millis(times)
            #if elapsed >= 50:
            if notes != pin_check():
                playing_notes.remove(notes)
                play_times.remove(times)
            if not playing_notes:
                CHANNEL.pulse_width_percent(0)
        print(playing_notes)

    else:
        if CHANNEL.pulse_width_percent() != 0.0:
            print("Volume Off")
            CHANNEL.pulse_width_percent(0)
        if servo.speed() != 0:
            pyb.delay(200)
            servo.speed(0, 1100)


    if SW() == True:
        volume += 1
        pyb.delay(200)
        if volume > 9:
            volume = 2
        print(volume)

