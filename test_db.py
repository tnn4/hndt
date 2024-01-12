#!/usr/bin/env python3

import unittest

import time
import random
import os
import json

import phnaw.hnapi as hnapi
import phnadb.db as hndb

SEC_IN_HR=3600

class TestDb(unittest.TestCase):
    def test_for_list(self):
        ids = hnapi.get_stories_asList('top')
        self.assertEqual(isinstance(ids, list), True)
    #end
#end

test_top_stories = [38381573,38375239,38379893,38378242,38380377,38377072,38381795,38380344,38378776,38378481,38361139,38379543,38379456,38380240,38381894,38359863,38378595,38379397,38376731,38378455,38378261,38376885,38368287,38381918,38379108,38379916,38346794,38381901,38362363,38375728,38378992,38371808,38364179,38378216,38379463,38377263,38357205,38361290,38372687,38380511,38376589,38376844,38371361,38376784,38357226,38361094,38380816,38380311,38365638,38373586,38354753,38381245,38373191,38364489,38351797,38366830,38369433,38360148,38372344,38361735,38370252,38353473,38368073,38352484,38380544,38362242,38374588,38362541,38370872,38374711,38368570,38377826,38346903,38366729,38360260,38356534,38354939,38360582,38343398,38347771,38362762,38366536,38362271,38364262,38371307,38370203,38361049,38367334,38372451,38371126,38368760,38363687,38360827,38366295,38357191,38363698,38358821,38360927,38368272,38361053,38378891,38362348,38378399,38343748,38365934,38362874,38373247,38368000,38379246,38373709,38344213,38374322,38374627,38342670,38360776,38369384,38373297,38375310,38377762,38354422,38378798,38361259,38363602,38357167,38378119,38361218,38361888,38375177,38362652,38353285,38370210,38360128,38379803,38354788,38364197,38335255,38361722,38368063,38360162,38376887,38341399,38344358,38378410,38343933,38357736,38349716,38368791,38377720,38379731,38372870,38343957,38378098,38343385,38358032,38364315,38372285,38360135,38361082,38371913,38367277,38370480,38377923,38363449,38376073,38353763,38368964,38366485,38338635,38365892,38363133,38371213,38372972,38376538,38375092,38364933,38376904,38367430,38367514,38374624,38344973,38371218,38368773,38361758,38365714,38351194,38351195,38367873,38365707,38372152,38370503,38372029,38342642,38374181,38357137,38346869,38377210,38354254,38343359,38376163,38338033,38355503,38375494,38370563,38353903,38370429,38351048,38363158,38366719,38373400,38361135,38345017,38343510,38359269,38379888,38356361,38375114,38369880,38365540,38356768,38352891,38360709,38371115,38353146,38351497,38345053,38368767,38362457,38376375,38361444,38366336,38371967,38369806,38365981,38378483,38343484,38366982,38374607,38344196,38366864,38354918,38366312,38369717,38351212,38365955,38361420,38337784,38340875,38369419,38354700,38371480,38350341,38341708,38369938,38373608,38375511,38374562,38351370,38374533,38375382,38359089,38360005,38361089,38353525,38367884,38345737,38368429,38336912,38345858,38347555,38366801,38370030,38363394,38361247,38374180,38374029,38369679,38347868,38362506,38353729,38350910,38369512,38370962,38374980,38369820,38344822,38377862,38345843,38361008,38356781,38349234,38371169,38340188,38370176,38366820,38374196,38370037,38364830,38363562,38346862,38336688,38367693,38360520,38371147,38342208,38347501,38334784,38339092,38353940,38360111,38337001,38353880,38372455,38356742,38356897,38367751,38367362,38359814,38366329,38356216,38366335,38364181,38340226,38360304,38359523,38365900,38352180,38365858,38354280,38341035,38375336,38358913,38370596,38339159,38375709,38365209,38361208,38373092,38355232,38372975,38365656,38348968,38372731,38372716,38369509,38369463,38369414,38357229,38365909,38365869,38368792,38348556,38360000,38352028,38375626,38371695,38368150,38334722,38371607,38365023,38356537,38350746,38338928,38371320,38348244,38372295,38339715,38371096,38360933,38376696,38354887,38359799,38364763,38343116,38341466,38370742,38370562,38337989,38370430,38348671,38365912,38345071,38338037,38344733,38373806,38344444,38359970,38361041,38369538,38369517,38340431,38359751,38365068,38365019,38334538,38359662,38359655,38356822,38356631,38364683,38366655,38356485,38338220,38337568,38368691,38368681,38370833,38337765,38363902,38357608,38362124,38345162,38352077,38342643,38361179,38357629,38349334,38359490,38362889,38346595,38355144,38361519,38346334,38366397,38338991,38362165,38358458,38360828,38356117,38365490,38359975,38361772,38358971,38355934,38359461,38361428,38368459,38378996,38361389,38354712,38337395,38345115,38346555,38338050,38336048,38359070,38353974,38335459,38349709,38336038,38339095,38369629,38358255,38359045,38353959,38335864,38338425,38339774,38335276,38343203,38357390,38352404,38339617,38358760,38373571,38337805,38341669,38335229,38336686,38347236,38355430,38378874,38365177,38358328,38337604,38358121,38364300,38361109,38361016,38352634,38352289,38354354,38356946,38374839,38360320,38342266,38337898,38337292,38355919,38352255,38340946,38349747,38348752,38355475,38340392,38355052,38340742,38345087,38345195,38345313,38336736]

