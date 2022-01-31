from ast import arg
import curses
import cv2
from PIL import Image
import sys

# Accii values 
chars = ["B","S","#","&","@","$","%","*","!",":","."]

# Initialize curses
stdscr = curses.initscr() 

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [file location] ")
        exit()

    start_curses()
    
    frames = get_video_frames()
    stdscr.addstr("Gettting screen size\n") 
      
    MaxY, MaxX  = stdscr.getmaxyx()
    
    stdscr.addstr(f"Screen size: [ {MaxX}, {MaxY} ]\n")
    resize_images(MaxX, frames)
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
        W, H = img.size

        # get all the pixels in the image
        pixels = img.load(); 
        
        # move through all pixels in the screen finding their ascii code and printing it out in the needed position 
        for i in range(W):
            for j in range(H):
                # some erors appeared becaue out pointer got oud of the screen so i just made this and it worked
                try:
                    stdscr.move(i, j)
                except:
                    continue
                # get pixel at coordinate j i 
                pixel = pixels[j, i]

                # find the needed ascii character to represent its color
                character = chars[int(int(pixel[0]) // 25)]

                # print out the result 
                stdscr.addstr(character)
                stdscr.refresh() 

# Resizes all images by callign reize_image multiple times
def resize_images(MaxX, framesAmount):
    stdscr.addstr("Started reszing images\n") 
    stdscr.refresh();

    # call resize image for every frame in the video 
    for i in range(framesAmount):
        resized_image = resize_image(i, MaxX)
        resized_image.save(f"resized/resized{i}.jpg")

    stdscr.addstr("Resized images\n")
    stdscr.refresh()


# Resizes 1 image keeping the aspect ratio
def resize_image(index, With):
    im = Image.open(f"frames/frame{index}.jpg") 
    W, H = im.size;
    ar = H / W # find ascpect ratio
    Height = ar * With 
    im = im.resize((With, int(Height))) # resize image
    return im


# reads all frames in video and saves them into folder
def get_video_frames():
    stdscr.addstr("Loading frames\n")
    stdscr.refresh()


    vidcap = cv2.VideoCapture(sys.argv[1])
    success,image = vidcap.read()
    count = 0
    while success:
        stdscr.refresh()
        cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
    stdscr.addstr("Finished loading frames\n")
    stdscr.refresh()
    return count


def start_curses():
    # cofnigure cureses
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)


def stop_curses():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)


if __name__ == "__main__":
    main()