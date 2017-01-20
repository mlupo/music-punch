import urandom
import pyb
from midi.midiout import MidiOut

# initiliaze the servo
servo = pyb.Servo(2)
servo.speed(0)

uart = pyb.UART(2, baudrate=31250)
midiout1 = MidiOut(uart, ch=1)
'''
pentatonic A minor
[A4, C5, D5, E5, G5, A5]

D minor
[D4, F4, G4, A4, C5, D5, F5, G5, A5]

E minor
[E4, G4, A4, B4, D5, E5, G5, A5, B5]
'''

'''
Contextualize existing practice, and how the work not only relates, but where it is coming from

8th fo Defense
'''
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

playing_notes = list()
play_times = list()
#pent_notes = [D4, F4, A4, C5, D5, F5, A5]
pent_notes = [E4, G4, A4, B4, D5, E5, G5, A5, B5]
iteration = 1
servo.speed(-9)
start = pyb.millis()

while True:
    print("bllop")
    #print(pyb.elapsed_millis(start))
    if pyb.elapsed_millis(start) >= 1200:
        print("play a note")
        note_play = urandom.choice(pent_notes)
        if note_play not in playing_notes:
            print("picking")
            play_times.append(pyb.millis())
            playing_notes.append(note_play)
            midiout1.note_on(note_play)
        start = pyb.millis()
    if playing_notes:
        for times, notes in zip(play_times, playing_notes):
            elapsed = pyb.elapsed_millis(times)
            if elapsed >= 3000:
                print("it's over 3000")
                midiout1.note_off(notes)
                playing_notes.remove(notes)
                play_times.remove(times)
