import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from webapp.database import Base


class Whitelist(Base):
    __tablename__ = "whitelist"
    id = Column(Integer, primary_key=True)
    ip_range = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_modified = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"<Whitelist(ip_range={self.ip_range}, "
                f"user_id={self.user_id}, "
                f"date_created={self.date_created}, "
                f"date_modified={self.date_modified})>")
