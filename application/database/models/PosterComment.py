from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from application.database import db
from application.database.models import *


class PosterComment(db.Model):
    __tablename__ = "PosterComment"

    commentId = Column(BIGINT, primary_key=True, unique=True,
                       autoincrement=True, nullable=False)
    content = Column(VARCHAR(200), nullable=False)

    posterId = Column(BIGINT, ForeignKey(Poster.posterId), nullable=False)
    poster = relationship(Poster, back_populates="comments")

    replyCommentId = Column(BIGINT, ForeignKey("PosterComment.commentId"), nullable=True)
    replies = relationship("PosterComment",
                           backref=backref("replyComment", remote_side=[commentId]))

    def to_json_adaptable(self):
        res = {
            "commentId": self.commentId,
            "content": self.content,
            "posterId": self.posterId
        }
        if self.replyCommentId is not None:
            res["replyCommentId"] = self.replyCommentId
        return res
