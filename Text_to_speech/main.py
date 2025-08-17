import pyttsx3


def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional: adjust voice, rate, and volume)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()


def main():
    print("Simple Text-to-Speech Web_app")
    print("Enter 'quit' to exit")

    while True:
        # Get user input
        user_input = input("\nEnter text to convert to speech: ")

        # Check for quit command
        if user_input.lower() == 'quit':
            print("Exiting app...")
            break

        # Convert input text to speech
        if user_input.strip():
            text_to_speech(user_input)
        else:
            print("Please enter some text!")


if __name__ == "__main__":
    main()