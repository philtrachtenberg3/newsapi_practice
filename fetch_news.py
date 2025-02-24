from newsapi import NewsApiClient
from dotenv import load_dotenv
import json
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('NEWS_API_KEY')

if not API_KEY:
    raise ValueError("Missing API key! Set NEWS_API_KEY as an environment variable.")

# Init
newsapi = NewsApiClient(api_key=API_KEY)

# Get top headlines
top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us')

# Get news sources
sources = newsapi.get_sources()

# Format output for readability
print("\n🔹 Top Business Headlines in the US 🔹\n")
for article in top_headlines['articles']:
    print(f"📰 {article['title']}")
    print(f"   🔗 {article['url']}\n")

# Sort sources by country
sorted_sources = sorted(sources['sources'], key=lambda x: x['country'])

print("\n🔹 Available News Sources 🔹\n")
for source in sorted_sources:
    print(f"📌 {source['name']} - {source['url'] if 'url' in source else 'No URL available'}, {source['country']}, {source['category']}")

# If you want full JSON output (optional)
# print(json.dumps(top_headlines, indent=4))
