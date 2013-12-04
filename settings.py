#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, getenv
from uuid import uuid5, NAMESPACE_OID
from tornado.options import define, options
from lib.session import Session


define("host", default="localhost", type=str)
define("port", default=8888, type=int)
define("debug", default=True, type=bool)
define("dbname", default=getenv("SICUN_DB", "wutong"), type=str)
define("dbhost", default=getenv("SICUN_DB_HOST", "localhost"), type=str)
define("dbport", default=getenv("SICUN_DB_PORT", 5432), type=str)
define("dbuser", default=getenv("SICUN_DB_USER", "wutong"), type=str)
define("dbpasswd", default=getenv("SICUN_DB_PASSWD", "wutong"), type=str)
options.parse_command_line()

settings = dict(
    sitename=u"思存工作室".encode("utf8"),
    template_path=path.join(path.dirname(__file__), "templates"),
    static_path=path.join(path.dirname(__file__), "static"),
    xsrf_cookies=False,
    login_url="/login",
    autoescape=None,
    host=options.host,
    port=options.port,
    debug=options.debug,
)

settings["cookie_secret"] = str(uuid5(NAMESPACE_OID, settings["sitename"]))
settings["session_secret"] = str(uuid5(NAMESPACE_OID, settings["cookie_secret"]))
Session.register(settings["session_secret"])

urls = [
    #(r"/", user.HomeHandler),
]


if settings["debug"]:
    options.dbname += "_test"

    from tornado.web import RequestHandler
    class DebugHandler(RequestHandler):
        def get(self, subpath):
            self.render(subpath)

    urls.append((r"/(.*)", DebugHandler))


settings["dsn"] = "dbname={dbname} user={dbuser} password={dbpasswd} host={dbhost} port={dbport}".format(
                       dbname=options.dbname,
                       dbuser=options.dbuser,
                       dbpasswd=options.dbpasswd,
                       dbhost=options.dbhost,
                       dbport=options.dbport
                   )
