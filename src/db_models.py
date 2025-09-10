from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/support_db")
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    clean_text = Column(Text)
    summary = Column(Text)
    sentiment = Column(String)
    topic_id = Column(Integer)

def create_tables():
    Base.metadata.create_all(engine)
    print("تم إنشاء الجداول.")

if __name__ == "__main__":
    create_tables()
