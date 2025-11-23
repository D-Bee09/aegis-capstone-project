# agents/tts_agent.py
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os


class TTSAgent:
    """
    Text-to-speech agent for providing audio feedback to paramedics.
    """

    def __init__(self, mode="offline"):
        self.mode = mode
        if mode == "offline":
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 165)
            self.engine.setProperty("volume", 0.9)

    def speak(self, text: str):
        """
        Converts text to speech and plays audio.

        Args:
            text: String to be spoken
        """
        print(f"🔊 AEGIS: {text}")

        try:
            if self.mode == "offline":
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                tts = gTTS(text)
                file = "aegis_tts.mp3"
                tts.save(file)
                playsound(file)
                # Clean up temp file
                if os.path.exists(file):
                    os.remove(file)
        except Exception as e:
            print(f"⚠️ TTS Error: {e}")