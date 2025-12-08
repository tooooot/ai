import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import random

class NewsEngine:
    def __init__(self):
        self.archive = [] # Store all processed news
        # In a real scenario, we'd use actual RSS URLs.
        self.sources = [
            "https://www.argaam.com/ar/company/marketnews/rss", 
            # Add more specific RSS feeds here
        ]

    def fetch_latest_news(self):
        """
        Fetches news from sources. 
        Stores them in history for verification.
        """
        news_items = []
        # Simulation of news including Twitter source simulation
        simulated_news = [
            {"source": "Argaam", "title": "أرباح ربع سنوية قوية لقطاع البتروكيماويات تدعم السوق.", "url": "https://argaam.com/example1"},
            {"source": "AlRajhi Capital", "title": "توقعات بارتفاع الفائدة تضغط على أسهم البنوك.", "url": "https://alrajhi-capital.com/research"},
            {"source": "SPA (Twitter)", "title": "ولي العهد يعلن عن مبادرات استثمارية جديدة.", "url": "https://twitter.com/spagov/status/123"},
            {"source": "Reuters", "title": "انخفاض طفيف في أسعار النفط يؤثر على أرامكو.", "url": "https://reuters.com/oil"},
            {"source": "Tadawul", "title": "قطاع الأسمنت يشهد انتعاشاً في الطلب المحلي.", "url": "https://tadawul.com.sa/cement"}
        ]
        
        from datetime import datetime
        
        for item in simulated_news:
            sentiment = self.analyze_sentiment(item["title"])
            
            news_obj = {
                "id": len(self.archive) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": item["source"],
                "source_url": item["url"],
                "title": item["title"],
                "sentiment": sentiment,
                "score": 1 if sentiment == "Positive" else -1 if sentiment == "Negative" else 0
            }
            
            news_items.append(news_obj)
            # Add to archive (simple in-memory dedup could be good, but for demo just append)
            self.archive.insert(0, news_obj)
            
        return news_items

    def get_archive(self):
        return self.archive[:50] # Return last 50 items

    def analyze_sentiment(self, text):
        """
        Analyzes Arabic text sentiment.
        """
        positive_keywords = ['ارتفاع', 'نمو', 'أرباح', 'إيجابي', 'صعود', 'قوية', 'انتعاش', 'صفقة', 'مبادرات', 'استثمار']
        negative_keywords = ['انخفاض', 'خسارة', 'تراجع', 'سلبي', 'هبوط', 'ضعف', 'ضغط']
        
        score = 0
        for word in positive_keywords:
            if word in text:
                score += 1
        for word in negative_keywords:
            if word in text:
                score -= 1
                
        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        else:
            return "Neutral"
