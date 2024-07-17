
from app.pipes.collect_trending.src.stages.extract.extract_html import ExtractHtml
from app.pipes.collect_video.run import run_pipeline_videos
from app.pipes.collect_channels.run import run_pipeline_channels
from app.db.database_connector import DatabaseConnector
from app.db.database_repository import DatabaseRepository

class MainPipeline:
    def __init__(self) -> None:
        self.__extract_html = ExtractHtml()

    def run_pipeline(self):
        # Collect videos URLS
        urls = self.__extract_html.extract()

        # Collect videos Informations
        videos_informations = run_pipeline_videos(urls, True)

        # Collect Channels Links from videos_informations

        channel_links = self.__get_links(videos_informations)
        channel_links_unique = list(set(channel_links))

        # Collect Channels informations 
        channels_information = run_pipeline_channels(channel_links_unique)

        # INSERT DATA

        # Insert channels
        # Channels should be insert before videos, because videos have a Foreign Key
        DatabaseConnector.connect()

        for channel in channels_information:
            
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
        
        # Insert Videos
        for video in videos_informations:
            DatabaseRepository.insert_video(video)


    def __get_links(self, videos_informations):
        channel_links = []
        for information in videos_informations:
            channel_links.append(information['channel_link'])

        return channel_links