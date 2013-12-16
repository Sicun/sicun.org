from tornado.web import authenticated
from base import BaseHandler


class IndexHandler(BaseHandler):
    def get_messages(self, page=0):
        messages = self.message.get_messages()
        return messages

    def get(self):
        messages = self.get_messages()
        self.render("index.html", messages=messages)


class NoticeHandler(BaseHandler):
    def get_notice(self, notice_id):
        notice = self.message.get_notice(notice_id)
        return notice

    def create_notice(self, title, content, sort=None, place=None, is_use_sms=False, is_use_email=False):
        id = self.message.create_notice(self.user_id, title, content, sort, place, is_use_sms, is_use_email)
        return id

    @authenticated
    def get(self):
        notice_id = self.get_argument("notice_id", None)
        notice = self.get_notice(notice_id)
        self.write(notice)

    @authenticated
    def post(self):
        title = self.get_argument("title")
        content = self.get_argument("content")
        sort = self.get_argument("sort", None)
        place = self.get_argument("place", None)
        is_use_sms = self.get_argument("is_use_sms", None)
        is_use_email = self.get_argument("is_use_email", None)

        notice_id = self.create_notice(title, content, sort, place, is_use_sms, is_use_email)
        self.write(notice_id)


class MessageHandler(BaseHandler):
    def get_message(self, message_id):
        message = self.message.get_message(message_id)
        return message

    def create_message(self, title, content):
        id = self.message.create_notice(self.user_id, title, content)
        return id

    def get(self):
        message_id = self.get_argument("message_id", None)
        message = self.get_notice(message_id)
        self.write(notice)

    @authenticated
    def post(self):
        title = self.get_argument("title")
        content = self.get_argument("content")

        message_id = self.create_message(title, content)
        self.write(message_id)
