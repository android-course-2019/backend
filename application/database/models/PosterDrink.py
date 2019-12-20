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
        res = {
            "posterDrinkId": self.posterDrinkId,
            "posterId": self.posterId
        }
        if self.drinkId is not None:
            res["drink"] = self.drink.to_json_adaptable()
        else:
            res["drink"] = self.drinkName
        return res
