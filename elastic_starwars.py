import requests
from elasticsearch import Elasticsearch
import json
from pprint import pprint

# make sure ES is up and running
r = requests.get('http://localhost:9200')

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# results when feeding data here
# https://github.com/ernestorx/es-swapi-test/blob/master/ES%20notebook.ipynb

i = 1

while r.status_code == 200:
  if i <= 10:
    r = requests.get('http://swapi.co/api/people/'+ str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i = i+1
  else:
    break
# we automatically created an index “sw” and a “doc_type” with de indexing command
pprint(i)

# try to get the document with id=5

pprint(es.get(index='sw', doc_type='people', id=5))

# To fetch more data from the api.
# comment out if you ran only one node
r = requests.get('http://localhost:9201')
i = 11

while r.status_code == 200:
  if i <= 20:
    r = requests.get('http://swapi.co/api/people/'+ str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i+ = 1
  else:
    break

# making query with name

pprint(es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}}))

# make a query with a prefix. (or regex kinda..)
pprint(es.search(index="sw", body={"query": {"prefix" : { "name" : "lu" }}}))

# to make a query for elements which are similar

pprint(es.search(index="sw", body={"query": {"fuzzy_like_this_field" : { "name" : {"like_text": "jaba", "max_query_terms":5}}}}))

# refer this link for other types of matches
# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
