from captcha.image import ImageCaptcha
from config import config
import string
import random

class CaptchaGenerator:
    def __init__(self):
        self.image_generator = ImageCaptcha(
            width=config.captcha_width,
            height=config.captcha_height,
        )

    def generate_text_captcha(self) -> str:
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=config.captcha_length
        ))
    def generate_image_captcha(self, text: str):
        return self.image_generator.generate_image(text)

captcha = CaptchaGenerator()
