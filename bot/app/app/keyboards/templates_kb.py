from typing import Optional
from contextlib import suppress
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData


class TemplatesCallbackFactory(CallbackData, prefix="templ"):
    action: str
    templates: str
    templ: Optional[str]


def get_templates_keyboard_fab(templates: str):
    """Templates names keyboard fabrique
    """
    builder = InlineKeyboardBuilder()
    for t in templates.split('|'):
        builder.button(
            text=t,
            callback_data=TemplatesCallbackFactory(
                action="change",
                templates=templates,
                templ=t
                    )
                )
    builder.button(
        text='👌 query for vacancies',
        callback_data=TemplatesCallbackFactory(
            action="finish",
            templates=templates,
                )
            )
    builder.adjust(3)
    return builder.as_markup()


async def update_choice_text_fab(message: Message, templ: str, templates: str):
    """Update template choice
    """
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Choose template for query: {templ}",
            reply_markup=get_templates_keyboard_fab(templates)
                )
