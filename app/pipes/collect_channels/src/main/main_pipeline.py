from app.pipes.collect_channels.src.stages.extract.extract_html import ExtractHtml
from app.pipes.collect_channels.src.stages.transform.transform_html import TransformHtml

class MainPipeline():
    def __init__(self) -> None:
        self.__extract_html = ExtractHtml()
        self.__transform_html = TransformHtml()

    def run_pipeline(self, urls):
        self.__extract_html.extract(urls)
        channels_informations = self.__transform_html.transform()

        return channels_informations
        