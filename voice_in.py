# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

#from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from time import sleep

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

#load_dotenv()

# We will collect the is_final=true messages here so we can use them when the person finishes speaking
is_finals = []
global x
x = False
def is_blank(s):
    return s.strip() == ''
def main():
    
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        # config = DeepgramClientOptions(
        #     verbose=verboselogs.DEBUG, options={"keepalive": "true"}
        # )
        # deepgram: DeepgramClient = DeepgramClient("", config)
        # otherwise, use default config
        API_KEY = "5112f394cfb185257a9ffddf6ffb982358ec1934"
        deepgram: DeepgramClient = DeepgramClient(API_KEY)

        dg_connection = deepgram.listen.live.v("1")

        def on_open(self, open, **kwargs):
            print(f"Connection Open")

        def on_message(self, result, **kwargs):
            global is_finals
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                # We need to collect these and concatenate them together when we get a speech_final=true
                # See docs: https://developers.deepgram.com/docs/understand-endpointing-interim-results
                is_finals.append(sentence)

                # Speech Final means we have detected sufficent silence to consider this end of speech
                # Speech final is the lowest latency result as it triggers as soon as the endpointing value has triggered
                if result.speech_final:
                    utterance = " ".join(is_finals)
                    #print(f"Speech Final: {utterance}")
                    #is_finals = []
                else:
                    y = True
                    # These are useful if you need real time captioning and update what the Interim Results produced
                    #print(f"Is Final: {sentence}")
            else:
                y = True
                # These are useful if you need real time captioning of what is being spoken
                #print(f"Interim Results: {sentence}")

        def on_metadata(self, metadata, **kwargs):
            y = True
            #print(f"Metadata: {metadata}")

        def on_speech_started(self, speech_started, **kwargs):
            #print(f"Speech Started")
            y = True

        def on_utterance_end(self, utterance_end, **kwargs):
            #print(f"Utterance End")
            global is_finals
            global idk_what
            global x
            x = True
            if len(is_finals) > 0:
                utterance = " ".join(is_finals)
                print(f"Utterance End: {utterance}")
                print(f"Writing to file: useroutput.txt")  
                with open('useroutput.txt', 'w') as f:
                    f.write(utterance) 
                is_finals = []
            microphone.finish()

            # Indicate that we've finished
            dg_connection.finish()

            print(f"Finished")
            on_close()

        # def write_to_file(self, filename):
        #     print(f"Writing to file: {filename}")
        #     with open('message.txt', 'w') as f:
        #     is_finals = []


        def on_close(self, close, **kwargs):
            print(f"Connection Closed")

        def on_error(self, error, **kwargs):
            print(f"Handled Error: {error}")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"Unhandled Websocket Message: {unhandled}")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        #return

        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        options: LiveOptions = LiveOptions(
            model="nova-2",
            language="en-US",
            # Apply smart formatting to the output
            smart_format=True,
            # Raw audio format details
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
            # Time in milliseconds of silence to wait for before finalizing speech
            endpointing=500,
        )

        addons = {
            # Prevent waiting for additional numbers
            "no_delay": "true"
        }

        print("\n\nPress Enter to stop recording...\n\n")
        if dg_connection.start(options, addons=addons) is False:
            print("Failed to connect to Deepgram")
            return

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        while x:
            print("Ending")

        # Wait for the microphone to close
            microphone.finish()

            # Indicate that we've finished
            dg_connection.finish()

            print("Finished")
            x = False
        # sleep(30)  # wait 30 seconds to see if there is any additional socket activity
        # print("Really done!")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()