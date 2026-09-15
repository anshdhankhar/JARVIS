# JARVIS — AI Personal Assistant & Automation System

JARVIS is a modular Python-based AI personal assistant focused on **voice interaction, task automation, application control, and LLM-powered responses**.

The system combines deterministic command handling with a local transformer model and an optional cloud LLM fallback. It is designed primarily for macOS and demonstrates practical integration of speech recognition, machine learning, automation, and API-based AI services.

## Key Features

- Voice-based command interaction
- Custom wake-word detection using Picovoice Porcupine
- Speech-to-text using SpeechRecognition
- Deterministic command interception for common tasks
- macOS application and system-level task automation
- Media playback and volume control
- Website and application launching
- Screenshot, battery, date and time utilities
- Local PyTorch transformer model
- Custom tokenizer for the local language model
- Optional Groq API integration for cloud-based responses
- Modular automation and AI architecture

## How It Works

```text
Voice Input
     │
     ▼
Speech Recognition
     │
     ▼
Command Processing
     │
     ├── Deterministic Command
     │        │
     │        ▼
     │   Automation Engine
     │
     └── AI Request
              │
              ▼
       Local Transformer
              │
              └── Optional Groq Fallback
                         │
                         ▼
                    Response / Action
```

A key design decision is the **deterministic command layer**. Simple commands such as opening websites, controlling media, checking battery status, or changing system settings can bypass the LLM entirely. This reduces unnecessary model inference and makes predictable system actions more reliable.

## Technology Stack

- **Python**
- **PyTorch**
- **SpeechRecognition**
- **Picovoice Porcupine**
- **PyAudio**
- **Tokenizers**
- **Groq API**
- **macOS Automation / AppleScript**
- **Git & GitHub**

## Project Structure

```text
Project-Jarvis-main/
│
├── core/
│   ├── audio.py
│   ├── automation.py
│   └── llm.py
│
├── models/
│   └── transformer.py
│
├── training/
│   └── jarvis_tokenizer.json
│
├── checkpoints/
│   └── jarvis_gpt_v1.pth
│
├── main.py
├── jarvis.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/anshdhankhar/JARVIS.git
cd JARVIS
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

JARVIS can use environment variables for external API credentials.

For Picovoice wake-word detection:

```bash
export PICOVOICE_ACCESS_KEY="your_key_here"
```

If Groq integration is enabled, configure the corresponding API key through the project's environment configuration.

**Never commit API keys or other credentials to GitHub.**

## Running JARVIS

```bash
python3 main.py
```

The wake-word system can activate the assistant when the required Picovoice configuration and keyword model are available.

If wake-word initialization fails, the application provides a fallback interaction path rather than requiring hard-coded credentials.

## Platform

JARVIS is currently designed primarily for **macOS**.

Several automation functions rely on macOS-specific utilities such as:

- AppleScript (`osascript`)
- `open`
- `pmset`
- macOS media controls
- macOS application management

Therefore, some functionality will not work unchanged on Windows or Linux.

## Project Goals

The project explores the practical engineering challenges involved in building a personal AI assistant by combining:

1. Natural language interaction
2. Speech recognition
3. Local machine learning
4. Cloud-based LLM services
5. Deterministic automation
6. Application and system task control

The focus is on building a modular system where AI reasoning and deterministic automation can work together rather than relying on an LLM for every operation.

## Academic Project

Final Year Engineering Project  
School of Engineering and Technology  
Amity University, Uttar Pradesh

**Authors:** Madhup Yadav, Ansh Dhankhar, Harsh Rao