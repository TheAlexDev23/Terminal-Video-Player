# Terminal Video Player

- This code will allow you to play any video in the terminal!
- Works perfectly with video formats like mkv mp4 and mov formats, other are still left to be tested
- Can download any video of YouTube and play it.

## How to run

### If you want to play a video saved on your computer run the following

```bash
python ./Player.py [Location of the file you want to play]
```

### If you want to play a video from YouTube run the following

```bash
python ./Player.py -y [URL of the YouTube video]
```

#### Or if you want to play the video from YouTube with subtitles there's 2 ways

Play with default subtitles:

```bash
python ./Player.py -y [URL of the YouTube video] -c
```

Play subtitles in a certain language:

```bash
python ./Player.py -y [URL of the YouTube video] -c [lang]
```

## Examples of usage

### Video from computer

```bash
python ./Player.py ~/Videos/NeverGonnaGiveYouUp.mp4
```

### Video from YouTube without subtitles

```bash
python ./Player.py -y "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Video from YouTube with default subtitles

```bash
python ./Player.py -y "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c
```

### Video from YouTube with english subtitles

```bash
python ./Player.py -y "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c en
```

## Things to know before using

- Playing any video would create 2 folders each having `X` amount of jpgs, where `X` is the amount of frames the video has
- Playing a video from YouTube would download it under ``` YouTubeTemporary/video.mp4 ```
- If you already played a video from YouTube and you want to play another one, you need to first delete the video.mp4 from the YouTubeTemporary folder (note, that this is not necessary if you would be playing the same video or a video from your computer)
- If subtitles are not found (maybe because there's no subtitles in the video or not in the specified language), an exception would be thrown
- If the video is not found (maybe because it doesn't exist or there's no internet connection) an exception would also be thrown
- Running the program requires the following dependencies:
  - Pillow
  - OpenCV-python
  - youtube_dl
  - pytube
  - youtube_transcript_api
