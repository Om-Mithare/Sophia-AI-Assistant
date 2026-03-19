import time
import pyttsx3
import speech_recognition as sr
import eel

# ✅ Text to speech
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

# ✅ Voice recognition
@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except Exception:
            return ""

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        time.sleep(1)
        eel.DisplayMessage(query)
    except Exception:
        return ""
    
    return query.lower()

# ✅ All commands
@eel.expose
def allCommands():
    query = takeCommand()
    print("Query:", query)

    if not query:
        from engine.features import playAssistantSound
        playAssistantSound()
        return

    # Local imports to avoid circular import
    from engine.features import (
        openCommand, PlayYoutube, sendWhatsAppMessage,
        getWeather, tellJoke, setTimer
    )

    # --- Commands ---
    if 'open' in query:
        openCommand(query)
    elif 'on youtube' in query:
        PlayYoutube(query)
    elif 'message' in query or 'whatsapp' in query:
        sendWhatsAppMessage(query)
    elif 'weather' in query:
        # Optional: extract city
        city = query.replace("weather", "").strip()
        if not city:
            city = "Shravan"
        getWeather(city)
    elif 'joke' in query:
        tellJoke()
    elif 'timer' in query:
        import re
        # extract seconds: "set timer for 10 seconds"
        match = re.search(r'(\d+)', query)
        if match:
            seconds = int(match.group(1))
            setTimer(seconds)
        else:
            speak("Please specify time in seconds")
    else:
        speak("Sorry, I can't do that yet.")

    eel.ShowHood()