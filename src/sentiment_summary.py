from transformers import pipeline
import pandas as pd

SENT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual"  # دعم عربي
SUM_MODEL = "UBC-NLP/AraT5v2-base-1024"  # تلخيص عربي

def init_sentiment_pipeline():
    return pipeline("sentiment-analysis", model=SENT_MODEL)

def init_summarizer_pipeline():
    return pipeline("summarization", model=SUM_MODEL)

def analyze_sentiment(texts: list, pipe, batch_size=32):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        results.extend(pipe(batch))
    return [r["label"] for r in results]

def summarize_texts(texts: list, pipe, max_len=100, min_len=20, batch_size=4):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        out = pipe(batch, max_length=max_len, min_length=min_len)
        results.extend([o["summary_text"] for o in out])
    return results

def summarize_topic(docs: list, pipe):
    joined = " ".join(docs)
    return pipe(joined, max_length=120, min_length=40)[0]["summary_text"]

if __name__ == "__main__":
    df = pd.read_csv("data/topics_assigned.csv", encoding="utf-8")
    texts = df["clean_text"].tolist()
    sent_pipe = init_sentiment_pipeline()
    df["sentiment"] = analyze_sentiment(texts, sent_pipe)
    sum_pipe = init_summarizer_pipeline()
    df["summary"] = summarize_texts(texts, sum_pipe)
    df.to_csv("data/analyzed_complaints.csv", index=False, encoding="utf-8")
    print("تم التحليل والتلخيص.")
