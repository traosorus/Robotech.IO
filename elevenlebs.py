from elevenlabs import clone , generate, stream
from elevenlabs import set_api_key

set_api_key("1ef66a6800a311364098d15abe21bb50")

audio_stream = generate(
  text="This is a... streaming voice!!",
  voice="Arnold",
  model='eleven_multilingual_v1',
  stream=True
)
stream(audio_stream)
