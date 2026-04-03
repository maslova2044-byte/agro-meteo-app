import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="🌿 АгроСистема", layout="wide")

# --- БАЗЫ ДАННЫХ ---
CITIES_DATA = {
    "Москва": {"last_frost": (5, 10), "soil_warm_10c": (4, 20)},
    "Смоленск": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Рославль": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Ельня": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Краснодар": {"last_frost": (3, 25), "soil_warm_10c": (3, 10)}
}

CROPS_DATA = {
    "🍅 Томаты": {
        "min_temp": 10, "frost_sensitive": True, "delay_days": 14, 
        "plan": ["🌱 Высадка", "+14 дней: Пасынкование", "+30 дней: Подкормка"]
    },
    "🥒 Огурцы": {
        "min_temp": 12, "frost_sensitive": True, "delay_days": 7, 
        "plan": ["🥒 Посев", "+10 дней: Прищипывание", "+25 дней: Сбор"]
    },
    "🥔 Картофель": {
        "min_temp": 7, "frost_sensitive": False, "delay_days": 0, 
        "plan": ["🥔 Посадка", "+20 дней: Окучивание", "+90 дней: Уборка"]
    }
}

# БАЗА ДИАГНОСТИКИ (вместо AI)
DISEASE_DB = {
    "🍅 Томаты": {
        "🟤 Коричневые пятна на листьях": {
            "diagnosis": "Альтернариоз (Сухая пятнистость)",
            "treatment": "🛡️ Препараты: Гамаир, Алирин-Б",
            "prevention": "Удалите больные листья. Не переувлажняйте."
        },
        "⚫ Черные пятна на стебле": {
            "diagnosis": "Фитофтороз",
            "treatment": "🛡️ Фитоспорин, Триходермин",
            "prevention": "Снизьте влажность. Проветривайте теплицу."
        },
        "🟡 Листья желтеют и скручиваются": {
            "diagnosis": "Недостаток азота или тля",
            "treatment": "💧 Подкормка азотом или Фитоверм от тли",
            "prevention": "Регулярно удобряйте."
        }
    },
    "🥒 Огурцы": {
        "🕸️ Паутина на листьях": {
            "diagnosis": "Паутинный клещ",
            "treatment": "🕷️ Фитоверм или хищный клещ",
            "prevention": "Повысьте влажность воздуха."
        },
        "⚪ Белый налет на листьях": {
            "diagnosis": "Мучнистая роса",
            "treatment": "🥛 Тиовит Джет или раствор сыворотки 1:10",
            "prevention": "Не перекармливайте азотом."
        }
    },
    "🥔 Картофель": {
        "🐛 Жуки на листьях": {
            "diagnosis": "Колорадский жук",
            "treatment": "🦠 Боверин, Бикол",
            "prevention": "Собирайте вручную или опрыскивайте био-препаратами."
        }
    }
}

# --- ИНТЕРФЕЙС ---
mode = st.sidebar.radio(
    "🌿 Выберите режим:",
    ["📅 Календарь посадок", "🔍 Диагностика болезней"],
    index=0
)

# РЕЖИМ 1: КАЛЕНДАРЬ
if mode == "📅 Календарь посадок":
    st.title("📅 АгроМетео: Планировщик")
    
    with st.sidebar:
        city = st.selectbox("Город:", list(CITIES_DATA.keys()))
        crop = st.selectbox("Культура:", list(CROPS_DATA.keys()))
    
    if st.button("🚀 Рассчитать", type="primary"):
        today = datetime.now()
        crop_info = CROPS_DATA[crop]
        city_info = CITIES_DATA[city]
        
        base_date = datetime(today.year, city_info["last_frost"][0], city_info["last_frost"][1])
        if not crop_info["frost_sensitive"]:
            base_date = datetime(today.year, city_info["soil_warm_10c"][0], city_info["soil_warm_10c"][1])
        
        planting = base_date + timedelta(days=crop_info["delay_days"])
        st.success(f"📅 Начать посадки: **{planting.strftime('%d %B')}**")
        
        st.write("📋 План работ:")
        for task in crop_info["plan"]:
            st.write(f"- {task}")

# РЕЖИМ 2: ДИАГНОСТИКА
else:
    st.title("🔍 Диагностика болезней растений")
    st.write("Выберите культуру и опишите симптомы:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox("1. Культура:", list(DISEASE_DB.keys()))
    
    with col2:
        symptoms = st.selectbox("2. Симптомы:", list(DISEASE_DB[crop].keys()))
    
    if st.button("🔍 Найти диагноз", type="primary"):
        disease = DISEASE_DB[crop][symptoms]
        
        st.error(f"🩺 **Диагноз:** {disease['diagnosis']}")
        st.success(f"💊 **Лечение:** {disease['treatment']}")
        st.info(f"🛡️ **Профилактика:** {disease['prevention']}")
    
    st.divider()
    st.caption("💡 Совет: Если не нашли свой симптом — выберите ближайший по описанию.")
