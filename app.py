# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from seo_fetcher import get_seo_metrics
from ai_generator import generate_blog_post
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

load_dotenv()
OPENAI_API_KEY = os.getenv("ai-blog-generator")

app = Flask(__name__)

PREDEFINED_KEYWORD = "wireless earbuds"

@app.route("/")
def home():
    return "Flask is running!"

def generate_and_save(keyword):
    seo_metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, seo_metrics)

    # Replace placeholders with dummy URLs
    post = post.replace("{{AFF_LINK_1}}", "https://www.amazon.com/Bluetooth-Headphones-Cancelling-Earphones-Waterproof/dp/B0CX1TJ228/ref=asc_df_B0CX1TJ228?tag=bingshoppinga-20&linkCode=df0&hvadid=80814295299799&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=&hvtargid=pla-4584413765559018&msclkid=a61113820e7b188f1d667bbeeb0ca4e5&th=1")
    post = post.replace("{{AFF_LINK_2}}", "https://goaxil.com/products/gx-extreme?variant=33887794561083&msclkid=bc72d9da694819380f48b1e68c3f2c3d")
    post = post.replace("{{AFF_LINK_3}}", "https://goaxil.com/products/nascar-xcor?msclkid=4558813ee68c1a6ee01ae90203fb2019")

    filename = f"generated_{keyword.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w") as f:
        f.write(post)
    print(f"Generated post saved to {filename}")

@app.route("/generate", methods=["GET"])
@app.route("/generate/", methods=["GET"])
def generate():
    print("🎯 /generate endpoint called")
    keyword = request.args.get("keyword", "wireless earbuds")  # default fallback

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    seo_metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, seo_metrics)

    # Replace placeholders
    post = post.replace("{{AFF_LINK_1}}", "https://www.amazon.com/Bluetooth-Headphones-Cancelling-Earphones-Waterproof/dp/B0CX1TJ228/ref=asc_df_B0CX1TJ228?tag=bingshoppinga-20&linkCode=df0&hvadid=80814295299799&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=&hvtargid=pla-4584413765559018&msclkid=a61113820e7b188f1d667bbeeb0ca4e5&th=1")
    post = post.replace("{{AFF_LINK_2}}", "https://goaxil.com/products/gx-extreme?variant=33887794561083&msclkid=bc72d9da694819380f48b1e68c3f2c3d")
    post = post.replace("{{AFF_LINK_3}}", "https://goaxil.com/products/nascar-xcor?msclkid=4558813ee68c1a6ee01ae90203fb2019")

    return jsonify({
        "keyword": keyword,
        "seo_metrics": seo_metrics,
        "blog_post": post
    })

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # Schedule daily job at 7 AM local time
    scheduler.add_job(lambda: generate_and_save(PREDEFINED_KEYWORD), 'cron', hour=7)
    scheduler.start()
    app.run(debug=True)

