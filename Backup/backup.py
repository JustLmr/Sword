import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
import pywhatkit
import datetime
import sys
import subprocess
import tools.volumelimiter as volumelimiter
import re



import cohere

an = datetime.datetime.now()
hour = datetime.datetime.strftime(an, '%X')

vol_file_path = "./Settings/music.txt"
output_path = "./Settings/output.mp3"
listening_path = "./Settings/listening.mp3"
değer = 10

co = cohere.ClientV2("edrULXSCYa86OYqBM1NKKmmBfgqyFwrHvVFrQ94r")



def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
def delete_audio():
    if os.path.exists(output_path):
        os.remove(output_path)
    print("Ses dosyası temizlendi.")
def vol_read():
    with open(vol_file_path, "r+") as file:
        return file.read().strip()
def vol_write(limiter):
    with open(vol_file_path, "w+") as file:
        file.write(str(limiter))

def process_user_question(user_question):
    question_endings = {
        "mı",
        "mi",
        "mu",
        "mü",
        "mısın",
        "misin",
        "musun",
        "müsün",
        "mıdır",
        "midir",
        "mudur",
        "müdür",
        "mıydı",
        "miydi",
        "muydu",
        "müydü",
        "nedir"
    }

    for ending in question_endings:
        if user_question.endswith(ending):
            base_question = user_question.replace(ending, "").strip()
            print(f"Sorulan: {base_question}")
            
            response = co.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": base_question}]
            )

            if response and response.message and response.message.content:
                for content_item in response.message.content:
                    if content_item.type == 'text':
                        return content_item.text
    return "Üzgünüm, anlayamadım."

def update_volume(vol):
    volumelimiter.update_volume(vol)

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
    elif "aç" in user_command: 
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

                            tts = gTTS(text=text, lang=language, slow=False)
                            tts.save(output_path)
                            play_audio(output_path)

                            os.execv(sys.executable, ['python'] + sys.argv)

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
