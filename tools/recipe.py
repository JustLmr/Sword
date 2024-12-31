import os
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
import configparser
import google.generativeai as genai

# Konfigürasyon
genai.configure(api_key="AIzaSyCJeZoWbIW1ClLa7AtIoiWO_EEuPSMaO_4")
config = configparser.ConfigParser()
question_cache = {}
backup_path = "./Settings/backuptext"
output_path = "./Sound/output.mp3"
ai = "gemini-2.0-flash-exp"

# Sesli yanıtlar için ses dosyasını oynatma
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.stop()  
    pygame.mixer.quit()  

# Ses dosyasını silme
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

# Kullanıcıdan gelen soruyu işleme
def process_user_question(user_question):
    if user_question in question_cache:
        return question_cache[user_question]
    with open(backup_path, "a", encoding="utf-8") as backup:
        backup.write(user_question + "\n")
    
    try:
        model = genai.GenerativeModel(ai)
        response = model.generate_content(user_question)
        question_cache[user_question] = response.text  
        return response.text
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return "Üzgünüm, bir hata oluştu."


def recipe_for_food():
    print("Merhaba! Yemek tariflerinde size yardımcı olabilirim.")
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        # Tarif almak için sesli komut dinle
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

            # Tarif adımlarını işlemeye başla
            steps = process_user_question(query)

            if not steps or not isinstance(steps, str): 
                print("Tarif bulunamadı veya bir hata oluştu.")
                continue

            # Her adımı düzgün bir şekilde al
            steps = [step.strip().replace("*", "") for step in steps.split("\n") if step.strip()] 

            print("\nTarif adımları:")
            step_index = 0
            while step_index < len(steps):
                print(f"Adım {step_index + 1}: {steps[step_index]}")
                tts = gTTS(text=steps[step_index], lang="tr", slow=False)
                tts.save(output_path)
                play_audio(output_path)

                # Devam et veya çıkış komutunu sesli dinle
                print("Devam etmek için 'devam et' veya 'çıkış' yazın.")
                tts = gTTS(text="Devam etmek için 'devam et' veya 'çıkış' yazın.", lang="tr", slow=False)
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




def assistant_listen_and_execute(keyword="hey kılıç", language='tr'):
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

                            if "tarif aç" in user_command:
                                print("Nasıl bir şekilde tarif oluşturmak istersiniz?")
                                recognizer.adjust_for_ambient_noise(source)
                                audio = recognizer.listen(source)
                                
                                try:
                                    recipe_for_food()
                                except sr.UnknownValueError:
                                    print("Resim açıklamasını anlayamadım, lütfen tekrar edin.")
                                except sr.RequestError as e:
                                    print(f"Google API hizmetine erişilemiyor: {e}")

                            tts = gTTS(text="Komut alındı", lang=language, slow=False)
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
