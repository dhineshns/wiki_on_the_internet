from flask.ext import restful
from flask import request, make_response
from utils import search, get_item, parse_to_alphanumeric
from .keyword_extractor import extract_keywords
from app import application, news, wiki
from flask.ext.restful import reqparse
from json import dumps


api = restful.Api()
parser = reqparse.RequestParser()

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api.representations = DEFAULT_REPRESENTATIONS


class Search(restful.Resource):
	def get(self,**kwargs):
		parser.add_argument('q', type=str)
		parser.add_argument('page', type=int)
		parser.add_argument('rows', type=int)

		args = parser.parse_args()

		qt = args.get('q')
		if not qt:
			qt = '*:*'

		rows = args.get('rows')
		if not rows:
			rows = 10

		page = args.get('page')
		if not page:
			page = 1

		query_terms = qt.split()

		query_term = query_terms[0]

		if len(query_terms)>1:
			query_term = "+".join(query_terms)

		search_results_ = search(wiki, query_term, page=page, rows=rows)

		error_message = "No results found for your search!"

		if search_results_:
			search_results = sear[0]
			result_snippets = sear [1]
			for res in search_results:
				_id = res['id']
				if _id in result_snippets:
					try:
						res['wiki_body'] = ("...").join(result_snippets[_id].get('wiki_body', []))
					except:
						del search_results[_id]
				else:
					del search_results[_id]

		if search_results:
			if len(search_results)>0:
				error_message = ""

		return dict(search_results=search_results, error_message=error_message, query_term=qt, current_page=page), 200
	def post(self,**kwargs):
		return


class SearchResult(restful.Resource):
	def get(self,**kwargs):
		result_id = kwargs.get('wiki_id')
		related_news = []
		related_tweets = []
		wiki_article = dict()
		news_articles = []

		wiki_article_solr = get_item(wiki, result_id)
		if wiki_article_solr:
			wiki_article = wiki_article_solr

		query_terms = []

		twitter_query = "";

		keywords = wiki_article.get('keywords',[])


		if not application.config.get('INDEX_KEYWORD_GENERATION'):
			keywords = extract_keywords(wiki_article['wiki_body'][0].encode('utf-8')).get('keywords')

		#since we are favoring precision over recall
		if len(keywords) > 1:
			for t in keywords:
				query_terms += t.split()
			query_term = "+".join(query_terms)
			twitter_query = " OR ".join(query_terms)

			news_articles = search(news, query_term)
		related_tweets = search_twitter(twitter_query) ;

		return dict(related_news=news_articles, wiki_article=wiki_article, related_tweets=related_tweets), 200
	def post(self, **kwargs):
		return

api.add_resource(Search, '/api/async/v1/')
api.add_resource(SearchResult, '/api/async/v1/results/<wiki_id>')