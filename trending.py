#!/usr/bin/env python3

import unittest

import time

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

app = Flask(__name__)

@app.route("/")
def get_trending():
    return main()
#end

def get_unique(ls):
    unique_terms = set(ls)
    return unique_terms
#end

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
    top_items = hnapi.get_items_from_ids(top_ids,max_items=10)
    if debug:
        print(top_items)
    #end
    
    title_list = ""
    
    for json_item in top_items:
        j = json.loads(json_item)
        if debug:
            print("title: " + j["title"])
        #end
        title_list = title_list + " " + j["title"]
    #loop
    
    print("title_list:" + title_list)
    # Tokenize string
    title_list = title_list.lower()
    word_list = title_list.split()
    # Filter for terms
    filtered_terms = [word for word in word_list if word not in stopwords.words('english')]
    
    # Turn list back to string for printing
    filtered_string = ' '.join(t for t in filtered_terms)
    print("filtered terms: " + filtered_string)
    
    # filter for uniqueness
    unique_filtered_terms = get_unique(filtered_terms)
    unique_filtered_string = ', '.join(t for t in unique_filtered_terms)

    print(Counter(filtered_terms))
    # don't send count
    terms_as_dict_as_str = str(dict(Counter(filtered_terms)))
    
    # Dict with trending terms with count
    trending_terms_with_count = {
        "trending": terms_as_dict_as_str
    }

    # Dict with uniquw trending terms
    print("unique_filtered_string:" + unique_filtered_string)
    trending_terms = {
        "trending": unique_filtered_string
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
    return trending_terms_as_json
#end

if __name__ == "__main__":
    # unittest.main()
    main()
#end