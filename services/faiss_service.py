import faiss
import numpy as np

def store_embeddings_faiss(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def retrieve_relevant_chunks(index, question, model):
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k=5)
    return indices
