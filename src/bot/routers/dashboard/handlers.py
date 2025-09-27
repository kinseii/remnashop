from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.core.constants import USER_KEY
from src.core.enums import AccessMode
from src.core.utils.formatters import format_log_user
from src.infrastructure.database.models.dto import UserDto
from src.services.access import AccessService


@inject
async def on_access_mode_selected(
    callback: CallbackQuery,
    widget: Select[AccessMode],
    dialog_manager: DialogManager,
    selected_mode: AccessMode,
    access_service: FromDishka[AccessService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]

    await access_service.set_mode(mode=selected_mode)
    logger.info(f"{format_log_user(user)} Set access mode -> '{selected_mode}'")
