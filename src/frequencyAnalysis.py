
import numpy as np
# Finds the maximum value of an array between two indexes and returns the index of the maximum
def findMaxFromTo(array, startIdx, endIdx):
    # the minimum possible number is -2^31
    maxValue = -2147483648
    maxIdx = 0
    for i in range(startIdx, endIdx):
        if array[i] > maxValue:
            maxValue = array[i]
            maxIdx = i
    return maxIdx


# calculalates the median distance between peaks
def find_peak_distances_and_peak_values(soundBuffer):
    if (soundBuffer.__len__() <= 0 ):
        return []

    minimumThresholdFactor = 0.3


    peakDistances = []  # liste um entfernungen zwischen peaks zu messen
    peakValues=[]


    wasWaveformPositive = True
    isBelowLowerThreshold = False  # waveform was below 10 percent

    peakDistanceSum = 0

    peakCount = 0
    lastPeakPosition = -1
    currentPeakPosition = -1
    lastMinimumPosition = -1
    currentMinimumPosition = -1
    distanceCounter = 0

    # getst the minimum value from the soundbuffer array
    minimumValue = min(soundBuffer)
    # calculate the minimum threshold value from the minimum value
    minimumThreshold = minimumValue * minimumThresholdFactor

    # iterate over the soundbuffer array
    for i in range(0, len(soundBuffer)):
        if (soundBuffer[i] < minimumThreshold):
            isBelowLowerThreshold = True
        else:
            isBelowLowerThreshold = False
        if (soundBuffer[i] > 0):
            wasWaveformPositive = True

        # if the waveform was positive and the current value is below the minimum threshold a minimum is expected there
        if (isBelowLowerThreshold and wasWaveformPositive):
            wasWaveformPositive = False
            lastMinimumPosition = currentMinimumPosition
            currentMinimumPosition = i

            if (lastMinimumPosition >= 0):
                # calculate maximum between last and current minimum
                # last peak = current peak
                # currentPeakPosition = maximum between last and current minimum

                # calculate distance between peaks and add it to the found peaks
                # backup current peak
                lastPeakPosition = currentPeakPosition
                # find the new peak
                currentPeakPosition = findMaxFromTo(soundBuffer, lastMinimumPosition, currentMinimumPosition)
                peakCount += 1

                peakValues.append(currentPeakPosition)

                if (lastPeakPosition >= 0):
                    peakDistanceSum += currentPeakPosition - lastPeakPosition

                    if (distanceCounter < 1000):
                        # append the peak to the peak distances list
                        peakDistances.append(currentPeakPosition - lastPeakPosition)
                        peakValues.append(soundBuffer[currentPeakPosition])
                        distanceCounter += 1
    # calculate the median of the peak distances
    #peakDistanceMedian = np.median(peakDistances)
    #print(peakDistances)
    #peakDistances.sort()
    #plt.plot(soundBuffer)

    return peakDistances,peakValues


def calculate_frequency_using_peaks(audio_data,sample_rate=44100):
    peak_distances,peakValues =  find_peak_distances(audio_data)

    median_distance=1
    if(peak_distances.__len__()!= 0):
        median_distance = np.median(peak_distances)

    f = calculate_frequency(median_distance,sample_rate)
    amplitude = np.average(peakValues)

    return f,amplitude

# calculate the frequency of a sample length
def calculate_frequency(waveformLength, sampleRate):
    return sampleRate / waveformLength

def isNaN(num):
    return num != num

def map_frequency_to_midi(frequency):
    #calculate the note to a frequency in midi
    #n = int((12 * np.log(frequency / 220.0) / np.log(2.0)) + 57.01);
    n = int((12 * np.log(frequency / 220.0) / np.log(2.0)) + 57.5);
    n = np.clip(n,0,127)
    return int(n)

def map_midi_to_note(midi_note):
    #calculate the note to a frequency

    music_scale = ["C","Cis","D","Dis","E","F","Fis","G","Gis","A","Ais","H"]

    note = music_scale[midi_note % (music_scale.__len__())]

    if(midi_note <=  35):# C1 C2 C3
        note = note + str((int(4-(midi_note)/12)))

    if(midi_note >= 48): #cdefgahc
        note =  note.lower()

    if(midi_note >= 60):# g''''''
        octav =  (int((midi_note-60)/12))+1
        octav_apostrophe = "'" * octav
        note = note + octav_apostrophe

    return note


