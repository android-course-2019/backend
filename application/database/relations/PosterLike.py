from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

from application.database import db


PosterLike = db.Table(
    "PosterLike",
    Column("userId", BIGINT, ForeignKey("User.userId"), primary_key=True, nullable=False),
    Column("posterId", BIGINT, ForeignKey("Poster.posterId"), primary_key=True, nullable=False)
)
