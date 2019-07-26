from threading import Thread
try:
    from queue import Queue  # Python 3 import
except ImportError:
    from Queue import Queue  # Python 2 import

import speech_recognition as sr
from googletrans import Translator
import asyncio

r = sr.Recognizer()
audio_queue = Queue()
translator = Translator()

loop = asyncio.get_event_loop()

async def text_to_speach(text):
    translated_text = translator.translate(text, dest='ja')
    print(translated_text.text)

def recognize_worker():
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done

        text = ""
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
#            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))

            text = r.recognize_google(audio)
            
        except sr.UnknownValueError:
            pass
#            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            pass
#            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        loop.run_until_complete(text_to_speach(text))

        audio_queue.task_done()  # mark the audio processing job as completed in the queue


# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source))
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stog
