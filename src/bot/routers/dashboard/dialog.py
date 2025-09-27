from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select, Start, SwitchTo
from magic_filter import F

from src.bot.states import (
    Dashboard,
    DashboardBroadcast,
    DashboardPromocodes,
    DashboardRemnashop,
    DashboardUsers,
    MainMenu,
)
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from src.core.enums import AccessMode, BannerName

from .getters import access_getter, dashboard_getter
from .handlers import on_access_mode_selected
from .remnawave.handlers import start_remnawave_window

dashboard = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-main"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-dashboard-statistics"),
            id="statistics",
            state=Dashboard.STATISTICS,
        ),
        Start(
            text=I18nFormat("btn-dashboard-users"),
            id="users",
            state=DashboardUsers.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard-broadcast"),
            id="broadcast",
            state=DashboardBroadcast.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Start(
            text=I18nFormat("btn-dashboard-promocodes"),
            id="promocodes",
            state=DashboardPromocodes.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-dashboard-access"),
            id="access",
            state=Dashboard.ACCESS,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-dashboard-remnawave"),
            id="remnawave",
            on_click=start_remnawave_window,
        ),
        Start(
            text=I18nFormat("btn-dashboard-remnashop"),
            id="remnashop",
            state=DashboardRemnashop.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        when="is_dev",
    ),
    Row(
        Start(
            text=I18nFormat("btn-back-menu"),
            id="back",
            state=MainMenu.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.MAIN,
    getter=dashboard_getter,
)

statistics = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-statistics-main"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.STATISTICS,
)

access = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-access-main"),
    Column(
        Select(
            text=I18nFormat("btn-access-mode", access_mode=F["item"]),
            id="mode",
            item_id_getter=lambda item: item.value,
            items="modes",
            type_factory=AccessMode,
            on_click=on_access_mode_selected,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=Dashboard.ACCESS,
    getter=access_getter,
)

router = Dialog(
    dashboard,
    statistics,
    access,
)
