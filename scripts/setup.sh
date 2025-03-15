#!/bin/bash

# Настройка окружения для разработки

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Начинаем настройку проекта Price Elastic...${NC}"

# Создаем директории для загруженных файлов
echo -e "${GREEN}Создаем директории для загруженных файлов...${NC}"
mkdir -p backend/uploads

# Установка Python зависимостей
echo -e "${GREEN}Устанавливаем Python зависимости...${NC}"
cd backend
python -m pip install -r requirements.txt

# Создание базы данных
echo -e "${GREEN}Инициализируем базу данных...${NC}"
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Создание тестовых данных (при необходимости)
echo -e "${GREEN}Создаем тестовые данные...${NC}"
python scripts/seed.py

echo -e "${GREEN}Настройка бэкенда завершена успешно!${NC}"

# Возвращаемся в корневую директорию
cd ..

echo -e "${YELLOW}Настройка проекта Price Elastic завершена.${NC}"
echo -e "${GREEN}Вы можете запустить бэкенд командой:${NC}"
echo -e "cd backend && python run.py"