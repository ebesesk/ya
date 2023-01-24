from sqlalchemy import(
    Column, 
    Integer, 
    String, 
    Boolean, 
    Date, 
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from db.base_class import Base


class Video(Base):
    id = Column(Integer, primary_key=True, index=True)
    dbid = Column(String, unique=True, nullable=False, index=True)
    width = Column(Integer)
    height = Column(Integer)
    showtime = Column(Integer)
    bitrate = Column(Integer)
    filesize = Column(Integer)
    cdate = Column(DateTime)
    
    display_quality = Column(String)
    country = Column(String)
    face = Column(String)
    look = Column(String)
    age = Column(String)
    pussy = Column(String)
    etc = Column(String)
    
    school_uniform = Column(Boolean)
    hip = Column(Boolean)
    group = Column(Boolean)
    pregnant = Column(Boolean)
    conversation = Column(Boolean)
    lesbian = Column(Boolean)
    ani = Column(Boolean)
    oral = Column(Boolean)
    masturbation = Column(Boolean)
    massage = Column(Boolean)
    uniform = Column(Boolean)
    family = Column(Boolean)
    
    ad_start = Column(Integer)
    ad_finish = Column(Integer)
    star = Column(Integer)
    
    date_posted = Column(Date)
    date_modified = Column(Date)


