from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from application.database import db
from application.database.models import *


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
