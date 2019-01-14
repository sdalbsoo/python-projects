from tqdm import tqdm
from loguru import logger


def create_tables(cursor):
    cursor.execute("""create table if not exists user(
        id varchar(22) not null,
        name varchar(225),
        email varchar(30),
        signup_date date NOT NULL,
        followers int NOT NULL,
        likes int NOT NULL,
        num_friends int NOT NULL,
        PRIMARY KEY (id));""")
    cursor.execute("""create table if not exists business(
        id varchar(22) not null,
        name varchar(255) NOT NULL,
        neighborhood varchar(255),
        address varchar(255),
        phone_no varchar(13) ,
        city varchar(255),
        state varchar(3),
        postal_code varchar(8),
        latitude float,
        longtitude float,
        is_open int(1),
        open_at char(5),
        close_at char(5),
        PRIMARY KEY (id));""")
    cursor.execute("""create table if not exists attribute(
        id int NOT NULL,
        business_id varchar(22),
        characteristic varchar(255) NOT NULL,
        description varchar(255) NOT NULL,
        PRIMARY KEY (id));""")
    cursor.execute("""create table if not exists category(
        id int(11) not null,
        business_id varchar(22),
        category varchar(40) NOT NULL,
        PRIMARY KEY (id));""")
    cursor.execute("""create table if not exists checkin(
        id int not null,
        business_id varchar(22),
        day varchar(9) NOT NULL,
        hour char(5) NOT NULL,
        count int NOT NULL,
        PRIMARY KEY(id));""")
    cursor.execute("""create table if not exists photo(
        id varchar(22) not null,
        business_id varchar(22),
        caption varchar(255),
        label varchar(10),
        PRIMARY KEY(id));""")
    cursor.execute("""create table if not exists review(
        id varchar(22) not null,
        business_id varchar(22),
        user_id varchar(22),
        stars int(1) NOT NULL,
        text_length int NOT NULL,
        date DATETIME NOT NULL,
        useful int NOT NULL,
        funny int NOT NULL,
        cool int NOT NULL,
        PRIMARY KEY(id));""")
    cursor.execute("""create table if not exists tip(
        id int not null,
        business_id varchar(22),
        user_id varchar(22),
        text_length int NOT NULL,
        date DATETIME,
        likes int NOT NULL,
        PRIMARY KEY(id));""")
    cursor.execute("""create table if not exists vip_history(
        id int not null,
        user_id varchar(22),
        year int(4) NOT NULL,
        PRIMARY KEY(id));""")


def insert_data(cnx, cursor, table_name, directory_in, chunk_size=10000):
    with open(directory_in, "r") as f:
        rows = [line.split(";") for line in f.read().strip().split("\n")]
    ncols = len(rows[0])
    nrows = len(rows)
    print(table_name, "의 ncols: ", ncols, ", nrows: ", nrows)
    colstring = ", ".join(["%s"] * ncols)
    niter = nrows // chunk_size + 1
    sql = f"insert into {table_name} values ({colstring})"
    cleanup_rows_inplace(rows)
    for n in tqdm(range(niter), desc=sql):
        cursor.executemany(
            sql, rows[n*chunk_size:(n+1)*chunk_size]
        )
        cnx.commit()


def cleanup_rows_inplace(rows):
    for rowidx, row in enumerate(rows):
        for elemidx, element in enumerate(row):
            if element == "None":
                # logger.debug(f"{rows[rowidx]} contains None string")
                rows[rowidx][elemidx] = None
            if element == "":
                logger.debug(f"{rows[rowidx]} contains empty string")
                rows[rowidx][elemidx] = None
