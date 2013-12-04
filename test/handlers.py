#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests
from util import path


class TestHandlerBase(unittest.TestCase):

    def setUp(self):
        self.url = "http://localhost:8888"

    def tearDown(self):
        pass


class TestUserHandler(TestHandlerBase):

    def test(self):
        req = requests.post(self.url + "/", data=dict())
        cookies = req.cookies
        req = requests.get(self.url + "/", cookies=cookies)
        req = requests.post(self.url + "/", cookies=cookies)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUserHandler("test"))
    return suite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__":
    main()
