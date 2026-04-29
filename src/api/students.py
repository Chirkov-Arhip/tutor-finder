from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from src.db.base import get_db
from src.db.models.profile import StudentProfile, TutorProfile
from src.db.models.subject import Subject
from src.db.models.application import Application

router = APIRouter()

# — Схемы данных —————————————————————————————————————
class StudentProfileRequest(BaseModel):
    user_id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    age: int
    phone: str
    about: Optional[str] = None

class ApplicationRequest(BaseModel):
    student_id: int
    tutor_id: int
    subject_id: Optional[int] = None
    custom_subject: Optional[str] = None

class TutorResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str]
    age: int
    experience: int
    about: Optional[str]
    subjects: list[dict]

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    status: str
    subject_id: Optional[int]
    custom_subject: Optional[str]

    class Config:
        from_attributes = True

# — Эндпоинты ————————————————————————————————————————
@router.post("/profile", status_code=201)
def create_profile(data: StudentProfileRequest, db: Session = Depends(get_db)):
    # Проверяем что профиль ещё не создан
    existing = db.query(StudentProfile).filter(
        StudentProfile.user_id == data.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Профиль уже существует")

    profile = StudentProfile(
        user_id=data.user_id,
        last_name=data.last_name,
        first_name=data.first_name,
        middle_name=data.middle_name,
        age=data.age,
        phone=data.phone,
        about=data.about
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"message": "Профиль создан", "id": profile.id}

@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return {"id": profile.id, "user_id": profile.user_id}

@router.get("/tutors")
def get_tutors(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    # Если передан фильтр по предмету — фильтруем
    if subject_id:
        tutors = db.query(TutorProfile).filter(
            TutorProfile.subjects.any(id=subject_id)
        ).all()
    else:
        tutors = db.query(TutorProfile).all()

    result = []
    for t in tutors:
        result.append({
            "id": t.id,
            "last_name": t.last_name,
            "first_name": t.first_name,
            "middle_name": t.middle_name,
            "age": t.age,
            "experience": t.experience,
            "about": t.about,
            "subjects": [{"id": s.id, "name": s.name} for s in t.subjects]
        })
    return result


@router.get("/subjects")
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return [{"id": s.id, "name": s.name} for s in subjects]


@router.post("/apply", status_code=201)
def apply(data: ApplicationRequest, db: Session = Depends(get_db)):
    # Проверяем что такой заявки ещё нет
    existing = db.query(Application).filter(
        Application.student_id == data.student_id,
        Application.tutor_id == data.tutor_id,
        Application.status == "pending"
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Заявка этому репетитору уже отправлена"
        )

    application = Application(
        student_id=data.student_id,
        tutor_id=data.tutor_id,
        subject_id=data.subject_id,
        custom_subject=data.custom_subject
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return {"message": "Заявка отправлена", "id": application.id}