import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime


#df = pd.read_pickle("summary.pkl")


lista = [ x.split(".")[0] for x in os.listdir("./data/PM/")]
genre = st.selectbox("What's your favorite movie genre", lista)


df = pd.read_pickle("./data/PM/"+genre+".pkl")
df = df.drop(["index"], axis =1)
df["sender_name"] = df["sender_name"].astype('object')
df["type"] = df["type"].astype('object')
df["reactions"] = df["reactions"].astype('object')
df["day"] = df["timestamp_ms"].apply(lambda x: datetime.fromtimestamp(x))

st.write(df.groupby('sender_name')["reactions"].value_counts())

cols = []
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
from_d = st.date_input("From")#.strftime('%d-%m-%y')
to_d = st.date_input("To")#.strftime('%d-%m-%y')
print(from_d,to_d)
st.write(df.loc[((from_d <= df["day"]) & (df["day"] <= to_d))][st_ms])



# fun = st.radio("Level of analysis",("Month","Quarter","Year"))
# if fun == "Month":
#     df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%m', time.localtime(x/1000)))
#     pass
# elif fun == "Quarter":
#     df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y-%m', time.localtime(x/1000)))
# else:
#     df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y', time.localtime(x/1000)))
#
# st.write(df.groupby(['cal', "sender_name"]).count())

#print(df)
#st.write(df.info())
