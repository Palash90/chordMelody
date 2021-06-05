# Chord Based Melody Creator

The `chordMelodyCreator.py` is a python utility script which generates 4/4 melody and chord progression based on
permutation and random picking. The script can help people find a musical idea, a small jingle or a background music.

**Note:** This does not use `Google Magenta` or any AI. But output generated by the script can be fed to `Magenta` for
continuation and Accompanying music generation.

## Prerequisite

1. python 3.x
1. MIDIFile (Dependency)
1. Basic idea of music theory i.e. knowledge on Rhythm, Harmony and Melody.
1. Some exposure with MIDI
1. Optional - Exposure to DAW in case you want to edit the generated midi and create your own music with different sound
   fonts.

## Usage

This is a step-by-step process.

1. Select Chords of your choice
1. Fill up the `input.json` as per requirement
1. Fill up the `midiNumberToNote.json` as per your requirement.
1. Run the `chordMelodyCreator.py`
1. Import the generated MIDI in DAW and use Soundfont of your choice

### Optional

1. The script also generates a `chordBot.json` which you can use in chordbot to generate accompanying backing track.
1. The script also generates a `noteSeq.json`. If you want to play an instrument on your own, this file gives you the
   generated melody in json format.

## Sample

The audio of [this video](https://www.youtube.com/watch?v=hPXw479nqSA) was completely generated using this script, no
manual intervention made in the chord progression or melody. I only chose the instruments.

## Input structure

There are two input files that you need to process as per your requirement.

### `input.json`

This is the main configuration file for the script to run. Please do not omit any field of the json or the script will
break. No Validation was added for the input provided by user.

Following are the details of the fields in the configuration.

* name

This is the name of the output that is going to be generated. If you are chordbot user, your chord progression will have
this name too.

* dir

The directory where the output will be generated

* length

The length of the composition. Each unit will have 4 beats.

* noteRangeLow

The lowest midi note number in the composition.

* noteRangeHigh

The highest midi note number in the comosition.

* excludedNotes

If you want to skip some notes in between the range provided by `noteRangeLow` and `noteRangeHigh`

* endWithFirstChord

This is to resolve the composition. If selected `true`, the chord progression will end on the first chord. This gives a
resolved feeling to the listener.

* tempo

Tempo of the composition

* auxilaryNotes

List of auxilary notes. A random note will be chosen when there is a repetition of same note for more than 2 beats. You
need to provide a list of auxilary notes for each of the notes.

* chords

A list of chords that you want in your composition. The melody will revolve around the notes in the chords.

Following is a detailed description of each field present in a chord.

#### Details of chord

* name

Name of the chord

* lowOctaveNotes

The lowest octave notes used in the chord.

* middleOctaveNotes

Notes of the chord from middle octave

* highOctaveNotes

Notes of the chord from high octave

* passingNotes

Passing notes for the chord of all three octaves. During melody generation a suitable passing note will be picked by the
script.

* chordbotSignature

This field is a little tricky to explain if you do not have experience with Chordbot. In case, you do not understand
what is going on, simply copy and paste this field in each chord.

### `midiNumberToNote.json`

As the name suggests, it is a simple one to one mapping from midi note numbers to human readable music notation.

Populate this file as per your requirement. following table can help you with the note number and note.
![alt text](https://raw.githubusercontent.com/Palash90/chordMelody/main/midi%20note%20numbers.png)