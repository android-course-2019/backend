from sqlalchemy import Column, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, DOUBLE

from application.database import db
from application.database.relations import *


class Poster(db.Model):
    __tablename__ = "Poster"

    posterId = Column(BIGINT, autoincrement=True, unique=True,
                      primary_key=True, nullable=True)
    content = Column(VARCHAR(140), nullable=False)
    createTime = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    location_longitude = Column(DOUBLE, nullable=True)
    location_latitude = Column(DOUBLE, nullable=True)

    sendById = Column(BIGINT, ForeignKey("User.userId"), nullable=False)
    sendBy = relationship("User", back_populates="posters")

    drinks = relationship("PosterDrink", back_populates="poster")
    images = relationship("PosterImage", back_populates="poster")
    comments = relationship("PosterComment", back_populates="poster", lazy=True)
    likedBy = relationship("User", secondary=PosterLike,
                           back_populates="likedPosters", lazy='dynamic')

    def __str__(self):
        return "<Poster id '{}' send by {}>".format(self.posterId, self.sendBy)

    def __repr__(self):
        return self.__str__()

    def to_json_adaptable(self):
        return {
            "posterId": self.posterId,
            "content": self.content,
            "createTime": self.createTime.timestamp(),
            "location": [self.location_longitude, self.location_latitude],
            "sendBy": self.sendBy.to_json_adaptable(),
            "drinks": [x.to_json_adaptable() for x in self.drinks],
            "images": [x.to_json_adaptable() for x in self.images],
            "comments": [x.to_json_adaptable() for x in self.comments],
            "likedNum": self.likedBy.count()
        }
