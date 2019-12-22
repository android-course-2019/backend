from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from application.database import db


class PosterDrink(db.Model):
    __tablename__ = "PosterDrink"

    posterDrinkId = Column(BIGINT, autoincrement=True, unique=True,
                           primary_key=True, nullable=False)
    posterId = Column(BIGINT, ForeignKey("Poster.posterId"), nullable=False)
    poster = relationship("Poster", back_populates="drinks")

    drinkName = Column(VARCHAR(32), nullable=True)

    drinkId = Column(BIGINT, ForeignKey("Drink.drinkId"), nullable=True)
    drink = relationship("Drink")

    def to_json_adaptable(self):
        if self.drinkId is not None:
            return self.drink.to_json_adaptable()
        else:
            return {
                "drinkName": self.drinkName
            }
