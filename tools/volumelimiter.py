import psutil
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes
from ctypes import cast, POINTER
import time
import configparser


global volume_value
volume_value = 100
config_path = "./Settings/config.ini"

config = configparser.ConfigParser()
config.read(config_path)
app_name = config["Settings"]["browser"]


def get_application_audio_session(app_name):
    sessions = AudioUtilities.GetAllSessions()
    
    for session in sessions:
        process = session.Process
        if process is not None:  
            process_name = process.name().lower()
            if app_name.lower() in process_name:
                return session
    return None

def set_application_volume(app_name, volume_percent):
    session = get_application_audio_session(app_name)

    if session:
        volume = session.SimpleAudioVolume
        volume.SetMasterVolume(volume_percent / 100.0, None)
        print(f"{app_name} uygulamasının sesi % {volume_percent} olarak ayarlandı.")
    else:
        print(f"{app_name} uygulaması bulunamadı.")
        

def update_volume(value):
    """
    Global ses seviyesini güncelle ve uygulamanın ses seviyesini ayarla.
    """
    global volume_value
    volume_value = value
    print(app_name)  
    print(f"Ses seviyesi güncellendi: {volume_value}")
    set_application_volume(app_name, volume_value)

update_volume(100)