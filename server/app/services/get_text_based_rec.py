import faiss
from fashion_clip.fashion_clip import FashionCLIP
from app.utils import map_idx_id
import numpy as np

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