from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

text = "Bir ses geliştirmek oldukça uzun zaman aldı ve şimdi onu bulduğumda susmayacağım."

speaker_wav = "C:/Users/Emire/Desktop/Kılıç/speaker.wav"

output_path = "output_turkish.wav" 

tts.tts_to_file(text=text, speaker_wav=speaker_wav, file_path=output_path, language="tr")

print(f"Ses dosyası {output_path} olarak oluşturuldu.")
