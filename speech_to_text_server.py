from threading import Thread
from queue import Queue  # Python 3 import 
import speech_recognition as sr
from googletrans import Translator
import asyncio
import asyncio
import websockets
from datetime import datetime

r = sr.Recognizer()
audio_queue = Queue()
text_queue = Queue()
translator = Translator()

event_loop = asyncio.get_event_loop()

def text_to_speach(text):
    translated_text = translator.translate(text, dest='ja')
    text_queue.put(translated_text.text)

def recognize_worker():
    while True:
        audio = audio_queue.get()
        if audio is None: break

        text = ""
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(e)
            pass
        text_to_speach(text)
        audio_queue.task_done()

def run_speech_to_text():
    with sr.Microphone() as source:
        try:
            while True:
                audio_queue.put(r.listen(source))
        except KeyboardInterrupt:
            pass
    
    audio_queue.join()


speech_to_text_thread = Thread(target=run_speech_to_text)
speech_to_text_thread.daemon = True

recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()

async def echo(websocket, path):
    speech_to_text_thread.start()
    while True:
        text = text_queue.get()
        if text is None: break
        await websocket.send(text)

if __name__ == "__main__":
    start_server = websockets.serve(echo, "localhost", 8765)
    event_loop.run_until_complete(start_server)
    event_loop.run_forever()
#    recognize_thread.join()
#    speech_to_text_threaid.join()
