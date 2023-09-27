from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

from webapp.database import Base


class Hive(Base):
    __tablename__ = 'hive'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    name = Column(String)
    bee_count = Column(Integer)
    is_active = Column(Boolean)
    lid_open = Column(Boolean)
    door_open = Column(Boolean)
    maintenance = Column(Boolean)
    apiary_id = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<Hive(id={self.id}, " \
               f"name=\"{self.email}\", " \
               f"bee_count=\"{self.bee_count}\", " \
               f"is_active=\"{self.is_active}\", " \
               f"lid_open=\"{self.lid_open}\", " \
               f"door_open=\"{self.door_open}\", " \
               f"maintenance=\"{self.maintenance}\", " \
               f"apiary_id=\"{self.apiary_id}\", " \
               f"status={self.status})>"
