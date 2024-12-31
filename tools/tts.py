from TTS.api import TTS

# Türkçe model ve vocoder isimleri
MODEL_NAME = "tts_models/tr/common-voice/glow-tts"

# TTS modelini yükleme
tts = TTS(MODEL_NAME)

# Türkçe metin
text = "Selam Dostum nasılsın umarım iyisindir".lower()

# Ses dosyasını oluşturma
output_path = "turkish_speech_output.wav"
tts.tts_to_file(text=text, file_path=output_path)

print(f"Ses dosyası {output_path} olarak oluşturuldu.")