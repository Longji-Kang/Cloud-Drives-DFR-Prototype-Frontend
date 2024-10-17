from azure.storage.blob import BlobClient

import os

class BlobInterface:
    def get_content_file(self, file_name: str):
        client = BlobClient.from_connection_string(
            conn_str       = os.environ['CUSTOMCONNSTR_BlobConnectionString'],
            container_name = os.environ['CONTAINER_NAME'],
            blob_name      = file_name
        )

        download_stream = client.download_blob()
        
        content = download_stream.readall()

        return content