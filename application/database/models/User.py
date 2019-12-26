import hashlib
from sqlalchemy import Column, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, CHAR, TINYINT, TIMESTAMP

from application.database import db
from .Message import Message
from application.database.relations import *
from config.private_data import db_password_salt


class User(db.Model):
    __tablename__ = 'User'
    userId = Column(BIGINT, primary_key=True, unique=True,
                    autoincrement=True, nullable=False)
    password = Column(CHAR(32), nullable=False)
    phone = Column(CHAR(11), unique=True, nullable=False)
    nickName = Column(VARCHAR(32), nullable=True)
    avatarUrl = Column(VARCHAR(128), nullable=False,
                       default="https://oss.yh0x13f.cn/androidcourse/avatar/defaultAvatar.png")
    gender = Column(TINYINT, nullable=True)
    createTime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    posters = relationship("Poster", back_populates="sendBy", lazy='dynamic')
    collectDrinks = relationship("Drink", secondary=DrinkCollect, lazy='dynamic')
    follower = relationship("User", secondary=UserFollow, foreign_keys=[UserFollow.c.followeeId],
                            secondaryjoin="User.userId==UserFollow.c.followeeId",
                            back_populates="followee", lazy='dynamic')
    followee = relationship("User", secondary=UserFollow, foreign_keys=[UserFollow.c.followerId],
                            secondaryjoin="User.userId==UserFollow.c.followerId",
                            back_populates="follower", lazy='dynamic')
    sentMessages = relationship("Message", lazy="dynamic",
                                back_populates="sender", foreign_keys=[Message.senderId])
    receivedMessages = relationship("Message", lazy="dynamic",
                                    back_populates="receiver", foreign_keys=[Message.receiverId])
    likedPosters = relationship("Poster", secondary=PosterLike,
                                back_populates="likedBy", lazy='dynamic')

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            raw_pass = kwargs['password']
            kwargs['password'] = hashlib.md5((db_password_salt + raw_pass).encode('utf-8')).hexdigest()
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return "<User '{}' id '{}'>".format(self.userName, self.userId)

    def __repr__(self):
        return self.__str__()

    def to_json_adaptable(self):
        return {
            "userId": self.userId,
            "phone": self.phone[:3] + "****" + self.phone[-4:],
            "nickName": self.nickName,
            "avatarUrl": self.avatarUrl,
            "gender": self.gender,
            "createTime": self.createTime.timestamp()
        }

