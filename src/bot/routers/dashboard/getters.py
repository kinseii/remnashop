from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.infrastructure.database.models.dto import UserDto
from src.services.access import AccessService


async def dashboard_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "is_dev": user.is_dev,
    }


@inject
async def access_getter(
    dialog_manager: DialogManager,
    access_service: FromDishka[AccessService],
    **kwargs: Any,
) -> dict[str, Any]:
    current_mode = await access_service.get_current_mode()
    modes = await access_service.get_available_modes()

    return {
        "access_mode": current_mode,
        "modes": modes,
    }
