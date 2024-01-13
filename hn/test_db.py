#!/usr/bin/env python3

DEBUG=True

import json
from types import SimpleNamespace

import time
import datetime
import os

import sqlite3
# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite

# Create virtual environment than install sqlalchemy
# pip install sqlachemy
# see: 
# https://docs.sqlalchemy.org/en/20/core/type_basics.html
# https://stackoverflow.com/questions/45604488/in-sqlalchemy-can-i-have-a-column-with-multiple-strings
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Numeric, Boolean, Date, DateTime, ARRAY, JSON
from sqlalchemy.orm import relationship

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL

# sqlite: insert or do nothing on conflict
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

# see: https://docs.sqlalchemy.org/en/20/core/engines.html
url_object = URL.create(
    "sqlite",
    database="test_hn.sqlite"
)

engine =  create_engine(url_object)
Session = sessionmaker(bind=engine)
session = Session()

import phnac as hndb

test_items = {
    "story": """
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
""",
    "comment": """
{
  "by" : "norvig",
  "id" : 2921983,
  "kids" : [ 2922097, 2922429, 2924562, 2922709, 2922573, 2922140, 2922141 ],
  "parent" : 2921506,
  "text" : "Aw shucks, guys ... you make me blush with your compliments.<p>Tell you what, Ill make a deal: I'll keep writing if you keep reading. K?",
  "time" : 1314211127,
  "type" : "comment"
}
""",

    "ask": """
{
  "by" : "tel",
  "descendants" : 16,
  "id" : 121003,
  "kids" : [ 121016, 121109, 121168 ],
  "score" : 25,
  "text" : "<i>or</i> HN: the Next Iteration<p>I get the impression that with Arc being released a lot of people who never had time for HN before are suddenly dropping in more often. (PG: what are the numbers on this? I'm envisioning a spike.)<p>Not to say that isn't great, but I'm wary of Diggification. Between links comparing programming to sex and a flurry of gratuitous, ostentatious  adjectives in the headlines it's a bit concerning.<p>80% of the stuff that makes the front page is still pretty awesome, but what's in place to keep the signal/noise ratio high? Does the HN model still work as the community scales? What's in store for (++ HN)?",
  "time" : 1203647620,
  "title" : "Ask HN: The Arc Effect",
  "type" : "story"
}
""",

    "job": """
{
  "by" : "justin",
  "id" : 192327,
  "score" : 6,
  "text" : "Justin.tv is the biggest live video site online. We serve hundreds of thousands of video streams a day, and have supported up to 50k live concurrent viewers. Our site is growing every week, and we just added a 10 gbps line to our colo. Our unique visitors are up 900% since January.<p>There are a lot of pieces that fit together to make Justin.tv work: our video cluster, IRC server, our web app, and our monitoring and search services, to name a few. A lot of our website is dependent on Flash, and we're looking for talented Flash Engineers who know AS2 and AS3 very well who want to be leaders in the development of our Flash.<p>Responsibilities<p><pre><code>    * Contribute to product design and implementation discussions\n    * Implement projects from the idea phase to production\n    * Test and iterate code before and after production release \n</code></pre>\nQualifications<p><pre><code>    * You should know AS2, AS3, and maybe a little be of Flex.\n    * Experience building web applications.\n    * A strong desire to work on website with passionate users and ideas for how to improve it.\n    * Experience hacking video streams, python, Twisted or rails all a plus.\n</code></pre>\nWhile we're growing rapidly, Justin.tv is still a small, technology focused company, built by hackers for hackers. Seven of our ten person team are engineers or designers. We believe in rapid development, and push out new code releases every week. We're based in a beautiful office in the SOMA district of SF, one block from the caltrain station. If you want a fun job hacking on code that will touch a lot of people, JTV is for you.<p>Note: You must be physically present in SF to work for JTV. Completing the technical problem at <a href=\"http://www.justin.tv/problems/bml\" rel=\"nofollow\">http://www.justin.tv/problems/bml</a> will go a long way with us. Cheers!",
  "time" : 1210981217,
  "title" : "Justin.tv is looking for a Lead Flash Engineer!",
  "type" : "job",
  "url" : ""
}
""",

    "poll": """
{
  "by" : "pg",
  "descendants" : 54,
  "id" : 126809,
  "kids" : [ 126822, 126823, 126993, 126824, 126934, 127411, 126888, 127681, 126818, 126816, 126854, 127095, 126861, 127313, 127299, 126859, 126852, 126882, 126832, 127072, 127217, 126889, 127535, 126917, 126875 ],
  "parts" : [ 126810, 126811, 126812 ],
  "score" : 46,
  "text" : "",
  "time" : 1204403652,
  "title" : "Poll: What would happen if News.YC had explicit support for polls?",
  "type" : "poll"
}
""",

    "poll_part": """
{
  "by" : "pg",
  "id" : 160705,
  "poll" : 160704,
  "score" : 335,
  "text" : "Yes, ban them; I'm tired of seeing Valleywag stories on News.YC.",
  "time" : 1207886576,
  "type" : "pollopt"
}
""",

}

