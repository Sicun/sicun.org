#!/usr/bin/env python
# -*- coding: utf-8 -*-


class UserModel(object):
    def __init__(self, db):
        self.db = db

    def get_userinfo(self, user_id):
        return None

    def get_user_id(self, nickname):
        return None
