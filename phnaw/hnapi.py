#!/usr/bin/env python3

# Python Hacker News  API Wrapper (PHNAW)

# rate limits
import time
WAIT_TIME=0.1

import os
import urllib.request
from enum import Enum
import json # for deserialization
import datetime # working with Unix Time
import sqlite3



HN_API_URL = "https://hacker-news.firebaseio.com/v0/"

class HnType(Enum):
    """Hacker News item type"""
    JOB = 1
    STORY = 2
    COMMENT = 3
    POLL = 4
    POLLOPT = 5
#end

# hacker news item as a class
class Item(object):
    def __init__(self):
        # unsigned
        self.id = ""
        # bool
        self.deleted: bool = False
        # enum
        self.type = "job | story | comment | poll | pollopt"
        # string
        self.by = "username of item's author"
        # UNIX TIME
        self.time = "creation time of th item in Unix time"
        # HTML
        self.text = "comment, story, or poll test in html"
        # BOOL
        self.dead = " true if item is dead"
        # another ITEM
        self.parent = "comment's parent; either another comment or relevant story"
        # POLL
        self.poll = "the pollopt's associated poll"

        self.kids = "ids of the items comments in ranked display order"
        # URL
        self.url = "url of the story"

        self.score = "the story's score or vortes for pollopt"
        # HTML
        self.title = "the titel of the story poll or job HTML"
        # 
        self.parts = "a list of related pollopts, in display order"
        # UNSIGNED
        self.descendants = " in the case of stories or polls, the total comment count"
    #end

    # Note that everything but id is optional
    def __init__(self, id, deleted=None, type=None, by=None, time=None, text=None, dead=None, parent=None, poll=None, kids=None, url=None, score=None, title=None, parts=None, descendants=None):
        """Every field is optional except for id"""
        self.id = id
        # bool
        self.deleted = deleted
        # enum
        self.type = type
        # string
        self.by = by
        # UNIX TIME
        self.time =  time
        # HTML
        self.text = text
        # BOOL
        self.dead = dead
        # another ITEM
        self.parent = parent
        # POLL
        self.poll = poll
        # ids of comments in display order
        self.kids = kids
        # URL
        self.url = url

        self.score = score
        # HTML
        self.title = title
        # 
        self.parts = parts
        # UNSIGNED
        self.descendants = descendants
    #end

#end

def item_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Item':
            return Item()
    return obj
# end

##
## Live Data
##

def get_stories(route):
    """
    Get updates, top, new, best, ask HN , show HN, job posts as a JSON String

    Args: 
        route=< 'updates' | top | new | best | ask | show | job >

    Returns:
        - JSON string of list of Hacker News item `ids`, if you want a actual List object use `get_stories_as_list()`
        - None if no route matches
    """
    match route:
        # updates
        case 'updates':
            _route='updates'
        # topstories
        case 'top':
            _route='topstories'
        # newstories
        case 'new':
            _route='newstories'
        # beststories
        case 'best':
            _route='beststories'
        # askstories
        case 'ask':
            _route='askstories'
        # showstories
        case 'show':
            _route='showstories'
        # jobstories
        case 'job':
            _route='jobstories'
        case _:
            print("ERR! unrecognized endpoint")
            return
    #end

    url=HN_API_URL+_route
    endpoint=url+".json"
    res_obj = urllib.request.urlopen(endpoint)
    contents = res_obj.read()
    try:
        json_string = contents.decode('utf-8')
    except:
        print("ERR! Unable to decode binary to UTF-8 string")
    #end

    return json_string
#end

def get_post_ids_from(route):
    """
    Get updates, top, new, best, ask HN , show HN, job posts as a JSON String

    Args: 
        route=< 'updates' | top | new | best | ask | show | job >

    Returns:
        - JSON string of list of Hacker News item `ids`, if you want a actual List object use `get_stories_as_list()`
        - None if no route matches
    """
    return get_stories(route)
#end

