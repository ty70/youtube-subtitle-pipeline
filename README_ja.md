🎥 YouTube動画に自動で字幕をつけるツール（Whisper + ffmpeg + yt-dlp）

このプロジェクトはYouTube動画をダウンロードし、その動画から音声を分離し、Whisperを使って文字起こしを行い、最終的に動画にハードサブタイトを埋め込むパイプラインです。

プロジェクト構成例
```
├── data/                   # 元の動画・音声ファイル
├── output/                 # 出力された字幕・最終動画
│   ├── sample.ass          # assファイル（サンプル）
│   ├── sample.mp4          # mp4ファイル（サンプル）
│   └── sample.srt          # srtファイル（サンプル）
├── scripts/
│   └── whisper_transcription.py
├── requirements.txt
├── README.md
└── README_ja.md(このファイル)
```
動画・字幕処理のサンプル出力
output/sample.mp4 

実行のステップ

1. YouTube 動画を mp4 でダウンロード
```
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 https://ダウンロードするURL -o data/input.mp4
```
2. mp4 から wav へ変換（Whisper用）
```
ffmpeg -i data/input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 data/input.wav
```
* -vn: 映像ストリームを無視します（音声のみを抽出）。

* -acodec pcm_s16le: リニアPCM（16ビット・リトルエンディアン）フォーマットでエンコード。

* -ar 16000: サンプリングレートを16kHzに設定。

* -ac 1: モノラル音声に変換。

3. Whisper で文字起こし

scripts/whisper_transcription.py は、ステップ2で変換された .wav ファイルを使って日本語の文字起こしを実行し、.srt 字幕ファイルを生成するPythonスクリプトです。

実行方法：
```
python scripts/whisper_transcription.py --input data/input.wav --output_dir ./output --model_size medium --language ja
```
このスクリプトを実行すると、output/input.srt に字幕ファイルが出力されます。

4. 字幕ファイル（.srt）を動画に埋め込む
```
ffmpeg -i data/input.mp4 -vf subtitles=output/input.srt output/final_with_subs.mp4
```
5. 縦型動画で字幕が切れる場合

縦長の動画では、.srt ファイルによる字幕が画面に収まりきらず、切れてしまうことがあります。この場合、.srt を .ass に変換し、画面サイズに合ったレイアウトを調整することで改善できます。
```
ffmpeg -i output/input.srt output/input.ass
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 data/input.mp4
```
上記 ffprobe の出力（例：202,360）を確認し、output/input.ass ファイルをテキストエディタで開いて以下のように修正します：
```
PlayResX: 202
PlayResY: 360
```
これにより、字幕のサイズと位置が縦型動画に適したものになります。

6. .ass 字幕を埋め込んだ最終動画出力
```
ffmpeg -i data/input.mp4 -vf "ass=output/input.ass" -c:a copy output/final_with_subs.mp4
```
📦 依存関係

- Python 3.8+
- `ffmpeg`
- `yt-dlp`
- `openai-whisper`

Python パッケージ
```
pip install git+https://github.com/openai/whisper.git

sudo snap install yt-dlp

pip install ffmpeg-python
```
📝 メモ

* 音声の品質が文字起こしの精度に影響します。

* WhisperはGPUを使うと高速です。

* .ass形式の字幕は、スタイルや画面サイズへの柔軟な対応が可能です。

このプロジェクトは MIT ライセンスのもとで公開されています。

意見や質問があれば歓迎します！