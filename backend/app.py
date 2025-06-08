# pip install pydub

from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
from pydub import AudioSegment

from audio_spliter import split_wav_to_chunks
from emotion_analyzer import analyze_emotion
from transcription import AudioTranscriber

app = Flask(__name__)
CORS(app)

def convert_webm_to_wav(input_path):
    """
    webm形式の音声ファイルをwavに変換してパスを返す
    """
    output_path = input_path.replace(".webm", ".wav")
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(output_path, format="wav")
    return output_path

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    file = request.files['audio']

    # 一時ファイルとして保存（ファイル拡張子に注意）
    ext = os.path.splitext(file.filename)[1]
    suffix = ext if ext else ".webm"  # 録音データは拡張子なしの場合もある
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        input_path = tmp.name

    # 必要に応じてwebm → wavに変換
    if suffix == ".webm":
        audio_path = convert_webm_to_wav(input_path)
        os.remove(input_path)  # 元のwebm削除
    else:
        audio_path = input_path

    # 音声ファイルを5秒ごとに分割
    chunks = split_wav_to_chunks(audio_path, chunk_duration=5000)

    transcriber = AudioTranscriber()
    results = []

    for chunk_io in chunks:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as chunk_tmp:
            chunk_tmp.write(chunk_io.read())
            chunk_path = chunk_tmp.name

        try:
            emotion = analyze_emotion(chunk_path)
        except Exception as e:
            emotion = "err"

        try:
            text = transcriber.transcribe(chunk_path)
            text = text.strip().replace("\n", "")
        except Exception as e:
            text = "エラー"

        if text:
            results.append({"text": text, "emotion": emotion})

        os.remove(chunk_path)

    os.remove(audio_path)  # 元のファイル削除

    return jsonify({"words": results})
    # dummy_result = {
    #     "words": [
    #         {"text": "こんにちは", "emotion": "neu"},
    #         {"text": "最悪", "emotion": "ang"},
    #         {"text": "まあまあ", "emotion": "hap"},
    #         {"text": "悲しい", "emotion": "sad"}
    #     ]
    # }
    # return jsonify(dummy_result)

if __name__ == '__main__':
    app.run(debug=True)