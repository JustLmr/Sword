import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
import pywhatkit
import datetime
import sys
import subprocess
import configparser
import pyperclip
# import timer

import tools.volumelimiter as volumelimiter
import google.generativeai as genai
from deep_translator import GoogleTranslator
import speech_recognition as sr
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs



import requests

genai.configure(api_key="AIzaSyCJeZoWbIW1ClLa7AtIoiWO_EEuPSMaO_4")

an = datetime.datetime.now()
hour = datetime.datetime.strftime(an, '%X')

config = configparser.ConfigParser()
client = ElevenLabs(
  api_key="sk_cbcb63d7a0bc8aef35b5a2f95ccdb156bf1ec24e47b57652", 
)



vol_file_path = "./Settings/music.txt"
output_path = "./Sound/output.mp3"
config_path = "./Settings/config.ini"
backup_path = "./Settings/backuptext"


now = datetime.datetime.strftime(an, '%Y-%m-%d %H:%M')

note_value = 1
name = os.getlogin()
config.read(config_path)
config_arl = config["Settings"]["path"]
file_path = rf"C:\Users\{name}{config_arl}"
local_path = rf"C:\Users\{name}\AppData\Local"

değer = 10


pygame.mixer.init()

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.stop()  
    pygame.mixer.quit()  

def delete_audio():
    for _ in range(5):  
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
                print("Ses dosyası temizlendi.")
            return
        except PermissionError:
            print("Dosya kullanımda, yeniden denenecek...")
            time.sleep(0.5) 
    print("Ses dosyası silinemedi, işlem devam ediyor.")


def vol_read():
    return int(config['Settings']["volume"])  
def vol_write(limiter):
    config["Settings"]["volume"] = str(limiter)  
def update_volume(vol):
    volumelimiter.update_volume(vol)

def Ai_value():
    global ai, choose_voice_id
    ai = config['Settings']["Ai"]
    choose_voice_id = config['Settings']["voice_id"]
    

vol = vol_read()
Ai_value()
print(ai)
question_cache = {}

def process_user_question(user_question):
    if user_question in question_cache:
        return question_cache[user_question]
    with open(backup_path, "a",encoding="utf-8") as backup:
        backup.write(user_question + "\n")
    
    try:
        model = genai.GenerativeModel(ai)
        response = model.generate_content(user_question)
        question_cache[user_question] = response.text  
        return response.text
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return "Üzgünüm, bir hata oluştu."

def translate_text(text, target_language='en'):
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        return f"Çeviri hatası: {e}"

def create_img(prompt):
    try:
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer sk-WcXhrXDl2vacXZ4pnQX7VCqjI4t80zSeHTlygB4R7V4Ct22E",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "jpeg",
            },
        )

        if response.status_code == 200:
            image_path = "./generated_image.jpeg"
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Resim oluşturuldu ve {image_path} olarak kaydedildi.")
        else:
            print(f"Resim oluşturulamadı: {response.json()}")
    except Exception as e:
        print(f"Resim oluşturma hatası: {e}")





def recipe_for_food():
    print("Merhaba! Yemek tariflerinde size yardımcı olabilirim.")
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("Tarifi almak için lütfen komut verin... (ör. 'makarna nasıl yapılır')")
        tts = gTTS(text="Tarifi almak için lütfen komut verin.", lang="tr", slow=False)
        tts.save(output_path)
        play_audio(output_path)

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio, language='tr').lower()
            print(f"Algılanan tarif: {query}")

            steps = process_user_question(query)

            if not steps or not isinstance(steps, str): 
                print("Tarif bulunamadı veya bir hata oluştu.")
                continue

            steps = [step.strip().replace("*", "") for step in steps.split("\n") if step.strip()] 

            print("\nTarif adımları:")
            step_index = 0
            while step_index < len(steps):
                print(f"Adım {step_index + 1}: {steps[step_index]}")
                tts = gTTS(text=steps[step_index], lang="tr", slow=False)
                tts.save(output_path)
                play_audio(output_path)

                print("Devam etmek için 'devam et' veya 'çıkış' söyleyin.")
                tts = gTTS(text="Devam etmek için 'devam et' veya 'çıkış' söyleyin.", lang="tr", slow=False)
                tts.save(output_path)
                play_audio(output_path)

                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                try:
                    user_input = recognizer.recognize_google(audio, language='tr').lower()
                    print(f"Algılanan komut: {user_input}")

                    if user_input == "devam et":
                        step_index += 1
                    elif user_input == "çıkış":
                        print("Görüşmek üzere!")
                        subprocess.Popen([sys.executable] + sys.argv)
                        sys.exit()  
                        return
                    else:
                        print("Geçersiz komut, lütfen 'devam et' veya 'çıkış' yazın.")
                
                except sr.UnknownValueError:
                    print("Komut anlaşılmadı, lütfen tekrar edin.")
                except sr.RequestError as e:
                    print(f"Google API hizmetine erişilemiyor: {e}")
        
        except sr.UnknownValueError:
            print("Tarif anlayamadım, lütfen tekrar edin.")
        except sr.RequestError as e:
            print(f"Google API hizmetine erişilemiyor: {e}")




