import random
import datetime
import json
from pyecharts.charts import Calendar
from pyecharts import options as opts
import streamlit as st
import pandas as pd
import numpy as np
import os
import altair as alt
import abc


def read_spotify_data():
    directory = (
        "/Users/jannisgehring/VSCode/wrapped-extended/data/spotify_streaming_history"
    )
    dfs = []
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if not (os.path.isfile(file) and file.endswith(".json")):
            continue
        with open(file, "r") as f:
            print(file)
            json_data = json.load(f)
            dfs.append(pd.DataFrame.from_dict(json_data))
    df = pd.concat(dfs)
    return df.reset_index(drop=True)


def main():
    st.set_page_config(
        page_title="Spotify Data", page_icon=":chart_with_upwards_trend:", layout="wide"
    )
    st.title("Spotify Data")

    df = read_spotify_data()


    st.components.v1.html(html_content, height=600)




if __name__ == "__main__":
    main()
