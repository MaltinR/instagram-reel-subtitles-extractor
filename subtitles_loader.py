import sys

verify_frame = 3 # How many frames it needs to will treat as verified data
sequence_frame = 10 # if same appear in the last x frames it will treat as the same

def get_frame_detail(frame_text : str, 
                     sentence_dict: dict, 
                     verify_frame : int = verify_frame, 
                     sequence_frame : int = sequence_frame,
                     black_list: list = []) -> list: 
    # print(frame_text)
    sentences = frame_text.split("|")

    # duplicate_list : a list storing frame distance to the current frame

    for key in sentence_dict.keys():
        # check if matched
        sentence_dict[key]["frame_to_last_match"] = sentence_dict[key]["frame_to_last_match"] + 1
        # move one frame distance & remove those records that are expired
        sentence_dict[key]["duplicate_list"] = list(filter(
            lambda x: x < sequence_frame, list(map(
                lambda x: x + 1, sentence_dict[key]["duplicate_list"]))))

    for sentence in sentences:
        # check if in dict
        sentence = sentence.strip(" ")

        if len(sentence) == 0:
            continue

        if sentence in sentence_dict.keys():
            if sentence_dict[sentence] != 0:
                sentence_dict[sentence]["duplicate_list"].append(0)
                sentence_dict[sentence] = { 
                    "frame_to_last_match": 0, 
                    "duplicate_list": sentence_dict[sentence]["duplicate_list"],
                    "verified": sentence_dict[sentence]["verified"]
                }
        else:
            if (sentence not in black_list):
                sentence_dict[sentence] = { 
                    "frame_to_last_match": 0, 
                    "duplicate_list": [0],
                    "verified": False
                }

    out_list = []

    remove_key_list = []

    for key in sentence_dict.keys():
        # check if matched
        if sentence_dict[key]["frame_to_last_match"] >= sequence_frame:
            remove_key_list.append(key)
        else:
            # if sentence_dict[key]["duplicate_count"] == verify_frame and sentence_dict[key]["verified"] == False:
            if len(sentence_dict[key]["duplicate_list"]) == verify_frame and sentence_dict[key]["verified"] == False:
                sentence_dict[key]["verified"] = True
                out_list.append(key)

    for remove_key in remove_key_list:
        del sentence_dict[remove_key]

    return out_list

def load_subtitles_from_file(file : str, 
                             outfile : str, 
                             black_list : list, 
                             verify_frame : int = verify_frame, 
                             sequence_frame : int = sequence_frame,
                             ) -> str:
    f = open(file, 'r')
    frame_text_list = f.read().split("\n")
    sentence_dict = {}
    out_sentence_list = []
    for frame_text in frame_text_list:
        new_sentence_list = get_frame_detail(frame_text, 
                                             sentence_dict, 
                                             verify_frame, 
                                             sequence_frame, 
                                             black_list=black_list)
        out_sentence_list.extend(new_sentence_list)

    out_text = f"{' '.join(out_sentence_list)}".lower()

    with open(outfile, 'w') as f:
        f.write(out_text)

    return out_text

if __name__ == "__main__":
    load_subtitles_from_file(sys.argv[1], sys.argv[2], [], 7, 12)