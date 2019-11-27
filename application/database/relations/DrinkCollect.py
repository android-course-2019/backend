from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

from application.database import db


DrinkCollect = db.Table(
    "DrinkCollect",
    Column("userId", BIGINT, ForeignKey("User.userId"), primary_key=True, nullable=False),
    Column("drinkId", BIGINT, ForeignKey("Drink.drinkId"), primary_key=True, nullable=False)
)
