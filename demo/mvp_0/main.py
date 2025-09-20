import os
import hashlib
import requests
from typing import List, Dict

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
from PIL import Image
import torch
import open_clip


# ==================== CONFIG ====================

QDRANT_FILE = os.getenv("QDRANT_FILE", "data/qdrant.db")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "ViT-B-32")
PRETRAINED = os.getenv("PRETRAINED", "laion2b_s34b_b79k")
TOP_K = int(os.getenv("TOP_K", "1"))

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
SOURCES_JSON = os.path.join(DATA_DIR, "sources.json")
FLAG_DIR = os.path.join(ROOT_DIR, ".state")
STATIC_DIR = os.path.join(ROOT_DIR, "static")

# ==================== SERVICES ====================


class ClipService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            MODEL_NAME, pretrained=PRETRAINED, device=self.device
        )
        self.tokenizer = open_clip.get_tokenizer(MODEL_NAME)
        self.model.eval()

    @torch.inference_mode()
    def embed_image(self, image_path: str):
        img = Image.open(image_path).convert("RGB")
        img_t = self.preprocess(img).unsqueeze(0).to(self.device)
        feats = self.model.encode_image(img_t)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        return feats.squeeze(0).cpu().numpy()

    @torch.inference_mode()
    def embed_text(self, text: str):
        tokens = self.tokenizer([text]).to(self.device)
        feats = self.model.encode_text(tokens)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        return feats.squeeze(0).cpu().numpy()


clip_service = ClipService()
qdrant = QdrantClient(path=QDRANT_FILE, api_key=QDRANT_API_KEY)


# ==================== INGEST ====================


def _download(url: str, dst_path: str):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(dst_path, "wb") as f:
        f.write(r.content)


def _path_for(category: str, idx: int) -> str:
    return os.path.join(IMAGES_DIR, category, f"{idx}.jpg")


def _hash_id(*parts: str) -> int:
    h = hashlib.md5("||".join(parts).encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def ensure_collection(name: str, dim: int):
    existing = [c.name for c in qdrant.get_collections().collections]
    if name in existing:
        return
    qdrant.recreate_collection(
        collection_name=name,
        vectors_config=qm.VectorParams(size=dim, distance=qm.Distance.COSINE),
    )


def ingest(flag_file: str):
    import json

    if os.path.exists(flag_file):
        return
    with open(SOURCES_JSON, "r", encoding="utf-8") as f:
        src: Dict[str, List[str]] = json.load(f)

    # get dim
    any_cat = next(iter(src.keys()))
    tmp_path = _path_for(any_cat, 0)
    if not os.path.exists(tmp_path):
        _download(src[any_cat][0], tmp_path)
    dim = clip_service.embed_image(tmp_path).shape[0]

    for category, urls in src.items():
        for i, url in enumerate(urls):
            path = _path_for(category, i)
            if not os.path.exists(path):
                try:
                    _download(url, path)
                except Exception:
                    continue

        ensure_collection(category, dim)

        points = []
        cat_dir = os.path.join(IMAGES_DIR, category)
        if not os.path.isdir(cat_dir):
            continue
        for fname in os.listdir(cat_dir):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(cat_dir, fname)
            try:
                vec = clip_service.embed_image(path)
            except Exception:
                continue
            pid = _hash_id(category, path)
            points.append(
                qm.PointStruct(
                    id=pid,
                    vector=vec.tolist(),
                    payload={"image_path": path.replace("\\", "/")},
                )
            )
        if points:
            qdrant.upsert(collection_name=category, points=points, wait=True)

    os.makedirs(os.path.dirname(flag_file), exist_ok=True)
    with open(flag_file, "w") as f:
        f.write("ok")


# ==================== FASTAPI APP ====================

app = FastAPI(title="Virtual Fitting Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    ingest(os.path.join(FLAG_DIR, "ingest.done"))


@app.get("/api/categories")
def categories() -> List[str]:
    if not os.path.isdir(IMAGES_DIR):
        return []
    return sorted(
        [
            d
            for d in os.listdir(IMAGES_DIR)
            if os.path.isdir(os.path.join(IMAGES_DIR, d))
        ]
    )


@app.get("/api/search")
def search(category: str = Query(...), prompt: str = Query(...), top_k: int = TOP_K):
    vec = clip_service.embed_text(prompt).tolist()
    hits = qdrant.search(
        collection_name=category, query_vector=vec, limit=top_k, with_payload=True
    )
    items = []
    for h in hits:
        p = h.payload.get("image_path", "")
        rel = os.path.relpath(p, DATA_DIR).replace("\\", "/")
        items.append(
            {"score": h.score, "image_url": f"/images/{rel.split('images/', 1)[-1]}"}
        )
    return {"items": items}


# ==================== ENTRYPOINT ====================


app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
