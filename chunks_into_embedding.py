import pdf_parsing as pp
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode chunks
embeddings = model.encode(pp.chunks)