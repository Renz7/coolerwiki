# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/28 11:06
"""
import os
from typing import Any

from pydantic import Field


def default_env_field(default: Any, env_name: str = None) -> Field:
    def get_env(name: str):
        _default = None
        if env_name:
            _default = os.environ.get(name)
        if _default is None:
            return default
        return _default

    return Field(default_factory=lambda: get_env(env_name), )
