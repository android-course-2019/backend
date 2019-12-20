from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from application.database import db


class Drink(db.Model):
    __tablename__ = "Drink"

    drinkId = Column(BIGINT, autoincrement=True,
                     unique=True, nullable=False, primary_key=True)
    drinkName = Column(VARCHAR(32), nullable=False)
    description = Column(VARCHAR(200), nullable=True)

    brandId = Column(BIGINT, ForeignKey("Brand.brandId"), nullable=False)
    brand = relationship("Brand", back_populates="drinks")

    def __str__(self):
        return "<Drink '{}' id '{}'>".format(self.drinkName, self.drinkId)

    def __repr__(self):
        return self.__str__()

    def to_json_adaptable(self):
        return {
            "drinkId": self.drinkId,
            "drinkName": self.drinkName,
            "description": self.description,
            "brand": self.brand.to_json_adaptable()
        }