def get_stories_as_list(route):
    """
    Get updates, top, new, best, ask HN , show HN, job posts as Python List object

    Args: 
        route=< 'updates' | top | new | best | ask | show | job >

    Returns:
        - string of list of Hacker News item `ids`
        - None if no route matches
    """
    match route:
        # updates
        case 'updates':
            _route='updates'
        # topstories
        case 'top':
            _route='topstories'
        # newstories
        case 'new':
            _route='newstories'
        # beststories
        case 'best':
            _route='beststories'
        # askstories
        case 'ask':
            _route='askstories'
        # showstories
        case 'show':
            _route='showstories'
        # jobstories
        case 'job':
            _route='jobstories'
        case _:
            print("ERR! unrecognized endpoint")
            return
    #end

    url=HN_API_URL+_route
    endpoint=url+".json"
    res_obj = urllib.request.urlopen(endpoint)
    contents = res_obj.read()
    try:
        json_string = contents.decode('utf-8')
    except:
        print("ERR! Unable to decode binary to UTF-8 string")
    #end
    
    json_obj = json.loads(json_string)

    return json_obj
#end

def get_posts_as_list(route):
    """
    Get updates, top, new, best, ask HN , show HN, job posts as Python List object

    Args: 
        route: < 'updates' | 'top' | 'new' | 'best '| 'ask' | 'show' | 'job' >

    Returns:
        - string of list of Hacker News item `ids`
        - None if no route matches
    """
    return get_stories_as_list(route)
#end

def get_kids_from_posts(route):
    """
    args:
        route: < 'updates' | 'top' | 'new' | 'best '| 'ask' | 'show' | 'job' >
    
    returns:
        all kids from each post in a list : list of list .e.g [[ kids of post1 ] [kids of post2 ]... [ kids of postn ]]
    """
    
#end
    
def ping_endpoint(route):
    """
    Pings endpoints: updates, top, new, best, ask HN , show HN, job posts for testing

    Args: 
        route=< updates | top | new | best | ask | show | job >

    Returns:
        - 200 on OK
        - 404 on FAILURE
    """
    match route:
        # updates
        case 'updates':
            _route='updates'
        # topstories
        case 'top':
            _route='topstories'
        # newstories
        case 'new':
            _route='newstories'
        # beststories
        case 'best':
            _route='beststories'
        # askstories
        case 'ask':
            _route='askstories'
        # showstories
        case 'show':
            _route='showstories'
        # jobstories
        case 'job':
            _route='jobstories'
        case _:
            print("ERR! unrecognized endpoint")
            return
    #end

    url=HN_API_URL+_route
    endpoint=url+".json"
    res_obj = urllib.request.urlopen(endpoint)
    status_code = res_obj.getcode()
    
    return status_code
#end

##
## Users
##

def ping_user_endpoint(user="pg"):
    """
    Ping user endpoint with `user`
    """
    # 
    
    url=HN_API_URL+"/v0/user/"+user
    endpoint=url+".json"
    res_obj = urllib.request.urlopen(endpoint)
    status_code = res_obj.getcode()
    
    return status_code

#end

def get_user_json(id):
    """
    Get Hacker News user with `id`
    
    Args:
        `id` - id of user
    Returns:
        - If Not Found(404): `None`
        - OK(200): string, JSON
    """
    url = HN_API_URL + "/user/"
    endpoint = url+str(id)+".json"
    res_obj  = urllib.request.urlopen(endpoint)
    status_code = res_obj.getcode()
    
    if status_code == 200:
        contents = res_obj.read()
    else:
        return
    #fi
    
    try:
        json_str = contents.decode('utf-8')
    except:
        print("ERR! Unable to decode binary to UTF-8 string")
    #end

    return json_str
#end



# https://stackoverflow.com/questions/998938/handle-either-a-list-or-single-integer-as-an-argument
def get_items_from_ids(ids, max_items=10, all_items=False):
    """
    Get HN items from a list of `id`s

    Args:
        - ids - list of HN item ids, recommended to use with `get_stories_as_list(route)` to get a list of `id`s
        - max_items - maximum items to get, default: 10 (max for each endpoint is either 1 or  200 or 500)
        - all_items - process all item ids, overrides max items
    Returns:
        - res_list - list of: 
            - `JSON` objects if the response status was OK (200) OR
            - `None` on NOT_FOUND(404)
    """
    
    res_list = []
    
    # listify item to make processing easier
    # print(f"type={type(ids)}")
    if type(ids) is not list: ids = [ids]
    
    if all_items: max_items = len(ids)

    i = 0
    for id in ids:
        print("id: " + str(id))
        if i < max_items:
            item = get_item_from_id(id)
            res_list.append(item)
            print(f"GET: id={id}")
            # rate limit 
            time.sleep(WAIT_TIME)
            i+=1
        else:
            break
    #loop
    # print(f"id type = {type(res_list[0])}")

    return res_list
