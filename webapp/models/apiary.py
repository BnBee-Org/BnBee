from sqlalchemy import Column, String, Integer, ForeignKey

from webapp.database import Base


class Apiary(Base):
    __tablename__ = 'apiary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    name = Column(String)

    def __repr__(self):
        return f"<Apiary(id={self.id}, " \
               f"name={self.name})>"
