import os
from datetime import datetime
import pandas as pd
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app import db
from app.api import api
from app.models import User, DataSource, Subscription
from app.api.data.utils import get_plan_limits, save_uploaded_file

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/data/sources', methods=['GET'])
@jwt_required()
def get_data_sources():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Получаем все источники данных пользователя или компании
    data_sources = DataSource.query.filter_by(company_id=user.company_id).all()
    
    return jsonify({
        'data_sources': [ds.to_dict() for ds in data_sources]
    }), 200

@api.route('/data/sources/<int:source_id>', methods=['GET'])
@jwt_required()
def get_data_source(source_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим источник данных
    data_source = DataSource.query.filter_by(id=source_id, company_id=user.company_id).first()
    
    if not data_source:
        return jsonify({'message': 'Источник данных не найден'}), 404
    
    # Определяем путь к файлу
    if data_source.source_type == 'file' and data_source.file_path:
        try:
            # Чтение CSV или Excel файла
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], data_source.file_path)
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:  # Excel
                df = pd.read_excel(file_path)
            
            # Ограничиваем количество строк для предпросмотра
            preview_rows = min(100, len(df))
            
            return jsonify({
                'data_source': data_source.to_dict(),
                'preview': df.head(preview_rows).to_dict(orient='records'),
                'columns': list(df.columns),
                'row_count': len(df)
            }), 200
        
        except Exception as e:
            return jsonify({
                'message': f'Ошибка чтения файла: {str(e)}',
                'data_source': data_source.to_dict()
            }), 500
    
    # Для других типов источников (Google Sheets и т.д.)
    return jsonify({
        'data_source': data_source.to_dict(),
        'message': 'Предпросмотр данных недоступен для этого типа источника'
    }), 200

@api.route('/data/sources', methods=['POST'])
@jwt_required()
def create_data_source():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Проверяем лимиты тарифного плана
    subscription = Subscription.query.filter_by(company_id=user.company_id).first()
    if not subscription or not subscription.is_active():
        return jsonify({'message': 'Нет активной подписки'}), 403
    
    # Проверка на тип источника
    source_type = request.form.get('source_type')
    if not source_type:
        return jsonify({'message': 'Не указан тип источника данных'}), 400
    
    # Создаем новый источник данных
    data_source = DataSource(
        user_id=user.id,
        company_id=user.company_id,
        name=request.form.get('name', 'Новый источник данных'),
        source_type=source_type
    )
    
    # Обработка файла
    if source_type == 'file':
        # Проверяем, был ли файл в запросе
        if 'file' not in request.files:
            return jsonify({'message': 'Файл не найден в запросе'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'Файл не выбран'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'message': 'Недопустимый тип файла. Разрешены только CSV и Excel файлы'}), 400
        
        # Получаем лимиты тарифного плана
        plan_limits = get_plan_limits(subscription.plan_type)
        
        try:
            # Чтение файла для проверки количества строк
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:  # Excel
                df = pd.read_excel(file)
            
            # Проверка количества строк
            row_count = len(df)
            if plan_limits['data_rows_limit'] > 0 and row_count > plan_limits['data_rows_limit']:
                return jsonify({
                    'message': f'Превышен лимит строк для вашего тарифного плана ({plan_limits["data_rows_limit"]})'
                }), 403
            
            # Сохраняем файл
            filename = secure_filename(file.filename)
            file_path = save_uploaded_file(file, filename, user.company_id)
            
            data_source.file_path = file_path
            data_source.row_count = row_count
            
        except Exception as e:
            return jsonify({'message': f'Ошибка обработки файла: {str(e)}'}), 500
    
    # Обработка Google Sheets
    elif source_type == 'google_sheets':
        sheet_id = request.form.get('google_sheet_id')
        if not sheet_id:
            return jsonify({'message': 'Не указан ID Google Sheets'}), 400
        
        data_source.google_sheet_id = sheet_id
        # TODO: Добавить синхронизацию с Google Sheets
    
    # Маппинг колонок (если предоставлен)
    column_mapping = request.form.get('column_mapping')
    if column_mapping:
        data_source.column_mapping = column_mapping
    
    db.session.add(data_source)
    db.session.commit()
    
    return jsonify({
        'message': 'Источник данных успешно создан',
        'data_source': data_source.to_dict()
    }), 201

@api.route('/data/sources/<int:source_id>', methods=['PUT'])
@jwt_required()
def update_data_source(source_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим источник данных
    data_source = DataSource.query.filter_by(id=source_id, company_id=user.company_id).first()
    
    if not data_source:
        return jsonify({'message': 'Источник данных не найден'}), 404
    
    data = request.form or request.get_json() or {}
    
    # Обновляем базовые поля
    if 'name' in data:
        data_source.name = data['name']
    
    # Обновляем маппинг колонок
    if 'column_mapping' in data:
        data_source.column_mapping = data['column_mapping']
    
    # Обновляем файл, если загружен новый
    if data_source.source_type == 'file' and 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '' and allowed_file(file.filename):
            try:
                # Удаляем старый файл
                if data_source.file_path:
                    old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], data_source.file_path)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Сохраняем новый файл
                filename = secure_filename(file.filename)
                file_path = save_uploaded_file(file, filename, user.company_id)
                
                # Чтение файла для обновления количества строк
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:  # Excel
                    df = pd.read_excel(file)
                
                data_source.file_path = file_path
                data_source.row_count = len(df)
                data_source.last_sync = datetime.utcnow()
                
            except Exception as e:
                return jsonify({'message': f'Ошибка обработки файла: {str(e)}'}), 500
    
    # Обновляем Google Sheets ID
    if data_source.source_type == 'google_sheets' and 'google_sheet_id' in data:
        data_source.google_sheet_id = data['google_sheet_id']
        # TODO: Добавить синхронизацию с Google Sheets
    
    db.session.commit()
    
    return jsonify({
        'message': 'Источник данных успешно обновлен',
        'data_source': data_source.to_dict()
    }), 200

@api.route('/data/sources/<int:source_id>', methods=['DELETE'])
@jwt_required()
def delete_data_source(source_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим источник данных
    data_source = DataSource.query.filter_by(id=source_id, company_id=user.company_id).first()
    
    if not data_source:
        return jsonify({'message': 'Источник данных не найден'}), 404
    
    # Удаляем файл, если это файловый источник
    if data_source.source_type == 'file' and data_source.file_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], data_source.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Удаляем источник данных
    db.session.delete(data_source)
    db.session.commit()
    
    return jsonify({
        'message': 'Источник данных успешно удален'
    }), 200