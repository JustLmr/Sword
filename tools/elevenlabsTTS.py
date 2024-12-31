from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_cbcb63d7a0bc8aef35b5a2f95ccdb156bf1ec24e47b57652", 
)

audio = client.generate(
    text="Herkese selam millet ben kılıç nasıl gidiyor",
    voice=Voice(
        voice_id='IuRRIAcbQK5AQk1XevPj',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=1.0, use_speaker_boost=True)
    )
)

play(audio)  # ffmpeg ile ses çalacak
