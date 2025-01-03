import configparser
import subprocess
import psutil  
import time

config_path = "./Settings/config.ini"
config = configparser.ConfigParser()
config.read(config_path)

restricted_apps = eval(config.get("Application", "restricted_apps"))  

def check_and_kill_restricted_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name'].lower()
            process_id = proc.info['pid']
            
            if any(app.lower() in process_name for app in restricted_apps):
                print(f"{process_name} kısıtlı uygulama, kapatılıyor...")
                subprocess.call(["taskkill", "/F", "/PID", str(process_id)])  # Uygulamayı kapat
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def restrict_applications():
    """Engellenen uygulamaları sürekli kontrol eder ve kapatır."""
    while True:
        for app in restricted_apps:
            check_and_kill_restricted_apps()
        time.sleep(2)  


if __name__ == "__main__":
    print("Kısıtlı uygulamalar kontrol ediliyor...")
    restrict_applications()