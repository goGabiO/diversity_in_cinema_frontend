import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from diversity_in_cinema_frontend.params import *

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



def only_men_screentime_bar(df):
    x = [df['only_men'].values[0], (100 - df['only_men'].values[0])]
    names = ['Only men present', 'Both men and women present']

    fig = px.bar(df,
                 x=names,
                 y=x,
                 labels={
                     "x": "",
                     "y": "Screentime [%]"
                 },
                 color=names)

    return fig



def only_women_screentime_bar(df):
    x = [df['only_women'].values[0], (100 - df['only_women'].values[0])]
    names = ['Only women present', 'Both women and men present']

    fig = px.bar(df,
                 x=names,
                 y=x,
                 labels={
                     "x": "",
                     "y": "Screentime [%]"
                 },
                 color=names)
    return fig


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

######### Moe's Plots ###########


def plot_gender_timeline(df, plot_type="bar", step=5):

    # group by decade
    df_grouped = df.groupby(
        pd.cut(df["year"],
               pd.date_range('1920', '2030', freq=f'{step}YS'),
               right=False)).mean()

    new_df = pd.DataFrame({
        'year':
        pd.date_range(start='01-01-1920', end='01-01-2030', freq=f'{step}YS')
    })
    df_stats_total = new_df.merge(df, on='year', how='left')
    df_grouped = df_stats_total.groupby(
        pd.Grouper(key='year', freq=f'{step}YS')).mean()
    df_grouped = df_grouped.dropna()

    if plot_type == "bar":
        # plot gender over time
        fig = px.bar(
            df_grouped,
            x=df_grouped.index,
            y=['man_screentime', 'woman_screentime', 'only_men', 'only_women'],
            barmode="overlay",
            labels={
                "value": "Screentime [%]",
                "year": ""
            })
        fig.show()

    elif plot_type == "line":
        fig = px.line(
            df_grouped,
            x=df_grouped.index,
            y=['man_screentime', 'woman_screentime', 'only_men', 'only_women'],
            labels={
                "value": "Screentime [%]",
                "year": ""
            })

    return fig



def plot_race_timeline(total_stats_df, plot_type="bar", step=5):

    # group by decade
    df_grouped = total_stats_df.groupby(
        pd.cut(total_stats_df["year"],
               pd.date_range('1920', '2030', freq=f'{step}YS'),
               right=False)).mean()

    new_df = pd.DataFrame({
        'year':
        pd.date_range(start='01-01-1920', end='01-01-2030', freq=f'{step}YS')
    })
    df_stats_total = new_df.merge(total_stats_df, on='year', how='left')
    df_grouped = df_stats_total.groupby(
        pd.Grouper(key='year', freq=f'{step}YS')).mean()
    df_grouped = df_grouped.dropna()

    if plot_type == "bar":
        # plot gender over time
        fig = px.bar(df_grouped,
                     x=df_grouped.index,
                     y=[
                         'asian_screentime', 'black_screentime',
                         'indian_screentime', 'latino_hispanic_screentime',
                         'middle_eastern_screentime', 'white_screentime',
                         'women_of_color'
                     ],
                     barmode="overlay",
                     labels={
                         "value": "Screentime [%]",
                         "year": ""
                     })

    elif plot_type == "line":
        fig = px.line(df_grouped,
                      x=df_grouped.index,
                      y=[
                          'asian_screentime', 'black_screentime',
                          'indian_screentime', 'latino_hispanic_screentime',
                          'middle_eastern_screentime', 'white_screentime',
                          'women_of_color'
                      ],
                      labels={
                          "value": "Screentime [%]",
                          "year": ""
                      })
    return fig


def race_screentime_bar(df):
    """
    Input: Original movie overview dataframe
    """

    one_movie_race = df[[
        'asian_screentime', 'black_screentime', 'indian_screentime',
        'latino_hispanic_screentime', 'middle_eastern_screentime',
        'white_screentime'
    ]]

    one_movie_race = one_movie_race.T

    fig = px.bar(one_movie_race,
                 x=one_movie_race.index,
                 y=one_movie_race[0],
                 labels={
                     "index": "",
                     "0": "Screentime [%]"
                 },
                 color=one_movie_race.index)
    return fig


