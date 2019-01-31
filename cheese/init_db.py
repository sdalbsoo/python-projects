import connectDB


def init_DB(app):
    with app.app.app_context():
        connectDB.create_table(app.get_db())


if __name__ == '__main__':
    init_DB()
