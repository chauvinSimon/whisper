# Record, Transcribe, and Copy to Clipboard

## Overview

The `my_tts.py` script records audio from your microphone, transcribes it to text using OpenAI's Whisper model, and copies the transcribed text to the clipboard.

## Features

- Start recording by pressing **Enter**.
- Stop recording early by pressing **Enter** again, or it will automatically stop after **30 seconds**.
- Saves the recorded audio as `tmp.mp3`.
- Uses Whisper's speech-to-text model to transcribe the recorded audio.
- Copies the transcribed text to the clipboard for easy pasting.

## installation

```bash
# Install Whisper (read its README for more details)
conda create -n whisper python=3.9.11
conda activate whisper
git clone https://github.com/openai/whisper.git
cd whisper/
pip install -e .
```

```bash
# On ubuntu:

# Install clipboard utility (choose one)
sudo apt-get install xclip
# OR
sudo apt-get install xsel
```

```bash
pip install pyperclip sounddevice soundfile
```

## How to Use

1. **Run the script**:

   ```sh
   python my_tts.py [--model base]
   ```

2. **Start recording**: Press **Enter**.

3. **Stop recording**: Press **Enter** again or wait for **30 seconds**.

4. **View transcription**: The transcribed text will be displayed in the terminal.

5. **Clipboard access**: The transcription is automatically copied to your clipboard, ready to paste anywhere.

## Trick: set an alias in `~/.bashrc`

```bash
# change the path to the script!
alias whisper="conda activate whisper; cd /home/simon-chauvin/drafts/whisper/scripts; conda activate whisper; python my_tts.py --model turbo"
```

