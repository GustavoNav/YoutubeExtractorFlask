from app.pipes.collect_video.src.stages.extract.extract_html import ExtractHtml
from app.pipes.collect_video.src.stages.transform.transform_html import TransformHtml

class MainPipeline:
    def __init__(self) -> None:
        self.__extract_html = ExtractHtml()
        self.__transform_html = TransformHtml()

    def run_pipeline(self, urls, trending):
        self.__extract_html.extract(urls)
        informations = self.__transform_html.transform(trending)

        return informations
