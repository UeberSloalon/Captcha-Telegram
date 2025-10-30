import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()

@dataclass
class Config:
    token: str = os.getenv("BOT_TOKEN", "")


    captcha_timeout: int = 120
    captcha_length: int = 6
    captcha_width: int = 300
    captcha_height: int = 150

    default_permissions: dict = None

    messages: dict = None

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    def __post_init__(self):
        if self.default_permissions is None:
            self.default_permissions = {
                "can_send_message": False,
                "can_send_media_messages": False,
                "can_send_stick_messages": False,
                "can_send_other_messages": False,
                "can_add_web_page_previews": False,
            }


        if self.messages is None:
            self.messages = {
                "welcome": "👋 Привет, {username}!\n\n**Чтобы получить доступ к чату, введи текст с картинки:**\n`{captcha_text}`\n\n⏰ У тебя {timeout} секунд!",
                "success": "✅ {username}, капча пройдена! Добро пожаловать в чат!",
                "wrong": "❌ Неверный код капчи! Попробуй еще раз.",
                "kicked": "⏰ Время вышло! Пользователь {username} кикнут."
            }

config = Config()
