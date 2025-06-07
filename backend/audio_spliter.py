# wavファイルを受け取ると、X秒ごとに分割する

# pip install pydub

from pydub import AudioSegment
from io import BytesIO
import math

def split_wav_to_chunks(wav_path, chunk_duration=3000):
    """
    wav_path: 入力のwavファイルパス
    chunk_duration: 分割する長さ（ミリ秒）例: 3000ms = 3秒
    """
    audio = AudioSegment.from_wav(wav_path)
    chunks = []

    total_duration = len(audio)
    num_chunks = math.ceil(total_duration / chunk_duration)

    for i in range(num_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, total_duration)
        chunk = audio[start:end]

        # メモリ上のBytesIOに保存
        wav_io = BytesIO()
        chunk.export(wav_io, format="wav")
        wav_io.seek(0)  # 読み込み位置を先頭に戻す
        chunks.append(wav_io)

    return chunks

if __name__ == "__main__":
    chunks = split_wav_to_chunks("sample_sounds/6月なのに暑すぎませんか.wav", chunk_duration=3000)
    for index, chunk in enumerate(chunks):
        with open(f"sample_sounds/chunk_{index}.wav", "wb") as f:
            f.write(chunk.getbuffer())
        print(f"Chunk {index} saved.")