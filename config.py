from os import getenv
from pathlib import Path


BASE_PATH = Path(__file__).parent.parent.resolve()
UPLOADS_DIR = "uploads/"


class Config:
    """Base application configuration class"""

    APP_NAME = "address_api"

    def __init__(self, **kwargs):
        for attribute, value in kwargs.items():
            if hasattr(self, attribute):
                try:
                    setattr(self, attribute, value)
                except AttributeError:
                    pass

    @property
    def db_url(self) -> str:
        """
        Property to get db connection url

        :raise ValueError: DB_URL env variable not present
        """

        if (db_url := getenv("DB_URL")) is not None:
            return db_url

        raise ValueError("You should set DB_URL env variable")

    def load_params(self) -> dict:
        """
        Load all configuration params

        :return: Configuration params
        :rtype: dict
        """

        return {
            attribute: getattr(self, attribute)
            for attribute in self.__dir__()
            if not attribute.startswith("__") and attribute.endswith("")
        }

    @classmethod
    def load_config(cls, **kwargs):
        """
        Make configuration and return it

        :param kwargs: Params to override
        :type kwargs: dict
        :return: Configuration params
        :rtype: dict
        """

        config = cls(**kwargs)

        return config.load_params()

    def get_db_params(self) -> dict:
        """Get all db params"""

        return {}