def insert_into_table_from_endpoint_batched(route='top'):
    """finish all web requests than insert into database"""
    # get list of id from HN API endpoint
    # ids = hnapi.get_stories(route)
    ids = hnapi.get_stories_as_list(route)

    print(f"type={type(ids)}")
    print(ids)
    

    # ERR! 400 Bad Request
    res_list = hnapi.get_items_from_ids(ids, all_items=True)
    
    # insert objects into sqlite db
    # the JSON object must be str, bytes or bytearray, not list
    #
    #hndb.insert_into_table_json_ls(res_list)
    for item in res_list:
        hndb.insert_into_table_json(item)
    #loop
#end

def insert_into_table_from_endpoint(route='top'):
    """GET JSON than insert into database individually"""
    
    # rate limit
    # wait on random invterval
    sleep_times=[1, 1.1, 1.2, 1.3, 1.5]
    set_size=len(sleep_times)
    max=set_size-1
    random.seed(time.time())

    # get top item ids
    ids = hnapi.get_stories_as_list(route)

    # insert id into database
    for id in ids:
        # get item
        res = hnapi.get_item_from_id(id)
        # insert item into database
        hndb.insert_into_table_json(res)
        
        # rate limit
        wait=sleep_times[random.randint(0, max)]
        print(f'wait={wait}')
        time.sleep(wait)
    #loop
#end

def test_wait():
    ids = range(1, 20)

    # wait on random invterval
    sleep_times=[1, 1.1, 1.2, 1.3, 1.5]
    set_size=len(sleep_times)
    print(f"set_size={set_size}")
    random.seed(time.time())

    # Get each id with wait_time
    for id in ids:
        res = hnapi.get_item_from_id(id)
        hndb.insert_into_table_json(res)
        wait=sleep_times[random.randint(0, set_size-1)]
        print(f'wait={wait}')
        time.sleep(wait)
    #loop
#end

def get_stories(calls_per_hour=2400):
    wait_time = SEC_IN_HR / calls_per_hour
    ids = hnapi.get_stories_as_list('top')

    for id in ids:
        item = hnapi.get_item_from_id(id)
        hndb.insert_into_table_json(item)
        time.sleep(wait_time)
    #loop
#end

