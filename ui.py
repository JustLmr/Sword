import tkinter as tk
import configparser
from tkinter import messagebox

config_path = "./Settings/config.ini"

config = configparser.ConfigParser()
config.read(config_path)

form = tk.Tk()
form.title("Sesli Asistan")
form.geometry("400x250")

g1 = tk.IntVar()
g1.set(0)

br = tk.IntVar()
br.set(0)


def submit():
    try:
        if g1.get() == 1:
            config["Settings"]["Ai"] = "gemini-1.5-flash-8b"
        elif g1.get() == 2:
            config["Settings"]["Ai"] = "gemini-1.5-flash"
        elif g1.get() == 3:
            config["Settings"]["Ai"] = "gemini-1.5-pro"

        if br.get() == 1:
            config["Settings"]["browser"] = "chrome.exe"
        elif br.get() == 2:
            config["Settings"]["browser"] = "brave.exe"
        elif br.get() == 3:
            config["Settings"]["browser"] = "opera.exe"
        messagebox.showinfo("Justlmr", "İşlem Başarılı") 
    except Exception as e:
        messagebox.showerror("Justlmr", f"Hata verdi hata içeriği: \n {e}") 

    with open(config_path, 'w') as configfile:
        config.write(configfile)

# Bileşenler
label = tk.Label(form, text="Sesli Asistan")
label.grid(row=0, column=0, sticky="w", padx=10, pady=5)




# Ai Choose
l1 = tk.Label(form, text="Yapay zeka seçim")
l1.grid(row=1, column=0, sticky="w", padx=10, pady=5)

ck1 = tk.Radiobutton(form, text="Gemini-1.5-flash-8b", variable=g1, value=1)
ck1.grid(row=2, column=0, sticky="w", padx=10, pady=5)

ck2 = tk.Radiobutton(form, text="Gemini-1.5-flash", variable=g1, value=2)
ck2.grid(row=3, column=0, sticky="w", padx=10, pady=5)

ck3 = tk.Radiobutton(form, text="Gemini-1.5-pro", variable=g1, value=3)
ck3.grid(row=4, column=0, sticky="w", padx=10, pady=5)






# Browser Choose
brlabel = tk.Label(form, text="Browser Seçim")
brlabel.grid(row=1, column=0, sticky="w", padx=200, pady=5)

br1 = tk.Radiobutton(form, text="Google", variable=br, value=1)
br1.grid(row=2, column=0, sticky="w", padx=200, pady=5)

br2 = tk.Radiobutton(form, text="Brave", variable=br, value=2)
br2.grid(row=3, column=0, sticky="w", padx=200, pady=5)

br3 = tk.Radiobutton(form, text="Opera", variable=br, value=3)
br3.grid(row=4, column=0, sticky="w", padx=200, pady=5)






button = tk.Button(form, text="Onayla", fg="white", bg="black", command=submit)
button.grid(row=5, column=0, sticky="w", padx=10, pady=5)

form.mainloop()
