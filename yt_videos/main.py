# pip freeze > requirements.txt

# *********** conda env *************
# conda create --name converter
# conda activate converter
# pip install pyinstaller
# pyinstaller main.py
#  pyinstaller --name yt_videos --onefile --windowed --icon=play.ico .\main.py

#11 05


import tkinter
import webbrowser
from PIL import ImageTk
import customtkinter
from pytube import YouTube
import os
import sys

home_dir = os.path.expanduser("~")


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


logo = resource_path("play.ico")


def start_download_video() -> None:
    ytLink = link.get()
    if not ytLink:
        return
    try:
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        video.download(output_path=home_dir)
        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        finishLabel.configure(text="Finalizado!")
	on_completed()

    except:
        finishLabel.configure(text="Erro ao baixar!", text_color="red")
        


def start_download_audio() -> None:
    ytLink = link.get()
    if not ytLink:
        return
    try:
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        audio = ytObject.streams.get_audio_only()
        audio.download(output_path=home_dir)
        title.configure(text=ytObject.title, text_color="white")
        on_completed()

    except:
        finishLabel.configure(text="Erro ao baixar!", text_color="red")


def on_completed():
    finishLabel.configure(text="")
    finishLabel.configure(text="Finalizado!")
    local_saved.configure(text="Salvo em: " + str(home_dir))
    webbrowser.open(str(home_dir))
    local_saved.pack(padx=10, pady=10)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + "%")
    pPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)


# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x340")
app.title("YouTube Download")

# Adding UI Elements
logo_img = ImageTk.PhotoImage(file=logo)
app.wm_iconbitmap()
app.iconphoto(False, logo_img)


# Link URL
title = customtkinter.CTkLabel(app, text="Insira um link do youtube")
title.pack(padx=10, pady=10)


# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=10, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()


# Download Button
download_video = customtkinter.CTkButton(app, text="Video", command=start_download_video, fg_color="red")
download_video.pack(padx=10, pady=10)

download_audio = customtkinter.CTkButton(app, text="Audio", command=start_download_audio, fg_color="yellow", text_color="black")
download_audio.pack(padx=10, pady=10)

# Progress
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Saved in
local_saved = customtkinter.CTkLabel(app, text_color="green")


# Run app
app.mainloop()
