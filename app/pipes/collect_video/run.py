from app.pipes.collect_video.src.main import main_pipeline

def run_pipeline_videos(urls, trending):
    channel_informations = main_pipeline.run_pipeline(urls, trending)
    return channel_informations