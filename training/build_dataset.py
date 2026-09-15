import json
import random

def generate_dataset(output_file="training/jarvis_dataset.jsonl"):
    """
    Generates a massive synthetic instruction-tuning dataset for JARVIS.
    Covers basic to intermediate system automation, media controls, toggles, and IoT.
    """
    
    intents = [
        # OS & System Power
        {"prompts": ["sleep mac", "go to sleep", "put the computer to sleep", "sleep system"], "completion": "[ACTION:SLEEP_MAC]"},
        {"prompts": ["lock mac", "lock the screen", "lock computer", "secure the mac"], "completion": "[ACTION:LOCK_MAC]"},
        {"prompts": ["empty trash", "clean the trash", "empty recycle bin"], "completion": "[ACTION:EMPTY_TRASH]"},
        
        # UI Toggles
        {"prompts": ["enable dark mode", "turn on dark mode", "dark mode on", "switch to dark mode"], "completion": "[ACTION:DARK_MODE_ON]"},
        {"prompts": ["disable dark mode", "turn off dark mode", "light mode on", "switch to light mode"], "completion": "[ACTION:DARK_MODE_OFF]"},
        
        # Audio & Media
        {"prompts": ["mute volume", "mute the volume", "mute audio", "silence", "mute the sound"], "completion": "[ACTION:MUTE_VOLUME]"},
        {"prompts": ["unmute volume", "unmute the volume", "unmute audio", "turn the sound on"], "completion": "[ACTION:UNMUTE_VOLUME]"},
        {"prompts": ["max volume", "maximum volume", "full volume", "volume 100", "turn it all the way up"], "completion": "[ACTION:MAX_VOLUME]"},
        {"prompts": ["min volume", "minimum volume", "volume down to zero"], "completion": "[ACTION:MIN_VOLUME]"},
        {"prompts": ["volume up", "increase volume", "louder", "turn it up"], "completion": "[ACTION:VOLUME_UP]"},
        {"prompts": ["volume down", "decrease volume", "quieter", "turn it down"], "completion": "[ACTION:VOLUME_DOWN]"},
        {"prompts": ["play music", "pause music", "stop music", "play media", "pause media"], "completion": "[ACTION:PLAY_PAUSE]"},
        {"prompts": ["next track", "skip song", "next song", "play the next one"], "completion": "[ACTION:NEXT_TRACK]"},
        {"prompts": ["previous track", "previous song", "go back a song", "play last track"], "completion": "[ACTION:PREV_TRACK]"},
        
        # Utilities
        {"prompts": ["take a screenshot", "capture screen", "take screenshot", "save the screen"], "completion": "[ACTION:TAKE_SCREENSHOT]"},
        {"prompts": ["what time is it", "tell me the time", "current time", "do you have the time"], "completion": "[ACTION:GET_TIME]"},
        {"prompts": ["what is the date", "tell me the date", "current date", "what day is it"], "completion": "[ACTION:GET_DATE]"},
        {"prompts": ["what is my battery", "check battery", "battery percentage", "power level"], "completion": "[ACTION:GET_BATTERY]"},
        
        # Web & Specific Apps (General 'open arbitrary app' handles most, but we can teach AI some core ones)
        {"prompts": ["open google", "launch google", "google please", "start google browser"], "completion": "[ACTION:OPEN_GOOGLE]"},
        {"prompts": ["open youtube", "launch youtube", "play some youtube"], "completion": "[ACTION:OPEN_YOUTUBE]"},
        {"prompts": ["open wikipedia", "launch wikipedia", "search wikipedia"], "completion": "[ACTION:OPEN_WIKIPEDIA]"},
        
        # Hardware / IoT Intents
        {"prompts": ["what is my heart rate", "check my vitals", "health report", "how am i doing physically", "read my pulse"], "completion": "[ACTION:GET_HEALTH_REPORT]"},
        {"prompts": ["check raspberry pi sensors", "get environment data", "room temperature", "what is the temperature", "air quality"], "completion": "[ACTION:GET_SENSOR_DATA]"},
        
        # Conversational / Persona Intents
        {"prompts": ["who are you", "what is your name", "identify yourself", "tell me about yourself"], "completion": "I am JARVIS-OS, a local intelligent AI assistant designed to automate your personal environment."},
        {"prompts": ["who created you", "who is your maker", "who programmed you"], "completion": "I was developed by my creator as a final year engineering project."},
        {"prompts": ["hello", "hi jarvis", "are you there jarvis", "wake up", "good morning", "greetings"], "completion": "Hello! All systems are online. How can I assist you today?"},
        {"prompts": ["goodbye", "shut down", "go to sleep", "quit", "exit system"], "completion": "[ACTION:SHUTDOWN]"},
        
        # Out-Of-Distribution / Hallucination Catch-all
        {"prompts": ["you have done wrong calculation", "you are wrong", "what color is the sky", "tell me a joke", "do you like pizza", "what is the meaning of life", "how do I cook pasta", "blah blah blah", "I am angry", "this is bad", "testing test", "who is the president"], "completion": "I am a local system automation AI. I am primarily programmed to control your OS and hardware, and cannot answer general knowledge queries."}
    ]
    
    dataset = []
    
    # Compile all prompts into our dataset list
    for intent in intents:
        for prompt in intent["prompts"]:
            dataset.append({
                "instruction": prompt,
                "output": intent["completion"]
            })
                
    # Massive Data Augmentation
    augmented_dataset = []
    prefixes = ["jarvis, ", "hey jarvis, ", "can you ", "please ", "jarvis ", "i want you to ", "could you ", "kindly ", "system, ", ""]
    suffixes = ["", " please", " now", " immediately", " for me"]
    
    for item in dataset:
        # Create many variations for each prompt to guarantee tokenizer learns English words deeply
        for _ in range(15): 
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            new_instruction = prefix + item["instruction"] + suffix
            augmented_dataset.append({
                "instruction": new_instruction.strip().capitalize(),
                "output": item["output"]
            })
            
    # Remove duplicates and shuffle
    unique_dataset = [dict(t) for t in {tuple(d.items()) for d in augmented_dataset}]
    random.shuffle(unique_dataset)
    
    # Save as JSONL (JSON Lines)
    with open(output_file, 'w') as f:
        for entry in unique_dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"✅ Successfully generated MASSSIVE dataset with {len(unique_dataset)} samples at {output_file}")

if __name__ == "__main__":
    generate_dataset()
