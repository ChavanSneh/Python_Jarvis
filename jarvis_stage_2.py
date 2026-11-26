# JARVIS STAGE 2 - THRUSTERS
# Rule: No AI, No Gemini, No ChatGPT. Only Python.
# New in Stage 2:
# 1. Memory - Local DB only, file jarvis.db, viewable, shareable
# 2. Ask Website or App - Human decides, not machine
# 3. More Commands - open youtube, remember this, what did I ask

import sqlite3
import datetime
import webbrowser
import jarvis_stage_1

# --- 1. LOCAL DB SETUP - Like a notebook Jarvis writes in ---
# jarvis.db is a file. You can copy it mobile -> laptop via WhatsApp / USB / Drive
DB_NAME = "jarvis.db"

def setup_db():
    # Connect to DB file, if not there, Python makes it
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Table 1: memory - what Jarvis remembers about you
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY,
            key TEXT,
            value TEXT
        )
    """)
    # Table 2: history - what you searched, only if NOT incognito
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            search_text TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def remember(key, value):
    # Example: remember("name", "KalaShade")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memory WHERE key = ?", (key,))
    cursor.execute("INSERT INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    print(f"Jarvis: Okay, I will remember {key} = {value}")

def recall(key):
    # Example: recall("name") -> KalaShade
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def save_history(search_text):
    # Only called when NOT incognito. Incognito = no history.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO history (search_text, time) VALUES (?, ?)", (search_text, now))
    conn.commit()
    conn.close()

def show_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT search_text, time FROM history")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("Jarvis: No history yet. Empty notebook.")
    else:
        print("Jarvis: Your history:")
        for text, time in rows:
            print(f" - {text} at {time}")

# --- 2. BASIC COMMANDS FROM STAGE 1 ---
# --- 3. STAGE 2 NEW: ASK WEBSITE OR APP ---
def ask_website_or_app(search_text, incognito):
    # Human decides, not machine. Jarvis asks like Google Assistant.
    print("Jarvis: Website or App?")
    print("Type: website / app / cancel")
    choice = input("You: ").lower().strip()

    if choice == "cancel":
        print("Jarvis: Okay, cancelled. I did not search.")
        return

    if choice == "website":
        # Confirm before search - Voice can mishear, so Jarvis asks confirm
        print(f"Jarvis: You want to search '{search_text}' on website? Type yes / no")
        confirm = input("You: ").lower().strip()
        if confirm == "yes":
            # Incognito = show only, no tell, no history
            # Non-Incognito = show + tell, saves history
            if incognito:
                print(f"Jarvis: [Incognito - Show Only] Opening website for {search_text}, not saving history.")
            else:
                print(f"Jarvis: [Show + Tell] Opening website for {search_text}, saving to history.")
                save_history(search_text)
            webbrowser.open(f"https://www.google.com/search?q={search_text}")
        else:
            print("Jarvis: Okay, not searching. Maybe I misheard.")
    
    elif choice == "app":
        print(f"Jarvis: Which app? Example: youtube / chrome / whatsapp")
        app = input("You: ").lower().strip()
        if app == "youtube":
            print(f"Jarvis: Opening YouTube for {search_text}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_text}")
            if not incognito:
                save_history(search_text)
        else:
            print(f"Jarvis: I don't know how to open {app} yet. I will open in website.")
            webbrowser.open(f"https://www.google.com/search?q={search_text}")

    else:
        print("Jarvis: I didn't understand. Say website or app.")

# --- MAIN LOOP - Activation: Voice OR App Touch ---
def main():
    setup_db()
    print("=== JARVIS STAGE 2 - THRUSTERS ===")
    print("Activation: You opened me, so I am ON.")
    print("To quit: type 'quit' or tap somewhere else to close me.")

    # Incognito choice - Privacy 1st
    print("Jarvis: Incognito? Type yes for Show Only, no for Show + Tell")
    incognito_input = input("You (yes/no): ").lower().strip()
    incognito = True if incognito_input == "yes" else False
    if incognito:
        print("Jarvis: Incognito ON - Show Only, No Tell, No History.")
    else:
        print("Jarvis: Incognito OFF - Show + Tell, History Saved.")

    while True:
        print("\nJarvis: What to do?")
        command = input("You: ").lower().strip()

        if command == "quit":
            print("Jarvis: Bye. Thrusters OFF.")
            break

        elif command == "search":
            print("Jarvis: What to search?")
            search_text = input("You: ")
            # Stage 2: Jarvis asks Website or App
            ask_website_or_app(search_text, incognito)

        elif command == "remember":
            print("Jarvis: What to remember? Example: my favourite food = egg omelette")
            print("Type as: key = value")
            text = input("You: ")
            if "=" in text:
                key, value = text.split("=", 1)
                remember(key.strip(), value.strip())
            else:
                print("Jarvis: Use = sign. Example: name = KalaShade")

        elif command == "what is my name":
            name = recall("name")
            if name:
                print(f"Jarvis: Your name is {name}")
            else:
                print("Jarvis: I don't know your name yet. Tell me: remember -> name = KalaShade")

        elif command == "history":
            if incognito:
                print("Jarvis: You are in Incognito. I did not save history.")
            else:
                show_history()

        else:
            answer = jarvis_stage_1.talk(command)
            print(answer)
            if "Bye" in answer:
                break

if __name__ == "__main__":
    main()