import os
import pandas as pd
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.api import api
from app.models import User, DataSource, Analysis, AnalysisResult, Subscription
from app.api.data.utils import get_plan_limits
from app.analytics.elasticity import calculate_elasticity
from app.analytics.forecasting import forecast_sales
from app.analytics.optimization import optimize_prices

@api.route('/analysis', methods=['GET'])
@jwt_required()
def get_analyses():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Получаем все анализы пользователя или компании
    analyses = Analysis.query.filter_by(company_id=user.company_id).all()
    
    return jsonify({
        'analyses': [analysis.to_dict() for analysis in analyses]
    }), 200

@api.route('/analysis/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis(analysis_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим анализ
    analysis = Analysis.query.filter_by(id=analysis_id, company_id=user.company_id).first()
    
    if not analysis:
        return jsonify({'message': 'Анализ не найден'}), 404
    
    # Получаем последний результат
    latest_result = AnalysisResult.query.filter_by(analysis_id=analysis.id).order_by(AnalysisResult.created_at.desc()).first()
    
    return jsonify({
        'analysis': analysis.to_dict(),
        'latest_result': latest_result.to_dict() if latest_result else None
    }), 200

@api.route('/analysis', methods=['POST'])
@jwt_required()
def create_analysis():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Проверяем лимиты тарифного плана
    subscription = Subscription.query.filter_by(company_id=user.company_id).first()
    if not subscription or not subscription.is_active():
        return jsonify({'message': 'Нет активной подписки'}), 403
    
    plan_limits = get_plan_limits(subscription.plan_type)
    
    # Проверяем количество анализов
    if plan_limits['analysis_limit'] > 0:
        analysis_count = Analysis.query.filter_by(company_id=user.company_id).count()
        if analysis_count >= plan_limits['analysis_limit']:
            return jsonify({
                'message': f'Превышен лимит анализов для вашего тарифного плана ({plan_limits["analysis_limit"]})'
            }), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Проверка обязательных полей
    required_fields = ['name', 'data_source_id', 'analysis_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Поле {field} обязательно'}), 400
    
    # Проверяем существование источника данных
    data_source = DataSource.query.filter_by(id=data['data_source_id'], company_id=user.company_id).first()
    if not data_source:
        return jsonify({'message': 'Источник данных не найден'}), 404
    
    # Создаем новый анализ
    analysis = Analysis(
        user_id=user.id,
        company_id=user.company_id,
        data_source_id=data['data_source_id'],
        name=data['name'],
        analysis_type=data['analysis_type'],
        status='pending'
    )
    
    # Сохраняем параметры анализа
    if 'parameters' in data:
        analysis.params = data['parameters']
    
    # Сохраняем расписание (если есть)
    if 'schedule' in data:
        analysis.schedule = data['schedule']
    
    db.session.add(analysis)
    db.session.commit()
    
    # Запускаем анализ (асинхронно или немедленно, в зависимости от реализации)
    run_analysis(analysis.id)
    
    return jsonify({
        'message': 'Анализ создан и запущен',
        'analysis': analysis.to_dict()
    }), 201

