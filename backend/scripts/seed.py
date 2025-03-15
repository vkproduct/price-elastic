#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для создания тестовых данных в базе данных.
"""

import sys
import os
import datetime

# Добавляем директорию проекта в путь для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Company, Subscription, DataSource
from werkzeug.security import generate_password_hash

def create_test_data():
    """Создание тестовых данных в базе данных."""
    
    # Создаем компанию
    company = Company(
        name='Тестовая компания',
        website='https://example.com'
    )
    db.session.add(company)
    db.session.flush()  # Для получения ID
    
    # Создаем администратора
    admin = User(
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Админ',
        last_name='Администраторов',
        is_active=True,
        is_admin=True,
        company_id=company.id,
        last_login=datetime.datetime.utcnow()
    )
    db.session.add(admin)
    
    # Создаем обычного пользователя
    user = User(
        email='user@example.com',
        password_hash=generate_password_hash('user123'),
        first_name='Юзер',
        last_name='Пользователев',
        is_active=True,
        is_admin=False,
        company_id=company.id
    )
    db.session.add(user)
    
    # Создаем бесплатную подписку
    subscription = Subscription(
        company_id=company.id,
        plan_type='free',
        status='active',
        start_date=datetime.datetime.utcnow()
    )
    db.session.add(subscription)
    
    # Создаем тестовый источник данных
    data_source = DataSource(
        user_id=admin.id,
        company_id=company.id,
        name='Тестовые данные',
        source_type='file',
        file_path='test_data.csv',
        column_mapping='{"date": "Дата", "product": "Товар", "price": "Цена", "quantity": "Количество"}',
        row_count=100,
        created_at=datetime.datetime.utcnow(),
        last_sync=datetime.datetime.utcnow()
    )
    db.session.add(data_source)
    
    # Сохраняем всё в базу
    db.session.commit()
    
    print("Тестовые данные успешно созданы!")
    print(f"Администратор: admin@example.com / admin123")
    print(f"Пользователь: user@example.com / user123")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        create_test_data()