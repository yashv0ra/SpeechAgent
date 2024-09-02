
import os
from deepgram import DeepgramClient, SpeakOptions
import playsound

#SPEAK_OPTIONS = {"text": "Hello, how can I help you today?"}
filename = "output.mp3"
def is_blank(s: str):
    return s.strip() == ''
def main():
    try:
        # STEP 1: Create a Deepgram client.
        # By default, the DEEPGRAM_API_KEY environment variable will be used for the API Key
        # Deepgram API key: 5112f394cfb185257a9ffddf6ffb982358ec1934
        deepgram = DeepgramClient()

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-zeus-en",
        )

        # STEP 3: Call the save method on the speak property
        repeat_check = ""
        answer = ""
        x = open('botoutput.txt','w')
        print("Welcome to Terry")
        playsound.playsound('/Users/Yash/Downloads/Terry - The AI App/vscode/greeting.mp3', True)
        while True:
        # Get user input from the console
            while answer == repeat_check or is_blank(answer):
                with open('botoutput.txt', 'r') as f:
                     answer = f.readline()
                sleep(0.1)
            repeat_check = answer
            SPEAK_OPTIONS = {"text": answer}
            response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
            #print(response.to_json(indent=4))
            print("Playing output.mp3...")
            playsound.playsound('/Users/Yash/Downloads/Terry - The AI App/vscode/output.mp3', True)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()