@api.route('/analysis/<int:analysis_id>', methods=['PUT'])
@jwt_required()
def update_analysis(analysis_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим анализ
    analysis = Analysis.query.filter_by(id=analysis_id, company_id=user.company_id).first()
    
    if not analysis:
        return jsonify({'message': 'Анализ не найден'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Отсутствуют данные'}), 400
    
    # Обновляем поля
    if 'name' in data:
        analysis.name = data['name']
    
    if 'parameters' in data:
        analysis.params = data['parameters']
    
    if 'schedule' in data:
        analysis.schedule = data['schedule']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Анализ успешно обновлен',
        'analysis': analysis.to_dict()
    }), 200

@api.route('/analysis/<int:analysis_id>/start', methods=['POST'])
@jwt_required()
def start_analysis(analysis_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим анализ
    analysis = Analysis.query.filter_by(id=analysis_id, company_id=user.company_id).first()
    
    if not analysis:
        return jsonify({'message': 'Анализ не найден'}), 404
    
    # Обновляем статус
    analysis.status = 'pending'
    db.session.commit()
    
    # Запускаем анализ
    run_analysis(analysis.id)
    
    return jsonify({
        'message': 'Анализ запущен',
        'analysis': analysis.to_dict()
    }), 200

@api.route('/analysis/<int:analysis_id>', methods=['DELETE'])
@jwt_required()
def delete_analysis(analysis_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим анализ
    analysis = Analysis.query.filter_by(id=analysis_id, company_id=user.company_id).first()
    
    if not analysis:
        return jsonify({'message': 'Анализ не найден'}), 404
    
    # Удаляем результаты анализа
    AnalysisResult.query.filter_by(analysis_id=analysis.id).delete()
    
    # Удаляем сам анализ
    db.session.delete(analysis)
    db.session.commit()
    
    return jsonify({
        'message': 'Анализ успешно удален'
    }), 200

@api.route('/analysis/<int:analysis_id>/results', methods=['GET'])
@jwt_required()
def get_analysis_results(analysis_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Пользователь не найден'}), 404
    
    # Находим анализ
    analysis = Analysis.query.filter_by(id=analysis_id, company_id=user.company_id).first()
    
    if not analysis:
        return jsonify({'message': 'Анализ не найден'}), 404
    
    # Получаем все результаты анализа
    results = AnalysisResult.query.filter_by(analysis_id=analysis.id).order_by(AnalysisResult.created_at.desc()).all()
    
    return jsonify({
        'analysis': analysis.to_dict(),
        'results': [result.to_dict() for result in results]
    }), 200

# Вспомогательная функция для запуска анализа
def run_analysis(analysis_id):
    # В реальной системе это будет асинхронная задача
    # Здесь сделаем синхронно для простоты
    analysis = Analysis.query.get(analysis_id)
    if not analysis:
        return
    
    try:
        analysis.status = 'running'
        db.session.commit()
        
        # Получаем данные для анализа
        data_source = DataSource.query.get(analysis.data_source_id)
        if not data_source:
            raise ValueError('Источник данных не найден')
        
        # Загружаем данные
        if data_source.source_type == 'file' and data_source.file_path:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], data_source.file_path)
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:  # Excel
                df = pd.read_excel(file_path)
        else:
            raise ValueError('Неподдерживаемый тип источника данных')
        
        # Запускаем соответствующий анализ
        result_data = {}
        
        if analysis.analysis_type == 'elasticity':
            result_data = calculate_elasticity(df, analysis.params)
        elif analysis.analysis_type == 'forecast':
            result_data = forecast_sales(df, analysis.params)
        elif analysis.analysis_type == 'optimization':
            result_data = optimize_prices(df, analysis.params)
        else:
            raise ValueError(f'Неподдерживаемый тип анализа: {analysis.analysis_type}')
        
        # Создаем результат анализа
        result = AnalysisResult(
            analysis_id=analysis.id,
            result_data=result_data,
            summary=generate_summary(result_data, analysis.analysis_type)
        )
        
        db.session.add(result)
        
        # Обновляем статус анализа
        analysis.status = 'completed'
        analysis.last_run = datetime.utcnow()
        
        db.session.commit()
        
    except Exception as e:
        # В случае ошибки
        analysis.status = 'failed'
        db.session.commit()
        
        # Логирование ошибки
        current_app.logger.error(f'Ошибка при выполнении анализа {analysis_id}: {str(e)}')

# Функция для генерации текстового резюме результатов анализа
def generate_summary(result_data, analysis_type):
    # В реальной системе здесь можно использовать OpenAI API
    # Для MVP сделаем простое резюме
    
    if analysis_type == 'elasticity':
        # Простое резюме для анализа эластичности
        summary = "Анализ ценовой эластичности показал следующие результаты:\n\n"
        
        if 'elasticity_by_product' in result_data:
            summary += "Эластичность по товарам:\n"
            for product, elasticity in result_data['elasticity_by_product'].items():
                elastic_type = "эластичный" if abs(elasticity) > 1 else "неэластичный"
                summary += f"- {product}: {elasticity:.2f} ({elastic_type})\n"
        
        if 'average_elasticity' in result_data:
            summary += f"\nСредняя эластичность: {result_data['average_elasticity']:.2f}"
        
        return summary
    
    elif analysis_type == 'forecast':
        # Простое резюме для прогноза
        summary = "Прогноз продаж показал следующие результаты:\n\n"
        
        if 'forecast_accuracy' in result_data:
            summary += f"Точность модели прогнозирования: {result_data['forecast_accuracy']:.2f}%\n\n"
        
        if 'forecast_summary' in result_data:
            summary += result_data['forecast_summary']
        
        return summary
    
    elif analysis_type == 'optimization':
        # Простое резюме для оптимизации цен
        summary = "Результаты оптимизации цен:\n\n"
        
        if 'optimal_prices' in result_data:
            summary += "Оптимальные цены для максимизации прибыли:\n"
            for product, price in result_data['optimal_prices'].items():
                summary += f"- {product}: {price} руб.\n"
        
        if 'expected_profit_increase' in result_data:
            summary += f"\nОжидаемое увеличение прибыли: {result_data['expected_profit_increase']:.2f}%"
        
        return summary
    
    return "Результаты анализа доступны в детальном отчете."