# YoutubeExtractorFlask

## Descrição
YoutubeExtractorFlask é um projeto pessoal desenvolvido para praticar conceitos de Engenharia de Dados, Análise de Dados e Ciência de Dados. Este projeto permite a extração de dados do YouTube, oferecendo atualmente duas funcionalidades:

- Extração de dados atuais de um canal.
- Extração de vídeos em alta (trending), incluindo os dados de todos os vídeos nos trending topics e seus respectivos canais.

A aplicação exibe para o usuário todos os canais e vídeos extraídos, juntamente com suas informações detalhadas. Além disso, são apresentadas métricas e gráficos dos dados coletados, utilizando as bibliotecas Dash e Plotly.

A aplicação foi desenvolvida com Flask, um framework web em Python. O backend foi implementado inteiramente em Python, enquanto o frontend utiliza recursos do Flask, CSS e JavaScript.


A arquitetura do projeto e ideia foram inspirados no conjunto de aulas de ETL Pipeline do [Programador Lhama](https://www.youtube.com/watch?v=D5mwXMMA0e0&list=PLAgbpJQADBGLuI1oR39tVfELOEZJSSbxQ).

## Requisitos
É necessário Python 3.10 e Docker version 24.0.7 (Pode não funcioanar em outras versões)

Primeiro clone o repositório, crie o ambiente virtual, ative o ambiente e instale o projeto e seus requerimentos.
### Windows

```
git clone https://github.com/GustavoNav/YoutubeExtractorFlask
python3 -m venv nome_do_ambiente
nome_do_ambiente\Scripts\activate
pip install -r requirements.txt
```
### Mac/Linux

```
git clone https://github.com/GustavoNav/YoutubeExtractorFlask
python3 -m venv nome_do_ambiente
source nome_do_ambiente/bin/activate
pip install -r requirements.txt
```

### Banco de Dados
O banco de dados utilizados é Mysql, para esse caso utilizei Docker, detalhes da conexão no arquivo *database_connector*.

Criar imagem do my_sql, as tabelas são criadas automaticamente, utilizando o arquivo db.sql:

```
docker build -t my_mysql_image ./database
```

Inicie o container na porta 3306

```
docker run --name my_mysql_container -d -p 3306:3306 my_mysql_image
```

Para não perder os dados ao encerrar o container, crie um volume, veja mais a respeito na documentação [Docker](https://docs.docker.com/engine/storage/volumes/).


### Iniciar o Projeto
Uma vez que as dependências tenham sido instaladas e banco de dados configurado. Configure o Pythonpath para o seu diretório corrente.

Execute o comando pwd para ver o caminho absoluto para o diretório corrente:

```
pwd
```
Copie o caminho absoluto e então execute:

```
export PYTHONPATH=/caminho_absoluto
```

Agora basta executar:

```
flask run
```

Acesse o endereço mostrado no Terminal e aproveite!


## Links Úteis 
[Python](https://www.python.org/)

[Flask](https://flask.palletsprojects.com/en/3.0.x/)

[Requests](https://docs.python-requests.org/en/latest/index.html)

[BeatifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)

[Dash](https://dash.plotly.com/)

[Plotly](https://plotly.com/python/)

[Youtube](https://www.youtube.com)

