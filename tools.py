import numpy as np

def string_enc(x):
    """ Fixing a string's coding"""
    try:
        return x.encode('latin').decode('utf-8')
    except:
        #print("Error in encoding {}".format(x))
        pass


def clean_columns(chat_data,kind,new_name):

    #chat_data.loc[chat_data[kind].isna() == False,kind] = True
    #chat_data.loc[chat_data[kind] == True, "type"] = new_name
    chat_data.loc[chat_data[kind].isna() == False, "type"] = new_name
    chat_data[kind] = chat_data[kind].fillna(False)

    return chat_data