import requests
from bs4 import BeautifulSoup
# Ensure we don't depend on lxml
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
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
        # Enhanced Simulation with Market Context
        simulated_news = [
            {"source": "Argaam", "title": "أرباح ربع سنوية قوية لقطاع البتروكيماويات تفوق التوقعات.", "url": "#"},
            {"source": "AlRajhi Capital", "title": "توقعات بارتفاع الفائدة قد تضغط على هوامش ربحية البنوك.", "url": "#"},
            {"source": "SPA (Twitter)", "title": "ولي العهد يعلن عن مبادرات استثمارية ضخمة في قطاع التكنولوجيا.", "url": "#"},
            {"source": "Reuters", "title": "ارتفاع مفاجئ في أسعار النفط يدفعه لتجاوز 90 دولاراً.", "url": "#"},
            {"source": "Tadawul", "title": "قطاع الأسمنت يشهد انتعاشاً ملحوظاً بدعم من المشاريع الكبرى.", "url": "#"},
            {"source": "Bloomberg", "title": "صناديق عالمية تزيد من وزن السوق السعودي في مؤشراتها.", "url": "#"},
            {"source": "CNBC Arabia", "title": "مخاوف من ركود عالمي تسيطر على معنويات المتداولين.", "url": "#"}
        ]
        
        # Pick 3 random items to keep feed fresh but not overwhelming
        import random
        selected_news = random.sample(simulated_news, 3)
        
        from datetime import datetime
        
        for item in selected_news:
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
            
            # Avoid exact duplicates in top 5
            if not any(n['title'] == news_obj['title'] for n in self.archive[:5]):
                news_items.append(news_obj)
                self.archive.insert(0, news_obj)
            
        return news_items

    def get_archive(self):
        return self.archive[:50] # Return last 50 items

    def analyze_sentiment(self, text):
        """
        Analyzes Arabic text sentiment with expanded vocabulary.
        """
        positive_keywords = [
            'ارتفاع', 'نمو', 'أرباح', 'إيجابي', 'صعود', 'قوية', 'انتعاش', 
            'صفقة', 'مبادرات', 'استثمار', 'مكاسب', 'توسع', 'قفزة', 'تدشين', 
            'زيادة', 'تجاوز'
        ]
        negative_keywords = [
            'انخفاض', 'خسارة', 'تراجع', 'سلبي', 'هبوط', 'ضعف', 'ضغط', 
            'مخاوف', 'انهيار', 'تعثر', 'ركود', 'أزمة', 'عقوبات'
        ]
        
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
