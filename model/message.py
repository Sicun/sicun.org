#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MessageModel(object):
    def __init__(self, db):
        self.db = db

    def get_message_list(self, page=0, number=20):
        offset = page * number
        limit = number
        select = "SELECT get_message_list(%s, %s)"
        message_list = self.db.getjson(select, offset, limit)
        return message_list

    def get_reply_list(self, reply_to, page=0, number=20):
        offset = page * number
        limit = number
        select = "SELECT get_reply_list(%s, %s, %s)"
        reply_list = self.db.getjson(select, reply_to, offset, limit)
        return reply_list

    def get_notice(self, id):
        select = "SELECT get_notice(%s)"
        notice = self.db.getjson(select, id)
        return notice

    def get_message(self, id):
        select = "SELECT get_message(%s)"
        message = self.db.getjson(select, id)
        return message

    def create_notice(self, uid, title, content,
                      sort=None, place=None,
                      is_use_sms=False, is_use_email=False):
        select = "SELECT create_notice(%s, %s, %s, %s, %s, %s, %s)"
        notice_id = self.db.getjson(select, uid, title, content,
                                    sort, place, is_use_sms, is_use_email)
        return notice_id

    def create_message(self, uid, title, content):
        select = "SELECT create_message(%s, %s, %s)"
        message_id = self.db.getjson(select, uid, title, content)
        return message_id

    def create_reply(self, uid, content, reply_to):
        select = "SELECT create_reply(%s, %s, %s)"
        reply_id = self.db.getjson(select, uid, content, reply_to)
        return reply_id
