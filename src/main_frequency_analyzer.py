from telnetlib import SE
import threading, time
import HTTP_shared_object_server as json_server
import json
import PythonAudioDataProvider
import frequencyAnalysis
import mido

class RawAudioData(object):
        def __init__(self):
            self.buffer = []

class SharedAudioObj(object):
    def __init__(self):
        self.note = "naNote"
        self.frequency = -1.0
        self.amplitude = -1.0
        self.midi_node_id = 201231
        self.duration = 0

    def __str__(self):
        sdict = self.__dict__
        retstr = "{"
        for key in sdict:
            if isinstance(sdict.get(key), float):
                retstr += str(key) + ": " + ("{0:8.2f}".format(sdict.get(key))) + ",\t"
            elif isinstance(sdict.get(key), str):
                retstr += str(key) + ": " + ("{:<8}".format(sdict.get(key))) + ",\t"
            else:
                retstr += str(key) + ": " +  str(sdict.get(key)) + ",\t"


        retstr += "}"
        return retstr

class MidiEventCreatorWorker(threading.Thread):
    def __init__(self,shared, *args ,**kwargs):
        super(MidiEventCreatorWorker, self).__init__(*args, **kwargs)
        self.shared = shared
        self.lastNodePlayed = 20;
        self.midiPort = mido.open_output("Microsoft GS Wavetable Synth 0")

        #Todo: Fehlertoleranz bzw außreißererkennung
        self.min_duration = 0.21 #fehlerfrei ohne außreißer
        self.min_amplitude = 500
        self.currentlyPlaying = []
        print(mido.get_output_names())

    def run(self):
        print(threading.current_thread(), 'MidiEventCreatorWorker' , 'start')
        while True:
            if (self.checkPlayConditions()):
                self.playNoteAsMidi(self.shared.midi_node_id)
                self.lastNodePlayed = self.shared.midi_node_id

            if (self.checkStopConditions()):
                self.stopNoteAsMidi()


            time.sleep(0.005) # Todo: no polling

    def checkStopConditions(self):
        if self.shared.amplitude > self.min_amplitude:
            return False
        return True



    def checkPlayConditions(self):
        if(self.lastNodePlayed == self.shared.midi_node_id):
            return False

        if(self.shared.duration < self.min_duration):
            return False

        if(self.shared.amplitude < self.min_amplitude):
            return False

        return True

    def playNoteAsMidi(self,note=60):
        if(note==127):
            return
        #msg = mido.Message('note_off', note=self.lastNodePlayed )
        #self.midiPort.send(msg)
        for n in self.currentlyPlaying:
            msg = mido.Message('note_off', note=n)
            self.midiPort.send(msg)


        msg = mido.Message('note_on', note=int(note))
        self.currentlyPlaying.append(note)
        self.midiPort.send(msg)

    def stopNoteAsMidi(self):
        for n in self.currentlyPlaying:
            msg = mido.Message('note_off', note=n)
            self.midiPort.send(msg)

class FrequenceAnalyzerWorker(threading.Thread):
    def __init__(self,shared, *args ,**kwargs):
        super(FrequenceAnalyzerWorker, self).__init__(*args, **kwargs)
        self.shared = shared
        self.audioStream = PythonAudioDataProvider.AudioStream()


    def run(self):
        print(threading.current_thread(), 'FrequenceAnalyzerWorker' , 'start')
        #TODO: Analyze audio forever
        while True:
            #print('analyzer running')
            #self.shared.frequency = self.shared.frequency
            #self.shared.amplitude = self.shared.amplitude
            #time.sleep(1)
            audio_data = self.audioStream.readData()
            f,amplitude = frequencyAnalysis.calculate_frequency_using_peaks(audio_data, self.audioStream.RATE)

            self.shared.amplitude = amplitude

            self.shared.frequency = f
            #self.shared.frequencys.append(f)
            self.shared.note = frequencyAnalysis.map_frequency_to_node(f)

            midi_node_id = frequencyAnalysis.map_frequency_to_midi(f)

            if (self.shared.midi_node_id == midi_node_id):
                self.shared.duration += self.audioStream.CHUNK*(1/self.audioStream.RATE)
            else:
                self.shared.duration = self.audioStream.CHUNK*(1/self.audioStream.RATE)
            self.shared.midi_node_id = midi_node_id


            #print(self.shared.__dict__)
            print(self.shared.__str__())
            pass
        print( 'shared', self.shared.image, id(self.shared))
        print( threading.current_thread(), 'done')


class FrequencyServer(threading.Thread):
    def __init__(self, shared, *args, **kwargs):
        super(FrequencyServer, self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):
        print(threading.current_thread(), 'FrequencyWorker', 'start')

        json_server.run(self.shared)

        print('shared', self.shared.image, id(self.shared))
        print(threading.current_thread(), 'done')



if __name__ == "__main__":
    audio_shared = SharedAudioObj()
    threads = [FrequenceAnalyzerWorker(shared=audio_shared, name='a'),
               FrequencyServer(shared=audio_shared, name='b'),
               MidiEventCreatorWorker(shared=audio_shared,name='c')
               ]
    for t in threads:
        t.start()



    for t in threads:
        t.join()



    print( 'DONE')