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
    Google Gemini 2.0 Flash を使って音声ファイルを日本語で文字起こしするクラス
    """

    def __init__(self, env_path=".env"):
        # .env から API キー読み込み
        load_dotenv(env_path)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY が環境変数に設定されていません。")

        # Gemini API キーを設定
        genai.configure(api_key=api_key)

        # モデルの初期化
        self.model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")

    def transcribe(self, wav_file_path: str) -> str:
        """
        音声ファイルを日本語で文字起こしする
        """
        try:
            # ファイルアップロード
            uploaded_file = genai.upload_file(wav_file_path)
            print(f"ファイルをアップロードしました: {uploaded_file.uri}")

            # 文字起こしリクエスト
            response = self.model.generate_content(
                [
                    "この音声ファイルの内容を日本語で文字起こししてください。音声がないときは「no-voice」と返してください。",
                    uploaded_file
                ]
            )

            return response.text

        except Exception as e:
            return f"エラーが発生しました: {e}"
        

if __name__ == "__main__":
    transcriber = AudioTranscriber()
    result = transcriber.transcribe("sample_sounds/6月なのに暑すぎませんか.wav")
    print("\n--- 文字起こし結果 ---\n")
    print(result)