# 🎓 Кредитный скоринг: прогнозирование дефолта

> Прогнозирование вероятности дефолта клиента при выплате кредита с помощью методов машинного обучения.

## 📋 Описание проекта

Проект реализует полный ML-пайплайн:
- **Разведочный анализ данных (EDA)** — визуализация распределений, корреляции
- **Feature Engineering** — конструирование признаков, агрегация таблиц
- **Сравнение моделей** — Logistic Regression, Random Forest, CatBoost
- **Оптимизация гиперпараметров** — байесовский поиск с Optuna
- **Финальная оценка** — ROC-AUC, Precision, Recall, F1

## 📊 Датасет

**Home Credit Default Risk** (Kaggle)

| Параметр | Значение |
|----------|----------|
| Основной файл | `application_train.csv` |
| Записей | 307 511 заявок |
| Признаков | 122 столбца |
| Целевая переменная | `TARGET` (0 — без дефолта, 1 — дефолт) |
| Дополнительные таблицы | `bureau`, `credit_card_balance`, `installments_payments`, `POS_CASH_balance`, `previous_application` |

[📎 Kaggle Competition](https://www.kaggle.com/competitions/home-credit-default-risk/data)

## 🛠 Стек технологий

| Инструмент | Назначение |
|------------|------------|
| **Python 3.x** | Язык программирования |
| **pandas, numpy** | Обработка и анализ данных |
| **matplotlib, seaborn** | Визуализация |
| **scikit-learn** | Базовые модели, метрики, кросс-валидация |
| **CatBoost** | Основная модель (GPU-ускорение) |
| **XGBoost, LightGBM** | Сравнительные модели |
| **Optuna** | Байесовская оптимизация гиперпараметров |
| **imbalanced-learn** | Работа со сбалансированностью классов |

## 📁 Структура проекта

```
├── data/                          # Исходные данные
│   ├── application_train.csv      # Обучающая выборка (307k строк)
│   ├── application_test.csv       # Тестовая выборка
│   ├── bureau.csv                 # История кредитов в других банках
│   ├── credit_card_balance.csv    # Данные по кредитным картам
│   ├── installments_payments.csv  # История платежей
│   ├── POS_CASH_balance.csv       # POS-кредиты
│   └── previous_application.csv   # Предыдущие заявки
├── notebooks/
│   ├── notebook.ipynb             # Исходный код (без результатов)
│   └── notebook_results.ipynb     # ✅ Выполненный ноутбук с результатами и графиками
├── scripts/                       # Вспомогательные скрипты
├── models/                        # Сохранённые модели
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/mukhitmakhmutov-cell/alpha-edu-individual-2-credit-score.git
cd alpha-edu-individual-2-credit-score
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Подготовка данных
Скачайте датасет с [Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk/data) и поместите CSV-файлы в папку `data/`.

### 5. Запуск
```bash
# Интерактивный режим
jupyter notebook notebooks/notebook.ipynb

# Или выполнение через командную строку
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=1200 --output notebook_results.ipynb notebooks/notebook.ipynb
```

## 📈 Результаты

### Сравнение моделей (3-fold Cross-Validation)

| Модель | ROC-AUC (mean) | ROC-AUC (std) |
|--------|---------------|---------------|
| LogisticRegression (balanced) | 0.7469 | 0.0016 |
| RandomForest | 0.7400 | 0.0002 |
| **CatBoost (GPU)** | **0.7599** | **0.0011** |

### Финальная модель: CatBoost (Optuna-оптимизированная)

| Метрика | Значение |
|---------|----------|
| **ROC-AUC** | **0.7682** |
| Accuracy | 0.7107 |
| Precision | 0.1729 |
| Recall | 0.6830 |
| F1-score | 0.2760 |

### Оптимизация гиперпараметров (Optuna)

- **Количество итераций:** 30
- **Лучший ROC-AUC (CV):** 0.7616
- **Приоритетная модель:** CatBoost (GPU)
- **Прирост относительно baseline:** +0.0213 ROC-AUC

## 🏗 Архитектура решения

### Предобработка данных
1. Загрузка и первичная очистка
2. Удаление константных признаков (`std < 1e-6`)
3. Кодирование категориальных переменных
4. Заполнение пропусков медианой/модой
5. Разделение на обучающую и тестовую выборки (80/20, стратификация)

### Feature Engineering
1. Агрегация по таблицам `bureau`, `credit_card`, `installments`, `POS_CASH`, `previous_application`
2. Создание признаков на основе дней (`DAYS_*`)
3. Логарифмическое преобразование skewed-признаков
4. Отбор признаков по корреляции и важности

### Моделирование
1. **Baseline:** Logistic Regression, Random Forest
2. **Основная:** CatBoost с GPU-ускорением (`task_type='GPU'`)
3. **Оптимизация:** Optuna для подбора гиперпараметров
4. **Кросс-валидация:** 3-fold StratifiedKFold

### GPU-ускорение
- **GPU:** NVIDIA GeForce RTX 3050 (4GB VRAM)
- **CatBoost:** `task_type='GPU'`, `devices='0'`
- **Примечание:** XGBoost и LightGBM отключены (ограничения WDDM на Windows)

## 📝 Выводы

1. **CatBoost** показал наилучшие результаты среди всех протестированных моделей
2. **GPU-ускорение** значительно сократило время обучения
3. **Optuna** дала прирост ~0.006 ROC-AUC по сравнению с дефолтными параметрами
4. **Class imbalance** успешно обрабатывается через `scale_pos_weight`
5. **Feature Engineering** на основе дополнительных таблиц улучшил качество модели

## 👤 Автор

**Mukhit Makhmutov** — разработка ML-пайплайна, оптимизация моделей, документация

## 📄 Лицензия

Проект создан в образовательных целях в рамках курса Alpha Edu.
