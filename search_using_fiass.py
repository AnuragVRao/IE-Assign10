from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from chunks_into_embedding import embeddings


model = SentenceTransformer('all-MiniLM-L6-v2')


# Normalize for cosine similarity
normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# Cosine similarity FAISS index
cos_index = faiss.IndexFlatIP(embeddings.shape[1])
cos_index.add(normalized_embeddings.astype('float32'))

# Dot-product similarity FAISS index
dot_index = faiss.IndexFlatIP(embeddings.shape[1])
dot_index.add(embeddings.astype('float32'))

# Query
query = "What is the main topic?"
query_emb = model.encode([query], convert_to_numpy=True)

# Cosine similarity search
query_emb_norm = query_emb / np.linalg.norm(query_emb)
D, I = cos_index.search(query_emb_norm.astype('float32'), k=5)

# Dot-product search
D2, I2 = dot_index.search(query_emb.astype('float32'), k=5)

print("Cosine results:", I)
print("Dot-product results:", I2)