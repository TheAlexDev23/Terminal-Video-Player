from __future__ import unicode_literals
import curses
import cv2
from PIL import Image
import sys
import youtube_dl

ydl_opts = {
    'format': ' bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
    'outtmpl': 'YouTubeTemporary/video.%(ext)s',
}

YT = False

# ASCII values for gray scale
chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ".", " "]

if len(sys.argv) != 2:
    if len(sys.argv) == 3:
        if sys.argv[1] == 'y':
            YT = True
        else:
            print(f"Usage: {sys.argv[0]} [file location] ")
            exit()
    else:
        print(f"Usage: {sys.argv[0]} [file location] ")
        exit()

# Initialize curses
stdscr = curses.initscr()


def main():
    start_curses()

    frames = get_video_frames()
    stdscr.addstr("Getting screen size\n")

    resize_images(frames)
    draw_images(frames)

    stdscr.getkey()
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


# Resizes all images by calling resize_image multiple times
def resize_images(framesAmount):
    stdscr.addstr("Started resizing images\n")
    stdscr.refresh()
    y, MaxX = stdscr.getmaxyx()
    y, x = stdscr.getyx()
    # call resize image for every frame in the video 
    for i in range(framesAmount):
        stdscr.move(y, x)
        resized_image = resize_image(i, y, x)
        resized_image.save(f"resized/resized{i}.jpg")
    stdscr.addstr("Resized images\n")
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
    stdscr.addstr("Loading frames\n")
    stdscr.refresh()

    if not YT:
        vidcap = cv2.VideoCapture(sys.argv[1])
    else:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sys.argv[2]])
            vidcap = cv2.VideoCapture("YouTubeTemporary/video.mp4")

    success, image = vidcap.read()
    count = 0
    y, x = curses.getsyx()
    while success:
        # output the frames being edited  
        stdscr.addstr(y, x, f"Frame {count}")
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
    stdscr.keypad(True)


# before stopping curses make the configuration go back to default
def stop_curses():
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)


if __name__ == "__main__":
    main()
