import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_elasticity(df, params=None):
    """
    Расчет ценовой эластичности спроса.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продажах
        params (dict): Параметры анализа
    
    Returns:
        dict: Результаты анализа эластичности
    """
    if params is None:
        params = {}
    
    # Определение колонок из параметров или по умолчанию
    price_col = params.get('price_column', 'price')
    quantity_col = params.get('quantity_column', 'quantity')
    product_col = params.get('product_column', 'product')
    date_col = params.get('date_column', 'date')
    
    # Проверка наличия необходимых колонок
    required_cols = [price_col, quantity_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"В данных отсутствуют обязательные колонки: {', '.join(missing_cols)}")
    
    # Инициализация результатов
    result = {
        'elasticity_by_product': {},
        'average_elasticity': 0,
        'elastic_products': [],
        'inelastic_products': [],
        'segmentation': {}
    }
    
    # Если есть колонка с продуктами, группируем по ней
    if product_col in df.columns:
        # Расчет эластичности для каждого продукта
        for product, group in df.groupby(product_col):
            elasticity = calculate_product_elasticity(group, price_col, quantity_col)
            result['elasticity_by_product'][product] = elasticity
            
            # Классификация по эластичности
            if abs(elasticity) > 1:
                result['elastic_products'].append(product)
            else:
                result['inelastic_products'].append(product)
        
        # Средняя эластичность
        if result['elasticity_by_product']:
            result['average_elasticity'] = sum(result['elasticity_by_product'].values()) / len(result['elasticity_by_product'])
        
        # Сегментация продуктов по эластичности
        elasticity_values = list(result['elasticity_by_product'].values())
        if elasticity_values:
            low_threshold = np.percentile(elasticity_values, 33)
            high_threshold = np.percentile(elasticity_values, 66)
            
            result['segmentation'] = {
                'low_elasticity': [p for p, e in result['elasticity_by_product'].items() if e <= low_threshold],
                'medium_elasticity': [p for p, e in result['elasticity_by_product'].items() if low_threshold < e <= high_threshold],
                'high_elasticity': [p for p, e in result['elasticity_by_product'].items() if e > high_threshold]
            }
    else:
        # Если нет колонки с продуктами, рассчитываем общую эластичность
        elasticity = calculate_product_elasticity(df, price_col, quantity_col)
        result['average_elasticity'] = elasticity
    
    # Если есть временная колонка, добавляем анализ по времени
    if date_col in df.columns and df[date_col].nunique() > 1:
        # Преобразование к datetime, если это строка
        if df[date_col].dtype == 'object':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Группировка по месяцам и расчет эластичности
        df['month'] = df[date_col].dt.to_period('M')
        result['elasticity_by_month'] = {}
        
        for month, group in df.groupby('month'):
            if product_col in df.columns:
                month_elasticities = {}
                for product, product_group in group.groupby(product_col):
                    if product_group[price_col].nunique() > 1:
                        month_elasticities[product] = calculate_product_elasticity(product_group, price_col, quantity_col)
                
                if month_elasticities:
                    result['elasticity_by_month'][str(month)] = {
                        'elasticities': month_elasticities,
                        'average': sum(month_elasticities.values()) / len(month_elasticities)
                    }
            else:
                if group[price_col].nunique() > 1:
                    result['elasticity_by_month'][str(month)] = calculate_product_elasticity(group, price_col, quantity_col)
    
    return result

def calculate_product_elasticity(df, price_col, quantity_col):
    """
    Расчет эластичности для конкретного продукта с использованием регрессии.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продукте
        price_col (str): Название колонки с ценой
        quantity_col (str): Название колонки с количеством
    
    Returns:
        float: Коэффициент эластичности
    """
    # Проверка наличия достаточного количества уникальных цен
    if df[price_col].nunique() <= 1:
        return 0  # Невозможно рассчитать эластичность при одной цене
    
    # Логарифмирование для расчета эластичности
    df = df.copy()
    df['log_price'] = np.log(df[price_col])
    df['log_quantity'] = np.log(df[quantity_col])
    
    # Создание модели регрессии
    model = LinearRegression()
    X = df['log_price'].values.reshape(-1, 1)
    y = df['log_quantity'].values
    
    # Обучение модели
    model.fit(X, y)
    
    # Коэффициент эластичности - это коэффициент наклона в логарифмической модели
    elasticity = model.coef_[0]
    
    return elasticity