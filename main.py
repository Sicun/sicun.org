#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from settings import urls, settings
from model.db import Pool


def main():
    application = Application(urls, **settings)
    application.db = Pool.instance(settings["dsn"])
    http_server = HTTPServer(application)
    http_server.listen(settings["port"], settings["host"])
    IOLoop.instance().start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        pass
