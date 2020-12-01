
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, PrimaryKeyConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    userStatus = Column(Integer)
    events = relationship("Event", secondary = association_table, back_populates="users")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    date = Column(String)
    description = Column(String)
    status = Column(String)
    name = Column(String)
    users = relationship("User", secondary = association_table, back_populates="events")