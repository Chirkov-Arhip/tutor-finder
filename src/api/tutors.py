from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from src.db.base import get_db
from src.db.models.profile import TutorProfile
from src.db.models.subject import Subject
from src.db.models.application import Application

router = APIRouter()

class TutorProfileRequest(BaseModel):
    user_id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    age: int
    experience: int
    phone: str
    about: Optional[str] = None
    subjects: list[int] = []

class UpdateTutorProfileRequest(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    age: Optional[int] = None
    experience: Optional[int] = None
    about: Optional[str] = None
    subjects: Optional[list[int]] = None
    custom_subject: Optional[str] = None

class ApplicationStatusRequest(BaseModel):
    status: str

@router.post("/profile", status_code=201)
def create_profile(data: TutorProfileRequest, db: Session = Depends(get_db)):
    existing = db.query(TutorProfile).filter(
        TutorProfile.user_id == data.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Профиль уже существует")

    profile = TutorProfile(
        user_id=data.user_id,
        last_name=data.last_name,
        first_name=data.first_name,
        middle_name=data.middle_name,
        age=data.age,
        experience=data.experience,
        phone=data.phone,
        about=data.about
    )
    db.add(profile)
    db.flush()

    for subject_id in data.subjects:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if subject:
            profile.subjects.append(subject)

    db.commit()
    db.refresh(profile)
    return {"message": "Профиль создан", "id": profile.id}


@router.get("/applications/{tutor_id}")
def get_applications(tutor_id: int, db: Session = Depends(get_db)):
    applications = db.query(Application).filter(
        Application.tutor_id == tutor_id
    ).all()

    result = []
    for a in applications:
        result.append({
            "id": a.id,
            "status": a.status,
            "subject": a.subject.name if a.subject_id else a.custom_subject,
            "created_at": str(a.created_at),
            "message": a.message,
            "proposed_dates": a.proposed_dates,
            "student": {
                "full_name": f"{a.student.last_name} {a.student.first_name} {a.student.middle_name or ''}".strip(),
                "age": a.student.age,
                "about": a.student.about,
                "phone": a.student.phone if a.status == "accepted" else None
            }
        })
    return result


@router.patch("/applications/{app_id}")
def respond_to_application(
    app_id: int,
    data: ApplicationStatusRequest,
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    if data.status not in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Неверный статус")

    application.status = data.status
    db.commit()
    return {"message": "Статус обновлён", "status": data.status}


@router.get("/profile/full/{user_id}")
def get_full_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(TutorProfile).filter(
        TutorProfile.user_id == user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return {
        "id": profile.id,
        "last_name": profile.last_name,
        "first_name": profile.first_name,
        "middle_name": profile.middle_name,
        "age": profile.age,
        "experience": profile.experience,
        "phone": profile.phone,
        "about": profile.about,
        "subjects": [{"id": s.id, "name": s.name} for s in profile.subjects]
    }


@router.patch("/profile/{user_id}")
def update_profile(user_id: int, data: UpdateTutorProfileRequest, db: Session = Depends(get_db)):
    profile = db.query(TutorProfile).filter(
        TutorProfile.user_id == user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")

    if data.last_name is not None:
        profile.last_name = data.last_name
    if data.first_name is not None:
        profile.first_name = data.first_name
    if data.middle_name is not None:
        profile.middle_name = data.middle_name
    if data.age is not None:
        profile.age = data.age
    if data.experience is not None:
        profile.experience = data.experience
    if data.about is not None:
        profile.about = data.about

    if data.subjects is not None:
        profile.subjects = []
        for subject_id in data.subjects:
            subject = db.query(Subject).filter(Subject.id == subject_id).first()
            if subject:
                profile.subjects.append(subject)

    if data.custom_subject:
        existing = db.query(Subject).filter(
            Subject.name == data.custom_subject
        ).first()
        if existing:
            if existing not in profile.subjects:
                profile.subjects.append(existing)
        else:
            new_subject = Subject(name=data.custom_subject)
            db.add(new_subject)
            db.flush()
            profile.subjects.append(new_subject)

    db.commit()
    return {"message": "Профиль обновлён"}
