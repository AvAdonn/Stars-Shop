from aiogram import Router

from . import (
    basic,
)

def get_routers() -> list[Router]:
    return [
        basic.router,
    ]