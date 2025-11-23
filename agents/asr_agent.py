# agents/asr_agent.py
import speech_recognition as sr


class ASRAgent:
    """
    Converts paramedic speech to text with robust error handling.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust for better recognition
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for speech input with timeout and phrase limits.

        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for phrase

        Returns:
            String of recognized text or empty string on failure
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                # Adjust for ambient noise with duration
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

                print("🔄 Recognizing speech...")
                # Use Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='en-US')
                return text

        except sr.WaitTimeoutError:
            print("⚠️ Listening timed out - no speech detected")
            return ""

        except sr.UnknownValueError:
            print("⚠️ Could not understand audio - speech unintelligible")
            return ""

        except sr.RequestError as e:
            print(f"⚠️ Could not request results from Google Speech Recognition service; {e}")
            return ""

        except Exception as e:
            print(f"⚠️ Unexpected error in speech recognition: {e}")
            return ""