import os
import time
import argparse
from reel_downloader import download_reel
from videoocr import get_subtitles_frames
from subtitles_loader import load_subtitles_from_file

def get_video_file_name(folder : str):
    for file in os.listdir(folder):
        if file.endswith(".mp4"):
            return os.path.join(folder, file)

def get_subtitles(uri : str, 
                  blacklist_text : str | None, 
                  lang_list_text : str, 
                  bottom_only : bool,
                  verify : int,
                  seq : int) -> str:
    blacklist = blacklist_text.split("|") if blacklist_text is not None else []
    lang_list = lang_list_text.split("|")
    start = time.time()

    if uri.startswith("http"):
        shortcode = uri[uri.index("www"):].split("/")[2]
    else:
        shortcode = uri

    print(f"Executing shortcode: '{shortcode}'")
    out_folder = shortcode
    folder_name = download_reel(shortcode, out_folder) # will add ./downloads/
    # video_file_name = get_video_file_name(folder_name)
    video_file_name = f"{folder_name}/{shortcode}_data.mp4"
    subtitle_frames_file_path = f"{folder_name}/{shortcode}_subtitle_frames.txt"
    get_subtitles_frames(video_file_name, subtitle_frames_file_path, 30, bottom_only, lang_list)
    out_subtitles_file_path = f"{folder_name}/{shortcode}.txt"
    out_subtitles = load_subtitles_from_file(subtitle_frames_file_path, 
                                    out_subtitles_file_path, 
                                    # blacklist, 6, 12)
                                    blacklist, verify, seq)
    print(f"Total execute time : {time.time() - start}")
    return out_subtitles

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("uri", type=str, help="uri or shortcode")
    parser.add_argument("--blacklist", type=str, default=None, help="blacklist of filter out the target sentence, separate by '|'")
    parser.add_argument("--langlist", type=str, default="en", help="list lang code that will use for ocr, separate by '|'")
    parser.add_argument("--bottomhalf", type=bool, default=True, action=argparse.BooleanOptionalAction, help="does it check the bottom half of the video only (The speed could be faster and more accurate if the subtitle is mainly in the bottom half)")
    parser.add_argument("--verify", type=int, default=7, help="threshold value of the number of frames that contain target text in the window, if more than or equal to this value the text will be treated as valid text")
    parser.add_argument("--seq", type=int, default=10, help="the window size of checking. If the target text doesn't exist in the window, it will be removed from the checking dictionary")

    args = parser.parse_args()

    print(get_subtitles(args.uri, 
                        args.blacklist, 
                        args.langlist, 
                        args.bottomhalf, 
                        args.verify, 
                        args.seq))