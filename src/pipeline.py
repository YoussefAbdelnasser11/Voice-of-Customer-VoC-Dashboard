import pandas as pd
from ingest import load_csv, save_raw_json
from preprocess import preprocess_df
from embed_store import generate_embeddings, store_embeddings
from topic_model import train_topic_model
from sentiment_summary import init_sentiment_pipeline, analyze_sentiment, init_summarizer_pipeline, summarize_texts
from db_models import Session, Complaint, create_tables
from utils import send_email

def run_pipeline(csv_path: str):
    create_tables()
    df = load_csv(csv_path)
    save_raw_json(df)
    df = preprocess_df(df)
    texts = df["clean_text"].tolist()
    embs = generate_embeddings(texts)
    store_embeddings(df.index.tolist(), texts, embs)
    _, topics, _ = train_topic_model(texts, embs)
    df["topic"] = topics
    sent_pipe = init_sentiment_pipeline()
    df["sentiment"] = analyze_sentiment(texts, sent_pipe)
    sum_pipe = init_summarizer_pipeline()
    df["summary"] = summarize_texts(texts, sum_pipe)
    sess = Session()
    for _, row in df.iterrows():
        complaint = Complaint(
            category=row["category"],
            clean_text=row["clean_text"],
            summary=row["summary"],
            sentiment=row["sentiment"],
            topic_id=int(row["topic"])
        )
        sess.merge(complaint)
    sess.commit()
    print("تم الانتهاء من البايبلاين.")
    # إرسال إيميل في النهاية
    body = f"تم معالجة {len(df)} شكوى بنجاح. أهم 5 مواضيع: {df['topic'].value_counts().head(5).to_string()}"
    send_email("تقرير معالجة الشكاوى", body)

if __name__ == "__main__":
    run_pipeline("data/complains 2.csv")
