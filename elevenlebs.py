import threading
import openai
from elevenlabs import clone, generate, stream
from elevenlabs import set_api_key

def discord(value):
    set_api_key("1ef66a6800a311364098d15abe21bb50")

    audio_stream = generate(
        text=value,
        voice="Arnold",
        model='eleven_multilingual_v1',
        stream=True
    )
    stream(audio_stream)

def ChatCompletion(request):
    openai.api_key = "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"

    toplay = ""
    balim = ""

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=request,
        temperature=0.7,
        stream=True
    )

    for chunk in response:
        try:
            chunk_message = chunk['choices'][0]['message']['content']
            toplay += chunk_message
            print(len(toplay))
            if len(toplay) > 500:
                discord(toplay)
                toplay = ""
                print("balim")
        except:
            pass

x = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': "200 mots à propos de la leucemie."}
]

thread = threading.Thread(target=ChatCompletion(x))
thread.start()

