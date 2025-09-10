from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd

def train_topic_model(texts: list, embeddings):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    topic_model = BERTopic(embedding_model=model, language="arabic", verbose=True, min_topic_size=5)
    topics, probs = topic_model.fit_transform(texts, embeddings)
    return topic_model, topics, probs

def get_topic_info(topic_model):
    return topic_model.get_topic_info()

def get_representative_docs(topic_model, topic_id, n=10):
    return topic_model.get_representative_docs(topic_id)[:n]

if __name__ == "__main__":
    df = pd.read_csv("data/processed_complaints.csv", encoding="utf-8")
    texts = df["clean_text"].tolist()
    from embed_store import generate_embeddings
    embs = generate_embeddings(texts)
    topic_model, topics, _ = train_topic_model(texts, embs)
    df["topic"] = topics
    df.to_csv("data/topics_assigned.csv", index=False, encoding="utf-8")
    info = get_topic_info(topic_model)
    print("أهم المواضيع:\n", info.head(5))
