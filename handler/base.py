from tornado.web import RequestHandler
from model.message import MessageModel
from model.user import UserModel


class BaseHandler(RequestHandler):
    @property
    def message(self):
        if not hasattr(self, "_message"):
            self._message = MessageModel(self.application.db)
        return self._message

    @property
    def user(self):
        if not hasattr(self, "_user"):
            self._user = UserModel(self.application.db)
        return self._user

    @property
    def user_id(self):
        return self.current_user
