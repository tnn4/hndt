#!/usr/bin/env python3

import unittest

import time

import random

import hn.api as hnapi
import hn.db as hndb

import hn

import json

from nltk.corpus import stopwords

def main():
    top_ids = hnapi.get_stories_as_list('top')
    # Show 10 items
    top_items = hnapi.get_items_from_ids(top_ids)
    print(top_items)
    
    title_list = ""
    
    for json_item in top_items:
        j = json.loads(json_item)
        print("title: " + j["title"])
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
    #hndb.create_database()
    # hn.cache_all_items()
    # hn.cache_posts('top')
    # hn.cache_posts('best')
    # hn.cache_all_items()
#end

if __name__ == "__main__":
    # unittest.main()
    main()
#end