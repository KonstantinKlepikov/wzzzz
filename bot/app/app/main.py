import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry, Dialog
# from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis
from app.handlers import start, templ, templates, template, add_template
from app.middleware.session import SessionMiddleware
from app.middleware.api_queries import QuerieMaker
from app.config import settings


async def main():
    """Start bot"""
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.TG_API_TOKEN.get_secret_value())
    dp = Dispatcher()
    qm = QuerieMaker(bot)
    qm_middlewire = SessionMiddleware(qm)
    # r = redis.Redis(host=settings.REDIS_URL_DEV, port=6379, db=0)
    # storage = RedisStorage(r)

    dp.include_routers(
        start.router,
        templ.router,
            )

    dp.message.middleware(qm_middlewire)
    dp.callback_query.middleware(qm_middlewire)
    # dp.message.middleware(ReddisMiddlewire(storage))

    # dialogues
    main_dialog = Dialog(
        start.start_window,
        templates.templates_window,
        template.template_window,
        add_template.define_name,
        add_template.define_text,
        add_template.create_template_window
            )
    registry = DialogRegistry()
    registry.register(main_dialog)
    registry.setup_dp(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
