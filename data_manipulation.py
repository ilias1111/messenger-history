import pandas as pd
import tools
import os
import numpy as np

def clean_dataframe(name, chat_data):

    current_col_names = ["photos", "videos", "sticker.uri", "files", "audio_files", "gifs"]
    formated_col_names = ["Photo", "Video", "Sticker", "File", "Audio", "GIF"]

    for i in range(0, len(current_col_names)):
        try:
            tools.clean_columns(chat_data, current_col_names[i], formated_col_names[i])
        except KeyError:
            chat_data[current_col_names[i]] = pd.Series([False for x in range(len(chat_data.index))])

    try:
        chat_data["sender_name"] = chat_data["sender_name"].apply(tools.string_enc)
        chat_data["content"] = chat_data["content"].apply(tools.string_enc)

    except:
        print("Error in " + str(name) + " at encoding")
    try:
        chat_data["Reaction"] = chat_data.loc[chat_data["reactions"].isna() == False, "reactions"].apply(lambda x: tools.string_enc(x[0]["reaction"]))
        chat_data["Reaction"] = chat_data["Reaction"].astype('category')
    except:
        pass

    try:
        chat_data["Actor"] = chat_data.loc[chat_data["reactions"].isna() == False, "reactions"].apply(lambda x: tools.string_enc(x[0]["actor"]))
        chat_data["Actor"] = chat_data["Actor"].astype('category')
    except:
        pass

    chat_data["type"] = chat_data["type"].astype('category')
    chat_data["sender_name"] = chat_data["sender_name"].astype('category')

    chat_data.drop(columns=["reactions"], inplace=True)

    return chat_data



def summary_table():

    summary = pd.DataFrame(columns=['Name'])

    chat_list = os.listdir("./data/PM/")

    for file in chat_list:

        chat_data = pd.read_pickle("./data/PM/" + file)
        name = file.split(".")[0]


        first_date = abs(
            (pd.Timestamp(chat_data["timestamp_ms"].min(), unit="ms") - pd.Timestamp.now()) / np.timedelta64(1, 'D'))
        last_date = abs(
            (pd.Timestamp(chat_data["timestamp_ms"].max(), unit="ms") - pd.Timestamp.now()) / np.timedelta64(1, 'D'))

        total = int(chat_data["type"].count())
        sent = int(len(chat_data["sender_name"] != name))
        received = int(len(chat_data["sender_name"] == name))

        try:
            call = chat_data["call_duration"].sum()
        except:
            call = 0



        # Categories

        generic = int(len(chat_data[chat_data["type"] == "Generic"]))
        sticker = int(len(chat_data[chat_data["type"] == "Sticker"]))
        photos = int(len(chat_data[chat_data["type"] == "Photo"]))
        share = int(len(chat_data[chat_data["type"] == "Share"]))
        audio = int(len(chat_data[chat_data["type"] == "Audio"]))
        gif = int(len(chat_data[chat_data["type"] == "GIF"]))
        video = int(len(chat_data[chat_data["type"] == "Video"]))
        file = int(len(chat_data[chat_data["type"] == "File"]))

        summary = summary.append({'Name': name,
                                  'Total': total,
                                  'Sent' : sent,
                                  'Received' : received,
                                  "Generic" : generic,
                                  "Photos" : photos,
                                  "Sticker" : sticker,
                                  "Share" : share,
                                  "Audio" : audio,
                                  "Gifs" : gif,
                                  "Video" : video,
                                  "File" : file,
                                  "Call Duration" : call,
                                  'First_Contact': first_date,
                                  'Last_Contact': last_date
                                  }, ignore_index="False")

    return summary


df = summary_table()
df.to_pickle("summary.pkl")