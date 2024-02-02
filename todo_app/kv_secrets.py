import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secrets() -> None:

    secret_names = [
        ('TRELLO-API-KEY', 'TRELLO_API_KEY'),
        ('TRELLO-SECRET', 'TRELLO_SECRET'),
        ('TRELLO-BOARD-ID', 'TRELLO_BOARD_ID'),
        ('TRELLO-TODO-LIST-ID', 'TRELLO_TODO_LIST_ID'),
        ('TRELLO-COMPLETED-LIST-ID', 'TRELLO_COMPLETED_LIST_ID')
    ]

    key_vault_name = os.environ['KEY_VAULT_NAME']
    kv_uri = f'https://{key_vault_name}.vault.azure.net'

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url= kv_uri, credential=credential)

    for secret, env_var_name in secret_names:
        os.environ[env_var_name] = client.get_secret(secret).value

if __name__ == "__main__":
    get_secrets()