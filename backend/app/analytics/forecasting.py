import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error

def forecast_sales(df, params=None):
    """
    Прогнозирование продаж на основе исторических данных.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продажах
        params (dict): Параметры анализа
    
    Returns:
        dict: Результаты прогнозирования
    """
    if params is None:
        params = {}
    
    # Определение колонок из параметров или по умолчанию
    price_col = params.get('price_column', 'price')
    quantity_col = params.get('quantity_column', 'quantity')
    product_col = params.get('product_column', 'product')
    date_col = params.get('date_column', 'date')
    
    # Проверка наличия необходимых колонок
    required_cols = [price_col, quantity_col, date_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"В данных отсутствуют обязательные колонки: {', '.join(missing_cols)}")
    
    # Преобразование даты в datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # Извлечение временных характеристик
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    df['day_of_week'] = df[date_col].dt.dayofweek
    df['week_of_year'] = df[date_col].dt.isocalendar().week
    
    # Инициализация результатов
    result = {
        'forecast': {},
        'forecast_accuracy': 0,
        'forecast_summary': '',
        'feature_importance': {}
    }
    
    # Если есть колонка с продуктами, группируем по ней
    if product_col in df.columns:
        forecasts_by_product = {}
        accuracy_by_product = {}
        
        for product, group in df.groupby(product_col):
            product_forecast, accuracy, importance = train_forecast_model(
                group, price_col, quantity_col, params.get('forecast_periods', 30)
            )
            
            forecasts_by_product[product] = product_forecast
            accuracy_by_product[product] = accuracy
            result['feature_importance'][product] = importance
        
        result['forecast'] = forecasts_by_product
        
        # Средняя точность прогноза
        if accuracy_by_product:
            result['forecast_accuracy'] = sum(accuracy_by_product.values()) / len(accuracy_by_product)
        
        # Создаем текстовое резюме прогноза
        result['forecast_summary'] = create_forecast_summary(forecasts_by_product, accuracy_by_product)
    else:
        # Если нет колонки с продуктами, делаем общий прогноз
        forecast_data, accuracy, importance = train_forecast_model(
            df, price_col, quantity_col, params.get('forecast_periods', 30)
        )
        
        result['forecast'] = forecast_data
        result['forecast_accuracy'] = accuracy
        result['feature_importance'] = importance
        result['forecast_summary'] = f"Общий прогноз продаж с точностью {accuracy:.2f}%."
    
    return result

def train_forecast_model(df, price_col, quantity_col, forecast_periods=30):
    """
    Обучение модели прогнозирования для конкретного продукта.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продукте
        price_col (str): Название колонки с ценой
        quantity_col (str): Название колонки с количеством
        forecast_periods (int): Количество периодов для прогноза
    
    Returns:
        tuple: (прогноз, точность, важность признаков)
    """
    # Подготовка данных для обучения
    features = ['year', 'month', 'day', 'day_of_week', 'week_of_year', price_col]
    X = df[features]
    y = df[quantity_col]
    
    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Обучение модели RandomForest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Оценка точности модели
    y_pred = model.predict(X_test)
    accuracy = 100 - (mean_absolute_percentage_error(y_test, y_pred) * 100)
    
    # Важность признаков
    feature_importance = dict(zip(features, model.feature_importances_))
    
    # Создание прогноза на будущие периоды
    last_date = df['year'].max() * 10000 + df['month'].max() * 100 + df['day'].max()
    forecast_data = []
    
    # Определяем базовые значения для прогноза
    last_price = df[price_col].iloc[-1]
    avg_price_change = df[price_col].diff().mean()
    
    # Создаем данные для прогноза
    for i in range(1, forecast_periods + 1):
        # Простая логика для генерации дат (можно доработать)
        date_num = last_date + i
        year = date_num // 10000
        month = (date_num // 100) % 100
        day = date_num % 100
        
        # Корректировка месяца и дня
        if day > 28:
            day = 1
            month += 1
        if month > 12:
            month = 1
            year += 1
        
        # Прогнозируем для разных цен
        price_scenarios = {
            'current_price': last_price,
            'increased_price': last_price * 1.05,  # +5%
            'decreased_price': last_price * 0.95   # -5%
        }
        
        scenario_predictions = {}
        for scenario, price in price_scenarios.items():
            # Создаем признаки для прогноза
            features_dict = {
                'year': year,
                'month': month,
                'day': day,
                'day_of_week': pd.Timestamp(year=year, month=month, day=day).dayofweek,
                'week_of_year': pd.Timestamp(year=year, month=month, day=day).isocalendar()[1],
                price_col: price
            }
            
            # Преобразуем в формат для модели
            features_for_prediction = pd.DataFrame([features_dict])
            
            # Делаем прогноз
            prediction = model.predict(features_for_prediction)[0]
            scenario_predictions[scenario] = prediction
        
        forecast_data.append({
            'period': i,
            'date': f"{year}-{month:02d}-{day:02d}",
            'predictions': scenario_predictions
        })
    
    return forecast_data, accuracy, feature_importance

def create_forecast_summary(forecasts_by_product, accuracy_by_product):
    """
    Создание текстового резюме прогноза.
    
    Args:
        forecasts_by_product (dict): Прогнозы по продуктам
        accuracy_by_product (dict): Точность прогнозов по продуктам
    
    Returns:
        str: Текстовое резюме
    """
    summary = "Результаты прогнозирования продаж:\n\n"
    
    for product, forecast in forecasts_by_product.items():
        summary += f"Продукт: {product}\n"
        summary += f"Точность прогноза: {accuracy_by_product.get(product, 0):.2f}%\n"
        
        # Анализируем тренд для текущей цены
        first_period = forecast[0]['predictions']['current_price']
        last_period = forecast[-1]['predictions']['current_price']
        change_pct = ((last_period - first_period) / first_period) * 100 if first_period else 0
        
        if change_pct > 5:
            trend = "увеличение"
        elif change_pct < -5:
            trend = "снижение"
        else:
            trend = "стабильность"
        
        summary += f"Прогноз на {len(forecast)} периодов показывает {trend} продаж "
        summary += f"на {abs(change_pct):.1f}% при сохранении текущих цен.\n"
        
        # Оценка влияния изменения цены
        last_current = forecast[-1]['predictions']['current_price']
        last_increased = forecast[-1]['predictions']['increased_price']
        last_decreased = forecast[-1]['predictions']['decreased_price']
        
        price_elasticity = ((last_decreased - last_increased) / last_current) / 0.1
        
        if abs(price_elasticity) > 1:
            summary += "Продукт проявляет высокую чувствительность к изменению цены.\n"
        else:
            summary += "Продукт демонстрирует низкую чувствительность к изменению цены.\n"
        
        summary += "\n"
    
    return summary