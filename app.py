from flask import Flask, request, jsonify, render_template
from newsapi import NewsApiClient

app = Flask(__name__)
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')

@app.route('/')
def index():
    """Serve the frontend HTML page"""
    return render_template('index.html')

@app.route('/get_sources', methods=['GET'])
def get_sources():
    """Returns a list of available news sources"""
    sources = newsapi.get_sources()
    return jsonify(sources['sources'])

@app.route('/get_news', methods=['GET'])
def get_news():
    """Fetch top headlines based on user selections"""
    country = request.args.get('country')
    category = request.args.get('category')
    sources = request.args.get('sources')

    # Ensure only valid parameter combinations are used
    if sources and (country or category):
        return jsonify({"error": "Cannot mix sources with country/category"}), 400

    # Fetch top headlines
    top_headlines = newsapi.get_top_headlines(
        country=country if country != "all" else None,
        category=category if category != "all" else None,
        sources=sources if sources != "all" else None
    )

    return jsonify(top_headlines['articles'])

if __name__ == '__main__':
    app.run(debug=True)
