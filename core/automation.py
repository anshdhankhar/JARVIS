import os
import webbrowser
import datetime
import subprocess

class AutomationEngine:
    """Handles parsing OS-level automation operations on macOS."""
    
    def __init__(self):
        self.sites = {
            "OPEN_YOUTUBE": "https://www.youtube.com",
            "OPEN_WIKIPEDIA": "https://www.wikipedia.com",
            "OPEN_GOOGLE": "https://www.google.com"
        }
    
    def parse_and_execute(self, ai_output):
        """
        Takes the raw output from the AI brain and checks if an [ACTION:...] tag exists.
        Executes the MacOS specific command if found.
        """
        # The Custom PyTorch Tokenizer natively inserts spaces when decoding subwords. 
        # e.g. "Jarvis m u te  au d i o [ ACTION :  MUTE_VOLUME ]"
        # Let's normalize it fully by stripping all space and enforcing uppercase for checking tags.
        normalized = ai_output.replace(" ", "").upper()
        
        # Check standard web tags
        for action_name, url in self.sites.items():
            if f"[ACTION:{action_name}]".upper() in normalized:
                webbrowser.open(url)
                return f"Opening {action_name.split('_')[1].lower()} now."

        if "[ACTION:MUTE_VOLUME]" in normalized:
            os.system("osascript -e 'set volume with output muted'")
            return "Volume muted."

        if "[ACTION:UNMUTE_VOLUME]" in normalized:
            os.system("osascript -e 'set volume without output muted'")
            return "Volume restored."

        if "[ACTION:MAX_VOLUME]" in normalized:
            os.system("osascript -e 'set volume output volume 100'")
            return "Volume set to max."

        if "[ACTION:MIN_VOLUME]" in normalized:
            os.system("osascript -e 'set volume output volume 0'")
            return "Volume set to min."

        if "[ACTION:VOLUME_UP]" in normalized:
            os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 15)'")
            return "Increasing volume."

        if "[ACTION:VOLUME_DOWN]" in normalized:
            os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 15)'")
            return "Decreasing volume."

        if "[ACTION:PLAY_PAUSE]" in normalized:
            os.system("osascript -e 'tell application \"Music\" to playpause'")
            return "Toggled Apple Music playback."

        if "[ACTION:NEXT_TRACK]" in normalized:
            os.system("osascript -e 'tell application \"Music\" to next track'")
            return "Skipping to next track."

        if "[ACTION:PREV_TRACK]" in normalized:
            os.system("osascript -e 'tell application \"Music\" to previous track'")
            return "Going to previous track."

        if "[ACTION:DARK_MODE_ON]" in normalized:
            os.system("osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to true'")
            return "Dark mode activated."

        if "[ACTION:DARK_MODE_OFF]" in normalized:
            os.system("osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to false'")
            return "Light mode activated."

        if "[ACTION:SLEEP_MAC]" in normalized:
            os.system("pmset sleepnow")
            return "Going to sleep mode. Goodnight sir."

        if "[ACTION:LOCK_MAC]" in normalized:
            os.system("pmset displaysleepnow")
            return "System locked."

        if "[ACTION:EMPTY_TRASH]" in normalized:
            os.system("osascript -e 'tell application \"Finder\" to empty trash'")
            return "Trash bin has been emptied."

        if "[ACTION:TAKE_SCREENSHOT]" in normalized:
            filepath = f"{os.path.expanduser('~')}/Desktop/Jarvis_Screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.system(f"screencapture {filepath}")
            return "Taken a screenshot and saved to your desktop."
            
        if "[ACTION:GET_TIME]" in normalized:
            now = datetime.datetime.now()
            return f"The current time is {now.strftime('%I:%M %p')}."

        if "[ACTION:GET_DATE]" in normalized:
            now = datetime.datetime.now()
            return f"Today's date is {now.strftime('%A, %B %d, %Y')}."

        if "[ACTION:GET_BATTERY]" in normalized:
            try:
                # Ask macOS for battery stats
                output = subprocess.check_output("pmset -g batt", shell=True).decode("utf-8")
                percent = output.split('\t')[1].split(';')[0]
                return f"Your battery is currently at {percent}."
            except:
                return "I could not retrieve the battery status, sir."

        if "[ACTION:OPEN_FACETIME]" in normalized:
            os.system("open /System/Applications/FaceTime.app")
            return "Opening FaceTime."
            
        # If it was a purely conversational output with no tag, just return the AI's native words
        if "[ACTION:" not in normalized:
            return ai_output
            
        return "I recognized the action tag, but I haven't been programmed to execute it yet."
        
    def intercept_os_command(self, query):
        """A highly robust regex/keyword Natural Language Understanding (NLU) layer 
        to execute OS commands instantly and 100% accurately without LLM hallucinations."""
        q = query.lower().strip()
        
        # Remove common conversational prefixes
        prefixes = [
            "jarvis", "hey jarvis", "can you", "could you", "please", 
            "i said", "i want you to", "kindly", "system", "tell me"
        ]
        for prefix in prefixes:
            if q.startswith(prefix):
                q = q[len(prefix):].strip()
        
        # Strip leading punctuation/commas that result from speech-to-text
        q = q.lstrip(",.?! ").strip()
                
        # 0. Conversational Catch-Alls (Bypass LLM for flawless small talk)
        if q in ["sorry", "i'm sorry", "i am sorry", "sorry jarvis", "sorry jar", "my bad", "apologies", "i said sorry"]:
            return "No need to apologize, sir. I am here to help."
        if q in ["hello", "hi", "hey", "greetings"]:
            return "Hello! How can I assist you?"
        if q in ["how are you", "how do you do", "are you okay"]:
            return "I am operating optimally, sir. Thank you for asking."
        if q in ["who are you", "identify yourself"]:
            return "I am JARVIS, a local system automation AI."
                
        # 1. System Utilities
        if "battery" in q:
            try:
                output = subprocess.check_output("pmset -g batt", shell=True).decode("utf-8")
                percent = output.split('\t')[1].split(';')[0]
                return f"Your battery is currently at {percent}."
            except:
                return "I could not retrieve the battery status, sir."
                
        if "time" in q and ("what" in q or "tell" in q):
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
            
        if "date" in q or "what day" in q:
            return f"Today's date is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
            
        if "screenshot" in q or ("screen" in q and "capture" in q):
            filepath = f"{os.path.expanduser('~')}/Desktop/Jarvis_Screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.system(f"screencapture {filepath}")
            return "Taken a screenshot and saved to your desktop."
            
        # 2. UI Toggles
        if "dark mode" in q:
            if "on" in q or "enable" in q:
                os.system("osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to true'")
                return "Dark mode activated."
            elif "off" in q or "disable" in q:
                os.system("osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to false'")
                return "Light mode activated."
            elif "toggle" in q:
                os.system("osascript -e 'tell application \"System Events\" to tell appearance preferences to set dark mode to not dark mode'")
                return "Toggled dark mode."
                
        # 3. Audio & Media Controls
        if "volume" in q or "audio" in q or "sound" in q:
            if "mute" in q or "silence" in q:
                os.system("osascript -e 'set volume with output muted'")
                return "Volume muted."
            elif "unmute" in q or "turn on" in q:
                os.system("osascript -e 'set volume without output muted'")
                return "Volume restored."
            elif "max" in q or "full" in q or "100" in q:
                os.system("osascript -e 'set volume output volume 100'")
                return "Volume set to max."
            elif "min" in q or "zero" in q:
                os.system("osascript -e 'set volume output volume 0'")
                return "Volume set to min."
            elif "up" in q or "increase" in q or "louder" in q:
                os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 15)'")
                return "Increasing volume."
            elif "down" in q or "decrease" in q or "quieter" in q:
                os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 15)'")
                return "Decreasing volume."
                
        if "play" in q or "pause" in q:
            if "music" in q or "song" in q or "media" in q:
                os.system("osascript -e 'tell application \"Music\" to playpause'")
                return "Toggled Apple Music playback."
        if "next track" in q or "skip song" in q or "next song" in q:
            os.system("osascript -e 'tell application \"Music\" to next track'")
            return "Skipping to next track."
        if "previous track" in q or "previous song" in q or "go back" in q:
            os.system("osascript -e 'tell application \"Music\" to previous track'")
            return "Going to previous track."
            
        # 4. OS Power 
        if "sleep mac" in q or "sleep system" in q or "put computer to sleep" in q:
            os.system("pmset sleepnow")
            return "Going to sleep mode. Goodnight sir."
        if "lock mac" in q or "lock screen" in q or "lock computer" in q:
            os.system("pmset displaysleepnow")
            return "System locked."
        if "empty trash" in q or "clean trash" in q:
            os.system("osascript -e 'tell application \"Finder\" to empty trash'")
            return "Trash bin has been emptied."

        # 5. App Management (Open/Close/Hide)
        for action_name, url in self.sites.items():
            name = action_name.split("_")[1].lower()
            if f"open {name}" in q or f"launch {name}" in q:
                webbrowser.open(url)
                return f"Opening {name} now."

        if q.startswith("open ") or q.startswith("launch "):
            app_name = q.split(" ", 1)[1].strip()
            
            # Clean up the app name from conversational suffixes
            suffixes = [" on my mac", " on the mac", " please", " now", " immediately"]
            for suffix in suffixes:
                if app_name.endswith(suffix):
                    app_name = app_name[:-len(suffix)].strip()
                    
            app_name_clean = app_name.title()
            
            result = os.system(f"open -a '{app_name_clean}' 2>/dev/null")
            if result == 0:
                return f"Opening {app_name_clean} for you, sir."
            else:
                app_path = os.popen(f"mdfind \"kMDItemKind == 'Application' && kMDItemFSName == '*{app_name}*.app'c\" | head -n 1").read().strip()
                if app_path:
                    os.system(f"open '{app_path}'")
                    return f"Opening {app_name_clean} for you, sir."
                else:
                    return f"Sir, I tried to open {app_name_clean}, but I could not find it installed on your Mac."
                    
        if q.startswith("hide "):
            app_name = q.split(" ", 1)[1].strip()
            app_name_clean = app_name.title()
            os.system(f"osascript -e 'tell application \"System Events\" to set visible of process \"{app_name_clean}\" to false' 2>/dev/null")
            return f"Hiding {app_name_clean}."
            
        if q.startswith("close ") or q.startswith("quit ") or q.startswith("exit "):
            app_name = q.split(" ", 1)[1].strip()
            app_name_clean = app_name.title()
            
            if os.system(f"killall -9 '{app_name}' 2>/dev/null") == 0:
                return f"Closing {app_name_clean} for you, sir."
            if os.system(f"killall -9 '{app_name_clean}' 2>/dev/null") == 0:
                return f"Closing {app_name_clean} for you, sir."
            app_path = os.popen(f"mdfind \"kMDItemKind == 'Application' && kMDItemFSName == '*{app_name}*.app'c\" | head -n 1").read().strip()
            if app_path:
                real_name = os.path.basename(app_path).replace(".app", "")
                if os.system(f"killall -9 '{real_name}' 2>/dev/null") == 0:
                    return f"Closing {real_name} for you, sir."
            if os.system(f"pkill -i '{app_name}' 2>/dev/null") == 0:
                return f"Closing {app_name_clean} for you, sir."
            return f"Sir, I could not find or close {app_name_clean}."
            
        return None
