from midiutil import MIDIFile
import fluidsynth
import os
import time
import psutil

def createMidiSong(pitches, durations):
    # Close Windows media player if open
    for proc in psutil.process_iter():
        if proc.name() == "wmplayer.exe":
            print("Windows Media Player is running")
            os.system("TASKKILL /F /IM wmplayer.exe")

            # Wait for media player to close
            time.sleep(0.75)
            break
    else:
        print("Windows Media Player is not running")

    # Define the tempo and duration of a quarter note
    tempo = 120
    quarter_note_duration = 60 / tempo

    # Create a MIDI file
    midi_file = MIDIFile(numTracks=1, adjust_origin=True)
    midi_file.addTempo(track=0, time=0, tempo=tempo)

    # Define the instrument to use (acoustic grand piano)
    program = 0  # 17=percussive organ #52=choir aahs #53=voice oohs #75=pan flute #79=ocarina
    midi_file.addProgramChange(channel=0, time=0, program=program, tracknum=0)

    # Add the notes to the MIDI file
    time = 0
    for pitch, duration in zip(pitches, durations):
        # # Convert the note name to a MIDI pitch number
        # pitch = MIDIFile().noteNameToMidi(note)

        # Add the note to the MIDI file
        midi_file.addNote(track=0, channel=0, pitch=pitch, time=time, duration=duration * quarter_note_duration,
                          volume=127)

        # Increment the time by the duration of the note
        time += duration * quarter_note_duration

    # Write the MIDI file to disk
    with open("star_wars.mid", "wb") as output_file:
        midi_file.writeFile(output_file)

    # Convert the MIDI file to MP3 using FluidSynth
    fs = fluidsynth.Synth()
    fs.start(driver="coreaudio")
    sfid = fs.sfload("GuitarA.sf2")
    fs.program_select(0, sfid, 0, program)
    import subprocess

    # Define the path to the FluidSynth executable
    fluidsynth_path = 'C:/Users/lprice/AppData/Chocolatey/chocoportable/bin/fluidsynth.exe'  # change this to the correct path on your system

    # Define the path to the soundfont file
    soundfont_path = 'venv/assets/midi/GuitarA.sf2'  # change this to the correct path on your system

    # Convert the MIDI file to wav using FluidSynth
    command = [
        fluidsynth_path,
        '-F', 'star_wars.wav',  # output file name
        '-ni', soundfont_path,
        'star_wars.mid'
    ]
    subprocess.run(command)

    # Convert the WAV file to MP3 using FFmpeg
    command = [
        'C:/Users/lprice/AppData/chocolatey/chocoportable/lib/ffmpeg/tools/ffmpeg/bin/ffmpeg.exe',
        '-y', '-i', 'star_wars.wav',
        '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
        'star_wars.mp3'
    ]
    subprocess.run(command)
    fs.delete()

    os.startfile(
        "C:/Users/lprice/OneDrive - Range Resources/Documents/Personal Working Files/7 - Tech/Python/PyCharm Projects/OCR_DDLs/star_wars.mid")


# Define duration variables
quarterNote = 2
halfNote = quarterNote * 2
eighthNote = quarterNote / 2
sixteenthNote = quarterNote / 4

# Define note pitches
notes = ['G4', 'G4', 'G4', 'Eb4', 'Bb4', 'G4', 'Eb4', 'Bb4', 'G4', 'D5', 'D5', 'D5', 'Eb5', 'Bb4', 'G4', 'Eb4',
         'Bb4', 'G4']
pitches = [67, 67, 67, 63, 70, 67, 63, 70, 67, 74, 74, 74, 75, 70, 66, 63, 70, 67]

# Define note durations
durations = [quarterNote, quarterNote, quarterNote, eighthNote + sixteenthNote, sixteenthNote, quarterNote,
             eighthNote + sixteenthNote, sixteenthNote, halfNote, quarterNote, quarterNote, quarterNote,
             eighthNote + sixteenthNote, sixteenthNote, quarterNote, eighthNote + sixteenthNote, sixteenthNote,
             halfNote + halfNote]

createMidiSong(pitches, durations)
