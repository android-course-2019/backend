import hashlib
from sqlalchemy import Column, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, CHAR, TINYINT, TIMESTAMP

from application.config.private_data import db_password_salt
from application.database import db
from application.database.models import *
from application.database.relations import *


class User(db.Model):
    __tablename__ = 'User'
    userId = Column(BIGINT, primary_key=True, unique=True,
                    autoincrement=True, nullable=False)
    userName = Column(VARCHAR(32), unique=True, nullable=False)
    password = Column(CHAR(32), nullable=False)
    phone = Column(CHAR(11), unique=True, nullable=False)
    nickName = Column(VARCHAR(32), nullable=True)
    avatarUrl = Column(VARCHAR(100), nullable=True)
    gender = Column(TINYINT, nullable=True)
    createTime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    posters = relationship("Poster", backref="sendBy", lazy=True)
    collectDrinks = relationship("Drink", secondary=DrinkCollect, lazy=True)
    follower = relationship("User", secondary=UserFollow,
                            secondaryjoin="User.userId==UserFollow.followeeId",
                            back_populates="followee", lazy=True)
    followee = relationship("User", secondary=UserFollow,
                            secondaryjoin="User.userId==UserFollow.followerId",
                            back_populates="follower", lazy=True)
    likedPosters = relationship("Poster", secondary=PosterLike,
                                back_populates="likedBy", lazy=True)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            raw_pass = kwargs['password']
            kwargs['password'] = hashlib.md5((db_password_salt + raw_pass).encode('utf-8')).hexdigest()
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return "<User '{}' id '{}'>".format(self.userName, self.userId)

    def __repr__(self):
        return self.__str__()
