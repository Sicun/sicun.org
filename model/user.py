#!/usr/bin/env python
# -*- coding: utf-8 -*-


class UserModel(object):
    def __init__(self, db):
        self.db = db

    def get_userinfo(self, user_id):
        select = "SELECT get_userinfo(%s)"
        userinfo = self.db.getjson(select, user_id)
        return userinfo

    def get_user_id(self, account):
        select = "SELECT get_user_id(%s)"
        user_id = self.db.getfirstfield(select, account)
        return user_id

    def do_login_user(self, account, password):
        select = "SELECT do_login_user(%s, %s)"
        user_id = self.db.getfirstfield(select, account, password)
        return user_id

    def do_register_user(self, email, password):
        select = "SELECT do_register_user(%s, %s)"
        hash_id = self.db.getfirstfield(select, email, password)
        return hash_id

    def do_activate_user(self, hash_id):
        select = "SELECT do_activate_user(%s)"
        user_id = self.db.getfirstfield(select, hash_id)
        return user_id
