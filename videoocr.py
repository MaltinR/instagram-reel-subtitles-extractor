import cv2
import easyocr

def get_text_from_image(reader : easyocr.Reader, image, timestamp, subtitles, bottom_half_only, threshold = 0.6):
    # print(f"Getting text from timestamp: {timestamp}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    new_width = int(gray.shape[1] / 2)
    new_height = int(gray.shape[0] / 2)
    # print(f"{new_width}, {new_height} | {gray.shape}")
    gray = cv2.resize(gray, (new_width, new_height))
    half_height = int(new_height / 2)
    if bottom_half_only:
        gray = gray[half_height:new_height+half_height,:]
        # print(f"{gray.shape[0]},{gray.shape[1]} | {gray.shape}")
    # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    text = reader.readtext(gray, detail=1, batch_size=5, decoder="wordbeamsearch")

    '''
    [
        (
            [[138, 304], [948, 304], [948, 360], [138, 360]], 
            'BERAPA NIH HARGA ALMET', 0.9496627139067964
        ), (
            [[246, 371], [837, 371], [837, 428], [246, 428]], 
            'ANAK HUKUM UMS?', 0.9672989199618675
        ), (
            [[410, 838], [496, 838], [496, 894], [410, 894]], 
            '8Bia', 0.4790264070034027
        ), (
            [[433, 891], [493, 891], [493, 933], [433, 933]], 
            'S9', 0.1362310774737849
        )
    ]
    '''
    # print(type(text))

    word_list = list(filter(lambda el: el[2] > threshold, text))

    # print(word_list[0])

    word_list = list(map(lambda el: el[1], word_list))

    output_text = "|".join(word_list)

    subtitles.append((timestamp, output_text))

def group_every(source, count):
    return [source[i:i+count] for i in range(0,len(source),count)]

def get_subtitles_frames(video_path : str, output, target_fps : int = 15, bottom_half_only : bool = True, lang_list: list = ["en"]):

    video = cv2.VideoCapture(video_path)

    fps = video.get(cv2.CAP_PROP_FPS)
    reader = easyocr.Reader(lang_list)

    subtitles = []

    frame_count = 0
    interval = fps / target_fps

    next_target_frame = 0

    while True:
        ret, frame = video.read()

        if not ret:
            break

        frame_count += 1
        if frame_count < next_target_frame:
            continue
        next_target_frame += interval
        print(f"Reading frame {frame_count} / {int(video.get(cv2.CAP_PROP_FRAME_COUNT))}")

        timestamp = video.get(cv2.CAP_PROP_POS_MSEC)

        get_text_from_image(reader, frame, timestamp, subtitles, bottom_half_only)

    video.release()

    with open(output, 'w') as f:
        for i, (timestamp, text) in enumerate(subtitles):
            try:
                f.write(f"{text}\n")
            except:
                pass