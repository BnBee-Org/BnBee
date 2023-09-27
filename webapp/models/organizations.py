from sqlalchemy import Column, String, Integer, DateTime, Boolean

from webapp.database import Base


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Organization(id={self.id}, " \
               f"name={self.name})>"
