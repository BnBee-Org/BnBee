"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

from webapp.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_role = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"hashed_password=\"{self.hashed_password}\", " \
               f"is_active={self.is_active})>"
