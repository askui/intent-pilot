import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.chat_models import ChatOllama

from intent_pilot.utils.terminal import get_env_values


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

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.openai_api_key = (
            None  # instance variables are backups in case saving to a `.env` fails
        )
        self.openai_base_url = None
        self.aui_workspace_id = None
        self.aui_token = None
        self.openai_temperature = 0.1
        self.openai_max_tokens = 1000

        # load from local .env file
        load_dotenv()

    def __read_from_env_or_ask(self, env_name: str) -> str:
        value = os.getenv(env_name)
        if value is None:
            value_dict = get_env_values([env_name])
            value = value_dict[env_name]
        return value

    def initialize_askui(self):
        self.aui_workspace_id = self.__read_from_env_or_ask("ASKUI_WORKSPACE_ID")
        self.aui_token = self.__read_from_env_or_ask("ASKUI_TOKEN")

    def assert_env_var(self, env_var):
        """
        Check and Raise an error indicating that the specified environment variable is not set.
        """
        if env_var is None:
            raise ValueError("Environment variable not set.")

    def initialize_openai(self, temperature=0.2, max_tokens=4096):
        self.openai_temperature = temperature
        self.openai_max_tokens = max_tokens
        if self.openai_api_key:
            api_key = self.openai_api_key
        else:
            api_key = self.__read_from_env_or_ask("OPENAI_API_KEY")
        self.assert_env_var(api_key)
        self.openai_api_key = api_key

        client = OpenAI(
            api_key=api_key,
        )
        client.api_key = api_key
        client.base_url = self.openai_base_url = os.getenv(
            "OPENAI_API_BASE_URL", client.base_url
        )
        return client

    def initialize_ollama(self, model="llava", temperature=0):
        client = ChatOllama(model=model, temperature=temperature)
        return client
