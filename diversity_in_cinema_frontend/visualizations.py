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


######### Moe's Plots ###########

def plot_race_timeline(total_stats_df, plot_type="line", step=5):

    # group by decade
    total_stats_df['year'] = pd.to_datetime(total_stats_df['year'])
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

    fig.update_layout(title_text='Screentime Distribution Timeseries - *POC',
                          font=dict(size=18))

    fig.update_layout(autosize=False,
                      width=1315,
                      height=500,
                      yaxis=dict(
                          title_text="Screentime [%]",
                          titlefont=dict(size=18),
                      ))
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
                     title=f"Distribution of {by.capitalize()} Over Film Runtime")

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

    x1 = total_stats_df["year"].values
    y_net_worth = total_stats_df["total_Woman"].values

    # Creating two subplots
    fig = make_subplots(rows=1,
                        cols=4,
                        specs=[[{}, {}, {}, {}]],
                        column_widths=[25, 5, 30, 2])

    fig.append_trace(
        go.Bar(
            x=y_saving,
            y=x1,
            marker=dict(
                color='rgb(24,116,205)',
                line=dict(color='rgb(0,191,255)', width=0.5),
            ),
            name='Screentime percentage of woman per movie',
            orientation='h',
        ), 1, 3)


    fig.append_trace(
        go.Scatter(
            x=y_net_worth,
            y=x2,
            mode='markers',
            hovertext=total_stats_df["title"],
            marker=dict(color='rgb(255,185,15)'),
            name='Number of Women on Screen vs. Movie Revenue',
        ), 1, 1)

    fig.update_layout(
        title='Women Screentime and Movie Revenue',
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

    fig.update_layout(font_size=15)


    # y axis labels
    fig['layout'][f'yaxis{1}'].update(title=f'Movie revenue [US$]',
                                      title_font_size=19)

    # x axis labels
    fig['layout'][f'xaxis{1}'].update(
        title=f'Cumulated number of women on screen', title_font_size=19)
    fig['layout'][f'xaxis{3}'].update(
        title=f'Percantage of screentime - Women', title_font_size=19)



    return fig


import plotly.graph_objects as go
import plotly.subplots as sp


def overall_race_dash(total_stats_df):

    total_stats_df["non_white_count"] = total_stats_df[[
        'total_asian', 'total_black', 'total_indian', 'total_latino_hispanic',
        'total_middle_eastern'
    ]].sum(axis=1)

    total_stats_df["non_white_count_percent"] = total_stats_df[
        "non_white_count"] / total_stats_df["total_white"]

    # Create figures in Express
    figure2 = plot_race_timeline(total_stats_df, plot_type="line", step=10)

    figure1 = px.scatter(total_stats_df,
                         x="non_white_count",
                         y="revenue",
                         hover_name="title",
                         width=800, height=400,
                         labels={
                             "revenue": "Movie Revenue [US$]",
                             "non_white_count": "*POC on screen count"
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
    this_figure = sp.make_subplots(rows=1,
                                   cols=3,
                                   specs=[[{}, {}, {}]],
                                   column_widths=[20,1,20])

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in figure1_traces:
        this_figure.append_trace(traces, row=1, col=1)

    for traces in figure2_traces:
        this_figure.append_trace(traces, row=1, col=3)

    this_figure.update_layout(height=500, width=1200)
    this_figure.update_layout(uniformtext_minsize=30)

    this_figure.update_layout(
        title_text=
        f"Number of *POC vs. Revenue  |  Screentime Percentage Evolution",
        title_font_size=24)

    # # x axis labels
    # fig['layout'][f'xaxis{1}'].update(
    #     title=f'Cumulated number of women on screen', title_font_size=19)
    # fig['layout'][f'xaxis{3}'].update(
    #     title=f'Percantage of Screentime - Women', title_font_size=19)

    this_figure['layout'][f'xaxis{1}'].update(title=f'Title {2}',
                                              title_font_size=30)
    this_figure['layout'][f'xaxis{3}'].update(title=f'Title {3}')
    # Add annotations in the center of the donut pies

    return this_figure



################### NEW PLOT #####################
def women_revenue_scatter(total_stats_df):

    total_stats_df.sort_values(by="woman_screentime",
                               ascending=False,
                               inplace=True)

    y = total_stats_df["revenue"].values
    x = total_stats_df["total_Woman"].values

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=x,
                   y=y,
                   mode='markers',
                   hovertext=total_stats_df["title"],
                   marker=dict(color='rgb(255,185,15)')))

    fig.update_layout(title_text='Number of Women on Screen vs. Movie Revenue',
                      font=dict(size=18))

    fig.update_layout(autosize=True,
                      width=1100,
                      height=500,
                      yaxis=dict(
                          title_text="Movie revenue [US$]",
                          titlefont=dict(size=18),
                      ),
                      xaxis=dict(
                          title_text="Cumulated number of women on screen",
                          titlefont=dict(size=18),
                      ))

    return fig


def women_movie_percentage(total_stats_df):

    total_stats_df.sort_values(by="woman_screentime",
                               ascending=False,
                               inplace=True)

    y = total_stats_df["title"].values
    x = total_stats_df["woman_screentime"].values

    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=x,
               y=y,
               hovertext=total_stats_df["revenue"],
               orientation='h',
               marker=dict(color='rgb(24,116,205)')))

    fig.update_layout(title_text='Screentime Percentage of Women in Movies',
                      font=dict(size=15))

    fig.update_layout(autosize=True,
                      width=1000,
                      height=500,
                      xaxis=dict(
                          title_text="Screentime [%]",
                          titlefont=dict(size=18),
                      ))

    return fig


