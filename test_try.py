import os
from google.cloud import speech

# Google Cloud 인증 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test2-388310-65b7d7dfa68e.json"

# 음성 파일 경로 설정
audio_file_path = "audio.wav"

# 원하는 단어 리스트
target_words = ["안녕하세요","멋진"]

# 클라이언트 초기화
client = speech.SpeechClient()

# 음성 파일을 읽어들임
with open(audio_file_path, "rb") as audio_file:
    audio_data = audio_file.read()

# 음성을 텍스트로 변환
audio = speech.RecognitionAudio(content=audio_data)
config = speech.RecognitionConfig(language_code="ko-KR")

response = client.recognize(config=config, audio=audio)

# 인식된 텍스트 확인 및 원하는 단어 검사
for result in response.results:
    transcript = result.alternatives[0].transcript
    print("인식된 텍스트:", transcript)
    
    for target_word in target_words:
        if target_word in transcript:
            print("원하는 단어 '{}'가 포함되어 있습니다.".format(target_word))
            # 원하는 단어를 기록하는 추가 작업 수행
            # ...
        else:
            print("원하는 단어 '{}'가 포함되어 있지 않습니다.".format(target_word))
