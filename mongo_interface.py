import os

from pymongo import MongoClient

class MongoInterface:
    def __connect_files(self):
        conn_string = os.environ['CUSTOMCONNSTR_EvidenceStoreConnectionString']
        collection  = os.environ['FILES_DB_COLLECTION']
        db_name     = os.environ['MONGO_DB_NAME']

        client = MongoClient(conn_string)

        db         = client[db_name]
        collection = db[collection]

        return collection

    def __connect_evidence(self):
        conn_string = os.environ['CUSTOMCONNSTR_EvidenceStoreConnectionString']
        collection  = os.environ['EVIDENCE_DB_COLLECTION']
        db_name     = os.environ['MONGO_DB_NAME']

        client = MongoClient(conn_string)

        db         = client[db_name]
        collection = db[collection]

        return collection

    def find_evidence_for_file(self, file_name: str):
        # Get list of evidence files
        collection = self.__connect_files()

        files_query_obj = {
            'current_file_name': file_name
        }

        result = collection.find(
            files_query_obj,
            {
                'file_id': 1,
                'current_file_name': 1,
                'evidence_files': 1,
                'current_file_path': 1
            }
        )

        data = []

        for current in result:
            del current['_id']

            data.append(current)

        return data
    
    def get_stored_plain_hash(self, file_name: str):
        collection = self.__connect_evidence()

        query_obj = {
            'evidence_file_id': file_name
        }

        result = collection.find_one(
            query_obj
        )

        return result['p_hash']

