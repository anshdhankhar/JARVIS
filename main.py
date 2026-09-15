import os
import sys
import random

# Import our custom OS components
from core.audio import AudioEngine
from core.automation import AutomationEngine
from core.iot import IotEngine
from core.llm import LlmEngine
from core.logger import Logger

# -------------------------------
# 🔑 CONFIGURATION
# -------------------------------
PICOVOICE_KEY = os.getenv("PICOVOICE_ACCESS_KEY", "")
KEYWORD_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "JARVIS_en_mac_v3_0_0.ppn"
)

def boot_system():
    print("-------------------------------------------------")
    print("🤖 JARVIS-OS INIT SEQUENCE")
    print("-------------------------------------------------")
    
    logger = Logger()
    logger.record("System boot initiated.")
    
    # Try loading Groq API key from .env file for cloud fallback
    use_online = False
    api_key = ""
    env_path = os.path.join("core", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GROQ_API_KEY="):
                    api_key = line.split("=")[1].strip()
                    if api_key and api_key != "your_key_here":
                        use_online = True
    
    # Initialize Core Engines
    try:
        audio_engine = AudioEngine(PICOVOICE_KEY, KEYWORD_PATH)
        automation_engine = AutomationEngine()
        iot_engine = IotEngine()
        llm_engine = LlmEngine(use_online=use_online, api_key=api_key)
        print("[✓] All Core Engines Localized & Loaded.")
    except Exception as e:
        print(f"[!] Critical failure during boot: {e}")
        sys.exit(1)
        
    audio_engine.speak("All systems online. JARVIS is ready.")
    
    return audio_engine, automation_engine, iot_engine, llm_engine, logger

def process_command(query, audio, auto, iot, llm, logger):
    logger.record(f"User Input: {query}")
    
    # Check for hard shutdown first to preserve battery
    if "quit" in query.lower() or "shut down" in query.lower():
        audio.speak("Goodbye. Shutting down JARVIS OS.")
        logger.record("System Shutdown.")
        sys.exit(0)
        
    # Super-fast OS-level Intent Detection (prevents offline neural network from hallucinating)
    os_response = auto.intercept_os_command(query)
    if os_response:
        logger.record(f"System Action: {os_response}")
        audio.speak(os_response)
        return

    # Route request to AI Model Brain for conversation or complex commands
    print(f"🧠 Consulting Brain...")
    ai_response = llm.generate_response(query)
    logger.record(f"AI Output: {ai_response}")
    
    # 1. Process Hardware/IoT Responses from AI Output
    normalized_ai = ai_response.replace(" ", "").upper()
    
    if "[ACTION:GET_HEALTH_REPORT]" in normalized_ai:
        report = iot.get_health_report()
        logger.record("IoT Action: Sent Health Report")
        audio.speak(report)
        return
        
    if "[ACTION:GET_SENSOR_DATA]" in normalized_ai:
        report = iot.get_environment_report()
        logger.record("IoT Action: Sent Environment Report")
        audio.speak(report)
        return

    if "[ACTION:SHUTDOWN]" in normalized_ai:
        audio.speak("Goodbye. Shutting down JARVIS OS.")
        logger.record("System Shutdown (AI Triggered).")
        sys.exit(0)
    
    # 2. Give the raw output to Automation to parse into macOS native scripts
    final_voice_reply = auto.parse_and_execute(ai_response)
    
    # TTS the parsed result back to user
    logger.record(f"Action Executed / Reply: {final_voice_reply}")
    audio.speak(final_voice_reply)

def main():
    # 1. Boot up completely
    audio, automation, iot, llm, logger = boot_system()
    
    # 2. Main Event Loop
    while True:
        # Block until user says "Jarvis"
        if audio.wait_for_wake_word():
            audio.speak("Yes, I'm listening.")
            
            # Enter Continuous Conversation Mode
            active_conversation = True
            
            while active_conversation:
                # Listen to the task command
                command = audio.listen_for_command()
                
                # If the user stays silent or mic fails, drop back to standby mode smoothly
                if not command or command in ["Error", "Network Error"]:
                    active_conversation = False
                    continue
                
                # If the user is done talking, dismiss the active loop but keep the system alive
                dismiss_phrases = ["thank", "that's all", "stop listening", "dismissed", "nevermind", "exit"]
                if any(p in command.lower() for p in dismiss_phrases) and len(command.split()) <= 4:
                    audio.speak("Standing by. Call me if you need anything else.")
                    active_conversation = False
                    continue
                    
                # Otherwise, execute the command and keep the conversation open!
                process_command(command, audio, automation, iot, llm, logger)

if __name__ == "__main__":
    main()
