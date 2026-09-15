import speech_recognition as sr
import os
import pvporcupine
import pyaudio
import struct

class AudioEngine:
    def __init__(self, picovoice_key, keyword_path):
        self.picovoice_key = picovoice_key
        self.keyword_path = keyword_path
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Convert text to speech."""
        print(f"JARVIS: {text}")
        # For Mac, using built-in 'say'.
        os.system(f'say "{text}"')

    def listen_for_command(self):
        """Listen and return speech as text using Google Speech Recognition."""
        with sr.Microphone() as source:
            print("🎙 Listening for command...")
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                query = self.recognizer.recognize_google(audio, language="en-in")
                print(f"✅ You said: {query}")
                return query
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return "Network Error"
            except Exception as e:
                return "Error"

    def wait_for_wake_word(self):
        """Block execution until wake word is detected."""
        try:
            porcupine = pvporcupine.create(
                access_key=self.picovoice_key,
                keyword_paths=[self.keyword_path],
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
            
            print("🔔 Wake word engine active. Say 'Jarvis' to activate.")
            
            while True:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("🔔 Wake word detected!")
                    return True
        except Exception as e:
            print(f"Wake word error: {e}. Bypassing wake word for now, press Enter to simulate wake word.")
            input()
            return True
