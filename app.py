from flask import Flask, request, jsonify, render_template
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('NEWS_API_KEY')

if not API_KEY:
    raise ValueError("Missing API key! Set NEWS_API_KEY as an environment variable.")

app = Flask(__name__)
newsapi = NewsApiClient(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sources', methods=['GET'])
def get_sources():
    sources = newsapi.get_sources()
    return jsonify(sources['sources'])

@app.route('/get_news', methods=['GET'])
def get_news():
    """Fetch top headlines based on user selections"""
    country = request.args.get('country')
    category = request.args.get('category')
    sources = request.args.get('sources')

    # Ensure only one search method is used
    if sources and (country or category):
        return jsonify({"error": "Cannot mix sources with country/category."}), 400

    if sources:
        top_headlines = newsapi.get_top_headlines(sources=sources)
    elif country:
        top_headlines = newsapi.get_top_headlines(country=country)
    elif category:
        top_headlines = newsapi.get_top_headlines(category=category)
    else:
        top_headlines = newsapi.get_top_headlines()

    return jsonify(top_headlines['articles'])

if __name__ == '__main__':
    app.run(debug=True)
