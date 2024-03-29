#!/usr/bin/env python3

import unittest

import time

from datetime import datetime

import random

import hn.api as hnapi
import hn.db as hndb

import hn

import json

from collections import Counter

# filter unnecessary terms
from nltk.corpus import stopwords

# web API
from flask import Flask




# Initialize flask api server
app = Flask(__name__)

@app.route("/")
def get_trending():
    return main()
#end

# Initialize templates

from jinja2 import Environment, PackageLoader, select_autoescape
jinja_env = Environment(
    loader=PackageLoader("trending"),
    autoescape=select_autoescape()
)

class HnPost:
    def __init__(self, title_, url_):
        self.title = title_
        if url_ is None:
            self.url = ""
        else:
            self.url = url_
        #fi
    #end
#end

def get_unique(ls):
    unique_terms = set(ls)
    return unique_terms
#end

MAX_ITEMS=20

def main(debug=False):
    # 500
    NEW_ITEMS = 'new'
    TOP_ITEMS = 'top'
    BEST_ITEMS = 'best'
    MAX_NEW_ITEMS = 500
    MAX_TOP_ITEMS = 500
    MAX_BEST_ITEMS = 500

    top_ids = hnapi.get_stories_as_list('top')
    # Show 10 items
    top_items = hnapi.get_items_from_ids(top_ids,max_items=MAX_ITEMS)
    if debug:
        print(top_items)
    #end
    
    all_titles_string = ""
    title_list = []
    url_list = []
    post_list = []
    for item in top_items:
        # j is json object
        j = json.loads(item)
        if debug:
            print("title: " + j["title"])
        #end
        all_titles_string = all_titles_string + " " + j["title"]
        title_list.append(j["title"])
        if "url" not in j:
            post_list.append(HnPost(j["title"], None))
        else:
            print("URL" + j["url"])
            url_list.append(j["url"])
            post_list.append(HnPost(j["title"], j["url"]))
        #fi
        
    #loop
    
    if debug:
        for t in title_list:
            print("title:" + t)
        #end
    #end
    
    # DEBUG
    # print(f"title_list: {title_list}")

    # Tokenize string
    all_titles_string = all_titles_string.lower()
    word_list = all_titles_string.split()
    # Filter for terms
    filtered_terms = [word for word in word_list if word not in stopwords.words('english')]
    
    # Turn list back to string for printing
    filtered_string = ' '.join(t for t in filtered_terms)
    # DEBUG
    # print("filtered terms: " + filtered_string)
    
    # filter for uniqueness
    unique_filtered_terms = get_unique(filtered_terms)
    unique_filtered_string = ', '.join(t for t in unique_filtered_terms)

    #print(Counter(filtered_terms))
    # don't send count
    terms_as_dict_as_str = str(dict(Counter(filtered_terms)))
    
    # Dict with trending terms with count
    trending_terms_with_count = {
        "trending": terms_as_dict_as_str
    }

    # Dict with uniquw trending terms
    # DEBUG
    # print("unique_filtered_string:" + unique_filtered_string)
    
    # Get date in %d/%m/%Y %H:%M:%S
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    
    # Create object to turn into json
    trending_terms = {
        "date": dt_string,
        "posts": title_list,
        "terms": unique_filtered_string
    }

    # Transform dictionary to Json
    trending_terms_with_count_as_json = json.dumps(trending_terms_with_count) 
    
    trending_terms_as_json = json.dumps(trending_terms)

    # Write to dictionary to file
    with open('hn-trending-terms.txt', 'w') as f:
        f.write(str(dict(Counter(filtered_terms))))
    #close
    
    # Write dictionary as Json to file
    with open('hn-trending-terms.json', 'w') as f:
        f.write(trending_terms_as_json)
    #close
    
    #hndb.create_database()
    # hn.cache_all_items()
    # hn.cache_posts('top')
    # hn.cache_posts('best')
    # hn.cache_all_items()
    
    # html template
    template = jinja_env.get_template("index.html")
    # we have to inject enumerate manually
    rendered_template = template.render(dict=trending_terms, titles=title_list, urls=url_list, posts=post_list, enumerate=enumerate)
    
    for idx , item in enumerate(title_list):
        print( str(idx) + item)
    #loop

    # return trending_terms_as_json
    return rendered_template
#end

if __name__ == "__main__":
    # unittest.main()
    main()
#end