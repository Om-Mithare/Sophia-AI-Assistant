import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel
import pywhatkit as kit
import requests
import random
import threading
import time
from engine.config import ASSISTANT_NAME

# 🔹 Database
conn = sqlite3.connect("sophia.db")
cursor = conn.cursor()

# ✅ Play assistant startup sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

# ✅ Click sound for mic button
@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)

# ✅ Open system or web apps
def openCommand(query):
    from engine.command import speak  # local import to avoid circular import

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query != "":
        try:
            # Check sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name)=?', (query,))
            results = cursor.fetchall()
            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return

            # Check web_command table
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name)=?', (query,))
            results = cursor.fetchall()
            if results:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            # fallback
            speak("Opening " + query)
            try:
                os.system('start ' + query)
            except Exception as e:
                speak(f"Unable to open {query}. Error: {str(e)}")
        except Exception as e:
            speak(f"Something went wrong: {str(e)}")

# ✅ YouTube play
def PlayYoutube(query):
    from engine.command import speak

    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find what to play on YouTube.")

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

# ✅ WhatsApp message
def sendWhatsAppMessage(query):
    from engine.command import speak

    try:
        query = query.lower()
        query = query.replace("send", "").replace("message", "").replace("on whatsapp", "").strip()
        words = query.split()
        if len(words) < 2:
            speak("Please specify contact and message")
            return

        name = words[0]
        message = " ".join(words[1:])

        contacts = {
            "ayush": "+918180041307",
            "om": "+919356703403"  # 🔥 put your friend's number
        }

        if name in contacts:
            speak(f"Sending message to {name}")
            kit.sendwhatmsg_instantly(
                contacts[name],
                message,
                wait_time=20,
                tab_close=False
            )
        else:
            speak("Contact not found")
    except Exception as e:
        print(e)
        speak("Failed to send message")

# ✅ Weather feature
def getWeather(city="Shravan"):
    from engine.command import speak
    api_key = "eacbb3768e0edb574f140efd94208bd6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            speak(f"The weather in {city} is {weather} with {temp}°C")
        else:
            speak("Sorry, I couldn't fetch the weather.")
    except Exception as e:
        speak("Something went wrong while fetching the weather.")

# ✅ Jokes
jokes = [
    "Why did the computer go to the doctor? Because it caught a virus!",
    "Why was the computer cold? It left its Windows open!",
    "Why do programmers prefer dark mode? Because light attracts bugs!"
]

def tellJoke():
    from engine.command import speak
    joke = random.choice(jokes)
    speak(joke)

# ✅ Timer
def setTimer(seconds):
    from engine.command import speak
    def timer_thread():
        time.sleep(seconds)
        speak("Time's up!")
    threading.Thread(target=timer_thread).start()
    speak(f"Timer set for {seconds} seconds")