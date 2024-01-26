# # pip freeze > requirements.txt
#
# # *********** conda env *************
# # conda create --name converter
# # conda activate converter
# # pip install pyinstaller
# # pyinstaller main.py
# #  pyinstaller --name yt_videos --onefile --windowed --icon=play.ico .\main.py
#

import tkinter
import tkinter.messagebox
import customtkinter
import webbrowser
from PIL import ImageTk
from pytube import YouTube, Playlist
import os
import sys
import threading

home_dir = os.path.expanduser("~/Videos")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


logo = resource_path("play.ico")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("LN-YTVIDEOS")
        self.geometry(f"{1100}x{580}")
        logo_img = ImageTk.PhotoImage(file=logo)
        self.wm_iconbitmap()
        self.iconphoto(False, logo_img)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Opções", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.start_thread_download_video, text="Video e Audio", fg_color="red")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.start_thread_download_audio, text="Audio", fg_color="yellow", text_color="black")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.start_thread_download_playlist, text="Baixar Playlist", fg_color="green")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        # Config
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Aparência:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Zoom:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Digite a URL...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Abrir pasta", command=self.open_folder)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, font=("Arial", 20))
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Qualidade do video:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0, text="720p +")
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1, text="480p -")
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        self.progressbar = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.pPercentage = customtkinter.CTkLabel(self.slider_progressbar_frame, text="0%")
        self.pPercentage.grid(row=3, column=0, padx=(20, 10), pady=(2, 2), sticky="ew")

        # create scrollable frame

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Downloads Completos")
        self.scrollable_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        # set default values
        self.downloaded_videos = 0
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.progressbar.set(0)

        # Threading
        self.thread_progressbar_start = threading.Thread(target=self.progressbar.start)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        per = str(int(percentage_of_completion))
        self.pPercentage.configure(text=per + "%")
        self.pPercentage.update()
        self.progressbar.set(float(percentage_of_completion) / 100)
        self.progressbar.update()

    def start_download_playlist(self):
        ytLink = self.entry.get()
        if not ytLink:
            return

        try:
            p = Playlist(ytLink)
            if not p.videos:
                self.textbox.insert("0.0", "Playlist não disponível")
                return

            self.progressbar.configure(mode="indeterminnate")
            self.thread_progressbar_start.start()
            count = 0
            len_videos = len(p.videos)

            for video in p.videos:
                if self.radio_var.get() == 0:
                    video.streams.get_highest_resolution().download(output_path=home_dir)
                elif self.radio_var.get() == 1:
                    video.streams.get_lowest_resolution().download(output_path=home_dir)

                count += 1
                self.start_thread_videos_completed(video)
                videos_downloaded = len_videos - count
                percentage_of_completion = videos_downloaded / len_videos * 100
                per = str(int(percentage_of_completion))
                self.pPercentage.configure(text=per + "%")
                self.pPercentage.update()
                self.progressbar.set(float(percentage_of_completion) / 100)
                self.progressbar.update()
                if count == len_videos:
                    self.progressbar.stop()
                    self.progressbar.configure(mode="determinate")

                    self.textbox.insert("0.0", "Playlist baixada!")
                    webbrowser.open(str(home_dir))

        except Exception as e:
            self.textbox.insert("0.0", f"Erro ao baixar playlist: {str(e)}")

    def start_download_video(self):
        ytLink = self.entry.get()
        if not ytLink:
            return
        try:
            ytObject = YouTube(ytLink, on_progress_callback=self.on_progress)
            if self.radio_var.get() == 0:
                video = ytObject.streams.get_highest_resolution()
                video.download(output_path=home_dir)
            elif self.radio_var.get() == 1:
                video = ytObject.streams.get_lowest_resolution()
                video.download(output_path=home_dir)

            self.on_completed(ytObject)
        except Exception as e:
            self.textbox.insert("0.0", f"Erro ao baixar playlist: {str(e)}")

    def start_download_audio(self):
        ytLink = self.entry.get()
        if not ytLink:
            return
        try:
            ytObject = YouTube(ytLink, on_progress_callback=self.on_progress)
            video = ytObject.streams.get_audio_only()
            video.download(output_path=home_dir)
            self.on_completed(ytObject)
        except Exception as e:
            self.textbox.insert("0.0", f"Erro ao baixar playlist: {str(e)}")

    def videos_completed(self, ytObject):
        self.downloaded_videos += 1
        checkbox = customtkinter.CTkCheckBox(master=self.scrollable_frame, text="Concluído",
                                             fg_color="green", hover_color="green", state="disabled")
        checkbox.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        checkbox.select()
        checkbox.configure(text=ytObject.title[:20])
        checkbox.grid(row=self.downloaded_videos, column=0, padx=10, pady=(0, 20))
        self.scrollable_frame_switches.append(checkbox)

    def open_folder(self):
        webbrowser.open(str(home_dir))

    def on_completed(self, ytObject):

        self.textbox.insert("0.0", f"{ytObject.title}\n\n" + f"Visitas: {str(ytObject.views)}\n" +
                            "Autor: " + f"{ytObject.author}\n\n" + "_______________________________\n\n")

        self.start_thread_videos_completed(ytObject)
        webbrowser.open(str(home_dir))

    def start_thread_download_playlist(self):
        thread_download_playlist = threading.Thread(target=self.start_download_playlist)
        thread_download_playlist.start()

    def start_thread_download_video(self):
        thread_download_video = threading.Thread(target=self.start_download_video)
        thread_download_video.start()

    def start_thread_download_audio(self):
        thread_download_audio = threading.Thread(target=self.start_download_audio)
        thread_download_audio.start()

    def start_thread_videos_completed(self, ytObject):
        thread_videos_completed = threading.Thread(target=self.videos_completed, args=(ytObject, ))
        thread_videos_completed.start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
