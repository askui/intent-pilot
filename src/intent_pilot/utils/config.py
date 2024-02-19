import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


class Config:
    """
    Configuration class for managing settings.

    Attributes:
        verbose (bool): Flag indicating whether verbose mode is enabled.
        openai_api_key (str): API key for OpenAI.
        google_api_key (str): API key for Google.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        self.verbose = True
        self.openai_api_key = (
            None  # instance variables are backups in case saving to a `.env` fails
        )
        self.aui_workspace_id=None
        self.aui_token=None
        self.openai_temperature = 0.1
        self.openai_max_tokens = 1000
    
    def initialize_askui(self):
        self.aui_workspace_id=os.getenv("ASKUI_WORKSPACE_ID")
        self.aui_token=os.getenv("ASKUI_TOKEN")

    def initialize_openai(self, temperature=0.7, max_tokens=1000):
        self.openai_temperature = temperature
        self.openai_max_tokens = max_tokens
        if self.openai_api_key:
            api_key = self.openai_api_key
        else:
            api_key = os.getenv("OPENAI_API_KEY")

        client = OpenAI(
            api_key=api_key,
        )
        client.api_key = api_key
        client.base_url = os.getenv("OPENAI_API_BASE_URL", client.base_url)
        return client
