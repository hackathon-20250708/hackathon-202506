# wavファイルを音声認識し、感情を分析するクラス

# 1. ライブラリインストール
# pip install transformers fugashi ipadic torch
# pip install unidic-lite
# pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --quiet
# pip install -U transformers librosa --quiet

import torch
import torchaudio
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

# モデルと特徴量抽出器の初期化（最初の1回だけ）
model_name = "superb/wav2vec2-base-superb-er"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)

def analyze_emotion(audio_path: str) -> str:
    """
    指定された音声ファイルから感情を分析し、ラベルを返す。
    Parameters:
        audio_path (str): 音声ファイルのパス
    Returns:
        str: 予測された感情ラベル
    """
    waveform, sr = torchaudio.load(audio_path)
    if sr != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(waveform)

    waveform = waveform[0].numpy()  # モノラルに変換

    inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = torch.argmax(logits).item()

    labels = model.config.id2label
    return labels[predicted_class_id]
