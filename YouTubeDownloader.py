from pytube import YouTube
import os


def GetCurrentWorkingDir():
    return os.getcwd()


def DownloadVideo(url, SAVE_PATH):
    yt = YouTube(url)

    mp4files = yt.filter('mp4')

    video_to_download = yt.get(mp4files[-1].extension, mp4files[-1].resolution)
    try:
        # downloading the video
        video_to_download.download(SAVE_PATH)
    except:
        print("Something Went Wrong!")
        exit()
