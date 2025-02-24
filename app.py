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

@app.route('/get_countries', methods=['GET'])
def get_countries():
    """Get a list of available countries from NewsAPI sources"""
    sources = newsapi.get_sources()

    country_codes = set()
    for source in sources['sources']:
        if source['country']:
            country_codes.add(source['country'].upper())

    return jsonify(sorted(list(country_codes)))  # Return sorted list of unique country codes


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
        # Instead of directly using the country parameter,
        # fetch sources for that country and then get headlines from those sources.
        sources_result = newsapi.get_sources(country=country)
        source_ids = [source['id'] for source in sources_result['sources']]
        if source_ids:
            top_headlines = newsapi.get_top_headlines(sources=",".join(source_ids))
        else:
            top_headlines = {"articles": []}
    elif category:
        top_headlines = newsapi.get_top_headlines(category=category)
    else:
        top_headlines = newsapi.get_top_headlines()

    # Return an error message if no articles found.
    if not top_headlines.get('articles'):
        return jsonify({"error": "No news found for the selected criteria."})

    return jsonify(top_headlines['articles'])

if __name__ == '__main__':
    app.run(debug=True)
