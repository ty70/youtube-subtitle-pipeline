🎥 Automatically Add Subtitles to YouTube Videos (Whisper + ffmpeg + yt-dlp)

This project builds a pipeline that downloads a YouTube video, extracts its audio, transcribes the speech using Whisper, and burns hard subtitles into the video.

Project Structure Example

├── data/                   # Original video and audio files
├── output/                 # Generated subtitles and final video
│   ├── sample.ass          # ass file (sample)
│   ├── sample.mp4          # mp4 file (sample)
│   └── sample.srt          # srt file (sample)
├── scripts/
│   └── whisper_transcription.py
├── requirements.txt
├── README.md
└── README_ja.md (Japanese version)

Sample output of video and subtitle processing

output/sample.mp4 

How to Use

1. Download YouTube Video as MP4

yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 https://your_video_url -o data/input.mp4

2. Convert MP4 to WAV for Whisper

ffmpeg -i data/input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 data/input.wav

* -vn: Ignore the video stream (extract only audio).

* -acodec pcm_s16le: Encode in Linear PCM (16-bit little endian) format.

* -ar 16000: Set the sampling rate to 16kHz.

* -ac 1: Convert to mono audio.

3. Transcribe Audio Using Whisper

scripts/whisper_transcription.py transcribes the .wav file from step 2 using OpenAI Whisper and outputs a .srt subtitle file.

Run the script:

python scripts/whisper_transcription.py --input data/input.wav --output_dir ./output --model_size medium --language ja

This will generate output/input.srt.

4. Burn Subtitles (.srt) into Video

ffmpeg -i data/input.mp4 -vf subtitles=output/input.srt output/output_with_subs.mp4

5. Fix Subtitle Cutoff in Vertical Videos

In portrait-oriented videos, .srt subtitles may get cut off. You can convert them to .ass format and customize layout resolution to fit.

ffmpeg -i output/input.srt output/input.ass
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 data/input.mp4

Example output might be 202,360. Open output/input.ass and update these values:

PlayResX: 202
PlayResY: 360

This adjusts subtitle scaling for vertical screens.

6. Burn .ass Subtitles into Final Video

ffmpeg -i data/input.mp4 -vf "ass=output/input.ass" -c:a copy output/final_with_subs.mp4

📦 Dependencies

- Python 3.8+
- `ffmpeg`
- `yt-dlp`
- `openai-whisper`

Python packages

pip install git+https://github.com/openai/whisper.git

sudo snap install yt-dlp

pip install ffmpeg-python

📝 Notes

* Audio quality significantly affects transcription accuracy.

* Whisper runs faster on GPUs.

* .ass subtitles provide more flexible styling and resolution support than .srt.

This project is released under the MIT license.

Feel free to open issues or suggestions!