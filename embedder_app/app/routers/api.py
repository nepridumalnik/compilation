from fastapi import APIRouter
from .v1_router import V1Router

_API_PREFIX: str = "/api"


class ApiRouter(APIRouter):
    """
    Класс для создания маршрутизатора API.
    """

    def __init__(self):
        """
        Инициализирует маршрутизатор API с префиксом "/api".
        """
        super().__init__(prefix=_API_PREFIX)

        self.__v1_router = V1Router()
        self.include_router(self.__v1_router)
