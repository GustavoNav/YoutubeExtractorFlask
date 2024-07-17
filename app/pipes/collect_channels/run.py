from app.pipes.collect_channels.src.main import main_pipeline

def run_pipeline_channels(urls):
    channels_informations = main_pipeline.run_pipeline(urls)

    return channels_informations
