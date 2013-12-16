#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler


class HomeHandler(BaseHandler):
    def get_userinfo(self):
        userinfo = self.user.get_userinfo(self.user_id)
        return userinfo

    def get_user_id(self, nickname):
        user_id = self.user.get_user_id(nickname)
        return user_id

    def get(self, nickname):
        user_id = self.get_user_id(nickname)
        userinfo = self.get_userinfo()
        self.render("index.html", user=userinfo)


class UserInfoHandler(BaseHandler):
    pass
