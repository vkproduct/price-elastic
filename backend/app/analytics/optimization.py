import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_prices(df, params=None):
    """
    Оптимизация цен для максимизации прибыли.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продажах
        params (dict): Параметры анализа
    
    Returns:
        dict: Результаты оптимизации цен
    """
    if params is None:
        params = {}
    
    # Определение колонок из параметров или по умолчанию
    price_col = params.get('price_column', 'price')
    quantity_col = params.get('quantity_column', 'quantity')
    product_col = params.get('product_column', 'product')
    cost_col = params.get('cost_column')  # Колонка с себестоимостью (опционально)
    
    # Проверка наличия необходимых колонок
    required_cols = [price_col, quantity_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"В данных отсутствуют обязательные колонки: {', '.join(missing_cols)}")
    
    # Инициализация результатов
    result = {
        'optimal_prices': {},
        'expected_profit_increase': 0,
        'expected_revenue_change': 0,
        'price_recommendations': []
    }
    
    # Если есть колонка с продуктами, оптимизируем по каждому продукту
    if product_col in df.columns:
        current_profit = 0
        optimized_profit = 0
        current_revenue = 0
        optimized_revenue = 0
        
        for product, group in df.groupby(product_col):
            # Рассчитываем оптимальную цену
            optimal_price, expected_quantity, current_price_avg, current_quantity_avg = find_optimal_price(
                group, price_col, quantity_col, cost_col
            )
            
            result['optimal_prices'][product] = optimal_price
            
            # Расчет текущей и ожидаемой прибыли
            current_cost = 0
            if cost_col and cost_col in group.columns:
                current_cost = group[cost_col].mean()
            
            current_product_profit = (current_price_avg - current_cost) * current_quantity_avg
            optimized_product_profit = (optimal_price - current_cost) * expected_quantity
            
            current_profit += current_product_profit
            optimized_profit += optimized_product_profit
            
            current_revenue += current_price_avg * current_quantity_avg
            optimized_revenue += optimal_price * expected_quantity
            
            # Добавляем рекомендацию
            change_pct = ((optimal_price - current_price_avg) / current_price_avg) * 100
            direction = "повышение" if change_pct > 0 else "снижение"
            
            recommendation = {
                'product': product,
                'current_price': current_price_avg,
                'optimal_price': optimal_price,
                'price_change_percent': change_pct,
                'expected_quantity': expected_quantity,
                'current_quantity': current_quantity_avg,
                'quantity_change_percent': ((expected_quantity - current_quantity_avg) / current_quantity_avg) * 100,
                'recommendation': f"Рекомендуется {direction} цены на {abs(change_pct):.1f}% для максимизации прибыли."
            }
            
            result['price_recommendations'].append(recommendation)
        
        # Расчет ожидаемого увеличения прибыли
        if current_profit > 0:
            result['expected_profit_increase'] = ((optimized_profit - current_profit) / current_profit) * 100
        
        # Расчет ожидаемого изменения выручки
        if current_revenue > 0:
            result['expected_revenue_change'] = ((optimized_revenue - current_revenue) / current_revenue) * 100
    else:
        # Если нет колонки с продуктами, делаем общую оптимизацию
        optimal_price, expected_quantity, current_price_avg, current_quantity_avg = find_optimal_price(
            df, price_col, quantity_col, cost_col
        )
        
        result['optimal_prices']['overall'] = optimal_price
        
        # Расчет текущей и ожидаемой прибыли
        current_cost = 0
        if cost_col and cost_col in df.columns:
            current_cost = df[cost_col].mean()
        
        current_profit = (current_price_avg - current_cost) * current_quantity_avg
        optimized_profit = (optimal_price - current_cost) * expected_quantity
        
        if current_profit > 0:
            result['expected_profit_increase'] = ((optimized_profit - current_profit) / current_profit) * 100
        
        # Расчет ожидаемого изменения выручки
        current_revenue = current_price_avg * current_quantity_avg
        optimized_revenue = optimal_price * expected_quantity
        
        if current_revenue > 0:
            result['expected_revenue_change'] = ((optimized_revenue - current_revenue) / current_revenue) * 100
        
        # Добавляем рекомендацию
        change_pct = ((optimal_price - current_price_avg) / current_price_avg) * 100
        direction = "повышение" if change_pct > 0 else "снижение"
        
        recommendation = {
            'product': 'overall',
            'current_price': current_price_avg,
            'optimal_price': optimal_price,
            'price_change_percent': change_pct,
            'expected_quantity': expected_quantity,
            'current_quantity': current_quantity_avg,
            'quantity_change_percent': ((expected_quantity - current_quantity_avg) / current_quantity_avg) * 100,
            'recommendation': f"Рекомендуется {direction} цены на {abs(change_pct):.1f}% для максимизации прибыли."
        }
        
        result['price_recommendations'].append(recommendation)
    
    return result

def find_optimal_price(df, price_col, quantity_col, cost_col=None):
    """
    Нахождение оптимальной цены для максимизации прибыли.
    
    Args:
        df (pandas.DataFrame): Датафрейм с данными о продукте
        price_col (str): Название колонки с ценой
        quantity_col (str): Название колонки с количеством
        cost_col (str, optional): Название колонки с себестоимостью
    
    Returns:
        tuple: (оптимальная цена, ожидаемое количество, средняя текущая цена, среднее текущее количество)
    """
    # Расчет средних значений
    current_price_avg = df[price_col].mean()
    current_quantity_avg = df[quantity_col].mean()
    
    # Если недостаточно вариаций цены, возвращаем текущую
    if df[price_col].nunique() <= 1:
        return current_price_avg, current_quantity_avg, current_price_avg, current_quantity_avg
    
    # Определение себестоимости
    cost = 0
    if cost_col and cost_col in df.columns:
        cost = df[cost_col].mean()
    
    # Создание модели зависимости количества от цены
    # Для простоты используем линейную регрессию для оценки эластичности
    X = df[price_col].values
    y = df[quantity_col].values
    
    # Подгонка линейной модели вида: quantity = a + b * price
    # Это упрощение; в реальности можно использовать более сложные модели
    A = np.vstack([X, np.ones(len(X))]).T
    b, a = np.linalg.lstsq(A, y, rcond=None)[0]
    
    # Функция для оценки количества при заданной цене
    def predict_quantity(price):
        return a + b * price
    
    # Функция прибыли для оптимизации (с отрицательным знаком для максимизации)
    def profit_function(price):
        quantity = predict_quantity(price[0])
        if quantity < 0:  # Физически невозможное количество
            return 0
        return -1 * (price[0] - cost) * quantity
    
    # Ограничения для оптимизации (цена должна быть положительной)
    constraints = ({'type': 'ineq', 'fun': lambda x: x[0]})
    
    # Начальное приближение (текущая цена)
    x0 = [current_price_avg]
    
    # Оптимизация
    result = minimize(profit_function, x0, constraints=constraints, method='SLSQP')
    
    # Извлечение оптимальной цены
    optimal_price = result.x[0]
    
    # Расчет ожидаемого количества при оптимальной цене
    expected_quantity = predict_quantity(optimal_price)
    
    # Проверка на отрицательное количество (нереалистичное)
    if expected_quantity < 0:
        return current_price_avg, current_quantity_avg, current_price_avg, current_quantity_avg
    
    return optimal_price, expected_quantity, current_price_avg, current_quantity_avg