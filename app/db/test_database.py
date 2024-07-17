import unittest
from app.db.database_connector import DatabaseConnector
from app.db.database_repository import DatabaseRepository

class Test(unittest.TestCase):
    
    #python -m unittest app.db.test_database.Test.test_select_channels_to_csv
    def test_select_channels_to_csv(self):
        DatabaseConnector.connect()
        DatabaseRepository.select_channels_to_csv()
    
    #python -m unittest app.db.test_database.Test.test_select_videos_to_csv
    def test_select_videos_to_csv(self):
        DatabaseConnector.connect()
        DatabaseRepository.select_videos_to_csv()