from app.controllers.bot import bot_router
from app.utils.constant import API_PREFIX

def configure_app(app):
    app.include_router(bot_router , prefix=API_PREFIX)
    return app