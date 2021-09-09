from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

class ContactGroup(Model):
    id = Column(Integer, primary_key = True)
    number = Column(String(11), unique = True, nullable = False)

    def __repr__(self):
        return self.number

class Contact(Model):
    id = Column(Integer, primary_key = True)
    number = Column(String(11), unique = True, nullable = False)
    name = Column(String(150), nullable = False)
    address = Column(String(564), nullable = False)

    def __repr__(self):
        return self.number
