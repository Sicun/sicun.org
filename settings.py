#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
from tornado.options import define, options
from tornado.web import RequestHandler
from handler import base, message, user


urls = [
    (r"/", message.IndexHandler),
    (r"/m/notice", message.NoticeHandler),
    (r"/m/message", message.MessageHandler),
    (r"/u/(\w+)", user.HomeHandler),
]


define("host", default="localhost", type=str)
define("port", default=8888, type=int)
define("debug", default=True, type=bool)
define("dbname", default=os.getenv("SICUN_DB", "sicun"), type=str)
define("dbhost", default=os.getenv("SICUN_DB_HOST", "localhost"), type=str)
define("dbport", default=os.getenv("SICUN_DB_PORT", 5432), type=str)
define("dbuser", default=os.getenv("SICUN_DB_USER", "sicun"), type=str)
define("dbpasswd", default=os.getenv("SICUN_DB_PASSWD", "sicun"), type=str)
options.parse_command_line()

if options.debug:
    class DebugHandler(RequestHandler):
        def get(self, subpath):
            self.render(subpath)

    urls.append((r"/(.*)", DebugHandler))
    options.dbname += "_test"
else:
    urls.append((r".*", base.BaseHandler))

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    login_url="/login",
    host=options.host,
    port=options.port,
    debug=options.debug,
    cookie_secret=str(options.debug or uuid.uuid1().hex),
    session_secret=str(options.debug or uuid.uuid4().hex),
    dsn="dbname=" + options.dbname      \
       +" user=" + options.dbuser       \
       +" password=" + options.dbpasswd \
       +" host=" + options.dbhost       \
       +" port=" + str(options.dbport)
)
