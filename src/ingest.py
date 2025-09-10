import pandas as pd
from pathlib import Path
import json

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding='utf-8-sig')  # دعم UTF-8 للعربية
    expected_cols = {"تصنيف الشكوى", "مضمون الشكوى"}
    if not expected_cols.issubset(df.columns):
        print("تحذير: بعض الأعمدة مفقودة، سنحاول التعامل معها.")
    df = df.rename(columns={"تصنيف الشكوى": "category", "مضمون الشكوى": "text"})  # توحيد الأسماء
    return df

def save_raw_json(df: pd.DataFrame, filename="raw_complaints.json"):
    out_path = DATA_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)
    print(f"تم حفظ الخام: {out_path}")

if __name__ == "__main__":
    df = load_csv(str(DATA_DIR / "complains 2.csv"))
    save_raw_json(df)
    print(f"تم جلب {len(df)} شكوى.")
