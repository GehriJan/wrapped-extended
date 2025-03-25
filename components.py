import numpy as np
import pandas as pd
import abc
import random
import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar


class DashboardComponent(abc.ABC):
    def __init__(self):
        pass

    def render(self, df):
        data = self.preprocess(df)
        html_content = self.get_html_content(data)

    @abc.abstractmethod
    def preprocess(self, df: pd.DataFrame):
        pass

    @abc.abstractmethod
    def get_html_content(self, data):
        pass

class Heatmap(DashboardComponent):

    def preprocess(self, df):
        return (
            pd.to_datetime(df["ts"])
            .dt.tz_convert("Europe/Berlin")
            .dt.floor("D")
            [(df["ts"] >= "2024-01-01") & ("2025-01-01" > df["ts"])]
            .dt.date.value_counts()
            .sort_index()
        )

    def get_html_content(self, data):
        calendar = (
            Calendar()
            .add(
                "Heatmap",
                list(data.items()),
                calendar_opts=opts.CalendarOpts(
                    range_=[str(data.index.min()), str(data.index.max())],
                    daylabel_opts=opts.CalendarDayLabelOpts(name_map="en"),
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Spotify Plays Heatmap"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=int(np.quantile(data.values, 0.8)),
                    min_=0,
                    orient="horizontal",
                    is_piecewise=False,
                    pos_top="10px",
                    pos_left="70%",
                    range_color=["#ffffff", "#d9f2d9", "#65d46e"],
                ),
            )
        )
        html_content = calendar.render_embed()
        return html_content