# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/28 12:43
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from component.db.config import MongoConfig

_config = MongoConfig()

mongo = MongoClient(_config.host,
                    _config.port,
                    username=_config.username,
                    password=_config.password
                    )
try:
    # The ping command is cheap and does not require auth.
    mongo.admin.command('ping')
    print("mongodb connected")
except ConnectionFailure:
    raise ConnectionFailure("Server not available")
