WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SOLR_URI = 'http://localhost:8983/solr/'
NEWS_COLLECTION_INSTANCE = 'newsArticleCollection'

#TODO: Set this to the correct solr instance used to index wikipedia articles
WIKI_ARTICLE_INSTANCE = 'wikiArticleCollection'
SNIPPET_FRAGMENT_SIZE = 100
SNIPPET_MAX = 10
SNIPPET_OPENING = "<mark>"
SNIPPET_CLOSING = "</mark>"
SNIPPET_GENERATION = "true"
SNIPPET_FIELDS = "*"