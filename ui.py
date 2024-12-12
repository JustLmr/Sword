import tkinter as tk
import configparser

config_path = "./Settings/config.ini"

config = configparser.ConfigParser()
config.read(config_path)

form = tk.Tk()
form.title("Sesli Asistan")
form.geometry("200x250")

g1 = tk.IntVar()
g1.set(0)

def submit():
    if g1.get() == 1:
        config["Settings"]["Ai"] = "gemini-1.5-flash-8b"
    elif g1.get() == 2:
        config["Settings"]["Ai"] = "gemini-1.5-flash"
    elif g1.get() == 3:
        config["Settings"]["Ai"] = "gemini-1.5-pro"
    
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# Bileşenler
label = tk.Label(form, text="Sesli Asistan")
label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

l1 = tk.Label(form, text="Yapay zeka seçim")
l1.grid(row=1, column=0, sticky="w", padx=10, pady=5)

ck1 = tk.Radiobutton(form, text="Gemini-1.5-flash-8b", variable=g1, value=1)
ck1.grid(row=2, column=0, sticky="w", padx=10, pady=5)

ck2 = tk.Radiobutton(form, text="Gemini-1.5-flash", variable=g1, value=2)
ck2.grid(row=3, column=0, sticky="w", padx=10, pady=5)

ck3 = tk.Radiobutton(form, text="Gemini-1.5-pro", variable=g1, value=3)
ck3.grid(row=4, column=0, sticky="w", padx=10, pady=5)

button = tk.Button(form, text="Onayla", fg="white", bg="black", command=submit)
button.grid(row=5, column=0, sticky="w", padx=10, pady=5)

form.mainloop()