def man_woman_screentime_bar(df):
    """
    Input: Original movie overview dataframe
    """

    one_movie_gender = df[["man_screentime", "woman_screentime"]]
    one_movie_gender = one_movie_gender.T

    fig = px.bar(one_movie_gender,
                 x=one_movie_gender.index,
                 y=one_movie_gender[0],
                 labels={
                     "index": "",
                     "0": "Screentime [%]"
                 },
                 color=one_movie_gender.index)

    return fig

def run_time(movie_title, by="gender"):

    movie_title = movie_title.replace("_", " ").replace(".csv", "") + ".csv"

    df = pd.read_csv(
    f"gs://{BUCKET_NAME}/output/{movie_title}", index_col=None,)

    # add seconds column -> 1 frame = 0.5 seconds
    df["seconds"] = df["frame_number"] / 2

    # add minutes
    df["minutes"] = round((df["seconds"] / 60))

    df_grouped = df.groupby(["minutes", by], as_index=False).count()


    fig = px.scatter(df_grouped,
                     x="minutes",
                     y="face_id",
                     size="face_id",
                     color=by,
                     size_max=60,
                     labels={"face_id": "Number of detected faces", "minutes": "Film length [minutes]"},
                    title=f"Distribution of {by.capitalize()} Over Film Run-time")
    return fig



def run_time_distribution(movie_title, by="gender"):

    movie_title = movie_title.replace("_", " ").replace(".csv", "") + ".csv"

    df = pd.read_csv(
    f"gs://{BUCKET_NAME}/output/{movie_title}", index_col=None,)

    # add seconds column -> 1 frame = 0.5 seconds
    df["seconds"] = df["frame_number"] / 2

    # add minutes
    df["minutes"] = round((df["seconds"] / 60))

    df_grouped = df.groupby(["minutes", by], as_index=False).count()


    fig = px.scatter(df_grouped,
                     x="minutes",
                     y="face_id",
                     size="face_id",
                     color=by,
                     size_max=60,
                     labels={"face_id": "Number of detected faces",
                             "minutes": "Film length [minutes]"},
                     title=f"Distribution of {by.capitalize()} Over Film Run-time")

    return fig

def dashboard_gender(movie_title, movie_stats_df):

    # grab csvs

    movie_name = movie_title.replace(" ", "_")
    file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/statistics'
    df = pd.read_csv(file_name)

    # Create figures in Express
    figure1 = run_time(movie_name, by="gender")
    figure2 = only_women_screentime_bar(movie_stats_df)
    figure3 = man_woman_screentime_bar(df)
    figure4 = only_men_screentime_bar(df)

    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces

    figure1_traces = []
    figure2_traces = []
    figure3_traces = []
    figure4_traces = []

    for trace in range(len(figure1["data"])):
        figure1_traces.append(figure1["data"][trace])

    for trace in range(len(figure2["data"])):
        figure2_traces.append(figure2["data"][trace])

    for trace in range(len(figure3["data"])):
        figure3_traces.append(figure3["data"][trace])

    for trace in range(len(figure4["data"])):
        figure4_traces.append(figure4["data"][trace])

    #Create a 1x2 subplot
    this_figure = sp.make_subplots(rows=2,
                                   cols=3,
                                   specs=[[{
                                       'colspan': 3
                                   }, None, None], [{}, {}, {}]])

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in figure1_traces:
        this_figure.append_trace(traces, row=1, col=1)

    for traces in figure2_traces:
        this_figure.append_trace(traces, row=2, col=2)

    for traces in figure3_traces:
        this_figure.append_trace(traces, row=2, col=1)

    for traces in figure4_traces:
        this_figure.append_trace(traces, row=2, col=3)

    this_figure.update_layout(height=900, width=1100)
    this_figure.update_layout(uniformtext_minsize=15)

    this_figure.update_layout(
        title_text=f"{movie_name.replace('_', ' ')} - Gender Statistics")
    # Add annotations in the center of the donut pies

    #the subplot as shown in the above image
    return this_figure


