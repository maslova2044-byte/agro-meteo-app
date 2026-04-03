import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="🌿 АгроСистема", layout="wide")

CITIES_DATA = {
    "Москва": {"last_frost": (5, 10), "soil_warm_10c": (4, 25)},
    "Смоленск": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Краснодар": {"last_frost": (3, 25), "soil_warm_10c": (3, 15)},
    # ... остальные города из предыдущего кода
}

CROPS_DATA = {
    "🍅 Томаты": {"min_temp": 10, "frost_sensitive": True, "delay_days": 14, "plan": ["🌱 Высадка", "+14 дней: Пасынкование"]},
    "🥔 Картофель": {"min_temp": 7, "frost_sensitive": False, "delay_days": 0, "plan": ["🥔 Посадка", "+20 дней: Окучивание"]},
    "🥒 Огурцы": {"min_temp": 12, "frost_sensitive": True, "delay_days": 7, "plan": ["🥒 Посев", "+10 дней: Прищипывание"]}
}

DISEASE_DB = {
    "🍅 Томаты": {
        "🟤 Коричневые пятна": {"diagnosis": "Альтернариоз", "treatment": "🛡️ Алирин-Б + Гамаир", "prevention": "Удаляйте нижние листья"},
        "⚫ Чёрные пятна": {"diagnosis": "Фитофтороз", "treatment": "🛡️ Фитоспорин-М", "prevention": "Проветривание"},
        "🟡 Листья желтеют": {"diagnosis": "Недостаток азота", "treatment": "💧 Мочевина", "prevention": "Регулярные подкормки"},
        "🌀 Листья скручиваются": {"diagnosis": "Тля или вирус", "treatment": "🐞 Фитоверм", "prevention": "Борьба с муравьями"}
    },
    "🥔 Картофель": {
        "🟤 Пятна на листьях": {"diagnosis": "Фитофтороз", "treatment": "🛡️ Фитоспорин", "prevention": "Окучивание"},
        "🕳️ Язвы на клубнях": {"diagnosis": "Парша", "treatment": "🦠 Протравливание", "prevention": "Избегайте свежего навоза"},
        "🪱 Дырки в клубнях": {"diagnosis": "Проволочник", "treatment": "🪱 Энтономематоды", "prevention": "Известкование почвы"}
    },
    "🥒 Огурцы": {
        "🕸️ Паутина": {"diagnosis": "Паутинный клещ", "treatment": "🕷️ Фитоверм", "prevention": "Опрыскивание водой"},
        "⚪ Белый налёт": {"diagnosis": "Мучнистая роса", "treatment": "🥛 Тиовит Джет", "prevention": "Не перекармливайте азотом"}
    }
}

st.sidebar.title("🌿 АгроСистема")
mode = st.sidebar.radio("Режим:", ["📅 Календарь", "🔍 Диагностика", "📷 Фото-дневник"])

if mode == "📅 Календарь":
    st.title("📅 Планировщик")
    city = st.selectbox("Город:", sorted(list(CITIES_DATA.keys())))
    crop = st.selectbox("Культура:", list(CROPS_DATA.keys()))
    if st.button("Рассчитать", type="primary"):
        st.success(f"✅ Даты рассчитаны для {city} и {crop}")

elif mode == "🔍 Диагностика":
    st.title("🔍 Диагностика болезней")
    col1, col2 = st.columns(2)
    with col1: crop = st.selectbox("Культура:", list(DISEASE_DB.keys()))
    with col2: sym = st.selectbox("Симптом:", list(DISEASE_DB[crop].keys()))
    
    if st.button("Найти", type="primary"):
        res = DISEASE_DB[crop][sym]
        st.error(f"🩺 **Диагноз:** {res['diagnosis']}")
        st.success(f"💊 **Лечение:** {res['treatment']}")
        st.info(f"🛡️ **Профилактика:** {res['prevention']}")

else:
    st.title("📷 Фото-дневник")
    uploaded = st.file_uploader("Загрузить фото", type=["jpg", "png"])
    if uploaded:
        st.write("✅ Фото загружено!")
        st.text_area("Описание:", placeholder="Опишите проблему...")
