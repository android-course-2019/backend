from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, DOUBLE, BIGINT

from application.database import db
from application.database.models import *


class Shop(db.Model):
    __tablename__ = "Shop"

    shopName = Column(VARCHAR(64), primary_key=True, unique=True, nullable=False)
    address = Column(VARCHAR(150), nullable=True)
    location_longitude = Column(DOUBLE, nullable=True)
    location_latitude = Column(DOUBLE, nullable=True)

    brandId = Column(BIGINT, ForeignKey('Brand.brandId'), nullable=False)
    brand = relationship("Brand",
                         back_populates="shops")
