from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from src.db.base import get_db
from src.db.models.profile import TutorProfile
from src.db.models.subject import Subject
from src.db.models.application import Application

router = APIRouter()

# — Схемы данных —————————————————————————————————————
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

class ApplicationStatusRequest(BaseModel):
    status: str

# — Эндпоинты ————————————————————————————————————————
@router.post("/profile", status_code=201)
def create_profile(data: TutorProfileRequest, db: Session = Depends(get_db)):
    # Проверяем что профиль ещё не создан
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
    db.flush()  # получаем id профиля до commit

    # Добавляем предметы
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
            "student": {
                "full_name": f"{a.student.last_name} {a.student.first_name} {a.student.middle_name or ''}".strip(),
                "age": a.student.age,
                "about": a.student.about,
                # телефон показываем только если заявка принята
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