from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

async def send_support_email(
    user_name: str,
    user_email: str,
    user_phone: str,
    subject: str,
    description: str
):
    message = MessageSchema(
        subject=f"[TutorFinder] Обращение в поддержку: {subject}",
        recipients=[settings.MAIL_TO],
        body=f"""
        <h3>Новое обращение в техподдержку</h3>
        <p><b>От:</b> {user_name}</p>
        <p><b>Email:</b> {user_email}</p>
        <p><b>Телефон:</b> {user_phone}</p>
        <hr>
        <p><b>Тема:</b> {subject}</p>
        <p><b>Описание:</b> {description}</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)