import pyttsx3
import threading

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech speed
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    tts_thread = threading.Thread(target=speak, args=(text,))
    tts_thread.start()
