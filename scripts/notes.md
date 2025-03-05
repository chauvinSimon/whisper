## installation

```bash
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
pip install sounddevice soundfile
```

## usage

```bash
python my_tts.py [--model base]
```

#### alias in `~/.bashrc`

```bash
alias whisper="conda activate whisper; cd /home/simon-chauvin/drafts/whisper/scripts; conda activate whisper; python my_tts.py"
```
