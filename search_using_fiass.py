import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pdf_parsing as pp

# Step 1: Load model and data
model = SentenceTransformer('all-MiniLM-L6-v2')
pdf_path = "sample-pdf.pdf"
chunks = pp.pdf_to_chunks(pdf_path, chunk_size=1024)

# Step 2: Encode chunks
embeddings = model.encode(chunks)

# Step 3: Normalize for cosine similarity
normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# Step 4: Build FAISS indices
cos_index = faiss.IndexFlatIP(embeddings.shape[1])
cos_index.add(normalized_embeddings.astype('float32'))

# Step 5: Query
query = "What is the main topic?"
query_emb = model.encode([query])
query_emb_norm = query_emb / np.linalg.norm(query_emb)

# Step 6: Search
D, I = cos_index.search(query_emb_norm.astype('float32'), k=5)

# Step 7: Show results
print("\nTop results:")
for idx in I[0]:
    print(f"\n--- Chunk {idx} ---\n{chunks[idx][:300]}...")
