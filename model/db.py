#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import psycopg2
import logging
from psycopg2.extensions import TRANSACTION_STATUS_IDLE
from tornado.escape import json_decode


class Pool(object):
    @classmethod
    def instance(cls, dsn=None, min_size=1, max_size=10000):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(dsn, min_size, max_size)
        return cls._instance

    def __init__(self, dsn, min_size=1, max_size=10000):
        self.pool = []
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size

        assert max_size >= min_size > 0
        for i in xrange(self.min_size):
            self._new_connection()

    def execute(self, sql, *args):
        return self._get_connection().execute(sql, *args)

    def getfirstfield(self, sql, *args):
        return self._get_connection().getfirstfield(sql, *args)

    def getjson(self, sql, *args):
        return self._get_connection().getjson(sql, *args)

    def getitem(self, sql, *args):
        return self._get_connection().getitem(sql, *args)

    def getitems(self, sql, *args):
        return self._get_connection().getitems(sql, *args)

    def release(self):
        count_busy = 0
        for cnn in self.pool:
            if cnn.is_busy():
                count_busy += 1

        size = len(self.pool)
        count_free = 0
        if count_busy < self.min_size:
            for cnn in self.pool:
                if not cnn.is_busy():
                    cnn.close()
                    self.pool.remove(cnn)
                    count_free += 1
                if size - count_free == self.min_size:
                    break

    def _new_connection(self):
        cnn = Connection(self.dsn)
        self.pool.append(cnn)
        return cnn

    def _get_connection(self):
        for cnn in self.pool:
            if not cnn.is_busy():
                return cnn
        if len(self.pool) < self.max_size:
            return self._new_connection()


class Connection(object):
    def __init__(self, dsn):
        self.cnn = psycopg2.connect(dsn=dsn)
        self.cur = self.cnn.cursor()

    @property
    def closed(self):
        # 0 = open, 1 = closed, 2 = 'something horrible happened'
        return self.cnn.closed > 0

    def close(self):
        self.cur.close()
        self.cnn.close()

    def is_busy(self):
        return self.cnn.isexecuting() or (self.cnn.closed == 0 and
               self.cnn.get_transaction_status() != TRANSACTION_STATUS_IDLE)

    def getitems(self, sql, *args):
        self.execute(sql, *args)
        try:
            result = self.cur.fetchall()
        except:
            result = [[None]]
        return result

    def getitem(self, sql, *args):
        self.execute(sql, *args)
        try:
            result = self.cur.fetchone()
        except:
            result = [None]
        return result

    def getfirstfield(self, sql, *args):
        return self.getitem(sql, *args)[0]

    def getjson(self, sql, *args):
        result = self.getfirstfield(sql, *args)
        if isinstance(result, basestring):
            return json_decode(result)
        else:
            return result

    def execute(self, sql, *args):
        if not args: args = None
        try:
            self.cur.execute(sql, args)
            result = True
        except Exception as e:
            dbsql = self.cur.mogrify(sql, args)
            logging.error("SQL: `%s`", dbsql)
            logging.error(str(e))
            result = False
        self.cnn.commit()
        return result
