from dash import Dash, html, dcc
import numpy as np
import os
import humanize
import pandas as pd
import plotly.express as px
from app.db.database_connector import DatabaseConnector
from app.db.database_repository import DatabaseRepository


def create_channels_dash(flask_app):
    dash_app = Dash(server=flask_app, name='Dashboard', url_base_pathname='/channels/') 
    return dash_app

def create_channels_layout():
    DatabaseConnector.connect()
    DatabaseRepository.select_channels_to_csv()

    file_path = os.path.abspath(os.path.join(__file__, '../../export/channels_data.csv'))
    df = pd.read_csv(file_path)

    df['date_creation'] = pd.to_datetime(df['date_creation'])

    df['year'] = df['date_creation'].dt.year

    df_year_grouped = df.groupby('year').size().reset_index(name='count')


    total_channels = len(df)

    df_cleaned = df[df['subscriptions'] != 'Unknown']
    df_cleaned.loc[:, 'subscriptions'] = pd.to_numeric(df_cleaned['subscriptions']).astype('Int64')

    top_10_views = df.sort_values(by='views',  ascending=False).head(10)

    top_10_subscriptions = df_cleaned.sort_values(by='subscriptions', ascending=False).head(10)

    channel_counts = df['channel_location'].value_counts().reset_index()
    channel_counts.columns = ['channel_location', 'count']

    mean = humanize.intword(df_cleaned['views'].mean())
    max_views = humanize.intword(df_cleaned['views'].max())
    min_views = humanize.intword(df_cleaned['views'].min())

    df_log = df_cleaned.copy()
    df_log['log_subscriptions'] = np.log(df_log['subscriptions'].astype(float))
    df_log['log_views'] = np.log(df_log['views'].astype(float))


    # CHARTS -----------------------------------------------------------------------------

    bars_top_10_views = px.bar(
        top_10_views, 
        y='channel_name', 
        x='views', 
        orientation='h', 
        width=680, 
        title='Top 10 Channel by Views'
    )
    bars_top_10_views.update_layout(
        title_font=dict(family='Arial, sans-serif', size=20, weight='bold'),
        title_x = 0.5
    )

    bars_top_10_subscriptions = px.bar(
        top_10_subscriptions, 
        y='channel_name', 
        x='subscriptions', 
        orientation='h', 
        width=680, 
        title='Top 10 Channel by Subscriptions'
    )
    bars_top_10_subscriptions.update_layout(
    title_font=dict(
        family='Arial, sans-serif', size=20, weight='bold'),
        title_x=0.5
    )

    pie_channel_location = px.pie(
        channel_counts, 
        names='channel_location',
        values='count', 
        title='Distribution of Channels by Country', 
        width=400
    )
    pie_channel_location.update_layout(
        title_font=dict(family='Arial, sans-serif',size=20, weight='bold'),
        title_x=0.5
    )

    histogram_subscriptions = px.histogram(
        df_log, 
        x='log_subscriptions',
        title='Distribution of Subscriptions (Log Scale)',
        nbins=20, 
        width=960,
        hover_data={'log_subscriptions': True, 'subscriptions': True}
    )
    histogram_subscriptions.update_layout(
        title_font=dict(family='Arial, sans-serif', size=20, weight='bold'),
        title_x=0.5,
        xaxis_title='Log of Subscriptions',
        yaxis_title='Count'
    )


    bars_date_creation = px.bar(
        df_year_grouped, 
        x='year',
        y='count',
        width=680,
        title='Number of Channels Created per Year'
    )
    bars_date_creation.update_layout(
        title_font=dict(family='Arial, sans-serif', size=20, weight='bold'),
        title_x=0.5,
        showlegend=False
    )

    scatter_videos_vs_views = px.scatter(
        df_log,
        x='log_subscriptions',
        y='log_views', 
        width=680,
        trendline="ols",
        title='Subscriptions vs Views'
    )
    scatter_videos_vs_views.update_layout(
        title_font=dict(family='Arial, sans-serif', size=20, weight='bold'),
        title_x=0.5,
        showlegend=False
    )



    # LAYOUT -----------------------------------------------------------------------------
    layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H2(f'Channels: {total_channels}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        html.Div([
            html.H2(f'Views Mean: {mean}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        html.Div([
            html.H2(f'Max Views: {max_views}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
        html.Div([
            html.H2(f'Min Views: {min_views}', style={'margin': '0'}),
        ], style={'background-color': '#f2f2f2', 'padding': '20px', 'border-radius': '8px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'flex': '1'}),
    ], style={'display': 'flex', 'gap': '10px', 'margin-bottom': '20px'}),
        html.Div([
            dcc.Graph(figure=bars_top_10_views),
            dcc.Graph(figure=bars_top_10_subscriptions),
        ], style={'display': 'flex', 'gap': '10px', 'padding': '10px'}),
        html.Div([
            dcc.Graph(figure=pie_channel_location),
            dcc.Graph(figure=histogram_subscriptions),
        ], style={'display': 'flex', 'gap': '10px', 'padding': '10px'}),
        html.Div([
            dcc.Graph(figure=bars_date_creation),
            dcc.Graph(figure=scatter_videos_vs_views),
        ], style={'display': 'flex', 'gap': '10px', 'padding': '10px'})
        ], style={'padding': '10px', 'height': '100vh', 'box-sizing': 'border-box'})
        
    return layout