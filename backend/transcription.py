# wavファイルを受け取ると、音声認識を行い、テキストに変換するクラス

# pip install python-dotenv
# pip install google-generativeai

# APIキーを環境変数から取得. 流出したらやばいから.envファイルに保存+.gitignoreに追加
# transcriber.py

from dotenv import load_dotenv
import google.generativeai as genai
#from google import genai
import os

class AudioTranscriber:
    """
    Google Geminiを使ってWAV音声ファイルを日本語で文字起こしするクラス
    """

    def __init__(self, env_path=".env"):
        # 環境変数（APIキー）の読み込み
        load_dotenv(env_path)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API_KEYが環境変数に設定されていません。.envファイルを確認してください。")

        # Geminiクライアントの初期化
        self.client = genai.Client(api_key=api_key)

    def transcribe(self, wav_file_path: str) -> str:
        """
        指定されたWAVファイルを日本語で文字起こしして返す

        Parameters:
            wav_file_path (str): 音声ファイル（.wav）のパス

        Returns:
            str: 文字起こし結果のテキスト
        """
        try:
            # ファイルアップロード
            print(f"アップロード中: {wav_file_path}")
            uploaded_file = self.client.files.upload(file=wav_file_path)

            # モデルに日本語での文字起こしを依頼
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["この音声ファイルの内容を日本語で文字起こししてください", uploaded_file]
            )
            
            print(response.text)

            return response.text

        except Exception as e:
            return f"エラーが発生しました: {e}"
        

if __name__ == "__main__":
    transcriber = AudioTranscriber()
    result = transcriber.transcribe("sample_sounds/6月なのに暑すぎませんか.wav")
    print("\n--- 文字起こし結果 ---\n")
    print(result)