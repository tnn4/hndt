#!/usr/bin/env python3

import unittest

import time

import random

import hn.api as hnapi
import hn.db as hndb

import hn

import json



def main():
    top_ids = hnapi.get_stories_as_list('top')
    top_items = hnapi.get_items_from_ids(top_ids)
    print(top_items)
    for json_item in top_items:
        j = json.loads(json_item)
        print("title: " + j["title"])
    #loop
        
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