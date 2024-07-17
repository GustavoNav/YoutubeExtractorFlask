import time
from app import app
from flask import jsonify, render_template, request

from app.dash.ChannelsDash import create_channels_dash, create_channels_layout
from app.dash.VideosDash import create_videos_dash, create_videos_layout
from app.db.database_connector import DatabaseConnector
from app.db.database_repository import DatabaseRepository
from app.pipes.collect_trending.run import run_pipeline_trending
from app.pipes.collect_channels.run import run_pipeline_channels


dash_app_channels = create_channels_dash(app)
dash_app_channels.layout = create_channels_layout

dash_app_videos = create_videos_dash(app)
dash_app_videos.layout = create_videos_layout

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/extract', methods=['PUT', 'POST'])
def extract_data():
    start_time = time.time()

    if request.method == 'POST':
        data = request.json
        links = data['links']
        urls = [url.strip() for url in links]

        channels_informations = run_pipeline_channels(urls)

        DatabaseConnector.connect()
        for channel in channels_informations:
            
            channel_about = {
                'channel_id': channel['channel_id'],
                'date_creation': channel['date_creation'],
                'channel_location': channel['channel_location']
            } 

            channel_metrics = {
                'channel_id': channel['channel_id'], 
                'channel_name': channel['channel_name'], 
                'icon': channel['icon'], 
                'banner': channel['banner'], 
                'subscriptions': channel['subscriptions'], 
                'videos': channel['videos'], 
                'views': channel['views'],
            }
            if channel_about['channel_id'] != '':
                DatabaseRepository.insert_channel_about(channel_about)
                DatabaseRepository.insert_channel_metrics(channel_metrics)

        end_time = time.time()
        time_taken = round(end_time - start_time)

        return jsonify({"time_taken": time_taken})

    if request.method == 'PUT':
        run_pipeline_trending()

        end_time = time.time()
        time_taken = round(end_time - start_time)

        return jsonify({"time_taken": time_taken})

@app.route('/data')
def data_channels():
    DatabaseConnector.connect()
    info = DatabaseRepository.select_channel_info()

    return render_template('data.html', info=info)

@app.route('/data_videos')
def data_videos():
    DatabaseConnector.connect()
    info = DatabaseRepository.select_videos()
    print(info)

    return render_template('data_videos.html', info=info)

@app.route('/measurements')
def measurements():

    return render_template('measurements.html')


