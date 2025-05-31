# 🎥 Auto-Subtitle Tool for YouTube Videos (Whisper + ffmpeg + yt-dlp)

This project is a pipeline that downloads YouTube videos, extracts audio from them, performs speech-to-text transcription using Whisper, and finally burns hard subtitles into the video.

## Project Structure Example

```
├── input/                  # Original video/audio files
├── output/                 # Output subtitles and final video
│   ├── sample.ass          # ASS subtitle file (example)
│   ├── sample.mp4          # MP4 file (example)
│   └── sample.srt          # SRT subtitle file (example)
├── scripts/
│   └── whisper_transcription.py
├── requirements.txt
├── README_ja.md            # japanese version 
└── README.md               # this file
```

### Example Output for Video and Subtitle Processing:

`output/sample.mp4`

## Execution Steps

### 1. Check available formats for the YouTube video

```bash
yt-dlp -F https://www.youtube.com/shorts/jqEtBwYljB4
```

### 2. Download the YouTube video in the desired format

```bash
yt-dlp -f 18 https://www.youtube.com/shorts/jqEtBwYljB4 -o input/sample.mp4
```

### 3. Convert MP4 to WAV for Whisper

```bash
ffmpeg -i input/sample.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 input/sample.wav
```

* `-vn`: Ignore video stream (extract audio only).
* `-acodec pcm_s16le`: Encode using Linear PCM (16-bit little endian).
* `-ar 16000`: Set sampling rate to 16kHz.
* `-ac 1`: Convert to mono audio.

### 4. Transcribe with Whisper

`scripts/whisper_transcription.py` is a Python script that transcribes the `.wav` file into Japanese text using Whisper and generates an `.srt` subtitle file.

To run:

```bash
python scripts/whisper_transcription.py --input input/sample.wav --output_dir ./output --model_size medium --language ja
```

The subtitles will be saved as `output/sample.srt`.

### 5. Handling subtitle clipping in vertical videos

In vertical videos, subtitles from `.srt` files may get cut off. In this case, convert `.srt` to `.ass` and adjust the layout for your video dimensions.

```bash
ffmpeg -i output/sample.srt output/sample.ass
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input/sample.mp4
```

Check the output dimensions (e.g., `360,640`) and edit `output/sample.ass` with a text editor:

```ass
PlayResX: 360
PlayResY: 640
```

This will reposition subtitles to better fit the vertical video format.

### 6. Burn .ass subtitles into the video

```bash
ffmpeg -i input/sample.mp4 -vf "ass=output/sample.ass" -c:a copy output/sample.mp4
```

## 📦 Dependencies

* Python 3.8+
* `ffmpeg`
* `yt-dlp`
* `openai-whisper`

Python packages:

```bash
pip install git+https://github.com/openai/whisper.git
sudo snap install yt-dlp
pip install ffmpeg-python
```

## 📝 Notes

* Audio quality affects transcription accuracy.
* Whisper performs faster with a GPU.
* `.ass` subtitle format offers more flexibility in styling and screen positioning.

This project is released under [the MIT License](./LICENSE).

Feedback and questions are always welcome!
