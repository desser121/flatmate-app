# FlatMate

Tinder-подобное приложение для поиска жилья и соседей.

## Описание

Не каталог объявлений, а персональный подбор: человек ↔ человек ↔ жильё. Механика свайпов и рекомендаций вместо длинных списков.

## Стек

### Frontend
- React
- TypeScript
- Vite
- PWA (mobile-first)

### Backend
- Python
- Django
- Django REST Framework

### Database
- PostgreSQL

## Быстрый старт

### Клонирование

```bash
git clone https://github.com/desser121/flatmate-app.git
cd flatmate-app
```

### Настройка окружения

```bash
cp .env.example .env
# Отредактируй .env под своё окружение
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Структура проекта

```
flatmate-app/
├── README.md
├── CHANGELOG.md
├── .gitignore
├── .env.example
├── backend/
├── frontend/
└── docs/
```

## Лицензия

MIT
