import argparse
from pathlib import Path

import whisper
import sounddevice as sd
import numpy as np
import soundfile as sf
import pyperclip
import time
import threading

# Create a temporary file
temp_audio_file_path = Path(__file__).parent / "temp.mp3"
temp_txt_file_path = Path(__file__).parent / "temp.txt"


def file_dump(data, file_path: Path):
    with file_path.open('w') as f:
        f.write(data)


def record_audio(
        max_duration=30,  # Maximum recording duration (seconds) set by whisper
        samplerate=44100,  # Sample rate (samples/second)
        channels=1
):
    print("Press `Enter` to START recording...")
    input()  # Wait for user to press Enter to start recording
    print(f"Recording... Press `Enter` to STOP early (Max {max_duration} seconds).")

    recording = []  # List to store recorded audio chunks
    start_time = time.time()  # Record start time
    stop_event = threading.Event()  # Event to signal stopping the recording

    # Function to listen for Enter key in a separate thread
    def wait_for_stop():
        input()  # Wait for user input (Enter key)
        stop_event.set()  # Signal to stop recording

    stop_thread = threading.Thread(target=wait_for_stop, daemon=True)  # Run input listener in background
    stop_thread.start()

    # Callback function for the audio stream
    def callback(indata, frames, stream_time, status):
        if status:  # Print any stream errors
            print(status)
        recording.append(indata.copy())  # Store incoming audio data

    # Start audio recording
    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
        while time.time() - start_time < max_duration:  # Continue recording until max duration
            if stop_event.is_set():  # Stop if Enter key was pressed
                break
            time.sleep(0.1)  # Sleep briefly to prevent CPU overuse

    # Combine recorded chunks into a single array
    audio_data = np.concatenate(recording, axis=0)

    # Save recording
    sf.write(temp_audio_file_path, audio_data, samplerate)
    print(f"Recording saved to {temp_audio_file_path}")
    return temp_audio_file_path


def transcribe_audio(model, filename):
    result = model.transcribe(filename)  # Transcribe the audio file
    text = result["text"]  # Extract transcribed text
    print(f"Transcription:\n{text}")
    return text


def main():
    parser = argparse.ArgumentParser(description='Continuous Audio Transcription Tool')
    parser.add_argument('-m', '--model',
                        type=str,
                        default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large', 'turbo'],
                        help='Whisper model size (default: base)')
    args = parser.parse_args()

    # Load the model once
    print(f"Loading Whisper {args.model} model...")
    model = whisper.load_model(args.model)
    print("Model loaded.\nTranscription tool started. Press Ctrl+C to quit.")

    try:
        while True:
            audio_file = record_audio()
            transcription = transcribe_audio(model, audio_file)
            file_dump(transcription, temp_txt_file_path)
            pyperclip.copy(transcription)  # Copy transcription to clipboard
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        print("Bye.")


if __name__ == "__main__":
    main()
