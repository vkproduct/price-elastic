import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def get_plan_limits(plan_type):
    """Получить лимиты для тарифного плана"""
    return current_app.config['PLAN_LIMITS'].get(plan_type, {})

def save_uploaded_file(file, filename, company_id):
    """Сохранить загруженный файл и вернуть относительный путь"""
    # Создаем уникальное имя файла
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Создаем директорию для компании, если она не существует
    company_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(company_id))
    if not os.path.exists(company_folder):
        os.makedirs(company_folder)
    
    # Полный путь к файлу
    file_path = os.path.join(company_folder, unique_filename)
    
    # Сохраняем файл
    file.save(file_path)
    
    # Возвращаем относительный путь для хранения в БД
    return os.path.join(str(company_id), unique_filename)