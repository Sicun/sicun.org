class MessageModel(object):
    def __init__(self, db):
        self.db = db

    def get_messages(self, offset=0, limit=20):
        return None

    def get_notice(self, id):
        return None

    def get_message(self, id):
        return None

    def create_notice(self, uid, title, content, sort=None, place=None, is_use_sms=False, is_use_email=False):
        return None

    def create_message(self, uid, title, content):
        return None
