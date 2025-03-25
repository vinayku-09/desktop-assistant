import speech_recognition as sr

def speech_to_text():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... Please speak.")
            audio = r.listen(source)
            return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand that."
    except sr.RequestError:
        return "Speech recognition service is unavailable."
    except OSError:
        return "Microphone not detected."


# Call the function to start speech recognition
speech_to_text()