def map_frequency_to_node(frequency):
    #calculate the note to a frequency

    music_scale = ["C","Cis","D","Dis","E","F","Fis","G","Gis","A","Ais","H"]
    midi_note = map_frequency_to_midi(frequency)
    note = map_midi_to_note(midi_note)
    return note



    '''
    if (frequency >= 906):
        return "High"
    elif (frequency >= 855):
        return "A"
    elif (frequency >= 807):
        return "Gis"
    elif (frequency >= 762):
        return "G"
    elif (frequency >= 719):
        return "Fis"
    elif (frequency >= 680):
        return "F"
    elif (frequency >= 640):
        return "E"
    elif (frequency >= 600):
        return "Dis"
    elif (frequency >= 571):
        return "D"
    elif (frequency >= 539):
        return "Cis"
    elif (frequency >= 508):
        return "C"
    elif (frequency >= 480):
        return "B"
    elif (frequency >= 453):
        return "Ais"
    elif (frequency >= 427):
        return "A"
    elif (frequency >= 403):
        return "Gis"
    elif (frequency >= 381):
        return "G"
    elif (frequency >= 360):
        return "Fis"
    elif (frequency >= 340):
        return "F"
    elif (frequency >= 320):
        return "E"
    elif (frequency >= 300):
        return "Dis"
    elif (frequency >= 280):
        return "D"
    elif (frequency >= 270):
        return "Cis"
    elif (frequency >= 254):
        return "C"
    elif (frequency >= 240):
        return "B"
    elif (frequency >= 226):
        return "Ais"
    elif (frequency >= 207):
        return "A"
    else:
        return "Low"
    '''
        



    '''
    88	C8	c5	4186,01
    87	B7	h4	3951,07
    86	A#7/Bb7	ais4/b4	3729,31
    85	A7	a4	3520
    84	G#7/Ab7	gis4/as4	3322,44
    83	G7	g4	3135,96
    82	F#7/Gb7	fis4/ges4	2959,96
    81	F7	f4	2793,83
    80	E7	e4	2637,02
    79	D#7/Eb7	dis4/es4	2489,02
    78	D7	d4	2349,32
    77	C#7/Db7	cis4/des4	2217,46
    76	C7	c4	2093,00
    75	B6	h3	1975,53
    74	A#6/Bb6	ais3/b3	1864,66
    73	A6	a3	1760
    72	G#6/Ab6	gis3/as3	1661,22
    71	G6	g3	1567,98
    70	F#6/Gb6	fis3/ges3	1479,98
    69	F6	f3	1396,91
    68	E6	e3	1318,51
    67	D#6/Eb6	dis3/es3	1244,51
    66	D6	d3	1174,66
    65	C#6/Db6	cis3/des3	1108,73
    64	C6	c3	1046,50
    63	B5	h2	987,767
    62	A#5/Bb5	ais2/b2	932,328
    61	A5	a2	880
    60	G#5/Ab5	gis2/as2	830,609
    59	G5	g2	783,991
    58	F#5/Gb5	fis2/ges2	739,989
    57	F5	f2	698,456
    56	E5	e2	659,255
    55	D#5/Eb5	dis2/es2	622,254
    54	D5	d2	587,330
    53	C#5/Db5	cis2/des2	554,365
    52	C5	c2	523,251
    51	B4	h1	493,883
    50	A#4/Bb4	ais1/b1	466,164
    49	A4[2]	a1	440 Kammerton
    48	G#4/Ab4	gis1/as1	415,305
    47	G4	g1	391,995
    46	F#4/Gb4	fis1/ges1	369,994
    45	F4	f1	349,228
    44	E4	e1	329,628
    43	D#4/Eb4	dis1/es1	311,127
    42	D4	d1	293,665
    41	C#4/Db4	cis1/des1	277,183
    40	C4[3]	c1	261,626
    39	B3	h	246,942
    38	A#3/Bb3	ais/b	233,082
    37	A3	a	220
    36	G#3/Ab3	gis/as	207,652
    35	G3	g	195,998
    34	F#3/Gb3	fis/ges	184,997
    33	F3	f	174,614
    32	E3	e	164,814
    31	D#3/Eb3	dis/es	155,563
    30	D3	d	146,832
    29	C#3/Db3	cis/des	138,591
    28	C3	c	130,813
    27	B2	H	123,471
    26	A#2/Bb2	Ais/B	116,541
    25	A2	A	110
    24	G#2/Ab2	Gis/As	103,826
    23	G2	G	97,9989
    22	F#2/Gb2	Fis/Ges	92,4986
    21	F2	F	87,3071
    20	E2	E	82,4069
    19	D#2/Eb2	Dis/Es	77,7817
    18	D2	D	73,4162
    17	C#2/Db2	Cis/Des	69,2957
    16	C2	C	65,4064
    15	B1	H1	61,7354
    14	A#1/Bb1	Ais1/B1	58,2705
    13	A1	A1	55
    12	G#1/Ab1	Gis1/As1	51,9131
    11	G1	G1	48,9994
    10	F#1/Gb1	Fis1/Ges1	46,2493
    9	F1	F1	43,6535
    8	E1	E1	41,2034
    7	D#1/Eb1	Dis1/Es1	38,8909
    6	D1	D1	36,7081
    5	C#1/Db1	Cis1/Des1	34,6478
    4	C1	C1	32,7032
    3	B0	H2	30,8677
    2	A#0/Bb0	Ais2/B2	29,1352
    1	A0	A2	27,5
    '''

    '''
    if(isNaN(frequency)):
        return 120
    if (frequency >= 906):
        return 100
    elif (frequency >= 855):
        return 81
    elif (frequency >= 807):
        return 80
    elif (frequency >= 762):
        return 79
    elif (frequency >= 719):
        return 78
    elif (frequency >= 680):
        return 77
    elif (frequency >= 640):
        return 76
    elif (frequency >= 600):
        return 75
    elif (frequency >= 571):
        return 74
    elif (frequency >= 539):
        return 73
    elif (frequency >= 508):
        return 72
    elif (frequency >= 480):
        return 71#"B"
    elif (frequency >= 453):
        return 70#"Ais"
    elif (frequency >= 427):
        return 69#"A"
    elif (frequency >= 403):
        return 68#"Gis"
    elif (frequency >= 381):
        return 67#"G"
    elif (frequency >= 360):
        return 66#"Fis"
    elif (frequency >= 340):
        return 65#"F"
    elif (frequency >= 320):
        return 64#"E"
    elif (frequency >= 300):
        return 63#"Dis"
    elif (frequency >= 280):
        return 62#"D"
    elif (frequency >= 270):
        return 61#"Cis"
    elif (frequency >= 254):
        return 60#"C"
    elif (frequency >= 240):
        return 59#"B"
    elif (frequency >= 226):
        return 58#"Ais"
    elif (frequency >= 207):
        return 57#"A"
    else:
        return 20
    '''
