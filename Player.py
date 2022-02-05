from __future__ import unicode_literals
import curses
import cv2
from PIL import Image
import sys
import youtube_dl
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi

# This would be used by the youtube_dl library to save videos
ydl_opts = {
    'format': ' bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
    'outtmpl': 'YouTubeTemporary/video.%(ext)s',
}

# If we are trying to download from YouTube this variable would be equal to True and used in other calculations
YT = False
# If we want to play our YT vid with captions, then this variable would be equal to true
Captions = False
CaptionsLang = None
CaptionsUseLang = False

# ASCII values for gray scale
chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ".", " "]

if len(sys.argv) != 2:
    if len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5:
        # a 'y' as argument indicates that the video should be played from YouTube
        if sys.argv[1] == '-y':
            YT = True
            # if after the -y [video link] there's a -c then we would enable captions
            if len(sys.argv) == 4 and sys.argv[3] == '-c':
                Captions = True
                CaptionsLang = None
                CaptionsUseLang = False
            # But if the same case as before but there's 5 arguments, the last would be used to specify the captions
            # language
            elif len(sys.argv) == 5 and sys.argv[3] == '-c':
                Captions = True
                CaptionsLang = sys.argv[4]
                CaptionsUseLang = True
        else:
            print(f"Usage: {sys.argv[0]} [file location] ")
            exit()
    else:
        print(f"Usage: {sys.argv[0]} [file location] ")
        exit()

# We will only start curses if we are not downloading from YouTube, in case we are this would be started later
if not YT:
    # Initialize curses
    stdscr = curses.initscr()


def main():
    if not YT:
        start_curses()

    frames = get_video_frames()
    if Captions:
        stdscr.addstr("Getting video captions")
        stdscr.refresh()
        get_captions()
        stdscr.addstr("Gotten captions")
        stdscr.refresh()

    resize_images(frames)
    draw_images(frames)

    stdscr.getkey()

    stdscr.refresh()
    stop_curses()


# Will draw ascii drawings for each frame in the video
def draw_images(imageAmount):
    stdscr.addstr("Press any key to start drawing\n")
    stdscr.refresh()
    stdscr.getch()

    for x in range(imageAmount):
        img = Image.open(f"resized/resized{x}.jpg")
        Y, X = stdscr.getmaxyx()

        # get all the pixels in the image
        pixels = img.load()

        # move through all pixels in the screen finding their ascii code and printing it out in the needed position 
        for i in range(Y):
            for j in range(X):
                if i == stdscr.getmaxyx()[0] - 1:
                    continue
                try:
                    stdscr.move(i, j)
                    # get pixel at coordinate j i 
                    pixel = pixels[j, i]
                    # find the needed ascii character to represent its color
                    character = chars[int(int(pixel) // 25)]
                    stdscr.addstr(character)
                except:
                    continue
                #  print out the result 
                stdscr.refresh()
        get_caption_at_frame(x)
        stdscr.refresh()


# Return captions if we are playing something from YouTube
def get_captions():
    # this is needed because multiple types of url might be used
    video_code = extract.video_id(sys.argv[2])
    global CaptionsArray
    if not CaptionsUseLang:
        CaptionsArray = YouTubeTranscriptApi.get_transcript(video_code)
    else:
        CaptionsArray = YouTubeTranscriptApi.get_transcript(video_code, languages=[CaptionsLang])


def get_caption_at_frame(frame):
    # Clear first the subtitles line
    for y in range(stdscr.getmaxyx()[1]-1):
        stdscr.addstr(stdscr.getmaxyx()[0]-1, y, " ")

    time_needed = frame / Video_FPS
    time_passed = CaptionsArray[0]["start"]

    for i in range(len(CaptionsArray)):
        time_passed += CaptionsArray[i]["duration"]
        if int(time_passed) == int(time_needed):
            # Print out the needed caption in the middle of the screen
            stdscr.addstr(stdscr.getmaxyx()[0] - 1, int(stdscr.getmaxyx()[1]/2 - len(CaptionsArray[i]["text"]) / 2),
                          CaptionsArray[i]["text"])


# Resizes all images by calling resize_image multiple times
def resize_images(framesAmount):
    stdscr.addstr("Started resizing images\n")
    stdscr.refresh()
    y, x = stdscr.getyx()
    # call resize image for every frame in the video 
    for i in range(framesAmount):
        stdscr.move(y, x)
        resized_image = resize_image(i, y, x)
        resized_image.save(f"resized/resized{i}.jpg")
    stdscr.addstr("\nResized images\n")
    stdscr.refresh()


# Resizes 1 image
def resize_image(index, y, x):
    stdscr.addstr(y, x, f"Resized Image {index}")
    stdscr.refresh()

    Height, Width = stdscr.getmaxyx()

    im = Image.open(f"frames/frame{index}.jpg")

    im = im.convert('L')
    im = im.resize((Width, Height))  # resize image
    return im


# reads all frames in video and saves them into the frames folder
def get_video_frames():
    # Get the video by file name
    if not YT:
        vidcap = cv2.VideoCapture(sys.argv[1])
    else:
        # Download the video using youtube_dl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sys.argv[2]])
            vidcap = cv2.VideoCapture("YouTubeTemporary/video.mp4")
            # If we marked to download the video from YouTube, we won't have started curses, so here we start it

            """
            The reason behind why I don't start it right away, is because youtube_dl usually logs some output which with
            curses enabled can have some weird behaviour.
            This is a solution that worked and I decided to keep it. 
            """

            global stdscr
            stdscr = curses.initscr()
            start_curses()

    stdscr.addstr("Loading frames\n")
    stdscr.refresh()

    global Video_FPS
    global Video_Frames
    Video_FPS = int(vidcap.get(cv2.CAP_PROP_FPS))
    Video_Frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    success, image = vidcap.read()
    count = 0
    y, x = curses.getsyx()
    while success:
        # output the frames being edited  
        stdscr.addstr(y, x, f"Frame {count} / {Video_Frames - 1}")
        stdscr.refresh()

        cv2.imwrite("frames/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += 1
    stdscr.addch("\n")
    stdscr.addstr("Finished loading frames\n")
    stdscr.refresh()
    return count


# basic default curses configuration
def start_curses():
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()


# before stopping curses make the configuration go back to default
def stop_curses():
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()


if __name__ == "__main__":
    main()
