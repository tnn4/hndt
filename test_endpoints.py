#!/usr/bin/env python3

print('Starting endpoint tests')

# rate limit
WAIT_TIME=1

import unittest
import time

import phnaw.phnaw as hnw

OK=200
NOT_FOUND=404
class TestEndpoints(unittest.TestCase):
    # newest
    # updates
    # top
    # new
    # best
    # ask
    # show
    # job
    # user
    def test_get_newest(self):
        self.assertEqual(hnw.ping_item_id('newest'), OK)
        time.sleep(WAIT_TIME)
    def test_get_top(self):
        self.assertEqual(hnw.ping_endpoint('updates'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_top(self):
        self.assertEqual(hnw.ping_endpoint('top'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_new(self):
        self.assertEqual(hnw.ping_endpoint('new'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_best(self):
        self.assertEqual(hnw.ping_endpoint('best'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_ask(self):
        self.assertEqual(hnw.ping_endpoint('ask'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_show(self):
        self.assertEqual(hnw.ping_endpoint('show'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_show(self):
        self.assertEqual(hnw.ping_endpoint('job'), OK)
        time.sleep(WAIT_TIME)
    #end
    def test_get_user(self):
        self.assertEqual(hnw.ping_endpoint('user'), OK)
        time.sleep(WAIT_TIME)
    #end
#end

def main():
    #print(phnaw.phnaw.get_items('top'))
    print(type(hnw.get_stories_id('x')))
    print(hnw.get_user('a'))
#end


if __name__ == "__main__":
    unittest.main()
#fi