#end


def get_item_from_id(id):
    """
    Get hacker news item with `id`

    Args: 
        item id - unsigned
    Returns:
        - If Not Found(404): `None`
        - OK: Hacker news API response: string JSON
    """
    url=HN_API_URL

    # If user fields exist, then we know its a user
    if id == 'newest' or id == 'latest':
        endpoint=url+"maxitem.json"
    else:
        url=HN_API_URL+"item/"
        endpoint=url+str(id)+".json"
    #fi

    print(f"Sent HTTP GET to: {endpoint}")
    res_obj = urllib.request.urlopen(endpoint)
    
    status_code = res_obj.getcode()
    
    if status_code == 200:
        contents = res_obj.read()
    else:
        print(f"ERR! Response: {status_code}")
        return
    #fi

    try:
        json_str = contents.decode('utf-8')
    except:
        print("ERR! Unable to decode binary to UTF-8 string")
    #end

    return json_str
#end


##
## Item id
##

def ping_item_id(id):
    """
    Ping item id

    Args:
    - `id`: HN item id

    Returns:
    - Status Code: `200` on OK or otherwise
    """
    # If user fields exist, then we know its a user
    if id == 'newest' or id == 'latest':
        endpoint=url+"maxitem.json"
    else:
        url=HN_API_URL+"item/"
        endpoint=url+str(id)+".json"
    #fi

    res_obj = urllib.request.urlopen(endpoint)
    status_code = res_obj.getcode()
    
    return status_code
#end

def get_kids_from_id(id):
    """
    Get kids from item `id`.
    Gets the response than parses the `kids` field to generate a list of `ids`.
    """
    j = get_item_from_id(id)
    # get json as dict
    # get as object instead? https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
    jd = json.loads(j)
    # print(f"jo={jo}")
    # Check for field?
    # The general practice in python is that, if the property is likely to be there most of the time, 
    # simply call it and either let the exception propagate, or trap it with a try/except block.
    kids = jd['kids']

    return kids
#end

def test_get_item(id):
    
    url=HN_API_URL

    if id == 'newest' or id == 'latest':
        endpoint=url+"maxitem.json"
    else:
        url=HN_API_URL+"item/"
        endpoint=url+str(id)+".json"
    #fi
    print(f"GET: {endpoint}")
    #j = json.loads(item1)
    #item2 = Item(**j)
    #print(item2)

#end


def get_newest_item():
    """
    Get newest / latest Hacker News item

    Walk backwards from here to get all items
    Returns: id of newest item: string
    """
    url=HN_API_URL+"maxitem"
    endpoint=url+".json"
    res_obj = urllib.request.urlopen(endpoint)
    contents = res_obj.read()
    try:
        json_string = contents.decode('utf-8')
    except:
        print("ERR! Unable to decode binary to UTF-8 string")
    #end

    return json_string
#end


def test_mock_json():
    testItem1 = """
{
  "by" : "dhouston",
  "descendants" : 71,
  "id" : 8863,
  "kids" : [ 8952, 9224, 8917, 8884, 8887, 8943, 8869, 8958, 9005, 9671, 8940, 9067, 8908, 9055, 8865, 8881, 8872, 8873, 8955, 10403, 8903, 8928, 9125, 8998, 8901, 8902, 8907, 8894, 8878, 8870, 8980, 8934, 8876 ],
  "score" : 111,
  "time" : 1175714200,
  "title" : "My YC app: Dropbox - Throw away your USB drive",
  "type" : "story",
  "url" : "http://www.getdropbox.com/u/2/screencast.html"
}
"""
    j = json.loads(testItem1)
    print(j)
    # Deserialize JSON to object
    item = Item(**j)
    # prints address of object
    print(item)
    # prints object as dictionary
    print(item.__dict__)

    # Process Unix Time
    dt = datetime.datetime.fromtimestamp(item.time)
    print(dt)
#end

def main():
    contents = urllib.request.urlopen("http://example.com")
    test_mock_json()
#end

if __name__ == "__main__":
    main()
#end
