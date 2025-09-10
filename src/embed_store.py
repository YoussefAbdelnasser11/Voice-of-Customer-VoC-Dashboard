from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # دعم عربي جيد

client = chromadb.Client(Settings(persist_directory="./chroma_db"))

def get_collection():
    return client.get_or_create_collection(name="complaints")

def generate_embeddings(texts: list, batch_size=64):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    return embeddings

def store_embeddings(ids: list, texts: list, embeddings):
    collection = get_collection()
    collection.add(
        ids=[str(i) for i in ids],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"id": i} for i in ids]
    )
    print(f"تم تخزين {len(ids)} embeddings.")

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data/processed_complaints.csv", encoding="utf-8")
    texts = df["clean_text"].tolist()
    embs = generate_embeddings(texts)
    store_embeddings(df.index.tolist(), texts, embs)
