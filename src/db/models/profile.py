from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.db.models.subject import tutor_subjects

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    age = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    about = Column(Text)

    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student")


class TutorProfile(Base):
    __tablename__ = "tutor_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    age = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    about = Column(Text)

    user = relationship("User", back_populates="tutor_profile")
    subjects = relationship("Subject", secondary=tutor_subjects, lazy="subquery")
    applications = relationship("Application", back_populates="tutor")