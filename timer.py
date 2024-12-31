import time
import os 
import datetime
import pyperclip

timer_path = "./Settings/timer.txt"
check_path = "./Settings/check.txt"
clipboard_path = "./Settings/clipboard.txt"

timer_value = input(f"2024-12-24 21:16 \nSayı girin: ")


clipboard_content = pyperclip.paste()


def create_time():
    with open(timer_path, "w+") as file:
        file.write(timer_value)

def create_check():
    with open(check_path, "w+") as file:
        file.write("True")

def clipboard_create():
    with open(clipboard_path,"w+") as file:
        file.write(clipboard_content)



def while_check():
    with open(timer_path,"r") as reading:
        read_value = reading.read()
        print(read_value)    
    
    while True:
        an = datetime.datetime.now()
        now = datetime.datetime.strftime(an, '%Y-%m-%d %H:%M')

        if read_value == now:
            print("evet")
            os.system("cls")
            create_check()
            time.sleep(5)
            continue
        elif read_value <= now:
            print("zaman geçti")
            os.remove(check_path)
            os.remove(timer_path)
            break
        else:
            print("hayır")
            time.sleep(1)
            os.system("cls")






if __name__ == "__main__":
    create_time()
    clipboard_create()
    while_check()
    