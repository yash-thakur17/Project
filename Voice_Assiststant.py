import speech_recognition as sr
import pyttsx3
import requests
import time
import webbrowser
import pyautogui
import os
import threading
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pywhatkit as kit

# =========================
# API KEYS
# =========================
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

# =========================
# LOGGER
# =========================
def log(message):
    print(f"[JARVIS] {message}")

# =========================
# TEXT TO SPEECH
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    log(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH TO TEXT
# =========================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="en-IN")
        log(f"You said: {command}")
        return command.lower()
    except:
        log("Could not understand")
        return ""

# =========================
# WAKE WORD
# =========================
def wait_for_wake_word():
    log("Waiting for wake word...")
    while True:
        command = take_command()
        if "hey edit" in command:
            log("Wake word detected")
            speak("Yes Yash")
            return

# =========================
# WEATHER
# =========================
def get_weather(city):
    log(f"Getting weather for {city}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()

    if str(data.get("cod")) != "200":
        speak("City not found")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    speak(f"{city} temperature is {temp} degree Celsius with {desc}")

# =========================
# NEWS
# =========================
def read_news():
    log("Reading news")
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    data = requests.get(url).json()

    if data["status"] != "ok":
        speak("News not available")
        return

    speak("Top headlines")
    for article in data["articles"][:5]:
        speak(article["title"])

# =========================
# TIME & DATE
# =========================
def tell_time():
    log("Telling time")
    now = datetime.now().strftime("%I:%M %p")
    speak(f"Time is {now}")

def tell_date():
    log("Telling date")
    today = datetime.now().strftime("%B %d %Y")
    speak(f"Today is {today}")

# =========================
# REMINDER (BACKGROUND)
# =========================
def reminder_thread(reminder_time):
    while True:
        if datetime.now().strftime("%H:%M") == reminder_time:
            speak("Reminder time")
            break
        time.sleep(20)

def set_reminder(reminder_time):
    log(f"Reminder set for {reminder_time}")
    speak(f"Reminder set for {reminder_time}")
    threading.Thread(target=reminder_thread, args=(reminder_time,), daemon=True).start()

# =========================
# VOLUME CONTROL
# =========================
def volume_control(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

def volume_up():
    log("Volume up")
    volume_control(0.8)
    speak("Volume up")

def volume_down():
    log("Volume down")
    volume_control(0.3)
    speak("Volume down")

def mute_volume():
    log("Volume muted")
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)
    speak("Volume muted")

# =========================
# OPEN APPS & WEBSITES
# =========================
def open_youtube():
    log("Opening YouTube")
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def open_google():
    log("Opening Google")
    speak("Opening Google")
    webbrowser.open("https://www.google.com")

def open_notepad():
    log("Opening Notepad")
    speak("Opening Notepad")
    os.system("notepad")

# =========================
# SEARCH FUNCTIONS
# =========================
def search_google(query):
    log(f"Google search: {query}")
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def search_youtube(query):
    log(f"YouTube search: {query}")
    speak(f"Searching YouTube for {query}")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)

def play_youtube_video(query):
    log(f"Playing on YouTube: {query}")
    speak(f"Playing {query} on YouTube")
    kit.playonyt(query)

# =========================
# MOUSE & KEYBOARD
# =========================
def mouse_click():
    log("Mouse click")
    pyautogui.click()
    speak("Clicked")

def move_mouse():
    log("Mouse moved")
    pyautogui.moveRel(100, 0, duration=0.5)
    speak("Mouse moved")

def type_text():
    speak("What should I type")
    text = take_command()
    if text:
        log(f"Typing: {text}")
        pyautogui.write(text, interval=0.05)
        speak("Typed")

# =========================
# ASSISTANT MODE
# =========================
def assistant_mode():
    log("Assistant mode started")
    speak("Tell me command")

    while True:
        command = take_command()

        if not command:
            continue

        if "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "weather" in command:
            speak("City name")
            city = take_command()
            if city:
                get_weather(city)

        elif "news" in command:
            read_news()

        elif "open youtube" in command or command == "youtube":
            open_youtube()

        elif "open google" in command or command == "google":
            open_google()

        elif "search google" in command:
            speak("What should I search on Google")
            query = take_command()
            if query:
                search_google(query)

        elif "search youtube" in command:
            speak("What should I search on YouTube")
            query = take_command()
            if query:
                search_youtube(query)

        elif command.startswith("play"):
            query = command.replace("play", "").strip()
            if query:
                play_youtube_video(query)

        elif "notepad" in command:
            open_notepad()

        elif "type" in command:
            type_text()

        elif "click" in command:
            mouse_click()

        elif "move mouse" in command:
            move_mouse()

        elif "volume up" in command:
            volume_up()

        elif "volume down" in command:
            volume_down()

        elif "mute" in command:
            mute_volume()

        elif "reminder" in command:
            speak("Tell time in 24 hour format. Example 18:30")
            reminder_time = take_command()
            if reminder_time:
                set_reminder(reminder_time)

        elif "sleep" in command:
            log("Going to sleep")
            speak("Going to sleep")
            return

        elif "bye" in command or "exit" in command:
            log("Exiting Jarvis")
            speak("Goodbye Yash")
            exit()

        else:
            speak("Say again")

# =========================
# MAIN LOOP
# =========================
log("Jarvis activated and running")
speak("Edit activated")

while True:
    wait_for_wake_word()
    assistant_mode()