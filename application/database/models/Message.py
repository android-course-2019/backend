from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP

from application.database import db


class Message(db.Model):
    __tablename__ = "Message"

    messageId = Column(BIGINT, autoincrement=True, unique=True,
                       primary_key=True, nullable=True)
    sendTime = Column(TIMESTAMP, nullable=False,
                      server_default=text("CURRENT_TIMESTAMP"))
    content = Column(VARCHAR(300), unique=False, nullable=False)

    senderId = Column(BIGINT, ForeignKey("User.userId"), nullable=True)
    sender = relationship("User", foreign_keys=[senderId], back_populates="sentMessages")

    receiverId = Column(BIGINT, ForeignKey("User.userId"), nullable=True)
    receiver = relationship("User", foreign_keys=[receiverId], back_populates="receivedMessages")
