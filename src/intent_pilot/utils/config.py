
import pathlib
import os
from dotenv import load_dotenv
from openai import OpenAI

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

    def __init__(self):
        self.verbose = False
        self.openai_api_key = (
            None  # instance variables are backups in case saving to a `.env` fails
        )
        self.openai_base_url=None
        self.aui_workspace_id=None
        self.aui_token=None
        self.openai_temperature = 0.1
        self.openai_max_tokens = 1000

        self.user_config_dir = pathlib.Path.home() / pathlib.Path(".askui")
        self.user_config_env_path  = self.user_config_dir / 'intent-pilot.env'

        # load from user config file
        load_dotenv(self.user_config_env_path)
        # load from local .env file
        load_dotenv()
    
    def __read_from_env_or_ask(self, env_name: str) -> str:
        value = os.getenv(env_name)
        if value is None:
            value_dict = get_env_values([env_name])
            value = value_dict[env_name]
        return value

    def is_user_config_exists(self) -> bool:
        return os.path.exists(self.user_config_env_path)

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
        client.base_url = self.openai_base_url = os.getenv("OPENAI_API_BASE_URL", client.base_url)
        return client
  
    def save_config(self):
        os.makedirs(self.user_config_dir, exist_ok=True)
        with open(self.user_config_env_path, 'w') as f:
            f.write(f"ASKUI_WORKSPACE_ID={self.aui_workspace_id}\n")
            f.write(f"ASKUI_TOKEN={self.aui_token}\n")
            f.write(f"OPENAI_API_KEY={self.openai_api_key}\n")
            f.write(f"OPENAI_API_BASE_URL={self.openai_base_url}\n")
