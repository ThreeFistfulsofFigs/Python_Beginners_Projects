import speech_recognition as sr


def speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print("Listening... Speak now!")
        try:
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            print("Processing...")
            # Use Google's speech recognition API to convert audio to text
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "No speech detected within timeout."
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"


def main():
    print("Simple Speech-to-Text Web_app")
    print("Enter 'quit' to exit")

    while True:
        # Prompt user to start speaking or quit
        user_input = input("\nPress Enter to start speaking, or type 'quit' to exit: ")

        if user_input.lower() == 'quit':
            print("Exiting app...")
            break

        # Convert speech to text
        result = speech_to_text()
        print(f"Recognized text: {result}")


if __name__ == "__main__":
    main()