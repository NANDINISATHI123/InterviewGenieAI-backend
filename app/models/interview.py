from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Interview(Base):

    __tablename__ = "interviews"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    email = Column(
        String,
        nullable=False
    )


    question = Column(
        Text,
        nullable=False
    )


    answer = Column(
        Text,
        nullable=False
    )


    feedback = Column(
        Text,
        nullable=False
    )


    score = Column(
        Integer,
        nullable=True
    )