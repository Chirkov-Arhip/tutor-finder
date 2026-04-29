from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutor_profiles.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    custom_subject = Column(String(100))
    status = Column(String(10), default="pending")
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("StudentProfile", back_populates="applications")
    tutor = relationship("TutorProfile", back_populates="applications")
    subject = relationship("Subject")