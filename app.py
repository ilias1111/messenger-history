import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
import time
import calendar
import help_functions

threads_list = [x.split(".")[0] for x in os.listdir("./data/PM/")]
thread = st.selectbox("Select the contact you want to analyze", threads_list)

df = pd.read_pickle("./data/PM/" + thread + ".pkl")
df = df.drop(["index"], axis=1)
df["sender_name"] = df["sender_name"].astype('object')
df["type"] = df["type"].astype('object')
df["Reaction"] = df["Reaction"].astype('object')
df["Actor"] = df["Actor"].astype('object')

df["day"] = df["timestamp_ms"].apply(lambda x: pd.Timestamp(x, unit="ms", tz="Europe/Athens"))

content_type_treemap = px.treemap(df.groupby("type").count()["timestamp_ms"].reset_index(), path=["type"], values="timestamp_ms")
st.plotly_chart(content_type_treemap)

reactions_dataframe = df.groupby('Actor')["Reaction"].value_counts().rename("Total").reset_index()
#st.write(df.groupby('Actor')["Reaction"].value_counts().unstack())
reaction_bar = px.bar(reactions_dataframe, x="Reaction", y="Total", color="Actor", barmode="group")
st.plotly_chart(reaction_bar)

st_ms = st.multiselect("Columns", df.columns.tolist(), default=[])
from_d = pd.Timestamp(st.date_input("From"), tz="Europe/Athens")
to_d = pd.Timestamp(st.date_input("To"), tz="Europe/Athens")
# print(from_d,to_d)
# st.write(df[st_ms])
st.write(df.loc[((from_d <= df["day"]) & (df["day"] <= to_d))][st_ms])

timeseries_mode = st.radio("Level of analysis", ("Week", "Month", "Year"))

if timeseries_mode == "Week":
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y-%W', time.localtime(x / 1000)))
elif timeseries_mode == "Month":
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y-%m', time.localtime(x / 1000)))
else:
    df["cal"] = df["timestamp_ms"].apply(lambda x: time.strftime('%Y', time.localtime(x / 1000)))

g_c_messages = df.groupby(['cal', "sender_name"]).count()["timestamp_ms"].unstack()
g_c_messages["Total"] = g_c_messages.sum(axis=1)
g_c_messages["Total_C"] = g_c_messages["Total"].cumsum()
st.write(g_c_messages)
st.line_chart(g_c_messages["Total_C"])

heatmap_mode = st.radio("Heatmap", ("Hour/Weekday", "Hour/Month", "Weekday/Month"))
tt = df
tt["Hour"] = tt["timestamp_ms"].apply(lambda x: time.strftime('%H', time.localtime(x / 1000)))
tt["Week"] = tt["timestamp_ms"].apply(lambda x: time.strftime('%a', time.localtime(x / 1000)))
tt["Month"] = tt["timestamp_ms"].apply(lambda x: time.strftime('%b', time.localtime(x / 1000)))

if heatmap_mode == "Hour/Weekday":
    heatmap = pd.DataFrame(columns=calendar.day_abbr[0:])
    heatmap = pd.concat([tt.groupby(["Hour", "Week"]).count()["timestamp_ms"].unstack(), heatmap]).fillna(0)
    messages_heatmap = go.Figure(data=go.Heatmap(z=heatmap[calendar.day_abbr[0:]],
                                    x=calendar.day_abbr[0:],
                                    y=[str(i) for i in range(0, 24)]))

elif heatmap_mode == "Hour/Month":
    heatmap = pd.DataFrame(columns=calendar.month_abbr[1:])
    heatmap = pd.concat([tt.groupby(["Hour", "Month"]).count()["timestamp_ms"].unstack(), heatmap]).fillna(0)
    messages_heatmap = go.Figure(data=go.Heatmap(z=heatmap[calendar.month_abbr[1:]],
                                    x=calendar.month_abbr[1:],
                                    y=[str(i) for i in range(0, 24)]))

else:
    heatmap = pd.DataFrame(columns=calendar.month_abbr[1:])
    heatmap = pd.concat([tt.groupby(["Week", "Month"]).count()["timestamp_ms"].unstack(), heatmap]).fillna(0)
    messages_heatmap = go.Figure(data=go.Heatmap(z=heatmap[calendar.month_abbr[1:]],
                                    x=calendar.month_abbr[1:],
                                    y=calendar.day_abbr[0:]))

st.write(messages_heatmap)
#st.write(heatmap)

em = help_functions.extract_emojis_from_thread(df)

# https://www.mikulskibartosz.name/how-to-split-a-list-inside-a-dataframe-cell-into-rows-in-pandas/

em = em.Emoji.apply(pd.Series) \
    .merge(em, right_index=True, left_index=True) \
    .drop(["Emoji"], axis=1) \
    .melt(id_vars=['sender_name', 'timestamp_ms'], value_name="Emoji") \
    .drop("variable", axis=1) \
    .dropna()


em = em.groupby(["sender_name", "Emoji"]).count()["timestamp_ms"].reset_index()
em["Category"] = em["Emoji"].apply(lambda x: help_functions.emoji_category(x))
st.write(em)

tree = px.treemap(em, path=["Category", "Emoji", "sender_name"], values="timestamp_ms")
st.write(tree)

