import json
import os
import openai
import requests

openai.api_key = os.getenv("ai-blog-generator")

AFFILIATE_LINKS = {
    "AFF_LINK_1": "https://www.amazon.com/Bluetooth-Headphones-Cancelling-Earphones-Waterproof/dp/B0CX1TJ228/ref=asc_df_B0CX1TJ228?tag=bingshoppinga-20&linkCode=df0&hvadid=80814295299799&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=&hvtargid=pla-4584413765559018&msclkid=a61113820e7b188f1d667bbeeb0ca4e5&th=1",
    "AFF_LINK_2": "https://goaxil.com/products/gx-extreme?variant=33887794561083&msclkid=bc72d9da694819380f48b1e68c3f2c3d",
    "AFF_LINK_3": "https://goaxil.com/products/nascar-xcor?msclkid=4558813ee68c1a6ee01ae90203fb2019",
}

def generate_blog_post(keyword, seo_metrics):
    prompt = f"""
    You are an expert SEO blog writer.

    Write a detailed blog post about "{keyword}" including an intro, 3 subheadings with paragraphs, and a conclusion.

    Insert 3 affiliate links as {{AFF_LINK_1}}, {{AFF_LINK_2}}, and {{AFF_LINK_3}} throughout the post.

    Also, mention the following SEO metrics naturally:
    - Monthly search volume: {seo_metrics['search_volume']}
    - Keyword difficulty: {seo_metrics['keyword_difficulty']}%
    - Average CPC: ${seo_metrics['avg_cpc']}

    Format the output in Markdown.
    """

    try:
        print("Trying OpenAI API...")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        post_content = response.choices[0].message.content
        for placeholder, link in AFFILIATE_LINKS.items():
            post_content = post_content.replace(f"{{{{{placeholder}}}}}", link)
        return post_content
    except Exception as e:
        # Try with DeepSeek API key if OpenAI fails
        try:
            print("Trying Groq API...")
            groq_api_key = os.getenv("groq-api-key")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {groq_api_key}"
            }
            payload = {
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024,
                "temperature": 0.7,
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            if response.status_code == 200:
                data = response.json()
                post_content = data["choices"][0]["message"]["content"]
                for placeholder, link in AFFILIATE_LINKS.items():
                    post_content = post_content.replace(f"{{{{{placeholder}}}}}", link)
                return post_content
            else:
                return f"Groq API error: {response.status_code} - {response.text}"
       
        except Exception as e2:
                    return f"Both OpenAI and Groq API calls failed: {str(e2)}"
