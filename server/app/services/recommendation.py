import faiss
from fashion_clip.fashion_clip import FashionCLIP
from app.utils import map_idx_id
import numpy as np
from PIL import Image


fclip = FashionCLIP('fashion-clip')

image_index = faiss.read_index(r"D:\CollegeWork\ShopLens-AR-Shopping-Assistant\server\notebooks\faiss_image.index")
n_image_vectors = image_index.ntotal
image_embeddings = image_index.reconstruct_n(0, n_image_vectors)

text_index = faiss.read_index(r"D:\CollegeWork\ShopLens-AR-Shopping-Assistant\server\notebooks\faiss_text.index")
n_text_vectors = text_index.ntotal
text_embeddings = text_index.reconstruct_n(0, n_text_vectors)

def get_text_based_rec(query, k=6):
    text_embedding = fclip.encode_text([query], 32)[0]

    similarities = text_embedding.dot(image_embeddings.T)

    top_k_indices = np.argsort(similarities)[-k:][::-1]

    product_ids = [map_idx_id(idx) for idx in top_k_indices]

    return product_ids

def get_image_based_rec(image: Image.Image, k=6):
    query_embedding = fclip.encode_images([image], batch_size=1)[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    query_embedding = np.expand_dims(query_embedding, axis=0).astype(np.float32)

    D, I = image_index.search(query_embedding, k=k)

    product_ids = [map_idx_id(idx) for idx in I[0]]

    return product_ids
