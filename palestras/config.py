import concurrent.futures
import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import subprocess

def transcribe_segment(audio_segment, language="pt-BR"):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        audio_segment.export(temp_filename, format="wav")

    with sr.AudioFile(temp_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError:
            text = "[Inaudível]"
        except sr.RequestError as e:
            text = f"[Erro: {e}]"
    
    os.unlink(temp_filename)
    return text

class YouTubeTranscriber:
    def __init__(self, url, download_path='downloads'):
        self.url = url
        self.download_path = download_path
        self.audio_path = ""
        self.transcription = None
        self.file = f"audio_{hash(url)}.wav"


    def check_ffmpeg_installed(self):
        try:
            subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def download_audio(self):
        try:
            if not self.check_ffmpeg_installed():
                print("ffmpeg não está instalado ou não foi encontrado no PATH.")
                return ""

            os.makedirs(self.download_path, exist_ok=True)
            self.audio_path = os.path.join(self.download_path, self.file)
            command = f"yt-dlp -x --audio-format wav -o {self.audio_path} {self.url}"
            print(f"Comando de download: {command}")
            subprocess.run(command, shell=True, check=True)
            print(f"Áudio baixado para {self.audio_path}")
            return self.audio_path
        except subprocess.CalledProcessError as e:
            print(f"Erro ao baixar o áudio: {e}")
            return ""

        
    def transcribe_large_audio(self, language="pt-BR", chunk_duration=30):
        audio = AudioSegment.from_wav(self.audio_path)
        chunks = [audio[i:i+chunk_duration*1000] for i in range(0, len(audio), chunk_duration*1000)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            transcriptions = list(executor.map(lambda chunk: transcribe_segment(chunk, language), chunks))
        
        self.transcription = " ".join(transcriptions).strip()
        return self.transcription

    def get_transcription(self):
        if self.transcription:
            return self.transcription
        else:
            print("Nenhuma transcrição disponível. Execute transcribe_large_audio() primeiro.")
            return None

    def process(self):
        if self.download_audio():
            return self.transcribe_large_audio()
        return None

