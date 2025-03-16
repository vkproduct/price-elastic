from datetime import datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    get_jwt_identity, get_jwt, verify_jwt_in_request
)
import traceback
from functools import wraps

from app import db, jwt
from app.api import api
from app.models import User, Company, Subscription
from app.api.auth.utils import admin_required

# Вспомогательная функция для отладки JWT
def debug_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                auth_header = request.headers.get('Authorization', '')
                current_app.logger.debug(f"Auth header: {auth_header}")
                
                if not auth_header:
                    return jsonify({'message': 'Отсутствует заголовок Authorization'}), 401
                
                # Пытаемся вручную проверить токен
                parts = auth_header.split()
                if len(parts) != 2 or parts[0] != 'Bearer':
                    return jsonify({'message': f'Неверный формат заголовка: {auth_header}'}), 401
                
                token = parts[1]
                current_app.logger.debug(f"Extracted token: {token[:20]}...")
                
                # Стандартная проверка JWT
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"JWT verification error: {str(e)}")
                traceback.print_exc()
                return jsonify({
                    'message': 'Ошибка проверки токена', 
                    'error': 'invalid_token',
                    'details': str(e)
                }), 401
        return decorator
    return wrapper

# Добавим тестовый эндпоинт без JWT для проверки
@api.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        'message': 'Тестовый эндпоинт работает!',
        'headers': dict(request.headers)
    }), 200

# Временный эндпоинт для подписок без JWT
@api.route('/subscriptions-test', methods=['GET'])
def get_subscription_test():
    try:
        # Здесь используем фиксированный ID пользователя = 1
        user_id = 1
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Пользователь не найден'}), 404
        
        # Находим активную подписку компании
        subscription = Subscription.query.filter_by(company_id=user.company_id).first()
        
        if not subscription:
            return jsonify({'message': 'Подписка не найдена'}), 404
        
        return jsonify({
            'subscription': subscription.to_dict(),
            'is_active': subscription.is_active()
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_subscription_test: {str(e)}")
        return jsonify({'message': f'Ошибка: {str(e)}'}), 500

# Остальные маршруты без изменений
@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Проверка обязательных полей
    required_fields = ['email', 'password', 'company_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Поле {field} обязательно'}), 400
    
    # Проверка на существование пользователя
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Пользователь с таким email уже существует'}), 409
    
    # Создаем компанию
    company = Company(name=data['company_name'])
    db.session.add(company)
    db.session.flush()  # Получаем ID без коммита
    
    # Создаем пользователя
    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        company_id=company.id,
        is_admin=True  # Первый пользователь компании всегда админ
    )
    user.password = data['password']
    db.session.add(user)
    
    # Создаем бесплатную подписку
    subscription = Subscription(
        company_id=company.id,
        plan_type='free',
        status='active'
    )
    db.session.add(subscription)
    
    db.session.commit()
    
    # Создаем токены
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Для отладки
    current_app.logger.debug(f"Created access token: {access_token[:20]}...")
    
    return jsonify({
        'message': 'Пользователь успешно зарегистрирован',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Проверка обязательных полей
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Необходимы email и пароль'}), 400
    
    # Поиск пользователя
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Неверный email или пароль'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Аккаунт деактивирован'}), 403
    
    # Обновляем время последнего входа
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Создаем токены
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Для отладки
    current_app.logger.debug(f"Created access token: {access_token[:20]}...")
    current_app.logger.debug(f"JWT secret key: {current_app.config.get('JWT_SECRET_KEY')[:5]}...")
    
    return jsonify({
        'message': 'Вход выполнен успешно',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@api.route('/auth/me', methods=['GET'])
@jwt_required()
def get_user_info():
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.debug(f"User ID from JWT: {current_user_id}")
        
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'Пользователь не найден'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'company': user.company.to_dict() if user.company else None
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_user_info: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'Ошибка: {str(e)}'}), 500

# Остальные маршруты с обычным @jwt_required() без изменений