from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.db.base import get_db
from src.db.models.user import User
from src.db.models.profile import StudentProfile, TutorProfile
from src.mail import send_support_email

router = APIRouter()

class SupportRequest(BaseModel):
    user_id: int
    subject: str
    description: str

@router.post("/support")
async def support(data: SupportRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем контактные данные в зависимости от роли
    if user.role == "student":
        profile = db.query(StudentProfile).filter(
            StudentProfile.user_id == data.user_id
        ).first()
    else:
        profile = db.query(TutorProfile).filter(
            TutorProfile.user_id == data.user_id
        ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")

    full_name = f"{profile.last_name} {profile.first_name} {profile.middle_name or ''}".strip()

    await send_support_email(
        user_name=full_name,
        user_email=user.email,
        user_phone=profile.phone,
        subject=data.subject,
        description=data.description
    )

    return {"message": "Обращение отправлено"}