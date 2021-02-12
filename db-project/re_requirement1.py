def create_table(cursor):
    cursor.execute("""CREATE TABLE if not exists vip_history(
        id INT NOT NULL,
        user_id VARCHAR(22),
        year INT(4) NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists tip(
        id INT NOT NULL,
        business_id VARCHAR(22),
        user_id VARCHAR(22),
        text_len INT NOT NULL,
        date DATETIME NOT NULL,
        likes INT NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists review(
        id VARCHAR(22) NOT NULL,
        business_id VARCHAR(22),
        user_id VARCHAR(22),
        stars INT(1) NOT NULL,
        text_length INT NOT NULL,
        date DATETIME NOT NULL,
        useful INT NOT NULL,
        funny INT NOT NULL,
        cool INT NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists photo(
        id VARCHAR(22) NOT NULL,
        business_id VARCHAR(22),
        caption VARCHAR(255),
        label VARCHAR(10) NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists checkin(
        id INT NOT NULL,
        business_id VARCHAR(22),
        day VARCHAR(22) NOT NULL,
        hour CHAR(5) NOT NULL,
        count INT NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists category(
        id INT(11) NOT NULL,
        business_id VARCHAR(22),
        category VARCHAR(40) NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists attribute(
        id INT NOT NULL,
        business_id VARCHAR(22),
        characteristic VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists business(
        id VARCHAR(22) NOT NULL,
        name VARCHAR(255) NOT NULL,
        neighborhood VARCHAR(255),
        address VARCHAR(255),
        phone_no VARCHAR(13),
        city VARCHAR(255),
        state VARCHAR(3),
        postal_code VARCHAR(8),
        latitude float,
        longtitude float,
        is_open INT(1) NOT NULL,
        open_at CHAR(5),
        close_at CHAR(5),
        PRIMARY KEY(id));
        """)
    cursor.execute("""CREATE TABLE if not exists user(
        id VARCHAR(22) NOT NULL,
        name VARCHAR(255),
        email VARCHAR(30),
        signup_date DATE NOT NULL,
        followers INT NOT NULL,
        likes INT NOT NULL,
        num_friends INT NOT NULL,
        PRIMARY KEY(id));
        """)


def clean_data(rows):
    for rowidx, row in enumerate(rows):
        for idx, element in enumerate(row):
            if element == 'None':
                rows[rowidx][idx] = None
    return rows
