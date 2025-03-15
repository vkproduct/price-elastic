from flask import Blueprint

api = Blueprint('api', __name__)

# Импортируем модули API
from app.api import auth, data, analysis, settings, subscriptions, errors

# Регистрируем обработчики URL
from app.api.auth import routes
from app.api.data import routes
from app.api.analysis import routes
from app.api.settings import routes
from app.api.subscriptions import routes