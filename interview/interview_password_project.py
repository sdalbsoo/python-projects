import hashlib
import os
import pymysql


class connectDB():
    def __init__(self, host, user, password):
        self.host, self.user, self.password = host, user, password
        self.conn = pymysql.connect(host = host, user = user, password = password)  # noqa

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("USE interview_password_project")
        cursor.execute("""CREATE TABLE if not exists id_password(
        id INT NOT NULL AUTO_INCREMENT,
        user_id VARCHAR(22) NOT NULL,
        user_password VARCHAR(22) NOT NULL,
        user_salt LONGTEXT NOT NULL,
        user_digest LONGTEXT NOT NULL,
        PRIMARY KEY(id));
        """)


def signup(user_id, user_password):
    user_password_bytes = user_password.encode('utf-8')
    user_salt = str(os.urandom(16))
    user_salt_bytes = user_salt.encode('utf-8')
    service_salt_bytes = make_service_salt()
    salt = service_salt_bytes+user_salt_bytes
    user_digest = hashlib.pbkdf2_hmac('sha256', user_password_bytes, salt, 1)

    with connectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        cursor = conDB.conn.cursor()
        sql = "INSERT INTO id_password (user_id, user_password, user_salt, user_digest) VALUES (%s, %s, %s, %s);"  # noqa
        val = (user_id, user_password, user_salt, str(user_digest))
        cursor.execute(sql, val)
        conDB.conn.commit()


def login(user_id, user_password):
    li_users = []
    service_salt_bytes = make_service_salt()
    user_password_bytes = user_password.encode('utf-8')

    with connectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        cursor = conDB.conn.cursor()
        cursor.execute("USE interview_password_project")
        cursor.execute("SELECT user_id, user_salt FROM id_password")
        users_existing_data = cursor.fetchall()
        row = len(users_existing_data)

        for num in range(row):
            li_users.append(users_existing_data[num][0])
            user_salt_bytes = users_existing_data[num][1].encode('utf-8')
            salt = service_salt_bytes+user_salt_bytes
            user_digest = hashlib.pbkdf2_hmac('sha256', user_password_bytes, salt, 1)  # noqa

            if (user_id == users_existing_data[num][0]):
                cursor.execute("USE interview_password_project")
                cursor.execute(f"SELECT user_digest FROM id_password WHERE user_id='{user_id}'")  # noqa
                user_existing = cursor.fetchone()
                if (str(user_digest) == user_existing[0]):
                    print(f"{user_id} 로그인 성공.")
                else:
                    print(f"{user_id}의 패스워드를 잘못 입력하셨습니다.")
            else:
                pass
    if user_id not in (li_users):
        print(f"{user_id}라는 아이디가 존재하지 않습니다.")


def make_service_salt():
    service = os.environ["SERVICE"]
    service_bytes = service.encode('utf-8')
    service_salt = hashlib.md5(service_bytes).hexdigest()
    service_salt_bytes = service_salt.encode('utf-8')
    return service_salt_bytes


def main():
    # with connectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        # conDB.create_table()
    # signup('sdalbsoo', 'hi')
    # signup('sbs', 'handsome')
    # signup('starbucks', 'good')
    login('sdalbsoo', 'hi')
    login('sdalbsoo', 'hi1')
    login('sbs', 'handsome')
    login('sbs', 'handsome1')
    login('starbucks', 'good')
    login('starbucks', 'good1')
    login('starbucks', 'good2')
    login('starbuck', 'good2')


if __name__ == '__main__':
    main()
