import os

_ENV_HOST: str = "HOST"
_ENV_PORT: str = "PORT"


class AppConfig:
    """
    Класс конфигурации приложения.
    """

    def __init__(self):
        """
        Инициализирует объект конфигурации приложения.
        """
        self.__host = os.getenv(_ENV_HOST, "127.0.0.1")
        self.__port = int(os.getenv(_ENV_PORT, "8000"))

    @property
    def host(self) -> str:
        """
        Возвращает хост приложения.
        """
        return self.__host

    @property
    def port(self) -> int:
        """
        Возвращает порт приложения.
        """
        return self.__port
