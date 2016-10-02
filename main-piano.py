import pyb
from midi.midiout import MidiOut

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

uart = pyb.UART(2, baudrate=31250)
midiout1 = MidiOut(uart, ch=1)

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

C5 = 72
D5 = 74
E5 = 76
F5 = 77
G5 = 79
A5 = 81
B5 = 83
C6 = 84
D6 = 86
E6 = 88
F6 = 89
G6 = 91
A6 = 93
B6 = 95

NOTE_LIST = [C5, D5, E5, F5, G5, A5, B5, C6, D6, E6, F6, G6, A6, B6]


class Boop:
    "class to monitor pins, and play the corresponding notes"
    def __init__(self, base_note, scale_note, note_pin, notes, octave_pin):
        "construct pins and notes"
        self.base_note = base_note
        self.scale_note = scale_note
        self.notes = notes
        self.note_pin = note_pin
        self.octave_pin = octave_pin
        self.start_time = 0
        self.on_timer = 0
        self.oct_timer = 0
        self.scale = 0
        self.note = 0


    def pin_check(self):
        "check a given pin, and return its value"
        if self.note_pin.value() == ON:
            #self.octave_check()
            self.on_timer += 1
            if self.on_timer >= 5:
                #self.on_timer = 0
                return True
            else:
                return False
        elif self.note_pin.value() == OFF:
            self.on_timer = 0
            #self.octave_check()
            #off_timer += 1
            #if off_timer >= 5:
            return False

    def octave_check(self):
        if self.octave_pin.value() == ON:
            self.oct_timer += 1
            #if self.oct_timer >= 2:
            #print("scale is", self.scale)
            self.scale = 7
            self.note = self.notes[self.notes.index(self.base_note) + self.scale]
        elif self.octave_pin.value() == OFF:
            self.oct_timer = 0
            #print("scale is", self.scale)
            self.scale = 0
            self.note = self.base_note


# PROGRAM START ##########################

LED.high()
pyb.delay(100)
playing_notes = []
play_times = []

C_NOTE = Boop(C5, C6, ONE, NOTE_LIST, OCTAVE_UP)
D_NOTE = Boop(D5, D6, TWO, NOTE_LIST, OCTAVE_UP)
E_NOTE = Boop(E5, E6, THREE, NOTE_LIST, OCTAVE_UP)
F_NOTE = Boop(F5, F6, FOUR, NOTE_LIST, OCTAVE_UP)
G_NOTE = Boop(G5, G6, FIVE, NOTE_LIST, OCTAVE_UP)
A_NOTE = Boop(A5, A6, SIX, NOTE_LIST, OCTAVE_UP)
B_NOTE = Boop(B5, B6, SEVEN, NOTE_LIST, OCTAVE_UP)

boop_list = [C_NOTE, D_NOTE, E_NOTE, F_NOTE, G_NOTE, A_NOTE, B_NOTE]

while True:
    pyb.delay(45)
    playing = STOP_PIN.value()
    if playing == OFF:
        servo.speed(-8)
        #pyb.delay(5)
        for boopers in boop_list:
            boopers.octave_check()
            if boopers.pin_check():
                #boopers.octave_check()
#                pyb.delay(5)
                if (boopers.note not in playing_notes):
                    print("on", boopers.note)
                    midiout1.note_on(boopers.note)
                    #pyb.delay(5)
                    boopers.start_time = pyb.millis()
                    playing_notes.append(boopers.note)
                    play_times.append(boopers.start_time)
            if boopers.scale == 7 and boopers.base_note in playing_notes:
                print("off", boopers.base_note)
                midiout1.note_off(boopers.base_note)
                #pyb.delay(5)
                playing_notes.remove(boopers.base_note)
            if boopers.scale == 0 and boopers.scale_note in playing_notes:
                print("off", boopers.scale_note)
                midiout1.note_off(boopers.scale_note)
                #pyb.delay(5)
                playing_notes.remove(boopers.scale_note)
            if not boopers.pin_check():
            # this would be true if the note for the selected pin is OFF
                if boopers.base_note in playing_notes:
                    print("off", boopers.base_note)
                    midiout1.note_off(boopers.base_note)
                    #pyb.delay(5)
                    playing_notes.remove(boopers.base_note)
                    #play_times.remove(boopers.start_time)
                if boopers.scale_note in playing_notes:
                    print("off", boopers.scale_note)
                    midiout1.note_off(boopers.scale_note)
                    #pyb.delay(5)
                    playing_notes.remove(boopers.scale_note)
    else:
        if playing_notes:
            print("midi all notes off signal")
            midiout1.all_sound_off()
            print("remove all notes")
            del playing_notes[:]
            del play_times[:]
        if servo.speed() != 0:
            servo.speed(0, 800)
            pyb.delay(800)

#    if SW() == True:
#        volume += 1
#        pyb.delay(200)
#        if volume > 9:
#            volume = 2
#        print(volume)

