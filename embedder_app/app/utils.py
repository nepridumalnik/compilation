import json
import fastapi

# Константа для указания типа содержимого (MIME-тип) в JSON-ответах
MEDIA_TYPE_JSON: str = "application/json"


def json_dump_ns(data) -> str:
    """
    Преобразует данные в строку JSON без лишних пробелов и отступов.

    Используется для минимизации размера JSON-ответа, отправляемого клиенту.

    Args:
        data (Any): Объект Python (например, dict, list), который будет сериализован в JSON.

    Returns:
        str: JSON-представление данных в виде строки без пробелов.
    """
    return json.dumps(data, separators=(",", ":"))


def make_json_response(data) -> fastapi.Response:
    """
    Создаёт HTTP-ответ с заданными данными в формате JSON.

    Args:
        data (Any): Данные, которые будут отправлены в теле ответа в виде JSON.

    Returns:
        fastapi.Response: Объект FastAPI Response, содержащий JSON-данные
                          и соответствующий заголовок Content-Type.
    """
    return fastapi.Response(
        content=json_dump_ns(data),
        media_type=MEDIA_TYPE_JSON,
    )
