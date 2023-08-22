import openai
import speech_recognition as spr
import sys
from gtts import gTTS
import os

conversation = ''
user_name = 'George'
bot_name = 'Ozzy'
openai.api_key = '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'
r = spr.Recognizer()
mic = spr.Microphone()

while True:
    with mic as source:
        print('\n' + bot_name + ' listening..')
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print(bot_name + ' not listening..\n')

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_string = response["choices"][0]["text"].replace("\n", "")
    response_string = response_string.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    conversation += response_string + "\n"
    print(response_string)
    
    # Use gTTS to convert the AI's response to speech
    tts = gTTS(text=response_string, lang='en')
    tts.save("response.mp3")

    # Play the generated audio
    os.system("afplay response.mp3")

    # Exit the loop when the exit word appears in user input
    if 'exit' in user_input:
        sys.exit()
