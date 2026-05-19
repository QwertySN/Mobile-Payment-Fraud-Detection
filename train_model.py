import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

# 1. Загружаем данные
df = pd.read_csv('synthetic_fraud_dataset.csv')

# 2. Подготовка данных
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
# Удаление лишнего
drop_cols = ['TXN_0', 'USER_0'] # Пример ID
# Если есть Risk_Score, его тоже удаляем, если он есть в датафрейме
if 'Risk_Score' in df.columns:
    drop_cols.append('Risk_Score')

df_clean = df.drop(columns=drop_cols, errors='ignore')
X = df_clean.drop(columns=['Fraud_Label'])
y = df_clean['Fraud_Label']

# 3. Определяем типы
num_cols = X.select_dtypes(include='number').columns
cat_cols = X.select_dtypes(include='object').columns

# 4. Создаем Пайплайн (Логистическая регрессия)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), cat_cols)
    ],
    remainder='drop'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
])

# 5. Обучаем и сохраняем
print("⏳ Обучаю модель локально...")
model.fit(X, y)

joblib.dump(model, 'pipeline.pkl')
print("Готово! Файл pipeline.pkl сохранен и совместим с твоим ПК.")