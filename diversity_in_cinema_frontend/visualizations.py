import pandas as pd
import plotly.graph_objects as go

def g_screentime_donut(df):
    x = [df['man_screentime'].values[0], df['woman_screentime'].values[0]]
    names = ['Man', 'Woman']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime per gender")
    return go_fig


def only_men_screentime_donut(df):
    x = [df['only_men'].values[0], (100-df['only_men'].values[0])]
    names = ['Only men present', 'Both men and women present']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime when only men are present")
    return go_fig


def only_women_screentime_donut(df):
    x = [df['only_women'].values[0], (100-df['only_women'].values[0])]
    names = ['Only women present', 'Both women and men present']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime when only women are present")
    return go_fig


def r_screentime_donut(df):
    x = [df['asian_screentime'].values[0],
        df['black_screentime'].values[0],
        df['indian_screentime'].values[0],
        df['latino_hispanic_screentime'].values[0],
        df['middle_eastern_screentime'].values[0],
        df['white_screentime'].values[0]
        ]
    names = ['Asian', 'Black', 'Indian', 'Latino Hispanic', 'Middle Eastern', 'White']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime per race")
    return go_fig


def woc_screentime_donut(df):
    x = [df['women_of_color'].values[0], (100-df['women_of_color'].values[0])]
    names = ['Women of color present', 'No women of color present']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)
    go_fig.add_annotation(text="Screentime when women of color are present")
    return go_fig
