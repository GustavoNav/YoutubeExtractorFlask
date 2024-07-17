import mysql.connector as mysql

class DatabaseConnector:
    connection = None
    @classmethod
    def connect(cls) -> None:
        db_connection = mysql.connect(
            host='localhost',
            port=3306,
            database='youtube_extractor_db',
            user='root',
            passwd='adm321'
        )
        cls.connection = db_connection