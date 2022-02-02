import curses
import cv2
from PIL import Image
import sys
import numpy as np

# Ascii values for gray scale
chars = ["B","S","#","&","@","$","%","*","!",":","."]

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [file location] ")
    exit()
else:
    # Initialize curses
    stdscr = curses.initscr() 

def main():
    start_curses()
    
    frames = get_video_frames()
    stdscr.addstr("Gettting screen size\n") 
      
    MaxY, MaxX  = stdscr.getmaxyx()
    
    stdscr.addstr(f"Screen size: [ {MaxX}, {MaxY} ]\n")
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
        pixels = img.load(); 
        
        # move through all pixels in the screen finding their ascii code and printing it out in the needed position 
        for i in range(Y):
            for j in range(X):
                # some erors appeared becaue out pointer got oud of the screen so i just made this and it worked
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

# Resizes all images by callign reize_image multiple times
def resize_images(framesAmount):
    stdscr.addstr("Started reszing images\n") 
    stdscr.refresh();
    y, MaxX = stdscr.getmaxyx()
    y,x = stdscr.getyx() 
    # call resize image for every frame in the video 
    for i in range(framesAmount):
        stdscr.move(y, x)
        resized_image = resize_image(i, MaxX, y, x)
        resized_image.save(f"resized/resized{i}.jpg")
    stdscr.addstr("Resized images\n")
    stdscr.refresh()


# Resizes 1 image keeping the aspect ratio
def resize_image(index, Width, y, x):
    stdscr.addstr(y, x, f"Resized Image {index}")
    stdscr.refresh()

    im = Image.open(f"frames/frame{index}.jpg") 
    np_image = np.array(im) 
    W, H = im.size;
    ar = H / W # find ascpect ratio
    Height = ar * Width 
    im = im.convert('L') 
    im = im.resize((Width, int(Height))) # resize image
    return im


# reads all frames in video and saves them into the frames folder
def get_video_frames():
    stdscr.addstr("Loading frames\n")
    stdscr.refresh()

    vidcap = cv2.VideoCapture(sys.argv[1])
    success,image = vidcap.read()
    count = 0
    y, x = curses.getsyx()
    while success:
        # output the frames being edited  
        stdscr.addstr(y,x, f"Frame {count}")
        stdscr.refresh()

        cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
    stdscr.addch("\n")
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