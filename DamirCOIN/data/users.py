from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coins = sqlalchemy.Column(sqlalchemy.Integer)
    one_click = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    one_sec = sqlalchemy.Column(sqlalchemy.Integer)
    upgrade_click1 = sqlalchemy.Column(sqlalchemy.Integer)
    upgrade_click2 = sqlalchemy.Column(sqlalchemy.Integer)
    upgrade_sec1 = sqlalchemy.Column(sqlalchemy.Integer)
    upgrade_sec2 = sqlalchemy.Column(sqlalchemy.Integer)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
