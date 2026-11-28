import speech_recognition as sr
import time
import datetime
import webbrowser
import asyncio
import edge_tts
import pygame

def speak(text):
    clean_text = text.replace("Jarvis:", "").strip()
    print(f"Jarvis: {clean_text}")
    if clean_text == "":
        return
    for attempt in range(2):
        try:
            asyncio.run(edge_tts.Communicate(clean_text, "en-IN-PrabhatNeural").save("jarvis_voice.mp3"))
            pygame.mixer.init()
            pygame.mixer.music.load("jarvis_voice.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
            break
        except Exception as e:
            print(f"DEBUG - Edge TTS try {attempt+1} failed: {e}")
            time.sleep(0.5)
            if attempt == 1:
                print("DEBUG - Edge failed twice, skipping audio, bro.")

listener = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source, duration=0.5)
        try:
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            print(f"You: {command}")
            return command.lower()
        except:
            print("...did not hear, waiting...")
            return ""

privacy_mode = "show-only"

def confirm_before_search(command):
    speak(f"You said {command}. Should I search?")
    answer = listen()
    if "yes" in answer:
        return True
    else:
        speak("Okay, not searching.")
        return False

# --- NEW STOP CHECK - This is the fix, bro ---
def is_stop(command):
    # All words that mean STOP, bro. Including Google's mistakes.
    stop_words = ["stop", "quit", "bye", "by", "buy", "bhai", "exit", "close", "band", "bas", "ruk"]
    for word in stop_words:
        if word in command:
            return True
    return False

def do_command(command):
# 1. HELLO
    if "hello" in command:
        return "Jarvis: Hello KalaShade. How are you?"

# 2. HOW ARE YOU
    elif "how are you" in command:
        return "Jarvis: I am doing great! How about you?"
    
# 3. TIME
    elif "time" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Time is {now.strftime('%I:%M %p')}"

# 4. DATE
    elif "date" in command:
        today = datetime.date.today()
        return f"Jarvis: Today is {today}"
    
# 5. MONTH
    elif "month" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Month is {now.strftime('%B')}"

# 6. DAY
    elif "day" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Today is {now.strftime('%A')}, {now.day}"
    
# 7. YEAR
    elif "year" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Year is {now.year}"

# 8. WHO ARE YOU
    elif "who are you" in command:
        return "Jarvis: I am Jarvis, Stage 3 Base. Created by KalaShade. No AI yet."

# 9. HELP - Shows all commands
    elif "help" in command:
        return "Jarvis: I can do:\n- hello, time, date, who are you\n- open youtube, open amazon\n- search for X, incognito search for X\n- bye"

# 10. OPEN YOUTUBE - Laptop + Mobile
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."

# 11. OPEN AMAZON - Your book page
    elif "open amazon" in command:
        webbrowser.open("https://www.amazon.in/dp/B0HS9617FD")
        return "Jarvis: Opening your Twisted Tales book..."

# 12. INCOGNITO SEARCH - Show only, No Tell, No History
    elif "incognito search for " in command:
        topic = command.replace("incognito search for ", "")
        webbrowser.open(f"https://www.bing.com/search?q={topic}")
        return f"Jarvis: Incognito mode. Showing only, no tell, no history."

# 13. SEARCH - Normal, Show + Tell
    elif "search for " in command:
        topic = command.replace("search for ", "")
        webbrowser.open(f"https://www.bing.com/search?q={topic}")
        return f"Jarvis: Showing results for {topic}"
    
speak("Hello KalaShade. Stage 3 ready. Ear and Voice on.")

while True:
    command = listen()
    print(f"DEBUG - Jarvis heard: [{command}]")  # <-- This tells us what Jarvis heard, bro

    if command == "":
        time.sleep(0.5)
        continue

    if is_stop(command):
        speak("Okay KalaShade, stopping now. Bye.")
        break

    if "jarvis" in command:
        # Remove "jarvis" and "hey", keep rest, bro. One step, bro.
        command = command.replace("jarvis", "").replace("hey", "").strip()
        if command == "":
            speak("Yes KalaShade, I am listening.")
            command = listen()
            print(f"DEBUG - Jarvis heard: [{command}]")
            if is_stop(command):
                speak("Okay KalaShade, stopping now. Bye.")
                break
        result = do_command(command)
        if result:
            speak(result)
        else:
            speak("I heard you, but that command is not set up yet.")