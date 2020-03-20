import numpy as np
import pandas as pd
import emojis
import emoji
import collections
import streamlit as st


def emoji_category(x):

    try:
        return (emojis.db.get_emoji_by_code(x))[3]
    except:
        return "Misc"


def test():
    st.write("dsadasdasdasda")

def string_enc(x):
    """ Fixing a string's coding"""
    try:
        return x.encode('latin').decode('utf-8')

    except:

        return x


def clean_columns(chat_data,kind,new_name):

    #chat_data.loc[chat_data[kind].isna() == False,kind] = True
    #chat_data.loc[chat_data[kind] == True, "type"] = new_name
    chat_data.loc[chat_data[kind].isna() == False, "type"] = new_name
    chat_data[kind] = chat_data[kind].fillna(False)

    return chat_data


def extract_emojis(str):

    try:
        return ' '.join(c for c in str if c in emoji.UNICODE_EMOJI).split(" ")
    except:
        return []


def extract_emojis_from_thread(df):

    df["sender_name"] = df["sender_name"].apply(string_enc)
    df["content"] = df["content"].apply(string_enc)
    df["Emoji"] = df["content"].apply(lambda x: extract_emojis(x))
    df = df[["sender_name","timestamp_ms","Emoji"]]
    df = df[df["Emoji"].apply(lambda x: any(x))]
    return df


def unlistify(df, column):


    """
    https://github.com/pandas-dev/pandas/issues/10511
    """

    matches = [i for i, n in enumerate(df.columns)
               if n == column]

    if len(matches) == 0:
        raise Exception('Failed to find column named ' + column + '!')
    if len(matches) > 1:
        raise Exception('More than one column named ' + column + '!')

    col_idx = matches[0]

    # Helper function to expand and repeat the column col_idx
    def fnc(d):
        row = list(d.values[0])
        bef = row[:col_idx]
        aft = row[col_idx + 1:]
        col = row[col_idx]
        z = [bef + [c] + aft for c in col]
        return pd.DataFrame(z)

    col_idx += len(df.index.shape)  # Since we will push reset the index
    index_names = list(df.index.names)
    column_names = list(index_names) + list(df.columns)
    return (df
            .reset_index()
            .groupby(level=0, as_index=0)
            .apply(fnc)
            .rename(columns=lambda i: column_names[i])
            .set_index(index_names)
            )
