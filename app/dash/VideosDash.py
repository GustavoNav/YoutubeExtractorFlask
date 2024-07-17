from dash import Dash, html, dcc
import os
import humanize
import numpy as np
import pandas as pd
import plotly.express as px
from app.db.database_connector import DatabaseConnector
from app.db.database_repository import DatabaseRepository



def create_videos_dash(flask_app):
    dash_app = Dash(server = flask_app, name='Dashboard', url_base_pathname='/videos/') 

    return dash_app

def create_videos_layout():
    DatabaseConnector.connect()
    DatabaseRepository.select_videos_to_csv()

    file_path = os.path.abspath(os.path.join(__file__, '../../export/videos_data.csv'))
    df = pd.read_csv(file_path)

    df = df.dropna()

    df['video_date'] = pd.to_datetime(df['video_date'])

    df_grouped = df.groupby('video_date')['views'].mean().reset_index()

    df['duration_minutes'] = df['duration'].apply(convert_to_minutes)
    df['log_minutes'] = np.log(df['duration_minutes'].astype(float))

    df['log_views'] = np.log(df['views'].astype(float))
    df['log_likes'] = np.log(df['likes'].astype(float))
    df['log_comments'] = np.log(df['comments'].astype(float))

    mean_duration_minutes = df['duration_minutes'].mean()

    # Converter a média de minutos de volta para o formato hh:mm:ss
    mean_hours = int(mean_duration_minutes // 60)
    mean_minutes = int(mean_duration_minutes % 60)
    mean_seconds = int((mean_duration_minutes * 60) % 60)

    mean_duration_formatted = f'{mean_hours:02}:{mean_minutes:02}:{mean_seconds:02}'
    total_videos = len(df)
    max_views =  humanize.intword(df['views'].max())
    min_views =  humanize.intword(df['views'].min())



    # CHARTS -----------------------------------------------------------------------------
    

    line_avg_views = px.line(
        df_grouped, 
        x='video_date', 
        y='views', 
        title='Average Views Over Time',
        width=680
    )
    line_avg_views.update_layout(
        title=dict(
            font=dict(family='Arial, sans-serif', size=20, weight='bold'),
            x=0.5
        )
    )

    boxplot_views = px.box(
        df, 
        x='log_views',
        points='all',
        width=680
    )
    boxplot_views.update_layout(
        title=dict(
            text='Box Plot of Log Views',
            font=dict(family='Arial, sans-serif', size=20, weight='bold'),
            x=0.5
        ),
        xaxis_title='Views'
    )

    scatter_comments_views = px.scatter(
        df, 
        x='log_views', 
        y='log_comments', 
        trendline='ols', 
        width=680
    )
    scatter_comments_views.update_layout(
        title=dict(
            text='Comments vs Log Views',
            font=dict(family='Arial, sans-serif', size=20, weight='bold'),
            x=0.5
        )
    )


    histogram_duration = px.histogram(
        df, 
        x='log_minutes', 
        width=680
    )
    histogram_duration.update_layout(
        title=dict(
            text='Distribution of Duration (Log Scale)',
            font=dict(family='Arial, sans-serif', size=20, weight='bold'),
            x=0.5
        ),
        xaxis_title='Log of Duration',
        yaxis_title='Count'
    )


    # LAYOUT -----------------------------------------------------------------------------
    layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H2(f'Videos: {total_videos}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        html.Div([
            html.H2(f'Duration Mean: {mean_duration_formatted}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
         html.Div([
            html.H2(f'Max Views: {max_views}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        html.Div([
            html.H2(f'Min Views: {min_views}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        

    ], style={'display': 'flex', 'gap': '10px', 'margin-bottom': '20px'}),
        html.Div([
            dcc.Graph(figure=line_avg_views),
            dcc.Graph(figure=boxplot_views),
        ], style={'display': 'flex', 'gap': '10px', 'padding': '10px'}),
        html.Div([
            dcc.Graph(figure=histogram_duration),
            dcc.Graph(figure=scatter_comments_views),
        ], style={'display': 'flex', 'gap': '10px', 'padding': '10px'}),
    ])

    return layout

def convert_to_minutes(duration):
    h, m, s = map(int, duration.split(':'))
    return h * 60 + m + s / 60