def cache_all_items(calls_per_hour=1000, start_from='newest', end=None):
    """
    Get all items from newest to oldest('DSC') or oldest to newest('ASC'))
    Starts from newest( max item) and walks backwards by default
    Newest has bigger id.

    Args:
    - calls_per_hour: default=1000 (to respect rate-limit)
    - start_from: ['newest' | 'oldest']  default='newest'
    - end: item id to stop at, 
        - if 'newest' default = oldest_item(1), 
        - if 'oldest' default = newest_item(max_item)
    
    direction ['DSC'| 'ASC']:

    'DSC' (descending)
    - max id  -> smallest
    - i.e. go from newest to oldest item
    'ASC' (ascending)
    - Start from 1
    - smallest(1) -> max id(newest)
    - i.e. go from oldest to newest item
    """
    increment = 1
    if start_from == 'newest':
        increment = -1
        direction = 'DSC'
    elif start_from == 'oldest':
        increment = 1
        direction = 'ASC'
    elif start_from is None:
        increment = -1
        direction = 'DSC'
    #fi

    

    # Big -> small id
    if direction == 'DSC' and end is None:
        start = hnapi.get_newest_item()
        end = 1
    elif direction == 'DSC' and end is not None:
        start = hnapi.get_newest_item()
        # Error handling
        if end > start:
            raise ValueError("Impossible to 'descend' to a bigger ID. Make sure end < start")
        #fi

    #fi


    # small -> Big id
    if direction == 'ASC' and end is None:
        start = 1
        end = hnapi.get_newest_item()
    elif direction == 'ASC' and end is not None:
        start = 1
        if end < 1:
            raise ValueError("Impossible to 'ascend' to a smaller ID. Make sure end > start")
        #fi
    #fi


    # Rate limit
    wait_time = SEC_IN_HR / calls_per_hour
    print(f"Calls per hour: {calls_per_hour }")
    # Get newest item
    newest_item = hnapi.get_newest_item()
    newest_item = int(newest_item)
    # print(f"newest_item={newest_item}")
    
    
    print(f"Starting from {start_from}. Ending at {end}")
    print(f"Rate limit: {calls_per_hour} calls / hr")
    print(f"""
start={start} {type(start)}
end={end} {type(end)}
increment={increment} {type(increment)}
          """)

    if isinstance(start, str):
        start = int(start)
    #fi
    if isinstance(end, str):
        end = int(end)
    #fi

    for id in range(start, end, increment):
        item = hnapi.get_item_from_id(id)
        print(f"GET item: {id}")
        time.sleep(wait_time)
        hndb.insert_into_table_json(item)
    #loop

        
    #fi


#end

def cache_posts(route, calls_per_hr=1000):
    """
    Cache posts and kids from endpoint into db

    Args:
    - route: < 'updates' | 'top' | 'new' | 'best '| 'ask' | 'show' | 'job' >
    """
    wait_time = SEC_IN_HR / calls_per_hr
    l = hnapi.get_posts_as_list(route)
    for id in l:
        # get item
        item = hnapi.get_item_from_id(id)
        hndb.insert_into_table_json(item)
        # get kids and insert into database
        jd = json.loads(item)
        
        # if the post has kids get them too
        if 'kids' in jd:
            kids = jd['kids']
            # insert kids into db
            for kid in kids:
                kid_item = hnapi.get_item_from_id(kid)
                hndb.insert_into_table_json(kid_item)
                time.sleep(wait_time)
            #loop
        #fi

        
        time.sleep(wait_time)
    #loop
#end

def main():
    pid = os.getpid()
    print(f"pid={pid}")

    hndb.create_database()
    
    # Test insert:
    # hndb.insert_into_table_json(hndb.test_users[0])
    # hndb.insert_into_table_json(hndb.test_items['story'])
    
    # Test query:
    # hndb.query_table(hndb.Item)
    # hndb.query_table(hndb.User)

    # insert_into_table_from_endpoint('top')
    # Test rate limit:
    # test_wait()

    # Test insert with all items:
    # get_all_items()
    # get_all_items(start_from='oldest')
    
    # Test insert with 
    cache_posts('top')
#end

if __name__ == "__main__":
    # unittest.main()
    main()
#end