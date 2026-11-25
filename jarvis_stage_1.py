# JARVIS STAGE 1 - STAND - Base, No AI
# Made by KalaShade - Laptop + Mobile, Same Code

import webbrowser
import datetime
import os

print("Hello, I am Jarvis. Created by KalaShade.")
print("Type 'help' to see what I can do.")
print("Type 'bye' to stop me.")
print("-----------------------------------")

# This loop keeps Jarvis running, listening to your typing
while True:
    # You type command here
    command = input("User: ").lower().strip()

    # 1. HELLO
def talk(command):
    if "hello" in command:
        return "Jarvis: Hello bro! I am here. Stand mode ON."
    
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
    
    #5. MONTH
    elif "month" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Month is {now.strftime('%B')}"

    #6. DAY
    elif "day" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Today is {now.strftime('%A')}, {now.day}"
    
    #7. YEAR
    elif "year" in command:
        now = datetime.datetime.now()
        return f"Jarvis: Year is {now.year}"

    # 8. WHO ARE YOU
    elif "who are you" in command:
        return "Jarvis: I am Jarvis, Stage 1 Base. Created by KalaShade. No AI yet."

    # 9. HELP - Shows all commands
    elif "help" in command:
        return "Jarvis: I can do:\n- hello, time, date, who are you\n- open youtube, open amazon\n- search for X, incognito search for X\n- bye"

    # 10. OPEN YOUTUBE - Laptop + Mobile
    elif "open youtube" in command:
        return "Opening YouTube..."
        webbrowser.open("https://www.youtube.com")

    # 11. OPEN AMAZON - Your book page
    elif "open amazon" in command:
        return "Jarvis: Opening your Twisted Tales book..."
        webbrowser.open("https://www.amazon.in/dp/B0HS9617FD")

    # 12. INCOGNITO SEARCH - Show only, No Tell, No History
    elif "incognito search for " in command:
        topic = command.replace("incognito search for ", "")
        return f"Jarvis: Incognito mode. Showing only, no tell, no history."
        webbrowser.open(f"https://www.bing.com/search?q={topic}")

    # 13. SEARCH - Normal, Show + Tell
    elif "search for " in command:
        topic = command.replace("search for ", "")
        return f"Jarvis: Searching for {topic} in Edge / Browser..."
        # This opens browser with search already done
        webbrowser.open(f"https://www.bing.com/search?q={topic}")
        return f"Jarvis: Showing results for {topic}"
    
    # 14. BYE - Stop Jarvis
    elif "bye" in command:
      return "Jarvis: Bye bro. Tap somewhere else to quit. See you again, pakka Bhaiyaa."
        

    # 15. IF JARVIS DOESN'T KNOW
    else:
        return "Jarvis: I don't know that yet. This is only Stage 1. We will add it in Stage 2."