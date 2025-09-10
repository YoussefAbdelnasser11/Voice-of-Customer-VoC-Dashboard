# Voice-of-Customer-VoC-Dashboard

# support-insights/
├── data/

│   └── complains 2.csv  # الملف اللي هتشتغل عليه (انسخ الداتا اللي فوق هنا)

├── src/
│   ├── ingest.py  # جلب الداتا من CSV
│   ├── preprocess.py  # تنظيف النصوص العربية وإزالة التكرارات
│   ├── embed_store.py  # حساب embeddings وتخزين في vector DB
│   ├── topic_model.py  # تجميع المواضيع بـ BERTopic
│   ├── sentiment_summary.py  # تحليل المشاعر والتلخيص
│   ├── db_models.py  # نماذج DB لـ Postgres
│   ├── utils.py  # دوال مساعدة، بما فيها إرسال إيميل
│   └── pipeline.py  # ربط كل الخطوات في سكربت واحد
├── app/
│   └── dashboard.py  # الداشبورد بـ Streamlit
├── .env  # للأسرار مثل DB_URL و SMTP credentials للإيميل
├── requirements.txt  # المكتبات
└── README.md  # وصف المشروع
