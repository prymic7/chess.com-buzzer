import selenium
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pygame import mixer
import time


windowW = 450
windowH = 250
window = tk.Tk()
window.title("Chess buzz")
window.geometry("450x250")
window.resizable(False, False)
window.eval('tk::PlaceWindow . center')

mixer.init()  # Initialize the mixer
mixer.music.load('audio/buzzer.mp3') 


drivers_running = False
name = None
seconds = None
error = None

def startDrivers(seconds_text, name_text):
    global name, seconds, error

    seconds_content = seconds_text.get()
    name_content = name_text.get()

    #Check if seconds left to buzz contains number, if yes, set go to False
    letter_in_number = True
    for char in seconds_content:
        if char.isalpha():
            letter_in_number = False
            print(char)
            break
        
    if not letter_in_number:
        print("Letter in number")
        error = "Letter in number"
        return
    #Check if both text entries are fullfilled with something   
    if(seconds_content != "" and name_content != ""):
        global drivers_running
        drivers_running = True
        name = name_content
        seconds = seconds_content
        getTime()
    else:
        print("Text entries are not fullfiled")
        error = "Text entries are not fullfiled"

def stopDrivers():
    global drivers_running
    drivers_running = False


execfirstTime = True
buzzFirstTime = True
def getTime():
    global execfirstTime, buzzFirstTime, drivers_running
    if drivers_running:
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://chess.com/play/online")
        time_element = driver.find_element(By.CLASS_NAME, "clock-time-monospace")
        result = time_element.text
        minutes, seconds = map(int, result.split(":"))
        total_seconds = minutes * 60 + seconds

        if total_seconds < seconds:
            mixer.music.play()
            drivers_running = False
        else:
            window.after(1000, getTime)


label_name_text = tk.StringVar()
label_name_text.set("Your chess.com name:")
set_name_label = tk.Label(window, textvariable=label_name_text, font=("Arial", 12))
set_name_label.pack(pady=(40, 0))

entry_secs_buzz_text = tk.StringVar()
entry_secs_buzz = tk.Entry(window, width=8, textvariable=entry_secs_buzz_text, font=("Arial", 14))
entry_secs_buzz.place(x=180, y=windowH-50)

label_secs_buzz_text = tk.StringVar()
label_secs_buzz_text.set("Seconds left to buzz:")
set_secs_label = tk.Label(window, textvariable=label_secs_buzz_text, font=("Arial", 12))
set_secs_label.place(x=20, y=windowH-50) 

entry_name_text = tk.StringVar()
entry_name = tk.Entry(window, textvariable=entry_name_text, font=("Arial", 14))
entry_name.pack(pady=10)

start_btn = tk.Button(window, text="Start", command=lambda: startDrivers(entry_secs_buzz_text, entry_name_text), width=8, height=2)
start_btn.place(x=290, y=windowH-60)

stop_btn = tk.Button(window, text="Stop", command=stopDrivers, width=8, height=2)
stop_btn.place(x=370, y=windowH-60)

window.mainloop()






