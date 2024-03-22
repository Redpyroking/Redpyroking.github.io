import pyttsx3

text_speech = pyttsx3.init()

answer = ""

text_speech.say(answer)
text_speech.runAndWait()

def speak(new_answer):
    text_speech.say(new_answer)
    text_speech.runAndWait()