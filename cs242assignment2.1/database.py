"""
upload json files to database
"""
import json
import os
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv

PROJECT_FOLDER = os.path.expanduser('~/Desktop/sp20-cs242-assignment2')
load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')


class PyMongo:
    """
    upload json files to database
    """
    @staticmethod
    def upload_to_database():
        """
        upload json files to database
        :return: if successfully upload json files to database
        """
        try:
            mongodb_client = (
                'mongodb+srv://%s:%s@cluster0-x2acz.mongodb.net/test?retryWrites=true&w=majority'
                % (MONGODB_USERNAME, MONGODB_PASSWORD))
            print(mongodb_client)
            print(MONGODB_USERNAME)
            print(MONGODB_PASSWORD)
            client = MongoClient(mongodb_client)
            database = client.goodreads_data
            collection = database.books_data
            with open('books.json') as file:
                file_data = json.load(file)
                collection.delete_many({})
                collection.insert_many(file_data)
            collection = database.authors_data
            with open('authors.json') as file:
                file_data = json.load(file)
                collection.delete_many({})
                collection.insert_many(file_data)
        except ConnectionError:
            print("could not connect to database")

    @staticmethod
    def download_from_database():
        """
        downloads info from database
        :return: info from database
        """
        try:
            mongodb_client = (
                'mongodb+srv://%s:%s@cluster0-x2acz.mongodb.net/test?retryWrites=true&w=majority'
                % (MONGODB_USERNAME, MONGODB_PASSWORD))
            print(mongodb_client)
            print(MONGODB_USERNAME)
            print(MONGODB_PASSWORD)
            client = MongoClient(mongodb_client)
            database = client.goodreads_data
            collection = database.authors_data
            file = open('authors_from_db.json', 'w')
            data = []
            for record in collection.find():
                # pprint.pprint(record)
                record.pop('_id')
                data.append(record)
            content = json.dumps(data, ensure_ascii=False, indent=4)
            file.write(content)
            file.close()
            collection = database.books_data
            file = open('books_from_db.json', 'w')
            data = []
            for record in collection.find():
                pprint.pprint(record)
                record.pop('_id')
                data.append(record)
            content = json.dumps(data, ensure_ascii=False, indent=4)
            file.write(content)
            file.close()
        except ConnectionError:
            print("could not connect to database")
        print("downloads successfully")


# if __name__ == "__main__":
#     print("Start")
#     # upload_data = PyMongo()
#     # upload_data.upload_to_database()
#     download_data = PyMongo()
#     download_data.download_from_database()
#     print("Finished")
