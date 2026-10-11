import wave
import struct
import math
import random

SAMPLE_RATE = 44100

def note_freq(note_name):
    notes = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
             'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
    letter = note_name[:-1]
    octave = int(note_name[-1])
    semitones = notes[letter] + (octave - 4) * 12
    return 440.0 * (2.0 ** ((semitones - 9) / 12.0))

def generate_track_1():
    # Synthwave Neon Grid - 110 BPM
    bpm = 110
    beat_dur = 60.0 / bpm
    total_seconds = 32.0
    total_samples = int(SAMPLE_RATE * total_seconds)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    bass_notes = ['A2', 'F2', 'C3', 'G2']
    arp_notes = [
        ['A3', 'C4', 'E4', 'A4'],
        ['F3', 'A3', 'C4', 'F4'],
        ['C3', 'E3', 'G3', 'C4'],
        ['G3', 'B3', 'D4', 'G4']
    ]

    chord_duration = beat_dur * 4 # 4 beats per chord
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        chord_idx = int((t / chord_duration) % 4)
        beat_idx = int((t / beat_dur) % 4)
        step_16th = int((t / (beat_dur / 4)) % 16)

        # 16th note arpeggio
        note_in_chord = arp_notes[chord_idx][step_16th % 4]
        freq_arp = note_freq(note_in_chord)
        # Synth pulse / saw
        t_note = (t % (beat_dur / 4))
        env_arp = math.exp(-t_note * 9.0)
        arp_val = (math.sin(2 * math.pi * freq_arp * t) + 0.5 * math.sin(4 * math.pi * freq_arp * t)) * env_arp * 0.25

        # Bassline (driving 8th notes)
        step_8th = int((t / (beat_dur / 2)) % 8)
        freq_bass = note_freq(bass_notes[chord_idx])
        t_bass = (t % (beat_dur / 2))
        env_bass = math.exp(-t_bass * 5.0)
        bass_val = (math.sin(2 * math.pi * freq_bass * t) + 0.4 * math.sin(2 * math.pi * freq_bass * 2 * t)) * env_bass * 0.35

        # Drums: Kick on beats 0, 1, 2, 3 (four on the floor)
        kick_val = 0.0
        t_kick = t % beat_dur
        if t_kick < 0.2:
            kick_freq = 150.0 * math.exp(-t_kick * 30.0) + 45.0
            kick_val = math.sin(2 * math.pi * kick_freq * t_kick) * math.exp(-t_kick * 15.0) * 0.5

        # Snare on beats 1 and 3
        snare_val = 0.0
        if beat_idx in [1, 3]:
            t_snare = t_kick
            if t_snare < 0.25:
                noise = (random.random() * 2.0 - 1.0) * math.exp(-t_snare * 20.0) * 0.3
                tone = math.sin(2 * math.pi * 180.0 * t_snare) * math.exp(-t_snare * 25.0) * 0.25
                snare_val = noise + tone

        # Hi-hat on 16th notes
        hat_val = 0.0
        t_hat = t % (beat_dur / 2)
        if t_hat < 0.05:
            hat_val = (random.random() * 2.0 - 1.0) * math.exp(-t_hat * 70.0) * 0.12

        l = (arp_val * 0.7 + bass_val * 0.5 + kick_val * 0.7 + snare_val * 0.6 + hat_val * 0.4)
        r = (arp_val * 0.3 + bass_val * 0.5 + kick_val * 0.7 + snare_val * 0.6 + hat_val * 0.6)

        left[i] = max(-0.95, min(0.95, l))
        right[i] = max(-0.95, min(0.95, r))

    return left, right

def generate_track_2():
    # Rainy Night Cafe (Lo-Fi Jazz) - 78 BPM
    bpm = 78
    beat_dur = 60.0 / bpm
    total_seconds = 30.0
    total_samples = int(SAMPLE_RATE * total_seconds)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Warm jazz chords (frequencies)
    # Dm9, G13, Cmaj9, A7b13
    chords = [
        [note_freq('D3'), note_freq('F3'), note_freq('A3'), note_freq('C4'), note_freq('E4')],
        [note_freq('G2'), note_freq('F3'), note_freq('B3'), note_freq('E4'), note_freq('A4')],
        [note_freq('C3'), note_freq('E3'), note_freq('G3'), note_freq('B3'), note_freq('D4')],
        [note_freq('A2'), note_freq('G3'), note_freq('C#4'), note_freq('F4'), note_freq('C5')]
    ]
    chord_dur = beat_dur * 4

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        chord_idx = int((t / chord_dur) % 4)
        t_in_chord = t % chord_dur

        # Electric piano chords
        chord_sig = 0.0
        env_chord = math.exp(-t_in_chord * 0.8) + 0.15
        for f in chords[chord_idx]:
            # Rhodes-like bell harmonics
            chord_sig += (math.sin(2 * math.pi * f * t) + 0.25 * math.sin(2 * math.pi * f * 2 * t) + 0.1 * math.sin(2 * math.pi * f * 3 * t))
        chord_sig = (chord_sig / len(chords[chord_idx])) * env_chord * 0.35

        # Lo-fi vinyl crackle & rain rustle
        crackle = 0.0
        if random.random() < 0.003:
            crackle = (random.random() * 2.0 - 1.0) * 0.15
        rain = (random.random() * 2.0 - 1.0) * 0.015

        # Chill beat: kick on 0 and 2.5, snare rim on 2
        beat_t = t % (beat_dur * 4)
        kick_val = 0.0
        if (beat_t < 0.2) or (beat_dur * 2.5 <= beat_t < beat_dur * 2.5 + 0.2):
            t_k = beat_t if beat_t < 0.2 else (beat_t - beat_dur * 2.5)
            kick_val = math.sin(2 * math.pi * (100.0 * math.exp(-t_k * 25.0) + 40.0) * t_k) * math.exp(-t_k * 12.0) * 0.45

        # Rimshot on beat 2
        rim_val = 0.0
        if beat_dur * 2 <= beat_t < beat_dur * 2 + 0.15:
            t_rim = beat_t - beat_dur * 2
            rim_val = (math.sin(2 * math.pi * 320.0 * t_rim) * 0.4 + (random.random() * 2.0 - 1.0) * 0.3) * math.exp(-t_rim * 35.0) * 0.35

        l = chord_sig * 0.6 + kick_val * 0.5 + rim_val * 0.4 + crackle + rain
        r = chord_sig * 0.65 + kick_val * 0.5 + rim_val * 0.4 + crackle + rain
        left[i] = max(-0.95, min(0.95, l))
        right[i] = max(-0.95, min(0.95, r))

    return left, right

