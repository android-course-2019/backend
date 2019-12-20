from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from application.database import db


class PosterImage(db.Model):
    __tablename__ = "PosterImage"

    posterImageId = Column(BIGINT, autoincrement=True, unique=True,
                           primary_key=True, nullable=False)
    posterId = Column(BIGINT, ForeignKey("Poster.posterId"), nullable=False)
    poster = relationship("Poster", back_populates="images")
    url = Column(VARCHAR(128), nullable=False)

    def to_json_adaptable(self):
        return {
            "posterImageId": self.posterImageId,
            "posterId": self.posterId,
            "url": self.url
        }
