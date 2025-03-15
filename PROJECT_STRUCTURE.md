# Структура проекта Price Elastic (упрощенная)
price-elastic/
├── frontend/                        # Next.js приложение
│   ├── public/                      # Статические файлы
│   ├── src/                         # Исходный код
│   │   ├── app/                     # Маршрутизация Next.js
│   │   ├── components/              # React компоненты
│   │   │   ├── ui/                  # UI компоненты из Shadcn
│   │   │   ├── dashboard/           # Компоненты дашборда
│   │   │   ├── analytics/           # Компоненты для аналитики
│   │   │   └── forms/               # Формы и инпуты
│   │   ├── lib/                     # Вспомогательные функции
│   │   ├── services/                # Сервисы для работы с API
│   │   └── contexts/                # React контексты
│   ├── tailwind.config.js           # Конфигурация Tailwind
│   ├── next.config.js               # Конфигурация Next.js
│   └── package.json                 # Зависимости и скрипты
│
├── backend/                         # Flask API + аналитика
│   ├── app/                         # Основной код приложения
│   │   ├── api/                     # API модули
│   │   │   ├── auth/                # Аутентификация
│   │   │   ├── data/                # Управление данными
│   │   │   └── analysis/            # API для анализа
│   │   ├── models/                  # Модели данных
│   │   └── analytics/               # Аналитический движок
│   │       ├── elasticity/          # Расчет эластичности
│   │       ├── forecasting/         # Прогнозирование
│   │       └── optimization/        # Оптимизация цен
│   ├── migrations/                  # Миграции базы данных
│   ├── tests/                       # Тесты
│   ├── config.py                    # Конфигурация
│   ├── requirements.txt             # Python зависимости
│   └── wsgi.py                      # Точка входа для WSGI
│
├── infrastructure/                  # Инфраструктурный код
│   └── docker/                      # Docker конфигурации
│       ├── frontend/                # Dockerfile для фронтенда
│       └── backend/                 # Dockerfile для бэкенда
│
├── docs/                            # Документация
│   ├── api/                         # API документация
│   ├── development/                 # Руководство разработчика
│   └── user/                        # Руководство пользователя
│
├── scripts/                         # Вспомогательные скрипты
│   ├── setup.sh                     # Скрипт настройки окружения
│   └── seed.py                      # Заполнение базы тестовыми данными
│
├── docker-compose.yml               # Конфигурация Docker Compose
├── .github/                         # GitHub конфигурации
│   └── workflows/                   # CI/CD пайплайны
│
├── .gitignore                       # Игнорируемые Git файлы
├── README.md                        # Общее описание проекта
└── LICENSE                          # Лицензия проекта