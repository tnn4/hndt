#!/usr/bin/env python3

import hnapi

def get_kids_from_first_item_from_route(route='top'):
    """print list as kids"""
    res = hnapi.get_stories_as_list(route)
    post_id = res[0]
    kids = hnapi.get_kids_from_id(post_id)
    print(kids)
#end

if __name__ == "__main__":
    get_kids_from_first_item_from_route()
#fi