from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

from application.database import db


UserFollow = db.Table(
    "UserFollow",
    Column("followerId", BIGINT, ForeignKey("User.userId"), primary_key=True, nullable=False),
    Column("followeeId", BIGINT, ForeignKey("User.userId"), primary_key=True, nullable=False)
)
