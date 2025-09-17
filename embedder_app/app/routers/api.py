from fastapi import APIRouter
from .v1_router import V1Router

_API_PREFIX: str = "/api"


class ApiRouter(APIRouter):
    """
    Маршрутизатор верхнего уровня для всего API приложения.

    Этот класс объединяет все версии API под единым префиксом `/api`.
    Внутри него подключаются версии маршрутов (например, `V1Router`).
    """

    def __init__(self) -> None:
        """
        Создаёт экземпляр маршрутизатора API с префиксом `/api`.

        В данный момент подключает маршрутизатор первой версии API (`V1Router`).
        """
        super().__init__(prefix=_API_PREFIX)

        self.__v1_router: V1Router = V1Router()
        self.include_router(self.__v1_router)
