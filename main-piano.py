import pyb
from midi.midiout import MidiOut

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

uart = pyb.UART(2, baudrate=31250)
midiout1 = MidiOut(uart, ch=1)

# set up the on board switch, and itial volume
SW = pyb.Switch()

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
COMMAND = pyb.Pin('B3', pyb.Pin.IN)

PIN_LIST = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN]


# all leds are powered from this pin
LED = pyb.Pin("B1", pyb.Pin.OUT_PP)

# the photo-resistors are simple on-off switches, instead of
# using them to recieve analogue input. This is due to a lack
# ADC pins, previously LIGHT = 1800 and DARK = 2200 were used
ON = 0
OFF = 1

C4 = 60
D4 = 62
E4 = 64
F4 = 65
G4 = 67
A4 = 69
B4 = 71
C5 = 72
D5 = 74
E5 = 76
F5 = 77
G5 = 79
A5 = 81
B5 = 83
C6 = 84

NOTE_LIST = [C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, B5, C6]


class Boop:
    "class to monitor pins, and play the corresponding notes"
    def __init__(self, note_pin, note_range):
        "construct pins and notes"
        self.note_pin = note_pin
        self.note_range = note_range
        self.on_counter = 0
        self.off_counter = 0
        self.already_up = False
        self.octave = -1
        self.note = 0

    def initiliazer(self):
        self.state_clear()
        self.note = 0
        self.octave = -1
        self.already_up = False

    def state_clear(self):
        self.on_counter = 0
        self.off_counter = 0

    def note_check(self):
        if self.note_pin.value() == ON:
            self.on_counter += 1
        elif self.note_pin.value() == OFF:
            self.off_counter += 1



class Commander:
    "monitor the command pin"
    def __init__(self, pin):
        self.pin = pin
        self.counter = 0
        self.mode = False

    def check(self):
        if self.pin.value() == ON:
             return True
        elif self.pin.value() == OFF:
            self.counter += 1
            if self.counter >= 10:
                self.counter = 0
                return False


# PROGRAM START ##########################

LED.high()
pyb.delay(100)
previous_notes = []
current_notes = []
play_times = []
initial_check = 0

C_NOTE = Boop(ONE, [C4, C5, C6])
D_NOTE = Boop(TWO, [D4, D5])
E_NOTE = Boop(THREE, [E4, E5])
F_NOTE = Boop(FOUR, [F4, F5])
G_NOTE = Boop(FIVE, [G4, G5])
A_NOTE = Boop(SIX, [A4, A5])
B_NOTE = Boop(SEVEN, [B4, B5])

boop_list = [C_NOTE, D_NOTE, E_NOTE, F_NOTE, G_NOTE, A_NOTE, B_NOTE]
command = Commander(COMMAND)

while True:
    pyb.delay(45)
    stopping = STOP_PIN.value()
    if stopping == OFF:
        servo.speed(-8)
        #pyb.delay(5)
        if not command.check():
            if initial_check == 0:
                for last_booped in boop_list:
                    last_booped.state_clear()
                    last_booped.initiliazer()
                previous_notes = current_notes
                current_notes = []
                initial_check = 1
            for boopers in boop_list:
                boopers.note_check()
                if boopers.on_counter >= 10:
                    if not boopers.already_up:
                        boopers.octave += 1
                        if boopers.octave > len(boopers.note_range):
                            boopers.octave = len(boopers.note_range - 1)
                    boopers.state_clear()
                if boopers.off_counter > 10 and boopers.octave > -1:
                    boopers.already_up = False

        elif command.check():
            for booped in boop_list:
                if booped.octave > -1:
                    booped.note = booped.note_range[booped.octave]
                    if (booped.note not in current_notes):
                        print("on", boopers.note)
                        midiout1.note_on(boopers.note)
                        #pyb.delay(5)
                        current_notes.append(booped.note)
                for i in previous_notes:
                    if i not in current_notes:
                        print("off", i)
                        midiout1.note_off(i)
                        #pyb.delay(5)
            initial_check = 0

    else:
        if current_notes:
            print("midi all notes off signal")
            midiout1.all_sound_off()
            print("remove all notes")
            del playing_notes[:]
            del play_times[:]
        if servo.speed() != 0:
            servo.speed(0, 800)
            pyb.delay(800)


