# -*- coding:utf-8 -*-
"""
@author ren
@time 2022/9/28 10:41
"""
import os
from hashlib import md5
from os import path

import click
from loguru import logger

from .mongo import mongo


@click.group()
def db():
    click.echo("MongoDB manger...")


@db.command()
@click.option("--file", type=str, help="init data csv file")
@click.option("--collection", type=str, help="mongo collection", default="poetry")
@click.option("--database", type=str, help="mongo database", default="poetry")
def init(file: str, collection: str, database: str):
    click.echo("load data from {}".format(file))
    if path.isdir(file):
        for child in os.listdir(file):
            init(path.join(file, child), collection, database)
    else:
        if not file.endswith(".csv"):
            click.echo("ignore file {}", file)
            return
    database = mongo.get_database(database)
    col = database.get_collection(collection)
    try:
        import csv
        csv_file = csv.reader(open(file))
        batch = []
        batch_size = 500
        batch_count = 0
        for line in csv_file:
            title, dynasty, author, content = line
            digest = md5(content.encode()).hexdigest()
            batch.append({
                "title": title,
                "author": author,
                "content": content,
                "dynasty": dynasty,
                "md5": digest
            }
            )
            if len(batch) % batch_size == 0:
                col.insert_many(batch)
                batch_count += 1
                batch.clear()
                logger.info("insert batch[size:{}] {}", batch_size, batch_count)
        if batch:
            col.insert_many(batch)
    except Exception as e:
        click.echo("read csv file error {}".format(e))