def handle_volume_commands(user_command):
    global vol
    text = ""
    if user_command == "müzik sesini kıs":
        vol = 10
        vol_write(vol)
        update_volume(vol)
        text = f"Müzik sesi %10'a indirildi."
    elif user_command == "müzik sesini aç":
        vol = 100
        vol_write(vol)
        update_volume(vol)
        text = f"Müzik sesi %100'e yükseltildi."
    elif user_command == "müzik sesini biraz aç":
        if vol == 100:
            text = "Müzik sesi zaten en yüksek seviyede."
        else:
            vol += değer
            if vol > 100:
                vol = 100
            vol_write(vol)
            update_volume(vol)
            text = f"Müzik sesi % {vol}'a yükseltildi."
    elif user_command == "müzik sesini biraz kıs":
        if vol == 0:
            text = "Müzik sesi zaten kapalı."
        else:
            vol -= değer
            if vol < 0:
                vol = 0
            vol_write(vol)
            update_volume(vol)
            text = f"Müzik sesi % {vol}'a düşürüldü."
    elif "videosunu aç" in user_command: 
        song_name = user_command.replace("aç", "").strip() 
        text = f"{song_name} adlı şarkıyı açıyorum"
        pywhatkit.playonyt(song_name) 
    


    
    return text

def assistant_listen_and_execute(keyword="hey kılıç", language='tr'):
    global vol
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    os.system("cls")
    print(f"Program çalışıyor. Tetikleme kelimesi: '{keyword}'. Çıkmak için Ctrl+C yapabilirsiniz.")

    try:
        while True:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Tetikleme kelimesini bekliyorum...")
                audio = recognizer.listen(source)

                try:
                    command = recognizer.recognize_google(audio, language=language).lower()
                    print(f"Algılanan: {command}")

                    if keyword in command:
                        print("Lütfen komutunuzu söyleyin...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)

                        try:
                            user_command = recognizer.recognize_google(audio, language=language)
                            print(f"Kullanıcı Komutu: {user_command}")

                            volume_response = handle_volume_commands(user_command)
                            if volume_response:
                                text = volume_response
                            else:
                                text = process_user_question(user_command)

                            if "resim modunu aç" in user_command:
                                print("Nasıl bir şekilde resim oluşturmak istersiniz?")
                                recognizer.adjust_for_ambient_noise(source)
                                audio = recognizer.listen(source)
                                
                                try:
                                    image_description = recognizer.recognize_google(audio, language=language)
                                    print(f"Resim açıklaması: {image_description}")

                                    translated_description = translate_text(image_description, target_language="en")
                                    print(f"İngilizce açıklama: {translated_description}")
                                    create_img(translated_description)

                                except sr.UnknownValueError:
                                    print("Resim açıklamasını anlayamadım, lütfen tekrar edin.")
                                except sr.RequestError as e:
                                    print(f"Google API hizmetine erişilemiyor: {e}")
                            
                            elif "tarif modunu aç" in user_command:
                                print("Nasıl bir şekilde tarif oluşturmak istersiniz?")
                                recognizer.adjust_for_ambient_noise(source)
                                audio = recognizer.listen(source)
                                
                                try:
                                    recipe_for_food()
                                except sr.UnknownValueError:
                                    print("Resim açıklamasını anlayamadım, lütfen tekrar edin.")
                                except sr.RequestError as e:
                                    print(f"Google API hizmetine erişilemiyor: {e}")

                            audio = client.generate(
                                text=text,
                                voice=Voice(
                                    voice_id=choose_voice_id,
                                    settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
                                )
                            )
                            play(audio)

                            tts = gTTS(text=text, lang=language, slow=False)
                            tts.save(output_path)
                            play_audio(output_path)

                        except sr.UnknownValueError:
                            print("Kullanıcı komutunu anlayamadım, lütfen tekrar edin.")
                        except sr.RequestError as e:
                            print(f"Google API hizmetine erişilemiyor: {e}")
                except sr.UnknownValueError:
                    print("Tetikleme kelimesini anlayamadım, tekrar deneyin.")
                except sr.RequestError as e:
                    print(f"Google API hizmetine erişilemiyor: {e}")
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    delete_audio()
    assistant_listen_and_execute()
    
    