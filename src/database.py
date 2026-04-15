"""
Set the database models.
Feature: Data Structures + SQLite connection
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timezone

DB_PATH = "data/industrial.db"

Base = declarative_base()

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    production_rate = Column(Float)

    events = relationship("MachineEvent", back_populates="machine")

class MachineEvent(Base):
    __tablename__ = "machine_events"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event_type = Column(String(50))
    duration_minutes = Column(Float)
    pieces_produced = Column(Integer, default=0)
    pieces_defective = Column(Integer, default=0)
    downtime_reason = Column(String(200), nullable=True)

    machine = relationship("Machine", back_populates="events")

def get_engine(db_path=DB_PATH):
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    return engine

def create_tables(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()