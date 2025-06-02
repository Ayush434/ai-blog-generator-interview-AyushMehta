# seo_fetcher.py
import random

def get_seo_metrics(keyword):
    # Mock values
    search_volume = random.randint(1000, 10000)
    keyword_difficulty = round(random.uniform(10, 80), 2)  # Percent
    avg_cpc = round(random.uniform(0.1, 5.0), 2)  # Cost per click in dollars

    return {
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "avg_cpc": avg_cpc
    }
