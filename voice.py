"""
Voice Module for OpenPRIME
Text-to-speech and speech-to-text using Character.AI style
"""

import subprocess
import os

class OpenPRIMEVoice:
    def __init__(self):
        self.tts_engine = None
        self.stt_engine = None
        self.voice_name = "default"
        print("🎤 Voice module initialized")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            # Try termux-tts-speak first (Android)
            result = subprocess.run(
                ["termux-tts-speak", text],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"🗣️ Speaking: {text[:50]}...")
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        try:
            # Fallback: espeak (Linux)
            result = subprocess.run(
                ["espeak", text],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"🗣️ Speaking: {text[:50]}...")
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        print("⚠️ No TTS engine available")
        return False
    
    def listen(self, timeout=5):
        """Convert speech to text"""
        try:
            # Try termux-speech-to-text (Android)
            result = subprocess.run(
                ["termux-speech-to-text"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0 and result.stdout:
                print(f"🎙️ Heard: {result.stdout[:50]}...")
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        print("⚠️ No STT engine available")
        return None
    
    def set_voice(self, voice_name):
        """Change voice personality"""
        self.voice_name = voice_name
        print(f"🎭 Voice changed to: {voice_name}")

# Quick test
if __name__ == "__main__":
    voice = OpenPRIMEVoice()
    voice.speak("The God speaks. OpenPRIME voice is ready.")
    print("✅ Voice test complete")
