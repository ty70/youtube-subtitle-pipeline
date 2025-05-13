# ==========================
# Whisper 音声文字起こしスクリプト
#
# 動作概要:
#   このスクリプトは、指定された音声ファイル（例: .wav）を OpenAI Whisper を使って文字起こしし、
#   SRT形式の字幕ファイルとして出力ディレクトリに保存します。
#
# 入力:
#   --input        音声ファイルのパス（必須）
#   --output_dir   出力先ディレクトリ（省略可、デフォルト: ./output）
#   --model_size   使用するWhisperモデルのサイズ（例: tiny, base, small, medium, large）
#   --language     音声の言語コード（例: ja = 日本語）
#
# 出力:
#   指定された output_dir に SRT 字幕ファイルを生成（例: output/input.srt）
#
# 実行例:
#   python whisper_transcription.py --input data/input.wav --output_dir output --model_size medium --language ja
# ==========================

import argparse      # コマンドライン引数を処理するためのモジュール
import os            # ファイルやディレクトリの操作に使用
import whisper       # OpenAIのWhisper音声認識ライブラリ
from whisper.utils import WriteSRT  # WhisperのSRT字幕出力ユーティリティ

def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Whisperで音声ファイルを文字起こしし、字幕ファイル（.srt）を出力します。")
    parser.add_argument('--input', type=str, required=True, help='入力音声ファイルのパス（例: audio.wav）')
    parser.add_argument('--output_dir', type=str, default='./output', help='字幕ファイルの出力先ディレクトリ（デフォルト: ./output）')
    parser.add_argument('--model_size', type=str, default='medium', help='使用するWhisperモデルのサイズ（例: tiny, base, small, medium, large）')
    parser.add_argument('--language', type=str, default='ja', help='音声の言語コード（例: ja は日本語）')
    args = parser.parse_args()

    # Whisperモデルの読み込み
    print(f"Whisperモデル「{args.model_size}」を読み込み中...")
    model = whisper.load_model(args.model_size)

    # 音声ファイルを文字起こし
    print(f"文字起こしを開始します: {args.input}")
    result = model.transcribe(args.input, language=args.language, task="transcribe")

    # 出力ディレクトリの作成（存在しない場合のみ）
    os.makedirs(args.output_dir, exist_ok=True)

    # SRT字幕ファイルの書き出し
    writer = WriteSRT(output_dir=args.output_dir)
    writer(result, args.input)

    # ファイル名の取得
    base_filename = os.path.splitext(os.path.basename(args.input))[0]
    srt_path = os.path.join(args.output_dir, f"{base_filename}.srt")

    print(f"文字起こしが完了しました。SRT字幕ファイルの保存先: {srt_path}")

if __name__ == "__main__":
    main()
