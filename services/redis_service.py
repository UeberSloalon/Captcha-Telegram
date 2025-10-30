import redis
import json
from config import config

class RedisStorage:
    def __init__(self):
        self.r = redis.from_url(config.redis_url, decode_responses=True)

    def save_captcha_data(self, user_id: int, chat_id: int, captcha_text: str):
        data = {
            "chat_id": chat_id,
            "captcha_text": captcha_text,
            "attempts": 0
        }
        self.r.setex(
            f"captcha:{user_id}",
            config.captcha_timeout,
            json.dumps(data)
        )

    def get_captcha_data(self, user_id: int) -> dict:
        data = self.r.get(f"captcha:{user_id}")
        return json.loads(data) if data else None

    def delete_captcha_data(self, user_id: int):
        self.r.delete(f"captcha:{user_id}")

    def increment_attempts(self, user_id: int):
        data = self.get_captcha_data(user_id)
        if data:
            data["attempts"] += 1
            self.r.setex(
                f"captcha:{user_id}",
                config.captcha_timeout,
                json.dumps(data)
            )
redis_storage = RedisStorage()