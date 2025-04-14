# utils/sentiment_g.py
from transformers import pipeline, BertTokenizer, BertForSequenceClassification

# KoBertTokenizer 대체 구현
tokenizer = BertTokenizer.from_pretrained("monologg/kobert")
model = BertForSequenceClassification.from_pretrained("monologg/kobert")
korean_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    device=0  # GPU 사용
)

def analyze_single_news_ko(text: str) -> float:
    try:
        result = korean_sentiment_pipeline(text[:500])[0]
        label = result['label']
        score = result['score']
        return round(score if label == "POSITIVE" else -score, 2)
    except:
        return 0.0

def analyze_news(news_list: list) -> float:
    texts = [item['title'][:500] for item in news_list]
    results = korean_sentiment_pipeline(texts, batch_size=16)
    total = 0
    for item, result in zip(news_list, results):
        score = round(result['score'] if result['label'] == "POSITIVE" else -result['score'], 2)
        item['sentiment_score'] = score
        total += score
    return round(total / len(news_list), 2) if news_list else 0.0