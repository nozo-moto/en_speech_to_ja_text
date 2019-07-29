from threading import Thread
from queue import Queue 
import speech_recognition as sr
from googletrans import Translator
import asyncio
# need to install python3-tk https://docs.python.org/ja/3/library/tkinter.html
# mac: brew install tcl-tk
# ubuntu: apt install python3-tk
import tkinter as tk
import tkinter.font as font

root = tk.Tk()
display_text_label = tk.StringVar()

r = sr.Recognizer()
audio_queue = Queue()
translator = Translator()

def text_to_speach(text):
    translated_text = translator.translate(text, dest='ja')
    if translated_text.text != "":
        display_text_label.set(translated_text.text)
        print(translated_text.text)

def recognize_worker():
    while True:
        audio = audio_queue.get() 
        if audio is None: break

        text = ""
        try:
            print("read ")
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass
        text_to_speach(text)

        audio_queue.task_done()

def run_speech_to_translated_text():
    print("run speech to translated_text")
    recognize_thread = Thread(target=recognize_worker)
    recognize_thread.daemon = True
    recognize_thread.start()
    while True:
        with sr.Microphone() as source:
            try:
                audio_queue.put(r.listen(source))
            except KeyboardInterrupt:
                break
            
    # audio_queue.join()
    # audio_queue.put(None)
    # recognize_thread.join()

def display():
    # Tkinter
    print("create display")
    root.title(u"English Speech To Text")
    root.geometry("400x100")

    label_font = font.Font(root,family="System",size=30,weight="normal")
    label = tk.Label(root, textvariable=display_text_label, font=label_font)
    label.pack()
    root.mainloop()


if __name__ == "__main__":
    speech_to_text_thread = Thread(target=run_speech_to_translated_text)
    speech_to_text_thread.start()
    display()