from fastapi import APIRouter, Response
from app.api.v1.handlers import V1Handler

_HTTP_METHOD_POST: str = "POST"
_HTTP_METHOD_GET: str = "GET"
_V1_PREFIX: str = "/v1"


class V1Router(APIRouter):
    """
    Класс для создания маршрутизатора API версии 1.
    """

    def __init__(self):
        super().__init__(prefix=_V1_PREFIX)

        self.__v1_handler = V1Handler()
        self.add_api_route(
            "/ping",
            self.__v1_handler.ping,
            methods=[_HTTP_METHOD_GET],
            summary="Health check endpoint",
            description="Обработчик GET-запроса к маршруту `/ping`. Возвращает JSON-ответ с сообщением 'pong'.",
            response_class=Response,
        )
        self.add_api_route(
            "/revert_vector",
            self.__v1_handler.revert_vector,
            methods=[_HTTP_METHOD_POST],
            summary="Revert vector endpoint",
            description="Обработчик POST-запроса к маршруту `/revert_vector`. Принимает вектор (список чисел), инвертирует его и возвращает обратно клиенту.",
            response_class=Response,
        )
