# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/28 10:56
"""
from pydantic import BaseModel

from util.env_util import default_env_field


class MongoConfig(BaseModel):
    host: str = default_env_field("localhost", "MONGO_HOST")
    port: int = default_env_field(27017, "MONGO_PORT")
    username: str = default_env_field("root", "MONGO_USERNAME")
    password: str = default_env_field("example", "MONGO_PASSWORD")
