# YoutubeExtractorFlask

## Descrição
YoutubeExtractorFlask é um projeto pessoal desenvolvido para praticar conceitos de Engenharia de Dados, Análise de Dados e Ciência de Dados. Este projeto permite a extração de dados do YouTube, oferecendo atualmente duas funcionalidades:

- Extração de dados atuais de um canal.
- Extração de vídeos em alta (trending), incluindo os dados de todos os vídeos nos trending topics e seus respectivos canais.

A aplicação exibe para o usuário todos os canais e vídeos extraídos, juntamente com suas informações detalhadas. Além disso, são apresentadas métricas e gráficos dos dados coletados, utilizando as bibliotecas Dash e Plotly.

A aplicação foi desenvolvida com Flask, um framework web em Python. O backend foi implementado inteiramente em Python, enquanto o frontend utiliza recursos do Flask, CSS e JavaScript.


A arquitetura do projeto e ideia foram inspirados no conjunto de aulas de ETL Pipeline do [Programador Lhama](https://www.youtube.com/watch?v=D5mwXMMA0e0&list=PLAgbpJQADBGLuI1oR39tVfELOEZJSSbxQ).

## Requisitos
Projeto testado no Python 3.12.

Primeiro clone o repositório, crie o ambiente virtual, ative o ambiente e instale o projeto e seus requerimentos.
### Windows

```
git clone https://github.com/GustavoNav/Data-Engineering-ETL-Youtube
python3 -m venv nome_do_ambiente
nome_do_ambiente\Scripts\activate
pip install .
```
### Mac/Linux

```
git clone https://github.com/GustavoNav/ETL-Youtube
python3 -m venv nome_do_ambiente
source nome_do_ambiente/bin/activate
pip install .
```

### Banco de Dados
O banco de dados utilizados é Mysql, a conexão foi criada utilizando o DBeaver, detalhes da conexão no arquivo *database_connector*.
![alt text](modelo_bd.png)
```
CREATE DATABASE IF NOT EXISTS youtube_extractor_db;

CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_channel_about` (
    channel_id VARCHAR(255) PRIMARY KEY,
    date_creation DATE,
    channel_location VARCHAR(255),
    extraction_date DATETIME
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_channel_metrics` (
    metric_id BIGINT NOT NULL AUTO_INCREMENT,
    channel_id VARCHAR(255),
    channel_name VARCHAR(255),
    icon VARCHAR(255),
    banner VARCHAR(255),
    subscriptions BIGINT,
    videos BIGINT,
    views BIGINT,
    extraction_date DATETIME,
    PRIMARY KEY (metric_id),
    FOREIGN KEY (channel_id) REFERENCES tb_channel_about(channel_id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS `youtube_extractor_db`.`tb_videos` (
    video_id BIGINT NOT NULL AUTO_INCREMENT,
    channel_id VARCHAR(255) NOT NULL,
    channel_link VARCHAR(255) not null,
    title VARCHAR(255),
    likes BIGINT,
    views BIGINT,
    comments BIGINT,
    duration TIME,
    video_date DATE,
    thumb VARCHAR(255),
    trending BOOLEAN,
    family_friend BOOLEAN,
    extraction_date DATETIME,
    PRIMARY KEY (video_id),
    FOREIGN KEY (channel_id) REFERENCES tb_channel_about(channel_id)
) ENGINE=INNODB;
```




## Links Úteis 
[Python](https://www.python.org/)

[Flask](https://flask.palletsprojects.com/en/3.0.x/)

[Requests](https://docs.python-requests.org/en/latest/index.html)

[BeatifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)

[Dash](https://dash.plotly.com/)

[Plotly](https://plotly.com/python/)

[Youtube](https://www.youtube.com)

