from fastapi import Response
from app.utils import make_json_response


class V1Handler:
    async def ping(self) -> Response:
        """
        Обработчик GET-запроса к маршруту `/ping`.

        Returns:
            Response: JSON-ответ с сообщением "pong".
        """

        return make_json_response({"message": "pong"})

    async def revert_vector(self, vector: list[float] | str) -> Response:
        """
        Обработчик POST-запроса к маршруту `/revert_vector`.

        Принимает вектор (список чисел), инвертирует его и возвращает обратно клиенту.

        Args:
            vector (list[float] | str): Входной вектор, переданный в теле запроса.

        Returns:
            Response: JSON-ответ с инвертированным вектором.
        """
        return make_json_response(vector[::-1])
