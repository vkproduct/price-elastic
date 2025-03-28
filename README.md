# Price Elastic
Веб-сервис для анализа ценовой эластичности, ориентированную на владельцев интернет-магазинов и маркетплейсов. Это гибридное решение, сочетающее веб-интерфейс, аналитический движок и систему автоматизации.

### Ключевые функции

- Расчет коэффициента ценовой эластичности по товарам и категориям
- Оценка эффективности маркетинговых акций
- Прогнозирование влияния изменений цен на объем продаж
- Расчет оптимальных цен для максимизации прибыли
- Интеграция с Google Sheets и другими источниками данных

## Архитектура

Система представляет собой гибридное решение, включающее:


- Фронтенд: Next.js, Shadcn/UI, TailwindCSS
- Бэкенд API: Flask/Python с интегрированным аналитическим движком
- База данных: PostgreSQL

## Разработка

### Требования

- Docker и Docker Compose
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

### Локальный запуск

```bash
# Клонировать репозиторий
git clone https://github.com/username/price-elastic.git
cd price-elastic

# Запустить проект с Docker Compose
docker-compose up -d