import re
import html
from langdetect import detect
from rapidfuzz import fuzz
import pandas as pd
from camel_tools.utils.normalize import normalize_alef_ar, normalize_alef_maksura_ar, normalize_teh_marbuta_ar

def normalize_arabic(text: str) -> str:
    text = normalize_alef_ar(text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_teh_marbuta_ar(text)
    text = re.sub(r"(.)\1{2,}", r"\1", text)  # إزالة التطويل
    text = re.sub(r"[ًٌٍَُِّْـ]", "", text)  # إزالة التشكيل
    return text.strip()

def clean_text(text: str) -> str:
    if not isinstance(text, str): return ""
    text = html.unescape(text)
    text = re.sub(r"http\S+", "", text)  # إزالة الروابط
    text = re.sub(r"\s+", " ", text)     # دمج المسافات
    text = re.sub(r"(?m)^>.*\n?", "", text)  # إزالة الاقتباسات
    text = normalize_arabic(text)
    return text

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def remove_duplicates(df: pd.DataFrame, text_col="clean_text", threshold=90) -> pd.DataFrame:
    texts = df[text_col].tolist()
    keep_indices = []
    for i, t in enumerate(texts):
        if all(fuzz.ratio(t, texts[j]) < threshold for j in keep_indices):
            keep_indices.append(i)
    return df.iloc[keep_indices].reset_index(drop=True)

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["clean_text"] = df["text"].apply(clean_text)
    df = df[df["clean_text"].str.len() > 10].reset_index(drop=True)  # إزالة النصوص القصيرة
    df["lang"] = df["clean_text"].apply(detect_language)
    df = remove_duplicates(df)
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/complains 2.csv", encoding="utf-8-sig")
    processed_df = preprocess_df(df)
    processed_df.to_csv("data/processed_complaints.csv", index=False, encoding="utf-8")
    print(f"تم معالجة {len(processed_df)} شكوى.")
