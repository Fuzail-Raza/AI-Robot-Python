from youtubesearchpython import VideosSearch
from pytube import YouTube
import vlc
import pafy
import threading


def search_and_get_video_url(song_name):
    query = f"{song_name} "
    videos_search = VideosSearch(query, limit = 1)
    
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

                     player = vlc.MediaPlayer(video_stream.url)
                     player.play()
                     t1=threading.Thread(target=download_video,args=[video_url,"E:\Programms\PYTHON\AI_Robot"])
                     t1.start()
                     while True:
                            state = player.get_state()
                            if state == vlc.State.Ended:
                                   if(t1.is_alive):
                                          t1.join()
                                   break
              except :
                     print("URL Error Occurrs")
    

def download_video(video_url, output_path):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path)



if __name__ == "__main__":
    song_name = input("Enter the name of the song: ")
    video_url = search_and_get_video_url(song_name)
    
    play_video_stream(video_url)
    # tumhahra naam musibat ma jab lya ho gaa by owais raza