def dashboard_race(movie_stats_df):

    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{
                            "type": "domain"
                        }, {
                            "type": "domain"
                        }]])

    fig1 = r_screentime_donut(movie_stats_df)
    fig2 = woc_screentime_donut(movie_stats_df)

    fig.add_trace(fig1, row=1, col=1)

    fig.add_trace(fig2, row=1, col=2)

    return fig


def overall_gender_dash(total_stats_df):

    total_stats_df.sort_values(by="woman_screentime",
                               ascending=False,
                               inplace=True)

    y_saving = total_stats_df["woman_screentime"].values

    x2 = total_stats_df["revenue"].values

    x1 = total_stats_df["title"].values
    y_net_worth = total_stats_df["total_Woman"].values

    # Creating two subplots
    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{}, {}]],
                        shared_xaxes=True,
                        shared_yaxes=False,
                        vertical_spacing=0.02,
                        horizontal_spacing=0.1)

    fig.append_trace(
        go.Bar(
            x=y_saving,
            y=x1,
            marker=dict(
                color='rgb(24,116,205)',
                line=dict(color='rgb(0,191,255)', width=1),
            ),
            name='Screentime percentage of woman per movie',
            orientation='h',
        ), 1, 1)

    fig.append_trace(
        go.Scatter(
            x=y_net_worth,
            y=x2,
            mode='markers',
            hovertext=total_stats_df["title"],
            marker=dict(color='rgb(255,185,15)'),
            name='Number of women on screen VS. movie revenue',
        ), 1, 2)

    fig.update_layout(
        title='Women screentime and movie revenue',
        yaxis=dict(showgrid=False,
                   showline=False,
                   showticklabels=True,
                   domain=[0, 0.85]),
        yaxis2=dict(showgrid=False,
                    showline=True,
                    showticklabels=True,
                    domain=[0, 0.85]),
        xaxis=dict(zeroline=False,
                   showline=True,
                   showticklabels=True,
                   showgrid=True,
                   domain=[0, 0.42]),
        xaxis2=dict(zeroline=False,
                    showline=True,
                    showticklabels=True,
                    showgrid=True,
                    domain=[0.47, 1]),
        height=600,
        width=1500,
        legend=dict(x=0.029, y=1.038, font_size=15),
        margin=dict(l=100, r=20, t=70, b=70),
    )

    fig.update_layout(shapes=[
        dict(
            type="line",
            xref='paper',
            yref='paper',
            x0=0.433,
            y0=0.89,
            x1=0.433,
            y1=0.002,
            line=dict(color="black", width=3),
        ),
    ], )

    return fig


import plotly.graph_objects as go
import plotly.subplots as sp


def overall_race_dash(total_stats_df):

    # Create figures in Express
    figure2 = plot_race_timeline(total_stats_df, plot_type="bar", step=10)

    figure1 = px.scatter(total_stats_df,
                         x="non_white_count",
                         y="revenue",
                         hover_name="title",
                         labels={
                             "revenue": "Movie Revenue [US$]",
                             "non_white_count": "POC on screen count"
                         },
                         color_discrete_sequence=['rgb(255,185,15)'])

    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces

    figure1_traces = []
    figure2_traces = []

    for trace in range(len(figure1["data"])):
        figure1_traces.append(figure1["data"][trace])

    for trace in range(len(figure2["data"])):
        figure2_traces.append(figure2["data"][trace])

    #Create a 1x2 subplot
    this_figure = sp.make_subplots(rows=1, cols=2, specs=[[{}, {}]])

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in figure1_traces:
        this_figure.append_trace(traces, row=1, col=1)

    for traces in figure2_traces:
        this_figure.append_trace(traces, row=1, col=2)

    this_figure.update_layout(height=500, width=1100)
    this_figure.update_layout(uniformtext_minsize=15)

    this_figure.update_layout(
        title_text=
        f"Number of POC VS. revenue                                  Screenttime percentage evoultion"
    )
    # Add annotations in the center of the donut pies

    return this_figure
