# Detection of fraudulent transactions in mobile transfers
AI Engineering Course Project: Machine Learning


## About the project
Development of an ML model for detecting fraud in the mobile payment flow. The main task is to find a balance between catching fraud (Recall) and minimizing false locks (FP) through a business—oriented threshold setting.


## Data
- Source: Kaggle (Synthetic Banking Dataset)
- Volume: 50,000 transactions
- Imbalance: ~68% honest, ~32% fraudulent
- Key features: timestamps, aggregated activity for 7 days, context (geo, device, authorization method)


## Methodology
- **EDA & Statistics:** KS distribution test, Pearson correlation (Failed_Transaction_Count_7d, r=0.51, p<0.001)
- **Models:** Logistic Regression (baseline), Random Forest + Optuna
- **Validation:** 80/20 chronological split (no leaks), cross-validation for tuning
- **Business logic:** Cost-Function (FN=1000, FP=250, StepUp=50), selecting the optimal threshold via predict_proba().


## Results (Test Set)
| Model | Threshold | Precision | Recall | Cost (tg)  |
|---------------------|-------|-----------|--------|------------|
| Logistic Regression | ~0.35 | 0.68      | 0.85   | ~750 000   |
| RF + Optuna         | ~0.19 | 0.37      | 0.90   | ~1 566 000 |

**Business solution:** At current error weights, LogReg with a threshold of ~0.35 is more cost-effective. RF requires Step-Up verification to justify high FP.


## How to launch
```bash
pip install -r requirements.txt
jupyter lab notebooks/01_EDA.ipynb
```




# Детекция мошеннических транзакций в мобильных переводах
Проект курса AI Engineering: Machine Learning


## О проекте
Разработка ML-модели для выявления мошенничества в потоке мобильных платежей. Основная задача — найти баланс между ловлей фрода (Recall) и минимизацией ложных блокировок (FP) через бизнес-ориентированную настройку порога срабатывания.


## Данные
- Источник: Kaggle (синтетический банковский датасет)
- Объём: 50 000 транзакций
- Дисбаланс: ~68% честные, ~32% мошеннические
- Ключевые признаки: временные метки, агрегированная активность за 7 дней, контекст (гео, устройство, способ авторизации)


## Методология
- **EDA & Статистика:** KS-тест распределений, корреляция Пирсона (Failed_Transaction_Count_7d, r=0.51, p<0.001)
- **Модели:** Logistic Regression (baseline), Random Forest + Optuna
- **Валидация:** Хронологический сплит 80/20 (без утечек), кросс-валидация для тюнинга
- **Бизнес-логика:** Cost-Function (FN=1000, FP=250, StepUp=50), подбор оптимального порога через predict_proba().


## Результаты (Test Set)
| Модель              | Порог | Precision | Recall | Cost (tg)  |
|---------------------|-------|-----------|--------|------------|
| Logistic Regression | ~0.35 | 0.68      | 0.85   | ~750 000   |
| RF + Optuna         | ~0.19 | 0.37      | 0.90   | ~1 566 000 |

**Бизнес-решение:** При текущих весах ошибок экономически эффективнее LogReg с порогом ~0.35. RF требует Step-Up верификации для оправдания высокого FP.


## Как запустить
```bash
pip install -r requirements.txt
jupyter lab notebooks/01_EDA.ipynb
