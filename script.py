import os, sys

def open_directory(path):
  if sys.platform.startswith('darwin'):  # macOS
    os.system('open "{}"'.format(path))
  elif sys.platform.startswith('win'):  # Windows
    os.system('start "" "{}"'.format(path))
  elif sys.platform.startswith('linux'):  # Linux
    os.system('xdg-open "{}"'.format(path))
  else:
    print("Unsupported operating system.")

from openai import OpenAI
from pathlib import Path

client = ''

def load_client(api_key):
  global client
  client = OpenAI(api_key=api_key)

def get_tts(text, model='tts-1', voice='alloy'):
  text_arr = text.split(' ')
  filename = '_'.join(text_arr[:min(len(text_arr), 3)]) + '.mp3'
  speech_file_path = Path(__file__).parent / filename
  response = client.audio.speech.create(
    model=model,
    voice=voice,
    input=text
  )
  response.stream_to_file(speech_file_path)
  open_directory(filename)

def get_stt(filename, model='whisper-1'):
  transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=filename
  )
  return transcript.text