import queue, os, threading
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import time
import pygame
from gtts import gTTS
import requests, json

q = queue.Queue()
recorder = False
recording = False

def complicated_record():
    with sf.SoundFile("temp.wav", mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
        with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
            while recording:
            	file.write(q.get())
        
def complicated_save(indata, frames, time, status):
    q.put(indata.copy())
    
def start():
    global recorder
    global recording
    recording= True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()
    
def stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')
    
start()
time.sleep(3)
stop()

#%%


headers = {
    #Transfer-Encoding: chunked # 보내는 양을 모를 때 헤더에 포함한다.
    'Host': 'kakaoi-newtone-openapi.kakao.com',
    'Content-Type': 'application/octet-stream',
    'X-DSS-Service': 'DICTATION',
    'Authorization': f'KakaoAK 37aaf49135840088d4fd3510d3905f37',
}

data = open("temp.wav", "rb").read() # wav 파일을 바이너리 형태로 변수에 저장한다.
response = requests.post('https://kakaoi-newtone-openapi.kakao.com/v1/recognize', headers=headers, data=data)
# 요청 URL과 headers, data를 post방식으로 보내준다.

text = response.text
text = text.split('finalResult","value":"')[1]
text = text.split('",')[0]

print(text)
#%%

def speak(text): 
	tts = gTTS(text=text, lang='ko') 
	tts.save('voice.mp3') 

speak(text)

#%%

pygame.mixer.init()
pygame.mixer.music.load('voice.mp3')
pygame.mixer.music.play()
