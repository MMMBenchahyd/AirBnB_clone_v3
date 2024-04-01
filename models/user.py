#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            pwd = kwargs.pop("password", None)
            User.__set_pass(self, pwd)
        super().__init__(*args, **kwargs)

    def __set_pass(self, passwd):
        """set password with md5"""

        securpass = md5(passwd.encode('utf-8')).hexdigest()
        setattr(self, "password", securpass)
