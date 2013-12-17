#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import authenticated
from base import BaseHandler


class MessageBaseHandler(BaseHandler):
    def get_reply_list(self, reply_to, page=0):
        reply_list = self.message.get_reply_list(reply_to, page)
        return reply_list


class IndexHandler(MessageBaseHandler):
    def get_message_list(self, page=0):
        message_list = self.message.get_message_list(page)
        return message_list

    def get(self):
        message_list = self.get_message_list()
        self.render("index.html", message_list=message_list)


class NoticeHandler(MessageBaseHandler):
    def get_notice(self, notice_id):
        notice = self.message.get_notice(notice_id)
        return notice

    @authenticated
    def get(self, notice_id):
        notice = self.get_notice(notice_id)
        reply_list = self.get_reply_list(notice_id)
        self.render("index.html", notice=notice, reply_list=reply_list)


class MessageHandler(MessageBaseHandler):
    def get_message(self, message_id):
        message = self.message.get_message(message_id)
        return message


    def get(self, message_id):
        message = self.get_message(message_id)
        reply_list = self.get_reply_list(message_id)
        self.render("index.html", message=message, reply_list=reply_list)


class CreateMessageHandler(MessageBaseHandler):
    def create_message(self, title, content):
        id = self.message.create_notice(self.user_id, title, content)
        return id

    def create_notice(self, title, content,
                      sort=None,
                      place=None,
                      is_use_sms=False,
                      is_use_email=False):
        id = self.message.create_notice(self.user_id,
                                        title, content,
                                        sort,
                                        place,
                                        is_use_sms,
                                        is_use_email)
        return id

    @authenticated
    def post(self):
        message_sort = self.get_argument("message_sort")
        title = self.get_argument("title")
        content = self.get_argument("content")
        sort = self.get_argument("sort", None)
        place = self.get_argument("place", None)
        is_use_sms = self.get_argument("is_use_sms", None)
        is_use_email = self.get_argument("is_use_email", None)

        if message_sort == "notice":
            id = self.create_notice(title, content,
                                    sort,
                                    place,
                                    is_use_sms,
                                    is_use_email)
        elif message_sort == "message":
            id = self.create_message(title, content)

        self.write(id)
