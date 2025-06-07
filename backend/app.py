from flask import Flask, request, jsonify
from flask_cors import CORS
from emotion_analyzer import analyze_emotion  # ← 同じフォルダなのでこれでOK
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        file.save(tmp.name)
        audio_path = tmp.name

    analyzed_result = analyze_emotion(audio_path)  # ← emotion_analyzer.pyの関数を実行

    dummy_result = {
        "words": [
            {"text": "こんにちは", "emotion": "neu"},
            {"text": "最悪", "emotion": "ang"},
            {"text": "まあまあ", "emotion": "hap"},
            {"text": "悲しい", "emotion": "sad"}
        ]
    }

    return jsonify(dummy_result)

    #return jsonify({"words": analyzed_result})

if __name__ == '__main__':
    app.run(debug=True)

