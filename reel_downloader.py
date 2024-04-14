import os
import sys
import instaloader

def download_reel(shortcode : str, folder_name : str):
    outfolder = os.path.join("downloads", folder_name)
    # outfolder = rf"downloads\{folder_name}"

    # check if folder exists -> if so, skip download
    if os.path.isdir(outfolder):
        return outfolder

    L = instaloader.Instaloader(dirname_pattern = outfolder, filename_pattern=f"{shortcode}_data") 

    post = instaloader.Post.from_shortcode(L.context, shortcode)

    L.download_post(post, outfolder)
    
    # printing success Message
    print('downloaded Successfully.')
    return outfolder

if __name__ == "__main__":
    download_reel(sys.argv[1]) # uri