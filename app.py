import streamlit as st
import pandas as pd
import joblib
import random

# 1. Загружаем готовый пайплайн
pipeline = joblib.load('pipeline.pkl')

st.title("Fraud Detection System")
st.markdown("Введите данные транзакции для проверки")

# 2. Простой UI с ключевыми признаками
col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Сумма транзакции (₸)", value=5000.0)
    device = st.selectbox("Устройство", ["Mobile", "Tablet", "Laptop"])
    location = st.selectbox("Локация", ["New York", "Tokyo", "London", "Sydney", "Mumbai"])
with col2:
    merchant = st.selectbox("Категория", ["Travel", "Clothing", "Groceries", "Electronics", "Restaurants"])
    auth = st.selectbox("Авторизация", ["Password", "PIN", "OTP", "Biometric"])
    card = st.selectbox("Карта", ["Visa", "Mastercard", "Amex", "Discover"])

# 3. Формируем DataFrame
# ВАЖНО: Мы добавляем отсутствующие колонки (Transaction_ID, User_ID и др.) с фиктивными значениями,
# чтобы удовлетворить строгие требования загруженной модели.
if st.button("Проверить транзакцию"):
    
    data = pd.DataFrame({
        # --- Поля из интерфейса ---
        'Transaction_Amount': [amount],
        'Device_Type': [device],
        'Location': [location],
        'Merchant_Category': [merchant],
        'Authentication_Method': [auth],
        'Card_Type': [card],
        
        # --- ОТСУТСТВУЮЩИЕ ПОЛЯ (DUMMY VALUES) ---
        # Добавляем их, чтобы закрыть ошибку ValueError
        'Transaction_ID': ['TXN_' + str(random.randint(1000, 9999))],
        'User_ID': ['USER_' + str(random.randint(1000, 9999))],
        'Transaction_Type': ['Online'],      # Просто выбираем один тип
        'Account_Balance': [5000.0],         # Фиктивная сумма на счету
        'Transaction_Distance': [10.0],      # Фиктивное расстояние
        
        # --- ОСТАЛЬНЫЕ НЕОБХОДИМЫЕ ПРИЗНАКИ ---
        # Убеждаемся, что все числовые/категориальные фичи из обучения присутствуют
        'Daily_Transaction_Count': [5],
        'Avg_Transaction_Amount_7d': [1200.0],
        'Failed_Transaction_Count_7d': [0],
        'Is_Weekend': [0],
        'IP_Address_Flag': [0],
        'Previous_Fraudulent_Activity': [0],
        'Card_Age': [180],
        'Risk_Score': [0.5] 
    })

    # 4. Предсказание
    try:
        # predict_proba возвращает [P(0), P(1)]
        probs = pipeline.predict_proba(data)
        fraud_prob = probs[0][1]
        
        st.metric("Вероятность мошенничества", f"{fraud_prob:.2%}")
        
        if fraud_prob >= 0.35:  # твой выбранный порог
            st.error("Блокировка рекомендована. Высокий риск.")
        else:
            st.success("Транзакция безопасна.")
            
    except Exception as e:
        st.error(f"Произошла ошибка при предсказании: {e}")
        st.caption("Убедитесь, что модель и данные соответствуют друг другу.")