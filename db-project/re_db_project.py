import os
from os.path import isfile, join

import pymysql
from tqdm import tqdm

from re_requirement1 import create_table
from re_requirement1 import clean_data
from re_utils import timeit_context


def requirement1():
    conn = pymysql.connect(
        host="localhost", user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    cursor = conn.cursor()

    with timeit_context("drop & create & use database"):
        cursor.execute("drop database DMA_team01")
        cursor.execute("CREATE DATABASE IF NOT EXISTS DMA_team01")
        cursor.execute("USE DMA_team01")

    # CREATE TABLE
    with timeit_context("create table"):
        create_table(cursor)

    with timeit_context("insert data"):
        files = [f for f in os.listdir("./DMA_datafiles") if isfile(
            join("./DMA_datafiles", f))]
        for file_name in tqdm(files, "file"):
            table_name = os.path.splitext(file_name)[0]
            with open("./DMA_datafiles/"+file_name, "r") as f:
                rows = [line.split(";") for line in f.read().strip().split("\n")]  # noqa
            ncols = len(rows[1])
            colstring = ", ".join(["%s"] * ncols)
            sql = f"INSERT INTO {table_name} VALUES ({colstring})"
            cursor.executemany(sql, clean_data(rows))
            conn.commit()

    cursor.execute('alter table attribute add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table category add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table checkin add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table photo add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table review add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table review add constraint foreign key (user_id) references user(id);')  # noqa
    cursor.execute('alter table tip add constraint foreign key (business_id) references business(id);')  # noqa
    cursor.execute('alter table tip add constraint foreign key (user_id) references user(id);')  # noqa
    cursor.execute('alter table vip_history add constraint foreign key (user_id) references user(id);')  # noqa

    conn.close()


def requirement2():
    conn = pymysql.connect(
        host="localhost", user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    cursor = conn.cursor()
    cursor.execute("USE DMA_team01;")
    cursor.execute("""SELECT U.year, U.sign_up_count, R.review, T.tip_count
    FROM (
    SELECT year(signup_date) AS year,
            COUNT(*) AS sign_up_count
    FROM user
    WHERE signup_date >= '2009/01/01'
    AND signup_date <= '2017/12/31'
    GROUP BY year ORDER BY year) AS U
    INNER JOIN
        (
        SELECT year(date) AS year,
                count(useful+funny+cool) AS review
        FROM review
        WHERE date >= '2009/01/01'
        AND date <= '2017/12/31'
        GROUP BY year
        ) AS R
    ON U.year=R.year
    INNER JOIN
        (
        SELECT year(date) AS year,
                count(likes) AS tip_count
        from tip
        WHERE date >= '2009/01/01'
            AND date <= '2017/12/31'
        GROUP BY year(date) ORDER BY year
        ) AS T
    ON U.year = T.year;""")
    result = cursor.fetchall()
    with timeit_context("project2_team01_req2"):
        write_data("project2_team01_req2.txt", result)
    cursor.close()


def requirement3():
    conn = pymysql.connect(
        host="localhost", user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    cursor = conn.cursor()
    cursor.execute("USE DMA_team01;")
    cursor.execute("""SELECT id, name, address, phone_no
    FROM business
    WHERE id IN (
    SELECT business_id
    FROM (SELECT business_id, count(*) AS count_reviews, AVG(stars)
            AS avg_stars
            FROM review
            WHERE business_id IN (SELECT business_id FROM category
            WHERE category = 'Restaurants')
            GROUP BY business_id
        ) RV
    WHERE RV.count_reviews >= 5
        AND RV.avg_stars > 4.8
        AND business_id in (
        SELECT business_id
        FROM (
              SELECT business_id,
                      MAX(count) AS max_count
              FROM checkin
              WHERE business_id IN (
                  (SELECT business_id
                  FROM category
                  WHERE category = 'Restaurants')
              )
              GROUP BY business_id
            ) AS CI
        WHERE CI.max_count < 5
      )
    )
    ORDER BY id ASC;""")
    result = cursor.fetchall()
    with timeit_context("project2_team01_req3"):
        write_data("project2_team01_req3.txt", result)
    cursor.close()


def requirement4():
    conn = pymysql.connect(
        host="localhost", user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    cursor = conn.cursor()
    cursor.execute("USE DMA_team01;")
    cursor.execute("""SELECT id, name
    FROM business
    WHERE  id IN (
    SELECT business_id
    FROM photo
    WHERE id IS NULL
        OR label IS NULL
    )
    or id IN (
    SELECT id
    FROM business
    WHERE phone_no IS NULL
        OR address IS NULL
    )
    or id IN (
    SELECT business_id
    FROM checkin
    WHERE count = '0'
    )
    or id IN (
    SELECT business_id
    FROM attribute
    WHERE characteristic = 'none'
    )
    ORDER BY id ASC;""")
    result = cursor.fetchall()
    with timeit_context("project2_team01_req4"):
        write_data("project2_team01_req4.txt", result)
    cursor.close()


def requirement5():
    conn = pymysql.connect(
        host="localhost", user=os.environ["USER"],
        password=os.environ["PASSWORD"]
    )
    cursor = conn.cursor()
    cursor.execute("USE DMA_team01;")
    cursor.execute("""SELECT id, email
    FROM user
    WHERE id IN (
    SELECT user_friends.id
    FROM (
            SELECT id
            FROM user
            WHERE email LIKE '%dbproject.com'
            ORDER BY num_friends DESC
            limit 5
        ) AS user_friends
    )
    OR id IN (
    SELECT user_likes.id
    FROM (
            SELECT id
            FROM user
            WHERE email LIKE '%dbproject.com'
            ORDER BY likes DESC
            limit 5
        ) AS user_likes
    )
    OR id IN (
    SELECT user_follows.id
    FROM (
            SELECT id
            FROM user
            WHERE email LIKE '%dbproject.com'
            ORDER BY followers DESC
            limit 5
        ) AS user_follows
    )
    OR id IN (
    SELECT result.user_id
    FROM (
            SELECT user_id
            FROM review
            WHERE user_id IN (
            SELECT id
            FROM user
            WHERE email LIKE '%dbproject.com'
            )
            GROUP BY user_id
            ORDER BY count(*) DESC
            LIMIT 5
        ) AS result
    )
    ORDER BY id ASC;""")
    result = cursor.fetchall()
    with timeit_context("project2_team01_req5"):
        write_data("project2_team01_req5.txt", result)
    cursor.close()


def write_data(file_name, result):
    row = len(result)
    column = len(result[0])
    fopen = open(file_name, "w", encoding="utf-8")
    for i in range(row):
        li = list(result[i])
        for j in range(column-1):
            str_result = str(li[j]) + ';'
            fopen.write(str_result)
        fopen.write(str(li[column-1]))
        fopen.write('\n')
    fopen.close()


def main():
    # requirement1()
    requirement2()
    requirement3()
    requirement4()
    requirement5()


if __name__ == '__main__':
    main()
