# import re
# from deepgram import Deepgram
# import requests

# DEEPGRAM_API_KEY = 'Y5112f394cfb185257a9ffddf6ffb982358ec1934'
# deepgram = Deepgram(DEEPGRAM_API_KEY)

# inputText = "Your long text goes here..."

# def segmentTextBySentence(text):
#     return re.findall(r"[^.!?]+[.!?]", text)

# def synthesizeAudio(text):
#     response = deepgram.speech.speak(
#         text,
#         model='aura-helios-en',
#         encoding='linear16',
#         container='wav',
#     )

#     if response.status_code == 200:
#         return response.content
#     else:
#         raise Exception('Error generating audio')

# def main():
#     segments = segmentTextBySentence(inputText)

#     for i, segment in enumerate(segments):
#         try:
#             audioData = synthesizeAudio(segment)
#             with open(f"output_{{i}}.wav", 'wb') as f:
#                 f.write(audioData)
#             print(f"Audio stream finished for segment: {{segment}}")
#         except Exception as error:
#             print(f"Error synthesizing audio: {{error}}")

#     print("Audio file creation completed.")

# main()