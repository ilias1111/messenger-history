import os
import glob
import json
import tools
import re
import pandas as pd
import data_manipulation


def name_exporter(folder_loc):
    """Gives us the name of the chat participant

    Parameters
    ----------
    file_loc : str
        The file location of the json

    Returns
    -------
    name
        The name of the chat participant
    """

    with open(folder_loc + "/message_1.json", "r", encoding='utf-8') as file:
        raw_data = json.load(file)

        if len(raw_data["participants"]) == 2:
            if raw_data["participants"][0]["name"] == "Facebook User":
                name = "Facebook_User_" + raw_data["thread_path"].split("_")[1]
            else:
                name = tools.string_enc(raw_data["participants"][0]["name"])
        else:
            name = tools.string_enc(raw_data["title"])

    return re.sub('[<>:"/|\?*]+', '', name)


def json_to_dataframe(file_loc):
    """Transforms json data to dataframe

    Parameters
    ----------
    file_loc : str
        The file location of the json

    Returns
    -------
    dataframe
        A dataframe of the chat data included in the json.
    """

    with open(file_loc, "r", encoding='utf-8') as file:
        raw_data = json.load(file)
        df = pd.json_normalize(raw_data["messages"])
    return df


def chat_to_dataframe(folder_loc):
    """Transforms raw chat data to a final dataframe by iterating all the json and concatenating the dataframes.

    Parameters
    ----------
    folder_loc : str
        The folder location of the json(s)

    Returns
    -------
    dataframe
        A dataframe of the chat data included in the json.
    """

    df = pd.DataFrame()
    list_of_jsons = glob.glob(folder_loc + "/*.json")
    for i in list_of_jsons:
        df = pd.concat([df, json_to_dataframe(i)])
    return df


def json_g_check(folder_loc):
    """ Checking if a thread is group chat"""

    with open(folder_loc + "/message_1.json", "r", encoding='utf-8') as file:
        raw_data = json.load(file)
        if raw_data["thread_type"] == "Regular":
            return False
        elif raw_data["thread_type"] == "RegularGroup":
            return True


def inbox_to_processed_data():
    inbox = "./user data/messages/inbox/"
    list_of_chats = os.listdir(inbox)
    for chat in list_of_chats:
        name = name_exporter(inbox + chat)
        df = chat_to_dataframe(inbox + chat)
        df = df.reset_index()
        df = data_manipulation.clean_dataframe(name, df)
        if not json_g_check(inbox + chat):
            df.to_pickle("./data/PM/{}.pkl".format(name))
        else:
            df.to_pickle("./data/GM/{}.pkl".format(name))

    return 0


inbox_to_processed_data()
