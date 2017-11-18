import pyb
from midi.midiout import MidiOut

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

# setup the UART pins and MIDI channel
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
COMMAND_PIN = pyb.Pin('B3', pyb.Pin.IN)

PIN_LIST = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN]


# all leds are powered from this pin. THE LEDs are hidden in the device, and
# provide the light necessary to activate the pins, whereever a hole is punched
# into the card
LED = pyb.Pin("B1", pyb.Pin.OUT_PP)

# the photo-resistors are simple on-off switches, instead of
# using them to recieve analogue input. This is due to a lack
# ADC pins, previously LIGHT = 1800 and DARK = 2200 were used
ON = 0
OFF = 1

# Each note is assigned a corresponding MIDI note number
C4 = 60
D4 = 62
Eb4 = 63
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

NOTE_LIST = [C4, D4, Eb4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, B5, C6]


class Boop:
    """class to monitor pins, and play the corresponding notes. Each pin is an
    instance of this class, which monitors its state and acts accordingly."""
    def __init__(self, note_pin, note_range):
        "Construct pins and notes"
        self.note_pin = note_pin
        self.note_range = note_range
        self.on_counter = 0
        self.off_counter = 0
        self.already_up = False
        self.octave = -1
        self.octave_limit = len(note_range) - 1
        self.note = 0

    def state_clear(self):
        """Resest the pin counters"""
        self.on_counter = 0
        self.off_counter = 0

    def initiliazer(self):
        """At the beginning of a loop, all attributes are reset"""
        self.state_clear()
        self.note = 0
        self.octave = -1
        self.already_up = False

    def note_check(self):
        """This is a debounce-esque function, which makes sure the light sensor
        recieves light for a given period of time"""
        if self.note_pin.value() == ON:
            self.on_counter += 1
            if self.on_counter > 1:
                self.on_counter = 1
        elif self.note_pin.value() == OFF:
            self.on_counter -= 1
            if self.on_counter < -1:
                self.on_counter = -1


class Commander:
    """A class to monitor the command pin. In this program, the 'command pin' is
    a light sensor which when activated initates the playback of the previously
    selected notes"""
    def __init__(self, pin):
        self.pin = pin
        self.counter = 0
        self.mode = False

    def check(self):
        if self.pin.value() == ON:
            return True
        elif self.pin.value() == OFF:
            self.counter += 1
            if self.counter >= 5:
                self.counter = 0
                return False


# PROGRAM START ##########################

LED.high()
pyb.delay(100)
# initiliaze the values
previous_notes = list()
current_notes = list()
play_times = list()
initial_check = int()
last_run = int()

# Each note pin is given its own Boop object. The args are the corresponding
# pin, and the notes that the pin is capable of playing.
C_NOTE = Boop(ONE, [C4, C5, C6])
D_NOTE = Boop(TWO, [D4, D5])
E_NOTE = Boop(THREE, [Eb4, E4, E5])
F_NOTE = Boop(FOUR, [F4, F5])
G_NOTE = Boop(FIVE, [G4, G5])
A_NOTE = Boop(SIX, [A4, A5])
B_NOTE = Boop(SEVEN, [B4, B5])

# put all of our Boop objects in a list
boop_list = [C_NOTE, D_NOTE, E_NOTE, F_NOTE, G_NOTE, A_NOTE, B_NOTE]
command = Commander(COMMAND_PIN)

while True:
    # The program's main loop, in which if the 'stopping' sensor is off, the
    # program will check the boop_list for any notes to be played. Once the
    # command pin is activated, those notes will be sent as a MIDI signal
    # to a connected device
    pyb.delay(45)
    stopping = STOP_PIN.value()
    if stopping == OFF:
        # if a card/roll of paper is inserted, the STOP_PIN is "off", and the
        # program can begin!
        servo.speed(-19)
        if not command.check():
            if initial_check == 0:
                # wipe the slate clean after the last check of the command pin
                for last_booped in boop_list:
                    last_booped.initiliazer()
                previous_notes = current_notes
                current_notes = list()
                initial_check = 1
                print("initial_check complete")
            for boopers in boop_list:
                # this is the fun part! For each Boop object, we check the pin
                boopers.note_check()
                # the note_check method raises or lowers the on_counter
                if boopers.on_counter >= 1:
                    # if the booper has been on long enough
                    if not boopers.already_up:
                        # for an octave to increase the light sensor has to be
                        # OFF, then ON. The already_up attribute makes sure the
                        # octave is not inreased unless an OFF->ON cycle occurs
                        boopers.octave += 1
                        if boopers.octave > boopers.octave_limit:
                            boopers.octave = boopers.octave_limit
                        if boopers.octave > -1:
                            boopers.note = boopers.note_range[boopers.octave]
                        print(boopers.note, "octave:", boopers.octave)
                    boopers.state_clear()
                    boopers.already_up = True
                if boopers.on_counter <= -1 and boopers.octave > -1:
                    # if the sensor has is off long enough, allow the octave to
                    # be increased for that pin
                    boopers.already_up = False

        elif command.check():
            # if the command pin is activated, it is time to cycle through the
            # selected notes.
            for booped in boop_list:
                if (booped.note not in current_notes):
                    # if the booped note is not already playing, send the
                    # MIDI signal for the note
                    if booped.note != 0:
                        print("on", booped.note)
                        midiout1.note_on(booped.note)
                        current_notes.append(booped.note)
                for i in previous_notes:
                    # for the last set of notes played, if the item is not
                    # currently set to play, turn it off
                    if i not in current_notes:
                        print("off", i)
                        midiout1.note_off(i)
                        previous_notes.remove(i)
            initial_check = 0

    else:
        # if there is paper in the machine, turn off the sound, and reset
        last_run = 1
        if current_notes:
            print("midi all notes off signal")
            midiout1.all_sound_off()
            print("remove all notes")
            del current_notes[:]
            del previous_notes[:]
            del play_times[:]
        if servo.speed() != 0:
            if last_run:
                midiout1.all_sound_off()
                last_run = 0
            servo.speed(0, 850)
            pyb.delay(500)
