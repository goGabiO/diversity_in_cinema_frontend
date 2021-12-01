import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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



def plot_race_timeline(df, plot_type="bar", step=5):

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
        fig.show()

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
