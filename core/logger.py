import datetime

class Logger:
    def __init__(self, log_file="Jarvis_Log.txt"):
        self.file = log_file

    def record(self, text):
        with open(self.file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {text}\n")
