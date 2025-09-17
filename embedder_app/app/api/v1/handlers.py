from fastapi import Response, Body, UploadFile, File
from app.utils import make_json_response
from app.lib.clip_embedder import CLIPEmbedder


class V1Handler:
    def __init__(self):
        self.__clip_embedder = CLIPEmbedder()

    async def ping(self) -> Response:
        """
        Обработчик GET-запроса к маршруту `/ping`.

        Returns:
            Response: JSON-ответ с сообщением "pong".
        """

        return make_json_response({"message": "pong"})

    async def post_text_to_embedding(self, text: str = Body(...)) -> Response:
        """
        Преобразовать текст в эмбеддинг.

        Args:
            text (str): Текст, который требуется преобразовать в эмбеддинг.

        Returns:
            Response: JSON-массив с эмбеддингом.
        """

        embedding = self.__clip_embedder.embed(text)
        return make_json_response(embedding.tolist())

    async def post_image_to_embedding(self, file: UploadFile = File(...)) -> Response:
        """
        Преобразовать изображение в эмбеддинг.

        Args:
            file (UploadFile): Изображение (jpg/png), переданное в теле запроса.

        Returns:
            Response: JSON-массив с эмбеддингом.
        """
        image_bytes = await file.read()
        embedding = self.__clip_embedder.embed_image(image_bytes)
        return make_json_response(embedding.tolist())

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