test_users = [
    """
{
  "about" : "This is a test",
  "created" : 1173923446,
  "delay" : 0,
  "id" : "jl",
  "karma" : 2937,
  "submitted" : [ 8265435, 8168423, 8090946, 8090326, 7699907, 7637962, 7596179, 7596163, 7594569, 7562135, 7562111, 7494708, 7494171, 7488093, 7444860, 7327817, 7280290, 7278694, 7097557, 7097546, 7097254, 7052857, 7039484, 6987273, 6649999, 6649706, 6629560, 6609127, 6327951, 6225810, 6111999, 5580079, 5112008, 4907948, 4901821, 4700469, 4678919, 3779193, 3711380, 3701405, 3627981, 3473004, 3473000, 3457006, 3422158, 3136701, 2943046, 2794646, 2482737, 2425640, 2411925, 2408077, 2407992, 2407940, 2278689, 2220295, 2144918, 2144852, 1875323, 1875295, 1857397, 1839737, 1809010, 1788048, 1780681, 1721745, 1676227, 1654023, 1651449, 1641019, 1631985, 1618759, 1522978, 1499641, 1441290, 1440993, 1436440, 1430510, 1430208, 1385525, 1384917, 1370453, 1346118, 1309968, 1305415, 1305037, 1276771, 1270981, 1233287, 1211456, 1210688, 1210682, 1194189, 1193914, 1191653, 1190766, 1190319, 1189925, 1188455, 1188177, 1185884, 1165649, 1164314, 1160048, 1159156, 1158865, 1150900, 1115326, 933897, 924482, 923918, 922804, 922280, 922168, 920332, 919803, 917871, 912867, 910426, 902506, 891171, 807902, 806254, 796618, 786286, 764412, 764325, 642566, 642564, 587821, 575744, 547504, 532055, 521067, 492164, 491979, 383935, 383933, 383930, 383927, 375462, 263479, 258389, 250751, 245140, 243472, 237445, 229393, 226797, 225536, 225483, 225426, 221084, 213940, 213342, 211238, 210099, 210007, 209913, 209908, 209904, 209903, 170904, 165850, 161566, 158388, 158305, 158294, 156235, 151097, 148566, 146948, 136968, 134656, 133455, 129765, 126740, 122101, 122100, 120867, 120492, 115999, 114492, 114304, 111730, 110980, 110451, 108420, 107165, 105150, 104735, 103188, 103187, 99902, 99282, 99122, 98972, 98417, 98416, 98231, 96007, 96005, 95623, 95487, 95475, 95471, 95467, 95326, 95322, 94952, 94681, 94679, 94678, 94420, 94419, 94393, 94149, 94008, 93490, 93489, 92944, 92247, 91713, 90162, 90091, 89844, 89678, 89498, 86953, 86109, 85244, 85195, 85194, 85193, 85192, 84955, 84629, 83902, 82918, 76393, 68677, 61565, 60542, 47745, 47744, 41098, 39153, 38678, 37741, 33469, 12897, 6746, 5252, 4752, 4586, 4289 ]
}
"""
]

