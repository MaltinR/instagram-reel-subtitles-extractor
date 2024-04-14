# IMPORTANT!

The goal of this project is not to get high accuracy subtitles text but to get all texts showing in the video

## Tested version

python 3.11 - Windows 10

## Dependencies

EasyOCR - OCR, you can change whatever OCR library you want  
OpenCV - Video & image processing  
Instaloader - For downloading reels for Instagram

## Usage

**Getting the text from reels**  
The program will download the reel from Instagram then process it

```
python main.py [uri/shortcode] [--blacklist] [--langlist] [--verify] [--seq]
```

## Weak point

This project doesn't perform very well when extracting word-by-word style subtitles, a type of video that each frame only contains one word. Because that type of video makes verifying valid subtitles more difficult, users need to fine-tune the verify frame and sequence frame.
