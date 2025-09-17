import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image
import io

_CLIP_MODEL = "sentence-transformers/clip-ViT-B-32"


class CLIPEmbedder:
    """Обёртка над моделью CLIP для генерации текстовых эмбеддингов.

    Использует SentenceTransformer с предобученной моделью CLIP-ViT-B-32.
    Автоматически выбирает устройство (GPU при наличии, иначе CPU).
    """

    def __init__(self):
        """Инициализация модели CLIP."""
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model = SentenceTransformer(_CLIP_MODEL).to(device=device)

    def embed(self, prompt: str) -> np.ndarray:
        """Преобразует текст или массив строк в эмбеддинг CLIP.

        Args:
            prompt (str | np.ndarray): Строка или массив строк для кодирования.

        Returns:
            np.ndarray: Нормализованный эмбеддинг размерности (d,),
                        где d зависит от используемой модели.
        """
        embedding = self.__model.encode(
            prompt, convert_to_numpy=True, normalize_embeddings=True
        ).astype(np.float32)
        return embedding

    def embed_image(self, image_bytes: bytes) -> np.ndarray:
        """Преобразует изображение в эмбеддинг CLIP.

        Args:
            image_bytes (bytes): Сырые байты изображения (jpg/png).

        Returns:
            np.ndarray: Нормализованный эмбеддинг изображения.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        embedding = self.__model.encode(  # type: ignore[arg-type]
            [image],  # type: ignore
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype(np.float32)
        return embedding[0]
