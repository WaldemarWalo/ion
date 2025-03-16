from dotenv import load_dotenv, find_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.azure_openai_endpoint = self._get_env_var("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_key = self._get_env_var("AZURE_OPENAI_API_KEY") 
        self.azure_openai_deployment = self._get_env_var("AZURE_OPENAI_DEPLOYMENT")

    def _get_env_var(self, name):
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value

    def __str__(self):
        return (
            f"Configuration:\n"
            f"AZURE_OPENAI_ENDPOINT: {self.azure_openai_endpoint}\n"
            f"AZURE_OPENAI_API_KEY: {self.azure_openai_api_key}\n"
            f"AZURE_OPENAI_DEPLOYMENT: {self.azure_openai_deployment}"
        )
