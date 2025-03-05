import argparse
from pathlib import Path
import threading
import queue
import numpy as np
import whisper
import sounddevice as sd
import soundfile as sf
import subprocess

# Create a temporary file
temp_audio_file_path = Path(__file__).parent / "temp.mp3"
temp_txt_file_path = Path(__file__).parent / "temp.txt"


def file_dump(data, file_path: Path):
    with file_path.open('w') as f:
        f.write(data)


def record_audio(
        max_duration=30,
        sample_rate=44100  # Standard audio sampling rate
) -> Path:
    print("Press `Enter` to START recording...")
    input()

    print(f"Recording (max {max_duration} seconds)... Press `Enter` to STOP early.")

    # Create a queue to communicate between threads
    audio_queue = queue.Queue()
    stop_event = threading.Event()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        audio_queue.put(indata.copy())

    def record_thread():
        with sd.InputStream(callback=audio_callback,
                            channels=1,
                            samplerate=sample_rate):
            stop_event.wait()

    # Collect audio data
    audio_data = []

    # Start recording thread
    record_thread = threading.Thread(target=record_thread)
    record_thread.start()

    # Wait for user to press Enter (stop recording)
    input()
    stop_event.set()
    record_thread.join()

    # Collect all audio from the queue
    while not audio_queue.empty():
        audio_data.append(audio_queue.get())

    # Convert to numpy array if not empty
    if audio_data:
        recording = np.concatenate(audio_data, axis=0)
    else:
        print("No audio recorded.")
        return None

    # Save recording
    sf.write(temp_audio_file_path, recording, sample_rate)
    print(f"Recording saved to {temp_audio_file_path}")

    return temp_audio_file_path


def copy_to_clipboard(text: str):
    # todo: try with pyperclip?
    try:
        # Try xclip first
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text, text=True, check=True)
        print("Copied to clipboard using xclip")
    except FileNotFoundError:
        try:
            # Try xsel as a backup
            subprocess.run(['xsel', '-b', '-i'], input=text, text=True, check=True)
            print("Copied to clipboard using xsel")
        except FileNotFoundError:
            print("Could not copy to clipboard. Please install xclip or xsel.")


def transcribe_and_copy(model):
    # Record audio
    audio_file_path = record_audio()

    if audio_file_path is None:
        print("Recording failed. Skipping transcription.")
        return None

    # Transcribe
    result = model.transcribe(str(audio_file_path))
    transcription = result["text"]

    # Save transcription to a text file
    file_dump(transcription, file_path=temp_txt_file_path)

    # Copy to clipboard
    copy_to_clipboard(transcription)

    print(f"Transcription:\n{transcription}")
    return transcription


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Continuous Audio Transcription Tool')
    parser.add_argument('-m', '--model',
                        type=str,
                        default='base',
                        choices=['tiny', 'base', 'small', 'medium', 'large', 'turbo'],
                        help='Whisper model size (default: base)')

    # Parse arguments
    args = parser.parse_args()

    # Load the model once
    print(f"Loading Whisper {args.model} model...")
    model = whisper.load_model(args.model)

    print("Model loaded.")

    print("Transcription tool started. Press Ctrl+C to quit.")

    try:
        while True:
            transcribe_and_copy(model)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    finally:
        print("Bye.")


def example():
    model = whisper.load_model("turbo")
    result = model.transcribe(str(temp_audio_file_path))
    print(result["text"])


if __name__ == "__main__":
    # example()
    main()
