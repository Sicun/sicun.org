#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.escape import json_encode
from base import BaseHandler


class UserBaseHandler(BaseHandler):
    def get_userinfo(self):
        userinfo = self.user.get_userinfo(self.user_id)
        return userinfo

    def get_user_id(self, account):
        user_id = self.user.get_user_id(account)
        return user_id


class HomeHandler(UserBaseHandler):
    def get(self, nickname):
        user_id = self.get_user_id(nickname)
        userinfo = self.get_userinfo()
        self.render("index.html", user=userinfo)


class LoginHandler(UserBaseHandler):
    def login(self, account, password):
        user_id = self.user.login(account, password)
        return user_id

    def get(self):
        self.render("index.html")

    def post(self):
        account = self.get_argument("account")
        password = self.get_argument("password")
        user_id = self.login(account, password)
        self.set_secure_cookie("uid", user_id)


class LogoutHandler(UserBaseHandler):
    def post(self):
        self.clear_cookie("uid")


class RegisterHandler(UserBaseHandler):
    def register(self, email, password):
        hash_id = self.user.login(email, password)
        return hash_id

    def get(self):
        self.render("index.html")

    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        hash_id = self.register(email, password)
