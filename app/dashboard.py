import streamlit as st
import pandas as pd
from src.db_models import Session, Complaint
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

def load_data():
    sess = Session()
    complaints = sess.query(Complaint).all()
    data = [{"id": c.id, "category": c.category, "summary": c.summary, "sentiment": c.sentiment, "topic_id": c.topic_id} for c in complaints]
    return pd.DataFrame(data)

st.title(reshape_arabic("لوحة تحكم رؤى الشكاوى"))

df = load_data()

# Top 5 topics
st.subheader(reshape_arabic("أكثر 5 مشاكل متكررة"))
topic_counts = df["topic_id"].value_counts().head(5)
st.bar_chart(topic_counts)

# Sentiment distribution
st.subheader(reshape_arabic("توزيع المشاعر"))
sent_counts = df["sentiment"].value_counts()
st.bar_chart(sent_counts)

# Drill-down
selected_topic = st.selectbox(reshape_arabic("اختر موضوعًا"), topic_counts.index)
filtered = df[df["topic_id"] == selected_topic]
st.dataframe(filtered[["id", "category", "summary", "sentiment"]].applymap(reshape_arabic))

# Export
if st.button(reshape_arabic("تصدير CSV")):
    filtered.to_csv("export.csv", index=False, encoding="utf-8")
    st.success(reshape_arabic("تم التصدير."))
