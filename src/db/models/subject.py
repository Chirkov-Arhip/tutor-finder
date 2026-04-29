from sqlalchemy import Column, Integer, String, Table, ForeignKey
from src.db.base import Base

tutor_subjects = Table(
    "tutor_subjects",
    Base.metadata,
    Column("tutor_id", Integer, ForeignKey("tutor_profiles.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)