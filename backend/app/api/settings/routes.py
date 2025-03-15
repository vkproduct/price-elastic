import json
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.api import api
from app.models import User
from app.api.auth.utils import admin_required

# Модель для хранения настроек пользователя
class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    settings_json = db.Column(db.Text)
    
    user = db.relationship('User', backref='settings_obj', uselist=False)
    
    @property
    def settings(self):
        if self.settings_json:
            return json.loads(self.settings_json)
        return {}
    
    @settings.setter
    def settings(self, settings_dict):
        self.settings_json = json.dumps(settings_dict)

@api.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Получаем настройки пользователя
    user_settings = UserSettings.query.filter_by(user_id=user.id).first()
    
    if not user_settings:
        # Создаем настройки по умолчанию, если их нет
        user_settings = UserSettings(user_id=user.id)
        user_settings.settings = {
            'notifications': {
                'email': True,
                'slack': False
            },
            'ui': {
                'theme': 'light',
                'language': 'ru'
            },
            'analysis': {
                'default_params': {}
            }
        }
        db.session.add(user_settings)
        db.session.commit()
    
    return jsonify({
        'settings': user_settings.settings
    }), 200

@api.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Получаем настройки пользователя
    user_settings = UserSettings.query.filter_by(user_id=user.id).first()
    
    if not user_settings:
        # Создаем настройки, если их нет
        user_settings = UserSettings(user_id=user.id)
        db.session.add(user_settings)
    
    # Обновляем настройки
    current_settings = user_settings.settings
    
    # Рекурсивное объединение словарей
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                deep_update(d[k], v)
            else:
                d[k] = v
    
    deep_update(current_settings, data)
    user_settings.settings = current_settings
    
    db.session.commit()
    
    return jsonify({
        'message': 'Настройки успешно обновлены',
        'settings': user_settings.settings
    }), 200

@api.route('/settings/integrations/slack', methods=['POST'])
@jwt_required()
@admin_required
def setup_slack_integration():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    if not data or 'webhook_url' not in data:
        return jsonify({'message': 'Webhook URL не указан'}), 400
    
    # Получаем настройки компании
    company_settings = CompanySettings.query.filter_by(company_id=user.company_id).first()
    
    if not company_settings:
        # Создаем настройки компании
        company_settings = CompanySettings(company_id=user.company_id)
        db.session.add(company_settings)
    
    # Обновляем настройки интеграции Slack
    settings = company_settings.settings
    if 'integrations' not in settings:
        settings['integrations'] = {}
    
    settings['integrations']['slack'] = {
        'webhook_url': data['webhook_url'],
        'enabled': True,
        'notify_on': data.get('notify_on', ['analysis_complete', 'subscription_expiring'])
    }
    
    company_settings.settings = settings
    db.session.commit()
    
    return jsonify({
        'message': 'Интеграция со Slack настроена',
        'integration': settings['integrations']['slack']
    }), 200

# Модель для хранения настроек компании
class CompanySettings(db.Model):
    __tablename__ = 'company_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), unique=True)
    settings_json = db.Column(db.Text)
    
    company = db.relationship('Company', backref='settings_obj', uselist=False)
    
    @property
    def settings(self):
        if self.settings_json:
            return json.loads(self.settings_json)
        return {}
    
    @settings.setter
    def settings(self, settings_dict):
        self.settings_json = json.dumps(settings_dict)

@api.route('/settings/company', methods=['GET'])
@jwt_required()
@admin_required
def get_company_settings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Получаем настройки компании
    company_settings = CompanySettings.query.filter_by(company_id=user.company_id).first()
    
    if not company_settings:
        # Создаем настройки по умолчанию
        company_settings = CompanySettings(company_id=user.company_id)
        company_settings.settings = {
            'integrations': {},
            'branding': {
                'logo_url': '',
                'primary_color': '#3B82F6'
            }
        }
        db.session.add(company_settings)
        db.session.commit()
    
    return jsonify({
        'settings': company_settings.settings
    }), 200

@api.route('/settings/company', methods=['PUT'])
@jwt_required()
@admin_required
def update_company_settings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Получаем настройки компании
    company_settings = CompanySettings.query.filter_by(company_id=user.company_id).first()
    
    if not company_settings:
        # Создаем настройки, если их нет
        company_settings = CompanySettings(company_id=user.company_id)
        db.session.add(company_settings)
    
    # Обновляем настройки
    current_settings = company_settings.settings
    
    # Рекурсивное объединение словарей
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                deep_update(d[k], v)
            else:
                d[k] = v
    
    deep_update(current_settings, data)
    company_settings.settings = current_settings
    
    db.session.commit()
    
    return jsonify({
        'message': 'Настройки компании успешно обновлены',
        'settings': company_settings.settings
    }), 200