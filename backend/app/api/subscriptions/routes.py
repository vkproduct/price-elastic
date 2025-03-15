from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.api import api
from app.models import User, Company, Subscription, Payment
from app.api.auth.utils import admin_required

@api.route('/subscriptions', methods=['GET'])
@jwt_required()
def get_subscription():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим активную подписку компании
    subscription = Subscription.query.filter_by(company_id=user.company_id).first()
    
    if not subscription:
        return jsonify({'message': 'Подписка не найдена'}), 404
    
    # Получаем последние платежи
    payments = Payment.query.filter_by(subscription_id=subscription.id).order_by(Payment.payment_date.desc()).limit(5).all()
    
    return jsonify({
        'subscription': subscription.to_dict(),
        'payments': [payment.to_dict() for payment in payments],
        'is_active': subscription.is_active()
    }), 200

@api.route('/subscriptions/upgrade', methods=['POST'])
@jwt_required()
@admin_required
def upgrade_subscription():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    if not data or 'plan_type' not in data:
        return jsonify({'message': 'Не указан тип тарифного плана'}), 400
    
    # Проверяем допустимость плана
    plan_type = data['plan_type']
    valid_plans = ['free', 'standard', 'business', 'enterprise']
    if plan_type not in valid_plans:
        return jsonify({'message': f'Недопустимый тип плана. Выберите один из: {", ".join(valid_plans)}'}), 400
    
    # Находим текущую подписку
    subscription = Subscription.query.filter_by(company_id=user.company_id).first()
    
    if not subscription:
        # Создаем новую подписку, если не существует
        subscription = Subscription(
            company_id=user.company_id,
            plan_type=plan_type,
            status='active',
            start_date=datetime.utcnow()
        )
        db.session.add(subscription)
    else:
        # Обновляем существующую подписку
        subscription.plan_type = plan_type
        subscription.status = 'active'
        subscription.start_date = datetime.utcnow()
    
    # Устанавливаем срок действия подписки
    if plan_type != 'free':
        subscription.end_date = datetime.utcnow() + timedelta(days=30)  # 30 дней для платных планов
    else:
        subscription.end_date = None  # Бессрочно для бесплатного плана
    
    # Для платных планов создаем запись о платеже
    if plan_type != 'free':
        payment_amount = 0
        if plan_type == 'standard':
            payment_amount = 49
        elif plan_type == 'business':
            payment_amount = 149
        elif plan_type == 'enterprise':
            payment_amount = 499
        
        payment = Payment(
            subscription_id=subscription.id,
            amount=payment_amount,
            currency='USD',
            payment_method=data.get('payment_method', 'card'),
            transaction_id=data.get('transaction_id', ''),
            status='completed',
            payment_date=datetime.utcnow()
        )
        db.session.add(payment)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Подписка успешно обновлена',
        'subscription': subscription.to_dict()
    }), 200

@api.route('/subscriptions/cancel', methods=['POST'])
@jwt_required()
@admin_required
def cancel_subscription():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим подписку
    subscription = Subscription.query.filter_by(company_id=user.company_id).first()
    
    if not subscription:
        return jsonify({'message': 'Подписка не найдена'}), 404
    
    # Отменяем подписку
    subscription.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        'message': 'Подписка успешно отменена',
        'subscription': subscription.to_dict()
    }), 200

@api.route('/webhooks/payment', methods=['POST'])
def payment_webhook():
    # Обработка уведомлений от платежной системы
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Проверка типа события
    event_type = data.get('type')
    if not event_type:
        return jsonify({'message': 'Тип события не указан'}), 400
    
    # Обработка различных типов событий
    if event_type == 'payment.succeeded':
        # Находим подписку по ID
        subscription_id = data.get('subscription_id')
        if not subscription_id:
            return jsonify({'message': 'ID подписки не указан'}), 400
        
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify({'message': 'Подписка не найдена'}), 404
        
        # Создаем запись о платеже
        payment = Payment(
            subscription_id=subscription.id,
            amount=data.get('amount', 0),
            currency=data.get('currency', 'USD'),
            payment_method=data.get('payment_method', ''),
            transaction_id=data.get('transaction_id', ''),
            status='completed',
            payment_date=datetime.utcnow()
        )
        db.session.add(payment)
        
        # Обновляем статус подписки
        subscription.status = 'active'
        subscription.end_date = datetime.utcnow() + timedelta(days=30)  # Продлеваем на 30 дней
        
        db.session.commit()
        
        return jsonify({'message': 'Платеж успешно обработан'}), 200
    
    elif event_type == 'payment.failed':
        # Обработка неудачного платежа
        subscription_id = data.get('subscription_id')
        if not subscription_id:
            return jsonify({'message': 'ID подписки не указан'}), 400
        
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify({'message': 'Подписка не найдена'}), 404
        
        # Создаем запись о неудачном платеже
        payment = Payment(
            subscription_id=subscription.id,
            amount=data.get('amount', 0),
            currency=data.get('currency', 'USD'),
            payment_method=data.get('payment_method', ''),
            transaction_id=data.get('transaction_id', ''),
            status='failed',
            payment_date=datetime.utcnow()
        )
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({'message': 'Неудачный платеж зарегистрирован'}), 200
    
    return jsonify({'message': 'Неизвестный тип события'}), 400