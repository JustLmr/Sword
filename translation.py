from deep_translator import GoogleTranslator
import speech_recognition as sr
import requests
import os

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
                "authorization": f"Bearer sk-ZZnyli5npU1I8a3QvrsOAV66jWDzFbkd95XNwv4vW1iKgEno",
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
                            user_command = recognizer.recognize_google(audio, language=language).lower()
                            print(f"Kullanıcı Komutu: {user_command}")

                            if "resim oluştur" in user_command:
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
                            else:
                                print("Bu komut için herhangi bir işlem yapılmayacak.")

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

assistant_listen_and_execute()
