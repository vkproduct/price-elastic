from flask import Flask
from config import config
from app.extensions import db, migrate, jwt, cors
from app.models.user import User

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Явное определение JWT-конфигурации
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)  # 1 час по умолчанию
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Включаем отладочный вывод
    app.logger.debug(f"Using secret key for JWT: {app.config.get('SECRET_KEY')[:5]}...")
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Обработчики JWT ошибок
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.debug(f"Expired token: {jwt_payload.get('sub')}")
        return {"message": "Срок действия токена истек", "error": "token_expired"}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.debug(f"Invalid token error: {error}")
        return {"message": "Недействительный токен", "error": "invalid_token", "details": str(error)}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        app.logger.debug(f"Missing token error: {error}")
        return {"message": "Отсутствует токен авторизации", "error": "missing_token"}, 401
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)  # Преобразуем ID в строку

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=int(identity)).one_or_none()
    
    # Регистрация API blueprints
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Регистрация обработчиков ошибок
    from app.api.errors import handle_404_error, handle_500_error
    app.register_error_handler(404, handle_404_error)
    app.register_error_handler(500, handle_500_error)
    
    return app