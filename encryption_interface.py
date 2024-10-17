from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from Crypto.Cipher import AES

import os

class EncryptionInterface:
    __KEY_VAULT_NAME = os.environ['KEY_VAULT_NAME']
    __KEY_VAULT_URI  = f'https://{__KEY_VAULT_NAME}.vault.azure.net'

    __AES_MODE = AES.MODE_EAX

    def __get_creds(self):
        creds = ManagedIdentityCredential(
            client_id = os.environ['ManagedIdentityCredential']
        )

        client = SecretClient(
            vault_url  = self.__KEY_VAULT_URI,
            credential = creds
        )

        return client

    def __get_evidence_aes_key(self):
        client = self.__get_creds()

        hex = client.get_secret(os.environ['EVIDENCE_ENCRYPTION_SECRET']).value

        return bytes.fromhex(hex)
    
    def __get_db_aes_key(self):
        client = self.__get_creds()

        hex = client.get_secret(os.environ['DB_ENCRYPTION_SECRET']).value

        return bytes.fromhex(hex)
    
    def __get_tag_nonce_split(self, data: str):
        result = {}

        result['tag'] = bytes.fromhex(data[0:32])
        result['nonce'] = bytes.fromhex(data[32:64])
        result['data'] = bytes.fromhex(data[64:])

        return result
        
    
    def decrypt_file_name(self, file_name: str):
        key_bytes = self.__get_db_aes_key()

        properties_dict = self.__get_tag_nonce_split(file_name)

        cipher = AES.new(
            key = key_bytes,
            mode = self.__AES_MODE,
            nonce = properties_dict['nonce']
        )

        decrypted_file_name = cipher.decrypt_and_verify(properties_dict['data'], properties_dict['tag'])

        return decrypted_file_name.decode('utf-8')
    
    def decrypt_content(self, file_contents: str):
        key_bytes = self.__get_evidence_aes_key()

        properties_dict = self.__get_tag_nonce_split(file_contents)        

        cipher = AES.new(
            key = key_bytes,
            mode = self.__AES_MODE,
            nonce = properties_dict['nonce']
        )

        decrypted_content = cipher.decrypt_and_verify(properties_dict['data'], properties_dict['tag'])

        return decrypted_content