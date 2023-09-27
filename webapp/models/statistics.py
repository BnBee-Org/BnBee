from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from webapp.database import Base


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hive_id = Column(Integer, ForeignKey('hive.id'))
    organization_id = Column(Integer, ForeignKey('organization.id'))
    datetime = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    weight = Column(Float)
    avr_sound = Column(Float)
    pressure = Column(Float)

    def __repr__(self):
        return f"<Statistics(id={self.id}, " \
               f"hive_id=\"{self.hive_id}\", " \
               f"datetime=\"{self.datetime}\", " \
               f"temperature=\"{self.temperature}\", " \
               f"humidity=\"{self.humidity}\", " \
               f"weight=\"{self.weight}\", " \
               f"avr_sound=\"{self.avr_sound}\", " \
               f"pressure={self.pressure})>"
