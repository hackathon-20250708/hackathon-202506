from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os


from audio_spliter import split_wav_to_chunks
from emotion_analyzer import analyze_emotion
from transcription import AudioTranscriber

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    # file = request.files['audio']
    
    # # 一時ファイルとして保存
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
    #     file.save(tmp.name)
    #     audio_path = tmp.name

    # # 音声ファイルを1秒ごとに分割（1000ms）
    # chunks = split_wav_to_chunks(audio_path, chunk_duration=5000)

    # # 文字起こしと感情分析のインスタンス
    # transcriber = AudioTranscriber()

    # results = []
    # for chunk_io in chunks:
    #     # 一時ファイルとして保存
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as chunk_tmp:
    #         chunk_tmp.write(chunk_io.read())
    #         chunk_path = chunk_tmp.name

    #     # 感情分析
    #     try:
    #         emotion = analyze_emotion(chunk_path)
    #     except Exception as e:
    #         emotion = "err"

    #     # 文字起こし
    #     try:
    #         text = transcriber.transcribe(chunk_path)
    #         # 余分な空白や改行を除去
    #         text = text.strip().replace("\n", "")
    #     except Exception as e:
    #         text = "エラー"

    #     # 結果に追加
    #     if text:  # 空でなければ
    #         results.append({"text": text, "emotion": emotion})

    #     os.remove(chunk_path)  # 一時ファイル削除

    # os.remove(audio_path)  # 元のファイル削除

    # return jsonify({"words": results})
    dummy_result = {
        "words": [
            {"text": "こんにちは", "emotion": "neu"},
            {"text": "最悪", "emotion": "ang"},
            {"text": "まあまあ", "emotion": "hap"},
            {"text": "悲しい", "emotion": "sad"}
        ]
    }
    return jsonify(dummy_result)

if __name__ == '__main__':
    app.run(debug=True)

