import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import time
from datetime import datetime


#df = pd.read_pickle("summary.pkl")


lista = [ x.split(".")[0] for x in os.listdir("./data/PM/")]
genre = st.selectbox("What's your favorite movie genre", lista)


df = pd.read_pickle("./data/PM/"+genre+".pkl")
df = df.drop(["index"], axis =1)
df["sender_name"] = df["sender_name"].astype('object')
df["type"] = df["type"].astype('object')
df["Reaction"] = df["Reaction"].astype('object')
df["Actor"] = df["Actor"].astype('object')

#df["day"] = df["timestamp_ms"].apply(lambda x: datetime.fromtimestamp(x))

temp = df.groupby('Actor')["Reaction"].value_counts().rename("Total").reset_index()
st.write(df.groupby('Actor')["Reaction"].value_counts().unstack())
fig = px.bar(temp, x="Reaction", y="Total", color="Actor", barmode="group")
st.plotly_chart(fig)

cols = []
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
from_d = st.date_input("From")#.strftime('%d-%m-%y')
to_d = st.date_input("To")#.strftime('%d-%m-%y')
#print(from_d,to_d)
st.write(df[st_ms])
#st.write(df.loc[((from_d <= df["day"]) & (df["day"] <= to_d))][st_ms])



fun = st.radio("Level of analysis",("Month","Quarter","Year"))
if fun == "Month":
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%m', time.localtime(x/1000)))
    pass
elif fun == "Quarter":
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y-%m', time.localtime(x/1000)))
else:
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y', time.localtime(x/1000)))

g_c_messages = df.groupby(['cal', "sender_name"]).count()["timestamp_ms"].unstack()
g_c_messages["Total"] = g_c_messages.sum(axis=1)
g_c_messages["Total_C"] = g_c_messages["Total"].cumsum()
st.write(g_c_messages)
st.line_chart(g_c_messages["Total_C"])

#print(df)
#st.write(df.info())
