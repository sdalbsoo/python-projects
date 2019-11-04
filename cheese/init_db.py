import db
import app


def init_db():
    with app.app.app_context():
        db.create_table(app.get_db())


if __name__ == "__main__":
    init_db()
