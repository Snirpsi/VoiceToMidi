import frequencyAnalysis
import mido

for i in range(0,127):
    print(i,frequencyAnalysis.map_midi_to_note(i))

with mido.open_input() as inport:
    for msg in inport:
        print(msg)