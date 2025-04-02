# AI Music Composer

An AI-powered music composition tool that creates original music in various styles with just a few clicks. The tool generates compositions based on musical parameters, either specified by you or suggested by the AI.

![AI Music Composer](generated-icon.png)

## 🎵 Quick Start

Just run the launcher script for the easiest experience:

```bash
./launch.sh
```

This gives you all the options you need to start composing, analyzing, and managing your AI-generated music.

## 🎹 Features

- **Multiple Music Styles**: Create compositions in classical, jazz, pop, rock, or electronic styles
- **AI-Suggested Parameters**: Let the AI choose appropriate musical parameters for coherent compositions
- **Custom Control**: Specify your own key, tempo, instruments, and more if you prefer
- **Multi-Style Generation**: Generate compositions in all styles at once to compare them
- **MIDI Analysis**: Examine the structure of any MIDI composition 
- **Composition Combining**: Merge multiple compositions either sequentially or layered

## 📋 Using the Tools

### Interactive Launcher

Run the interactive launcher for the simplest experience:

```bash
./launch.sh
```

### Generate a Quick Composition

For a fast composition with AI-suggested parameters:

```bash
./run_composer.sh
```

This will:
1. Generate a composition with AI-suggested parameters
2. Save it as `ai_composition.mid`
3. Analyze the composition structure

### Custom Composition

To create a composition with your own parameters:

```bash
python main.py
```

Then select option 1 and follow the prompts to specify:
- Tempo (BPM)
- Key (C, D, E, F, G, A, B with optional # or b)
- Mode (major or minor)
- Style (classical, jazz, pop, rock, electronic)
- Duration (in seconds)
- Instruments (comma-separated list)
- Chord complexity (0.0-1.0)
- Rhythm variation (0.0-1.0)

### Generate in Multiple Styles

To create compositions in all available styles:

```bash
./explore_styles.sh
```

### Analyze a MIDI File

To examine the structure of a MIDI file:

```bash
python analyze_midi.py your_file.mid
```

### Combine MIDI Files

To merge multiple compositions together:

```bash
python combine_midi.py
```

This tool allows you to combine files either:
- **Sequentially**: Play one composition after another
- **Layered**: Play all compositions simultaneously

### Play a MIDI File

To attempt playback (requires proper audio setup):

```bash
python play_music.py your_file.mid
```

Note: Playback requires Timidity configuration which may not be available in all environments.

## 🧩 Project Structure

- `launch.sh` - Interactive launcher for all features
- `compose.py` - User-friendly interactive menu interface
- `main.py` - Command-line interface for composition
- `ai_composer.py` - Core AI composer orchestration
- `music_generator.py` - Music generation logic
- `audio_processor.py` - Audio file handling
- `analyze_midi.py` - Tool for inspecting MIDI file content
- `combine_midi.py` - Tool for merging multiple compositions
- `play_music.py` - Playback functionality
- `run_composer.sh` - Helper script for quick generation
- `explore_styles.sh` - Helper script for multi-style generation
- `models/` - Data models for music parameters and styles
- `utils/` - Helper utilities for music theory and file handling

## 📋 Available Music Styles

- **Classical**: Traditional Western classical patterns with rich harmonies
- **Jazz**: Swinging rhythms and complex harmonies with improvisation-like melodies
- **Pop**: Catchy and repetitive patterns with simple chord progressions
- **Rock**: Driving rhythms with guitar-focused arrangements
- **Electronic**: Modern electronic music patterns with synthesizer sounds

## 🎻 Available Instruments

The system supports many instruments including:
- Piano, Guitar, Electric Guitar
- Bass, Bass Guitar, Double Bass 
- Violin, Cello, Flute, Saxophone
- Drums, Synth, Synth Lead, Synth Bass, Pad

## 🔍 Examining Your Compositions

When you generate a composition, the system will provide a preview showing:
- Number of parts/instruments
- Number of measures
- Number of notes per instrument
- Preview of notes and patterns

For a deeper analysis, use the analyze_midi.py tool which shows:
- MIDI format details
- Track information
- Instrument assignments
- Note distribution and velocities

## 💾 Downloading Your Compositions

To use your compositions outside of this environment:
1. Generate compositions using any of the methods described
2. Download the .mid files
3. Open them with any MIDI player, DAW, or notation software

## 🧪 Experimental Features

- **Composition Combining**: The `combine_midi.py` tool allows you to merge multiple generated compositions
- **Style Explorer**: The `explore_styles.sh` script generates compositions in all available styles at once

## 📚 Dependencies

- music21 - Music analysis and manipulation framework
- pygame - Used for audio playback
- mido - MIDI file handling
- numpy - Numerical operations