def test_create_database(db_name="test_hn.sqlite"):

    db = db_name

    
    if DEBUG:
        print(f"db_name={db}")
    #fi

    item_table="items"
    user_table="users"
    try:
        con = sqlite3.connect(db)
        print(f"Created database: {db}")
    except Error as e:
        print(e)
    #end
    cur = con.cursor()

    # Create db if it doesn't exist

    # Cursor executes a sql statement
    cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {item_table}
                    (id PRIMARY KEY, -- required
                    deleted NULL, 
                    type NULL, 
                    by NULL, 
                    time NULL, 
                    text NULL, 
                    dead NULL, 
                    parent NULL, 
                    poll NULL, 
                    kids NULL, 
                    url NULL, 
                    score NULL, 
                    title NULL, 
                    parts NULL, 
                    descendants NULL)
                    """)
    print(f"Created TABLE {item_table}")
    cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {user_table}
                    (id PRIMARY KEY, -- required
                    created NOT NULL, -- required
                    karma NOT NULL, -- required
                    delay,
                    about NULL, 
                    submitted NULL)
                """)
    print(f"Created TABLE {user_table}")
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
    item = hndb.Item(**j)
    # prints address of object
    #print(item)
    # prints object as dictionary
    #print(item.__dict__)

    # Process Unix Time
    dt = datetime.datetime.fromtimestamp(item.time)
    #print(dt)
#end



def test_insert_into_table_json(json_string=None):
    """
    params: json string
    json string deserialized to an items object and will be inserted into sqlite table as a row
    """

    # Create instances of your Items than try adding them to the database
    story_json = json.loads(test_items['story'])
    # print(story_json)
    
    # Deserialize JSON to object
    item_story = hndb.Item(**story_json)
    item_comment = hndb.deserialize_as_item(test_items['comment'])
    item_ask = hndb.deserialize_as_item(test_items['ask'])
    # convert json data into python object
    item_job_obj = json.loads(test_items['story'], object_hook=lambda d: SimpleNamespace(**d))

    print(f"type={type(item_comment.kids)}")

    # Add objectes to list
    obj_list = []
    obj_list_as_dict = []
    raw_obj_list = []
    raw_obj_list_as_dict = []

    obj_list.append(item_story)
    obj_list.append(item_comment)
    obj_list.append(item_ask)
    raw_obj_list.append(item_job_obj)

    for obj in obj_list:
        obj_list_as_dict.append(obj.__dict__)
    #end

    for obj in raw_obj_list:
        raw_obj_list_as_dict.append(obj.__dict__)

    print(f"raw_object_list={obj_list_as_dict}")

    # see: https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert
    stmt = sqlite_upsert(hndb.Item).values(
        raw_obj_list_as_dict
    )
    stmt = stmt.on_conflict_do_nothing(
        index_elements=['id']
    )
    hndb.session.execute(stmt)
    # Add Python objects to database
    # session.add_all(obj_list)
    for obj in obj_list:
        print(f"Adding {obj}")
        # You can use sql directly
        # https://stackoverflow.com/questions/63556777/sqlalchemy-add-all-ignore-duplicate-key-integrityerror
        # see: https://github.com/sqlalchemy/sqlalchemy/discussions/9675#discussioncomment-5668047
        # see: https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert
        # session.add(obj)
    #loop

    print("Session COMMIT")
    hndb.session.commit()

#end 

def test_query_table(class_name):
    for item in hndb.session.query(class_name):
        print(f"item.id={item.id}")
    #end
#end



def main():
    test_create_database()
    test_insert_into_table_json(test_users[0])
    test_insert_into_table_json(test_items['story'])
    #test_query_table(hndb.Item)
    #test_query_table(hndb.User)
#end

if __name__ == "__main__":
    main()
#end