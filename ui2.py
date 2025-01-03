import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import os

# config dosyasının yolu
config_path = "./Settings/config.ini"
config = configparser.ConfigParser()

def get_restricted_apps():
    """config.ini dosyasındaki restricted_apps verisini alır."""
    config.read(config_path)
    restricted_apps = eval(config.get("Application", "restricted_apps"))
    return restricted_apps

def save_restricted_apps(restricted_apps):
    """restricted_apps listesini config.ini dosyasına kaydeder."""
    config.read(config_path)
    config.set("Application", "restricted_apps", str(restricted_apps))
    with open(config_path, "w") as configfile:
        config.write(configfile)

def open_file():
    """Sadece .exe dosyalarını seçebileceğimiz bir dosya seçim penceresi açar."""
    file_path = filedialog.askopenfilename(
        title="Bir .exe dosyası seçin",
        filetypes=[("Executable Files", "*.exe")]
    )
    
    if file_path:  # Eğer bir dosya seçildiyse
        # Dosya yolunun sadece son kısmını (dosya adını) al
        file_name = os.path.basename(file_path)
        selected_file_label.config(text=f"Seçilen Dosya: {file_name}")
        # Dosya adını global değişkende sakla
        global selected_file
        selected_file = file_name
    else:
        messagebox.showinfo("Hata", "Bir dosya seçilmedi.")

def submit_file():
    """Seçilen dosyayı restricted_apps listesine ekler ve kaydeder."""
    if not selected_file:
        messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")
        return
    
    # restricted_apps listesini al
    restricted_apps = get_restricted_apps()
    
    # Eğer dosya zaten listede yoksa ekle
    if selected_file.lower() not in [app.lower() for app in restricted_apps]:
        restricted_apps.append(selected_file)
        save_restricted_apps(restricted_apps)
        messagebox.showinfo("Başarılı", f"{selected_file} başarıyla eklendi.")
        selected_file_label.config(text="Seçilen dosya yok")
    else:
        messagebox.showwarning("Uyarı", "Bu uygulama zaten kısıtlı uygulamalar listesinde.")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Uygulama Seçici")
root.geometry("400x300")

# Başlık
label = tk.Label(root, text="Bir .exe dosyası seçin", font=("Arial", 14))
label.pack(pady=10)

# Seçilen dosya etiketini gösterecek label
selected_file_label = tk.Label(root, text="Seçilen dosya yok", font=("Arial", 10))
selected_file_label.pack(pady=10)

# "Dosya Aç" butonu
open_button = tk.Button(root, text="Dosya Aç", command=open_file, font=("Arial", 12))
open_button.pack(pady=10)

# "Submit" butonu
submit_button = tk.Button(root, text="Submit", command=submit_file, font=("Arial", 12))
submit_button.pack(pady=20)

# Pencereyi çalıştır
root.mainloop()
