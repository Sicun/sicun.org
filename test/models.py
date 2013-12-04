#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from util import path
from model.db import Pool


class TestModelBase(unittest.TestCase):

    def setUp(self):
        self.dsn = "host=%s dbname=%s user=%s password=%s" % (
            "localhost", "sicun_test", "sicun", "sicun"
        )
        self.db = Pool.instance(self.dsn)


class TestDBModel(TestModelBase):

    def test(self):
        self.assertEqual(self.db.getfirstfield('SELECT 1'), 1)
        self.assertEqual(self.db.getjson("SELECT '1'"), 1)
        self.assertEqual(self.db.getitem('SELECT 1'), (1,))
        self.assertEqual(self.db.getitems('SELECT 1'), [(1,)])
        dirpath = path("model/dbschema/")
        sql = open(dirpath + "schema.sql", "r").read()
        self.assertTrue(self.db.execute(sql))


class TestUserModel(TestModelBase):

    def setUp(self):
        super(TestUserModel, self).setUp()
        #self.model = UserModel(self.db)

    def tearDown(self):
        #self.db.execute('DELETE FROM "user" *')
        pass

    def test(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDBModel("test"))
    suite.addTest(TestUserModel("test"))
    return suite

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__":
    main()
