from fastapi import FastAPI
import uvicorn


from app.configure import AppConfig
from app.routers.api import ApiRouter


class WebApp(FastAPI):
    """
    Веб-приложение на основе FastAPI, предоставляющее минимальный API для проверки состояния сервера
    и обработки векторов (списков чисел).
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует веб-приложение и регистрирует маршруты API.

        Args:
            *args: Позиционные аргументы, передаваемые в базовый класс FastAPI.
            **kwargs: Именованные аргументы, передаваемые в базовый класс FastAPI.
        """
        super().__init__(*args, **kwargs)
        self.__api_router = ApiRouter()
        self.include_router(self.__api_router)
        self.__config = AppConfig()

    def run(self):
        """
        Запускает веб-сервер на указанном хосте и порту с использованием Uvicorn.
        Если параметры не указаны, используются значения из переменных окружения или значения по умолчанию.

        Args:
            host (str, optional): IP-адрес хоста, на котором будет запущен сервер.
                                  По умолчанию используется значение переменной окружения HOST или "127.0.0.1".
            port (int, optional): Порт, на котором будет запущен сервер.
                                  По умолчанию используется значение переменной окружения PORT или 8000.
        """

        uvicorn.run(self, host=self.__config.host, port=self.__config.port)
