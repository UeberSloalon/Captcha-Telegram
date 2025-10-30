from aiogram import Router, F
from aiogram.types import Message, ChatPermissions, BufferedInputFile, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

from config import config
from services.redis_service import redis_storage
from services.captcha_service import captcha
import asyncio

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_new_member(event: ChatMemberUpdated):
    user = event.new_chat_member.user

    if user.is_bot:
        return

    captcha_text = captcha.generate_text_captcha()
    captcha_image = captcha.generate_image_captcha(captcha_text)

    await redis_storage.save_captcha_data(user.id, event.chat.id, captcha_text)

    await event.bot.restrict_chat_member(
        chat_id=event.chat.id,
        user_id=user.id,
        permissions=ChatPermissions(**config.default_permissions)
    )

    photo = BufferedInputFile(captcha_image.getvalue(), "captcha.png")
    await event.bot.send_photo(
        chat_id=event.chat.id,
        photo=photo,
        caption=config.messages["welcome"].format(
            username=user.first_name,
            captcha_text=captcha_text,
            timeout=config.captcha_timeout
        )
    )

    asyncio.create_task(kick_timer(user.id, event.chat.id, event.bot))


async def kick_timer(user_id: int, chat_id: int, bot):
    await asyncio.sleep(config.captcha_timeout)

    if await redis_storage.get_captcha_data(user_id):
        await bot.ban_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id)
        await redis_storage.delete_captcha_data(user_id)


@router.message(F.text)
async def check_captcha(message: Message):
    user_data = await redis_storage.get_captcha_data(message.from_user.id)

    if not user_data:
        return

    if message.text.upper() == user_data["captcha_text"]:
        await message.bot.restrict_chat_member(
            chat_id=user_data["chat_id"],
            user_id=message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )

        await message.answer(
            config.messages["success"].format(username=message.from_user.first_name)
        )
        await redis_storage.delete_captcha_data(message.from_user.id)
    else:
        await message.answer(config.messages["wrong"])
        await redis_storage.increment_attempts(message.from_user.id)