def generate_track_3():
    # Starglow Symphony (Cosmic Ambient) - 60 BPM
    total_seconds = 32.0
    total_samples = int(SAMPLE_RATE * total_seconds)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Deep ethereal drone
        f1 = 55.0 # A1
        f2 = 110.0 # A2
        f3 = 164.81 # E3
        f4 = 220.0 # A3
        f5 = 277.18 # C#4
        f6 = 329.63 # E4

        # Shimmering slow LFOs
        lfo1 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.2 * t)
        lfo2 = 0.5 + 0.5 * math.cos(2 * math.pi * 0.15 * t)
        lfo3 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.33 * t)

        pad_l = (math.sin(2 * math.pi * f1 * t) * 0.3 +
                 math.sin(2 * math.pi * f2 * t) * 0.25 * lfo1 +
                 math.sin(2 * math.pi * f3 * t) * 0.2 * lfo2 +
                 math.sin(2 * math.pi * f5 * t) * 0.15 * lfo3)
                 
        pad_r = (math.sin(2 * math.pi * f1 * t) * 0.3 +
                 math.sin(2 * math.pi * f2 * t) * 0.25 * lfo2 +
                 math.sin(2 * math.pi * f4 * t) * 0.2 * lfo1 +
                 math.sin(2 * math.pi * f6 * t) * 0.15 * lfo3)

        # Celestial twinkling chime every 4 seconds
        t_chime = t % 4.0
        chime_val = 0.0
        if t_chime < 1.5:
            cf = 880.0 if (int(t / 4.0) % 2 == 0) else 1108.73
            chime_val = math.sin(2 * math.pi * cf * t_chime) * math.exp(-t_chime * 3.5) * 0.2

        left[i] = max(-0.95, min(0.95, (pad_l * 0.6 + chime_val * 0.3)))
        right[i] = max(-0.95, min(0.95, (pad_r * 0.6 + chime_val * 0.7)))

    return left, right

def generate_track_4():
    # Golden Coastline (Sunset Acoustic/Tropical Chill) - 96 BPM
    bpm = 96
    beat_dur = 60.0 / bpm
    total_seconds = 30.0
    total_samples = int(SAMPLE_RATE * total_seconds)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Pluck melody notes
    melody = ['G4', 'B4', 'D5', 'E5', 'D5', 'B4', 'A4', 'G4']

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        step = int((t / (beat_dur / 2)) % len(melody))
        t_note = t % (beat_dur / 2)

        freq = note_freq(melody[step])
        # Guitar/kalimba pluck simulation
        env = math.exp(-t_note * 8.0)
        pluck = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * freq * 2 * t)) * env * 0.35

        # Warm bass
        bass_freq = note_freq('G2') if step < 4 else note_freq('C2')
        bass = math.sin(2 * math.pi * bass_freq * t) * 0.3

        # Shaker groove
        t_shaker = t % (beat_dur / 4)
        shaker = (random.random() * 2.0 - 1.0) * math.exp(-t_shaker * 45.0) * 0.08

        # Warm ocean breeze swell
        breeze = (random.random() * 2.0 - 1.0) * (0.02 + 0.015 * math.sin(2 * math.pi * 0.2 * t))

        l = pluck * 0.7 + bass * 0.5 + shaker * 0.3 + breeze
        r = pluck * 0.4 + bass * 0.5 + shaker * 0.7 + breeze
        left[i] = max(-0.95, min(0.95, l))
        right[i] = max(-0.95, min(0.95, r))

    return left, right

def save_wav(filename, left, right):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for l, r in zip(left, right):
            l_int = int(l * 32767.0)
            r_int = int(r * 32767.0)
            frames.extend(struct.pack('<hh', l_int, r_int))
        wf.writeframes(frames)
    print(f"Generated {filename}")

if __name__ == '__main__':
    print("Synthesizing track 1...")
    l1, r1 = generate_track_1()
    save_wav('assets/audio/synthwave_neon_grid.wav', l1, r1)

    print("Synthesizing track 2...")
    l2, r2 = generate_track_2()
    save_wav('assets/audio/rainy_night_cafe.wav', l2, r2)

    print("Synthesizing track 3...")
    l3, r3 = generate_track_3()
    save_wav('assets/audio/starglow_symphony.wav', l3, r3)

    print("Synthesizing track 4...")
    l4, r4 = generate_track_4()
    save_wav('assets/audio/golden_coastline.wav', l4, r4)
    print("Done!")
