# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/28 12:46
"""

import click

from component.db.manage import db


@click.group
def manage():
    pass


manage.add_command(db, name="db")

if __name__ == '__main__':
    manage()
