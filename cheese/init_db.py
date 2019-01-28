import click

from connectDB import ConnectDB


@click.command()
@click.option("--USER", prompt="your DB user name", help="DB user name")
@click.option("--PW", prompt="your DB PW", help="DB PW")
def init_DB(user, pw):
    with ConnectDB("localhost", user, pw) as conDB:
        conDB.create_table()


if __name__ == '__main__':
    init_DB()
