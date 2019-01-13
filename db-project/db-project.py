from pathlib import Path
import argparse
import os

import mysql.connector
from loguru import logger

from db.utils import timeit_context
import db.req1 as req1


team = 0


def requirement1(
    host,
    user,
    password,
    directory,
    max_allowed_packet,
    chunk_size,
):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")

    with timeit_context("Drop database & Create Database"):
        cursor.execute("drop database DMA_team%02d;" % team)
        cursor.execute("CREATE DATABASE IF NOT EXISTS DMA_team%02d;" % team)
        cursor.execute("USE DMA_team%02d;" % team)

    cursor.execute(f"SET GLOBAL max_allowed_packet={max_allowed_packet};")

    with timeit_context("Create empty tables"):
        req1.create_tables(cursor)

    tables = ["user", "review", "attribute", "business", "category",
              "checkin", "photo", "tip", "vip_history"]

    # Performance Note on user Table
    # insert_bulk chunk_size = 20000, 59 seconds
    # insert_bulk chunk_size = 50000, 51 seconds
    # insert_bulk chunk_size = 100000, 50 seconds
    # After SET bulk_insert_buffer_size,
    # insert_bulk chunk_size = 100000, 1 minute and 1.51 second
    # After removing every variables,
    # insert_bulk chunk_size = 200000, 55 seconds
    # After max_allowed_packet = 2G,
    # insert_bulk chunk_size = 200000, 59 seconds
    # After max_allowed_packet = 2G,
    # insert_bulk chunk_size = 200000, 59 seconds

    for table in tables:
        with timeit_context(f"Insert {table} table"):
            rows = req1.read_data(Path(directory) / f"{table}.txt")
            counts = req1.select_count(cursor, table)
            if counts == len(rows):
                logger.info(f"{table} already contains data (nrows: {counts})")
                continue
            else:
                logger.info(
                    f"{table} has {counts} rows, but it should be {len(rows)}"
                )
                cursor.execute(f"DELETE FROM {table};")
                with timeit_context(f"Cleanup {table} data in-place"):
                    req1.cleanup_rows_inplace(rows)
                req1.insert_bulk(cnx, cursor, table, rows, chunk_size)

    cursor.execute("alter table attribute add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table category add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table checkin add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table photo add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table review add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table review add constraint foreign key (user_id) references user(id);")  # noqa
    cursor.execute("alter table tip add constraint foreign key (business_id) references business(id);")  # noqa
    cursor.execute("alter table tip add constraint foreign key (user_id) references user(id);")  # noqa
    cursor.execute("alter table vip_history add constraint foreign key (user_id) references user(id);")  # noqa

    cnx.close()
    cursor.close()


def requirement2(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")
    cursor.execute("USE DMA_team%02d;" % team)
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE

    fopen = open("project2_team%02d_req2.txt" % team, "w", encoding="utf8")
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE
    fopen.close()
    cursor.close()


def requirement3(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")
    cursor.execute("USE DMA_team%02d;" % team)
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE

    fopen = open("project2_team%02d_req3.txt" % team, "w", encoding="utf8")
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE
    fopen.close()
    cursor.close()


def requirement4(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")
    cursor.execute("USE DMA_team%02d;" % team)
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE

    fopen = open("project2_team%02d_req4.txt" % team, "w", encoding="utf8")
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE
    fopen.close()
    cursor.close()


def requirement5(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")
    cursor.execute("USE DMA_team%02d;" % team)
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE

    fopen = open("project2_team%02d_req5.txt" % team, "w", encoding="utf8")
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE
    fopen.close()
    cursor.close()


def requirement6(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute("SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;")
    cursor.execute("USE DMA_team%02d;" % team)
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE

    fopen = open("project2_team%02d_req6.txt" % team, "w", encoding="utf8")
    # TODO: WRITE CODE HERE

    # TODO: WRITE CODE HERE
    fopen.close()
    cursor.close()


def main(args):
    if 1 in args.requirements:
        requirement1(
            host=args.host, user=args.user, password=args.password,
            directory=args.directory_in,
            max_allowed_packet=args.max_allowed_packet,
            chunk_size=args.chunk_size,
        )
    if 2 in args.requirements:
        requirement2(host=args.host, user=args.user, password=args.password)
    if 3 in args.requirements:
        requirement3(host=args.host, user=args.user, password=args.password)
    if 4 in args.requirements:
        requirement4(host=args.host, user=args.user, password=args.password)
    if 5 in args.requirements:
        requirement5(host=args.host, user=args.user, password=args.password)
    if 6 in args.requirements:
        requirement6(host=args.host, user=args.user, password=args.password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="localhost", type=str)
    parser.add_argument("--user", default="root", type=str)
    parser.add_argument("--password", default=os.environ["DB_PASSWORD"],
                        type=str)
    parser.add_argument("--directory_in", default="./DMA_datafiles", type=str)
    parser.add_argument("--requirements", nargs="*", default=[1], type=int)

    parser.add_argument("--max_allowed_packet", default="4294967296", type=str)
    parser.add_argument("--chunk_size", default=100000, type=int)
    args = parser.parse_args()

    main(args)
