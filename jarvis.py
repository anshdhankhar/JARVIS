# JARVIS AI Assistant - Extended Version
# Features: Wake Word, Voice Commands, AI Chat, System Automation, IoT Simulation, Daily Logs

import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import pvporcupine
import pyaudio
import struct
import random

# -------------------------------
# 🔑 CONFIGURATION
# -------------------------------

# Picovoice Access Key — stored locally, never committed to Git
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY", "")

# Path to the bundled wake-word model
KEYWORD_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "JARVIS_en_mac_v3_0_0.ppn"
)

chat_history = ""
log_file = "Jarvis_Log.txt"
reminders = []

# -------------------------------
# 🎤 SPEECH FUNCTIONS
# -------------------------------

def say(text):
    os.system(f'say "{text}"')

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening for command...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"✅ You said: {query}")
            log_activity(f"User said: {query}")
            return query
        except:
            return "Some Error Occurred. Sorry from Jarvis"

# -------------------------------
# 📅 LOGGING SYSTEM
# -------------------------------

def log_activity(activity):
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - {activity}\n")

# -------------------------------
# 🧑‍⚕️ HEALTH VITALS (Simulated IoT)
# -------------------------------

def get_health_report():
    heart_rate = random.randint(60, 100)
    steps = random.randint(2000, 8000)
    calories = random.randint(1500, 2500)
    sleep_hours = random.randint(6, 9)

    report = (f"Your heart rate is {heart_rate} bpm, "
              f"you have walked {steps} steps, "
              f"burned around {calories} calories, "
              f"and slept {sleep_hours} hours last night.")
    
    log_activity("Health Report generated")
    say(report)
    return report

# -------------------------------
# ⏰ REMINDERS
# -------------------------------

def set_reminder(task, time):
    reminders.append((task, time))
    log_activity(f"Reminder set: {task} at {time}")
    say(f"Reminder set for {task} at {time}")

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for reminder in reminders:
        if reminder[1] == now:
            say(f"Reminder: {reminder[0]}")

# -------------------------------
# 🤖 OPENAI CHAT
# -------------------------------

def chat(query):
    global chat_history
    chat_history += f"User: {query}\nJarvis: "
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_history,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    answer = response["choices"][0]["text"].strip()
    say(answer)
    chat_history += f"{answer}\n"
    log_activity(f"Jarvis: {answer}")
    return answer

# -------------------------------
# 🖥️ SYSTEM AUTOMATION
# -------------------------------

def execute_command(query):
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com"
    }
    
    for site in sites:
        if f"open {site}" in query.lower():
            say(f"Opening {site}...")
            webbrowser.open(sites[site])
            return

    if "open music" in query.lower():
        say("Music file is not configured on this machine.")
        return

    if "time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        say(f"The time is {hour} hours and {minute} minutes")
        return

    if "health report" in query.lower():
        get_health_report()
        return

    if "set reminder" in query.lower():
        say("What should I remind you about?")
        task = take_command()
        say("At what time? Please say in HH:MM format.")
        time = take_command()
        set_reminder(task, time)
        return

    if "open facetime" in query.lower():
        os.system("open /System/Applications/FaceTime.app")
        return

    if "quit" in query.lower():
        say("Goodbye Ansh. Shutting down Jarvis.")
        exit()

    # Default → AI Chat
    chat(query)

# -------------------------------
# 🔔 WAKE WORD DETECTION
# -------------------------------

def listen_for_wake_word():
    porcupine = pvporcupine.create(
        keyword_paths=[KEYWORD_PATH],
        sensitivities=[0.65]
    )
    
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    say("Jarvis is on standby. Say 'Jarvis' to activate me.")
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            say("Yes Ansh, I'm listening.")
            return

# -------------------------------
# 🚀 MAIN LOOP
# -------------------------------

if __name__ == "__main__":
    print("🤖 JARVIS AI Assistant Running...")
    
    while True:
        listen_for_wake_word()
        query = take_command()
        execute_command(query)
        check_reminders()