def plot_gender_timeline(total_stats_df, plot_type="line", step=5):

    # group by decade
    total_stats_df['year'] = pd.to_datetime(total_stats_df['year'])
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
        fig = px.bar(
            df_grouped,
            x=df_grouped.index,
            y=['man_screentime', 'woman_screentime', 'only_men', 'only_women'],

            labels={
                "value": "Screentime [%]",
                "year": ""
            })

    elif plot_type == "line":
        fig = px.line(
            df_grouped,
            x=df_grouped.index,
            y=['man_screentime', 'woman_screentime', 'only_men', 'only_women'],
            labels={
                "value": "Screentime [%]",
                "year": "",
                "variable":""
            })

    fig.update_layout(
            title_text='Screentime Distribution Timeseries - Gender',
            font=dict(size=18))

    fig.update_layout(autosize=False,
                      width=1250,
                      height=500,
                      yaxis=dict(
                          title_text="Screentime [%]",
                          titlefont=dict(size=18),
                      ))

    return fig


def poc_scatter_revenue(total_stats_df):

    total_stats_df["non_white_count"] = total_stats_df[[
        'total_asian', 'total_black', 'total_indian', 'total_latino_hispanic',
        'total_middle_eastern'
    ]].sum(axis=1)

    total_stats_df["non_white_count_percent"] = total_stats_df[
        "non_white_count"] / total_stats_df["total_white"]


    fig = px.scatter(total_stats_df,
                         x="non_white_count",
                         y="revenue",
                         hover_name="title",
                         width=800,
                         height=400,
                         labels={
                             "revenue": "Movie Revenue [US$]",
                             "non_white_count": "*POC on screen count"
                         },
                         color_discrete_sequence=['rgb(255,185,15)'])

    fig.update_layout(title_text='Cumulated number of *POC on screen',
                      font=dict(size=18))

    fig.update_layout(autosize=False,
                      width=1120,
                      height=500,
                      yaxis=dict(
                          title_text="Movie Revenue [US$]",
                          titlefont=dict(size=18),
                      ))

    return fig


def run_time(movie_title, by="gender"):

    movie_title = movie_title.replace("_", " ").replace(".csv", "") + ".csv"

    df = pd.read_csv(
        f"gs://{BUCKET_NAME}/output/{movie_title}",
        index_col=None,
    )

    # add seconds column -> 1 frame = 0.5 seconds
    df["seconds"] = df["frame_number"] / 2

    # add minutes
    df["minutes"] = round((df["seconds"] / 60))

    df_grouped = df.groupby(["minutes", by], as_index=False).count()

    fig = px.scatter(
        df_grouped,
        x="minutes",
        y="face_id",
        size="face_id",
        color=by,
        width=1200, height=600,
        size_max=30,
        labels={
            "face_id": "Number of detected faces",
            "minutes": "Film length [minutes]"
        },
        title=f"Distribution of {by.capitalize()} Over Film Runtime")

    fig.update_layout(font=dict(size=20))

    fig.update_layout(autosize=False,
                      width=1000,
                      height=500,
                      yaxis=dict(
                          titlefont=dict(size=20)))


    return fig


def only_women_screentime_donut(df):
    x = [
        df['only_women'].values[0], (df['only_men'].values[0]),
        (100 - (df['only_men'].values[0] + df['only_women'].values[0]))
    ]
    names = ['Frames with only women', 'Frames with only Men', 'Frames with both women and men']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.4)
    go_fig.add_trace(do_fig)

    go_fig.update_layout(autosize=False,
                         width=1195,
                         height=600)

    go_fig.update_layout(title_text='Proportion of Frames Containing Only Men or Only Women',
                         font=dict(size=20))

    return go_fig


def man_woman_screentime_bar(df):
    """
    Input: Original movie overview dataframe
    """

    one_movie_gender = df[["man_screentime", "woman_screentime"]].copy()
    one_movie_gender.rename({"man_screentime": "Men", "woman_screentime": "Women"}, axis=1, inplace=True)
    one_movie_gender = one_movie_gender.T


    fig = px.bar(one_movie_gender,
                 x=one_movie_gender.index,
                 y=one_movie_gender[0],
                 labels={
                     "index": "",
                     "0": "Frames [%]"
                 },
                 color=one_movie_gender.index)

    fig.update_layout(autosize=False, width=1000, height=500)

    fig.update_layout(
        title_text='Distribution of Men and Women Over All Movie Frames',
        font=dict(size=20))

    return fig



def r_screentime_donut(df):
    x = [
        df['asian_screentime'].values[0], df['black_screentime'].values[0],
        df['indian_screentime'].values[0],
        df['latino_hispanic_screentime'].values[0],
        df['middle_eastern_screentime'].values[0],
        df['white_screentime'].values[0]
    ]
    names = [
        'Asian', 'Black', 'Indian', 'Latino Hispanic', 'Middle Eastern',
        'White'
    ]

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)

    go_fig.update_layout(autosize=False, width=1195, height=600)

    go_fig.update_layout(
        title_text='Distribution of Race',
        font=dict(size=20))

    return go_fig


def woc_screentime_donut(df):
    x = [
        df['women_of_color'].values[0], (100 - df['women_of_color'].values[0])
    ]
    names = ['Women of color', 'White women']

    go_fig = go.Figure()

    do_fig = go.Pie(labels=names, values=x, hole=0.5)
    go_fig.add_trace(do_fig)

    go_fig.update_layout(autosize=False, width=1195, height=600)

    go_fig.update_layout(
        title_text='Proportion of Frames Featuring Women of Color',
        font=dict(size=20))

    return go_fig
