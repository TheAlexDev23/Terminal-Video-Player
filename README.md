# Terminal Video Player

- This code will allow you to play any video in the terminal!
- Works perfectly with video formats like mkv mp4 and mov formats, other are still left to be tested
- Can download any video of YouTube and play it.

## How to run

```bash
python Player.py [Video to play]
```
Or if you want a video from YouTube:
```bash
python Player.py -y [Video Url]
```
Note that adding the "y" argument would make the program search in YouTube for a video

### For example:

```bash
python Player.py ~/Videos/BadApple.mp4
```

Or if you want to play a YouTube video:

```bash
python Player.py -y "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
