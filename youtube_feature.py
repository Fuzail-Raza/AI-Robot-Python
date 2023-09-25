
import vlc
import threading
import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from youtubesearchpython import VideosSearch

class VideoPlayerApp:
    def __init__(self, master, video_url, download_path):
        self.master = master
        self.master.title("Video Player")
        self.video_url = video_url
        self.download_path = download_path

        self.instance = vlc.Instance("--no-xlib")
        self.media = self.instance.media_new(self.video_url)
        self.player = self.instance.media_player_new()
        self.player.set_media(self.media)

        self.create_ui()

    def create_ui(self):
        # Play Button
        self.play_button = ttk.Button(self.master, text="Play", command=self.play)
        self.play_button.pack()

        # Pause Button
        self.pause_button = ttk.Button(self.master, text="Pause", command=self.pause)
        self.pause_button.pack()

        # Stop Button
        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop)
        self.stop_button.pack()

        # Seek Slider
        self.seek_slider = ttk.Scale(self.master, from_=0, to=100, orient="horizontal", command=self.seek)
        self.seek_slider.pack(fill="x")

        # Start the player
        self.play()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def seek(self, value):
        percentage = float(value) / 100
        self.player.set_position(percentage)

def search_and_get_video_url(song_name):
    query = f"{song_name} "
    videos_search = VideosSearch(query, limit=1)

    results = videos_search.result()

    if results:
        video_url = results['result'][0]['link']
        return video_url
    else:
        print("No search results found.")
        return None

def play_video_stream(video_url):
    try:
        youtube = YouTube(video_url)
        video_stream = youtube.streams.get_highest_resolution()

        root = tk.Tk()
        
        app = VideoPlayerApp(root, video_stream.url, "E:\Programms\PYTHON\AI_Robot")
        
        t1 = threading.Thread(target=download_video, args=[video_url, "E:\Programms\PYTHON\AI_Robot"])
        t1.start()

        # while True:
        state = app.player.get_state()
        if state == vlc.State.Ended:
            if t1.is_alive:
                t1.join()
            exit()
        
        root.mainloop()

    except:
        print("URL Error Occurs")

def download_video(video_url, output_path):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path)

if __name__ == "__main__":
    song_name = input("Enter the name of video : ")
    video_url = search_and_get_video_url(song_name)
    
    play_video_stream(video_url)
   
