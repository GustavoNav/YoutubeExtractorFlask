import csv
import os
from datetime import datetime
from typing import Dict
from app.db.database_connector import DatabaseConnector

class DatabaseRepository:
    @classmethod
    def select_channel_id(cls) -> list:
        query = f'''
            SELECT channel_id
            FROM tb_channel_about
        '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        
        channel_ids = [row[0] for row in result]

        return channel_ids
    

    @classmethod
    def select_channel_info(cls) -> list:
        query = f'''
            SELECT 
                IFNULL(about.channel_location, 'Unknown'), 
                about.date_creation,
                IFNULL(metrics.channel_name, 'Unknown'), 
                metrics.views, 
                metrics.videos,
                IFNULL(metrics.subscriptions, 'Unknown'),
                metrics.extraction_date,
                metrics.icon,
                metrics.banner 
            FROM 
                tb_channel_about AS about
            JOIN 
                tb_channel_metrics AS metrics ON about.channel_id = metrics.channel_id
            WHERE 
                metrics.extraction_date = (
                    SELECT MAX(extraction_date) 
                    FROM tb_channel_metrics 
                    WHERE channel_id = about.channel_id
                );
        '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        columns = [
            'channel_location',
            'date_creation',
            'channel_name',
            'views',
            'videos',
            'subscriptions',
            'extraction_date',
            'icon',
            'banner',
        ]

        latest_channel_info = [
            dict(zip(columns, row))
            for row in result
        ]
        
        return latest_channel_info
    
    @classmethod
    def select_videos(cls) -> list:
        query = '''
        select distinct 
            cm.channel_name,
            v.extraction_date,
            v.title,
            v.views,
            IFNULL(v.likes, 0) AS likes,
            v.comments,
            v.duration,
            v.video_date,
            v.thumb
        FROM
            tb_channel_metrics cm
        JOIN
            tb_videos v ON cm.channel_id = v.channel_id
        JOIN (
            SELECT
                channel_id,
                title,
                MAX(extraction_date) AS latest_extraction_date
            FROM
                tb_videos
            GROUP BY
                channel_id, title
        ) lv ON v.channel_id = lv.channel_id AND v.title = lv.title AND v.extraction_date = lv.latest_extraction_date
        ORDER BY
            v.extraction_date DESC;
        '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        columns = [
            'channel_name',
            'extraction_date',
            'title',
            'views',
            'likes',
            'comments',
            'duration',
            'video_date',
            'thumb',
        ]

        latest_video_info = [
            dict(zip(columns, row))
            for row in result
        ]
        
        return latest_video_info

    @classmethod
    def insert_channel_about(cls, data: Dict) -> None:
        query = '''
            INSERT IGNORE INTO tb_channel_about
                (channel_id, date_creation, channel_location, extraction_date)
            VALUES
                (%s, %s, %s, %s)
            '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query, (
            data['channel_id'], 
            data['date_creation'], 
            data['channel_location'],
            datetime.now()
        ))

        DatabaseConnector.connection.commit()

    @classmethod
    def insert_channel_metrics(cls, data: Dict) -> None:
        query = '''
            INSERT INTO tb_channel_metrics
                (channel_id, channel_name, icon, banner, subscriptions, videos, views, extraction_date)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query, (
            data['channel_id'], 
            data['channel_name'], 
            data['icon'], 
            data['banner'], 
            data['subscriptions'], 
            data['videos'], 
            data['views'],
            datetime.now()
        ))

        DatabaseConnector.connection.commit()

    @classmethod
    def insert_video(cls, data: Dict) -> None:
        query = '''
            INSERT INTO tb_videos
                (channel_id, channel_link, title, likes, views, comments, duration, video_date, thumb, trending, family_friend, extraction_date)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query, (
            data['channel_id'], 
            data['channel_link'],
            data['title'], 
            data['likes'], 
            data['views'], 
            data['comments'], 
            data['duration'], 
            data['video_date'], 
            data['thumb'], 
            data['trending'],
            data['family_friend'],
            datetime.now()
        ))

        DatabaseConnector.connection.commit()

    @classmethod
    def select_channels_to_csv(cls) -> None:
        query='''
        SELECT 
            IFNULL(about.channel_location, 'Unknown'), 
            about.date_creation,
            IFNULL(metrics.channel_name, 'Unknown'), 
            metrics.views, 
            metrics.videos,
            IFNULL(metrics.subscriptions, 'Unknown'),
            metrics.extraction_date,
            metrics.icon,
            metrics.banner 
        FROM 
            tb_channel_about AS about
        JOIN 
            tb_channel_metrics AS metrics ON about.channel_id = metrics.channel_id
        WHERE 
            metrics.extraction_date = (
                SELECT MAX(extraction_date) 
                FROM tb_channel_metrics 
                WHERE channel_id = about.channel_id
            )
        order by metrics.channel_name;    
        '''

        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        column_names = ['channel_location', 'date_creation', 'channel_name', 'views', 'videos', 'subscriptions', 'extration_date', 'icon', 'banner']

        file_path = os.path.abspath(os.path.join(__file__, '../../export/channels_data.csv'))

        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  
            writer.writerows(result)  

    @classmethod
    def select_videos_to_csv(cls) -> None:
        query='''
            select distinct 
                cm.channel_name,
                v.extraction_date,
                v.title,
                v.views,
                IFNULL(v.likes, 0) AS likes,
                v.comments,
                v.duration,
                v.video_date,
                v.thumb
            FROM
                tb_channel_metrics cm
            JOIN
                tb_videos v ON cm.channel_id = v.channel_id
            JOIN (
                SELECT
                    channel_id,
                    title,
                    MAX(extraction_date) AS latest_extraction_date
                FROM
                    tb_videos
                GROUP BY
                    channel_id, title
            ) lv ON v.channel_id = lv.channel_id AND v.title = lv.title AND v.extraction_date = lv.latest_extraction_date
            ORDER BY
                v.extraction_date DESC;   
        '''

        cursor = DatabaseConnector.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        column_names = ['channel_name','extraction_date','title','views','likes','comments','duration','video_date','thumb']

        file_path = os.path.abspath(os.path.join(__file__, '../../export/videos_data.csv'))

        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  
            writer.writerows(result)  