import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secrets() -> None:

    secret_names = [
        ('MONGO-CONNECTION-STRING', 'MONGO_CONNECTION_STRING'),
        ('MONGO-DATABASE-NAME', 'MONGO_DATABASE_NAME'),
        ('GITHUB-OAUTH-CLIENT-ID', 'GITHUB_OAUTH_CLIENT_ID')
        ('GITHUB-OAUTH-CLIENT-SECRET', 'GITHUB_OAUTH_CLIENT_SECRET')
    ]
    
    key_vault_name = os.environ['KEY_VAULT_NAME']
    kv_uri = f'https://{key_vault_name}.vault.azure.net'

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url= kv_uri, credential=credential)

    for secret, env_var_name in secret_names:
        os.environ[env_var_name] = client.get_secret(secret).value

if __name__ == "__main__":
    get_secrets()