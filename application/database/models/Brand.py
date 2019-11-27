from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT

from application.database import db
from application.database.models import *


class Brand(db.Model):
    __tablename__ = "Brand"

    brandId = Column(BIGINT, primary_key=True,
                     autoincrement=True, nullable=False)
    brandName = Column(VARCHAR(32), nullable=False, unique=True)

    shops = relationship("Shop", back_populates="brand", lazy=True)
    drinks = relationship("Drink", back_populates="brand", lazy=True)

    def __str__(self):
        return "<Brand '{}' id '{}'>".format(self.brandName, self.brandId)

    def __repr__(self):
        return self.__str__()
