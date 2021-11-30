import pandas as pd
import plotly.graph_objects as go

def g_screentime_donut(df):
    x = df['gender_screentime']
    names = df['gender']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime per gender")
    return go_fig


def single_g_screentime_donut(df):
    x = df['only_1_screentime']
    names = df['gender']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime when only 1 gender is present")
    return go_fig


def r_screentime_donut(df):
    x = df['race_screentime']
    names = df['race']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime per race")
    return go_fig
