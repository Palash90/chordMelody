import json
import random

from midiutil.MidiFile import MIDIFile


def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation


def permutations(lst):
    if len(lst) <= 1:
        return [lst]  # [[X]]
    l = []
    for i in range(len(lst)):
        m = lst[i]
        remlst = lst[:i] + lst[i + 1:]
        for p in permutations(remlst):
            l.append([m] + p)
    return l  # return at end of outer for loop


# Load the input configuration for the midi to be generated
inputFile = open('input.json')
config = json.load(inputFile)

noteToMidiNumber = json.load(open('noteToMidiNumber.json'))

chordbotTemplateFile = open('ChordbotTemplate.json')
chordbotTemplate = json.load(chordbotTemplateFile)

noteSequence = []

# create your MIDI object
mf = MIDIFile(1)  # only 1 track
track = 0  # the only track

time = 0  # start at the beginning
mf.addTrackName(track, time, config['name'])
mf.addTempo(track, time, config["tempo"])

# add some notes
channel = 0
volume = 90

outputChords = []

choices = list(range(config['length']))
random.shuffle(choices)

numOfChords = len(config['chords'])
chordCombinations = []

excludedNotes = config["excludedNotes"]

if numOfChords < 3:
    print("This script will not generate expected results for less than 3 chords in input")

for i in range(numOfChords):
    for j in range(numOfChords):
        for k in range(numOfChords):
            for l in range(numOfChords):
                if i != j and i != k and i != l and j != k and j != l and k != l:
                    chordCombinations.append(tuple([i, j, k, l]))

if config["endWithFirstChord"]:
    config['chords'][chordCombinations[choices[len(choices) - 1]][3]] = config['chords'][
        chordCombinations[choices[0]][0]]

for i in choices:
    combination = chordCombinations[i]

    for j in range(len(combination)):
        chord = config['chords'][combination[j]]

        chordbotSignature = chord['chordbotSignature']
        chordbotSignature['duration'] = 4
        outputChords.append(chordbotSignature)

        lowOctaveNotes = chord['lowOctaveNotes']
        middleOctaveNotes = chord['middleOctaveNotes']
        highOctaveNotes = chord['highOctaveNotes']
        passingNotes = chord['passingNotes']

        totalNotes = lowOctaveNotes + middleOctaveNotes + highOctaveNotes

        filteredNotes = []
        for note in totalNotes:
            noteRangeLow = noteToMidiNumber[config["noteRangeLow"]]
            noteNumber = noteToMidiNumber[note]
            noteRangeHigh = noteToMidiNumber[config["noteRangeHigh"]]

            if noteRangeLow <= noteNumber <= noteRangeHigh and note not in excludedNotes:
                filteredNotes.append(note)

        permutedNotes = permutations(filteredNotes)
        random.shuffle(permutedNotes)
        chosenNoteSequence = permutedNotes[0]

        L = list(sums(len(filteredNotes), 4 * 2))
        random.shuffle(L)
        chosenDurationSequence = L[0]

        for noteCounter in range(len(chosenNoteSequence)):
            note = chosenNoteSequence[noteCounter]
            duration = chosenDurationSequence[noteCounter]

            passingNote = None

            if passingNotes is not None and noteCounter > 0:
                lastNote = chosenNoteSequence[noteCounter - 1]
                passingNoteArr = []
                for passing in passingNotes:
                    if lastNote <= passing <= note and passing not in excludedNotes:
                        passingNoteArr.append(passing)
                random.shuffle(passingNoteArr)
                if len(passingNoteArr) > 0:
                    passingNote = passingNoteArr[0]
                    if config['noteRangeLow'] <= passingNote <= config['noteRangeHigh']:
                        pass
                    else:
                        passingNote = None

            if duration == 0:
                continue
            else:
                if duration <= 2:
                    addPassing = bool(random.getrandbits(1))
                    if addPassing and passingNote is not None:
                        noteSequence.append({"note": passingNote, "duration": duration * 0.5})
                        mf.addNote(track, channel, noteToMidiNumber[str(passingNote)], time, duration * 0.5, volume)
                        time = time + duration * 0.5
                    else:
                        noteSequence.append({"note": note, "duration": duration * 0.5})
                        mf.addNote(track, channel, noteToMidiNumber[note], time, duration * 0.5, volume)
                        time = time + duration * 0.5
                else:
                    fullNotes = int(duration / 2)
                    halfNote = int(duration % 2)

                    for fullNote in range(fullNotes - 1):
                        noteSequence.append({"note": note, "duration": 1})
                        mf.addNote(track, channel, noteToMidiNumber[note], time, 1, volume)
                        time = time + 1

                    auxilaryNote = None
                    auxilaryNotes = config["auxilaryNotes"][str(note)]
                    random.shuffle(auxilaryNotes)
                    auxilaryNote = auxilaryNotes[0]

                    if auxilaryNote is not None:
                        noteSequence.append({"note": auxilaryNote, "duration": 0.5})
                        mf.addNote(track, channel, noteToMidiNumber[str(auxilaryNote)], time, 0.5, volume)
                        time = time + 0.5
                        noteSequence.append({"note": note, "duration": 0.5})
                        mf.addNote(track, channel, noteToMidiNumber[note], time, 0.5, volume)
                        time = time + 0.5
                    else:
                        noteSequence.append({"note": note, "duration": 1})
                        mf.addNote(track, channel, noteToMidiNumber[note], time, 1, volume)
                        time = time + 1

                    if halfNote != 0:
                        noteSequence.append({"note": note, "duration": 0.5})
                        mf.addNote(track, channel, noteToMidiNumber[note], time, 0.5, volume)
                        time = time + 0.5

chordbotTemplate["tempo"] = config["tempo"]
chordbotTemplate['songName'] = config["name"]
chordbotTemplate['sections'][0]["chords"] = outputChords

for note in noteSequence:
    note["duration"] = note["duration"] * 60.0 / float(config["tempo"])

# write it to disk
with open(config['dir'] + config['name'] + ".midi", 'wb') as outputFile:
    mf.writeFile(outputFile)

with open(config['dir'] + config['name'] + "-chordBot.json", 'w') as outputFile:
    json.dump(chordbotTemplate, outputFile)

with open(config['dir'] + config['name'] + "-noteSeq.json", 'w') as outputFile:
    json.dump(noteSequence, outputFile)
