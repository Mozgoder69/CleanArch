CleanArch
PostgreSQL + Python + Psycopg2 + Pyramid + Dynamic Interfaces

Structure is aligned with Clean Architecture principles

CleanArch/
│
├─ database/       # Адаптеры данных
│  └─ postgres.py  # Подключения БД
│
├─ domain/         # Micro-ORM
│  ├─ models.py    # Отношения (может содержать код из models.py)
│  └─ events.py    # Бизнес-Логика
│
├─ interface/      # Micro-API
│  ├─ endpoints/   # Маршруты
│  │  └─ views.py  # Представления
│  └─ documents/    # Сериализация
│     └─ templates/  # Шаблоны
│
├─ framework/      # Micro-Web
│  └─ pyramid/     # Pyramid
│     └─ middlewares/ # Логирование
│
├─ config/         # Администрирование
│  └─ settings.py  # Метаданные приложения
│
├─ test/           # Тесты
│  ├─ test_orm.py  # Тесты Micro-ORM
│  ├─ test_api.py  # Тесты Micro-API
│  └─ test_web.py  # Тесты Micro-Web
│
└─ main.py          # Точка входа