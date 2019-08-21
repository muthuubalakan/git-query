#!/usr/bin/python
# coding: utf-8
import os
import addict
import json
import sys
import logging
import asyncio
import pymongo
import requests
from aiohttp import web
from collections import OrderedDict


PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "gitcom")
STATIC = os.path.join(PATH, "app", "static")
INDEX_HTML = os.path.join(PATH, "app","index.html")
CONFIG_FILE = "assets/conf.json"

API = "https://api.github.com"

USER_REQ = "users"
REP_REQ = "repos"


log = logging.getLogger()
GIT_OAUTH = "https://github.com/login/oauth/authorize"


class AppView:

    @staticmethod
    def check_file(filename):
        if not os.path.isfile(filename):
            return False
        return open(filename).read()

    async def home(self, request):
        if not self.check_file(INDEX_HTML):
            return web.Response(text="<h6>Server Error</h6>")
        return web.Response(text=self.check_file(INDEX_HTML), content_type="text/html")

    async def git_auth(self, request):
        return web.HTTPFound(GIT_OAUTH)

    def get_json(self, url):
        return requests.get(url)

    async def gitsearch(self, request):
        post_data = await request.post()
        user = post_data.get('user', None)
        if not user: pass
        url = "{}/{}/{}/repos?".format(API, USER_REQ, user)
        resp = self.get_json(url)
        json_resp = resp.json()
        return web.json_response(json_resp)


def setup_routes(app):
    view = app["view"]
    app.router.add_route("GET", "/", view.home)
    app.router.add_route("POST", "/api/v1/gitsearch", view.gitsearch)
    app.router.add_route("GET", "/gitlogin", view.git_auth)
    app.router.add_static("/static/", STATIC, name="static")



def init_logging(conf):
    log_level_conf = "warning"
    if conf.common.logging:
        log_level_conf = conf.common.logging
    numeric_level = getattr(logging, log_level_conf.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(numeric_level))
    logging.basicConfig(level=numeric_level, format='%(message)s')
    log.error("Log level configuration: {}".format(log_level_conf))


def load_configuration_file(filename):
    with open(filename) as f:
        return addict.Dict(json.load(f))


def main(filename):
    app = web.Application()
    app["view"] = AppView()
    conf = load_configuration_file(filename)
    init_logging(conf)
    setup_routes(app)
    web.run_app(app, host=conf.common.host, port=conf.common.port)


if __name__ == '__main__':
    sys.stdout.write("Starting the App....\n")
    assert os.path.isfile(CONFIG_FILE),(
        'Configuration file required.'
    )
    main(CONFIG_FILE)
