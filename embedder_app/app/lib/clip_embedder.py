import torch
import numpy as np
from sentence_transformers import SentenceTransformer

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

    def embed(self, prompt: str | np.ndarray) -> np.ndarray:
        """Преобразует текст или массив строк в эмбеддинг CLIP.

        Args:
            prompt (str | np.ndarray): Строка или массив строк для кодирования.

        Returns:
            np.ndarray: Нормализованный эмбеддинг размерности (d,),
                        где d зависит от используемой модели.
        """
        embedding = self.__model.encode(
            prompt, convert_to_numpy=True, normalize_embeddings=True
        )
        return embedding
