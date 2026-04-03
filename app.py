import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import os

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="🌿 АгроСистема: Календарь + AI", layout="wide")

# --- 1. БАЗЫ ДАННЫХ (КАЛЕНДАРЬ) ---
CITIES_DATA = {
    "Москва": {"last_frost": (5, 10), "soil_warm_10c": (4, 20)},
    "Смоленск": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Рославль": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Ельня": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Краснодар": {"last_frost": (3, 25), "soil_warm_10c": (3, 10)},
    "Казань": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Ярославль": {"last_frost": (5, 22), "soil_warm_10c": (5, 12)}
}

CROPS_DATA = {
    "🍅 Томаты": {
        "min_temp": 10, "frost_sensitive": True, "delay_days": 14, 
        "plan": ["🌱 Высадка рассады", "+14 дней: Пасынкование", "+30 дней: Подкормка", "+60 дней: Сбор урожая"]
    },
    "🥔 Картофель": {
        "min_temp": 7, "frost_sensitive": False, "delay_days": 0, 
        "plan": ["🥔 Посадка клубней", "+20 дней: Окучивание", "+40 дней: Обработка", "+90 дней: Уборка"]
    },
    "🥒 Огурцы": {
        "min_temp": 12, "frost_sensitive": True, "delay_days": 7, 
        "plan": ["🥒 Посев", "+10 дней: Прищипывание", "+25 дней: Сбор"]
    },
    "🥕 Морковь": {
        "min_temp": 5, "frost_sensitive": False, "delay_days": 0, 
        "plan": ["🥕 Посев", "+30 дней: Прореживание", "+90 дней: Уборка"]
    },
    "🥬 Капуста": {
        "min_temp": 5, "frost_sensitive": False, "delay_days": 0, 
        "plan": ["🥬 Посадка", "+15 дней: Окучивание", "+70 дней: Срезка"]
    }
}

# --- 2. БАЗА ЗНАНИЙ ДЛЯ AI (СОВЕТЫ ПО ЛЕЧЕНИЮ) ---
TREATMENT_DB = {
    "Early_blight": {"name": "Альтернариоз (Пятнистость)", "solution": "🛡️ Препараты: Гамаир, Алирин-Б. Удалите больные листья."},
    "Late_blight": {"name": "Фитофтороз", "solution": "🛡️ Препараты: Фитоспорин, Триходермин. Снизьте влажность."},
    "Healthy": {"name": "Здоровое растение ", "solution": "✅ Растение здорово! Продолжайте уход."},
    "Tomato_mosaic_virus": {"name": "Вирус табачной мозаики", "solution": "🗑️ Лечению не подлежит. Удалите куст."},
    "Spider_mites": {"name": "Паутинный клещ", "solution": "🕷️ Препарат Фитоверм или хищный клещ."},
    "Powdery_mildew": {"name": "Мучнистая роса", "solution": "🥛 Тиовит Джет или раствор сыворотки (1:10)."}
}

# --- 3. ФУНКЦИИ ---

def get_moon_advice(date_obj):
    # Упрощенный расчет фаз луны
    new_moon_ref = datetime(2026, 2, 17)
    days_diff = (date_obj - new_moon_ref).days
    moon_age = days_diff % 29.53
    if moon_age < 2 or moon_age > 27.5: return "🌑 Новолуние (Отдых)"
    elif 13 < moon_age < 16: return "🌕 Полнолуние (Прополка)"
    elif moon_age < 14: return "🌒 Растущая луна (Надземные)"
    else: return "🌘 Убывающая луна (Корни)"

def query_ai(image_data):
    # Запрос к нейросети Hugging Face
    HF_TOKEN = os.environ.get("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/srihari-humbarwadi/plant-disease-recognition"
    
    if not HF_TOKEN:
        return {"error": "Не настроен ключ API"}

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        response = requests.post(API_URL, headers=headers, data=image_data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- 4. ИНТЕРФЕЙС (МЕНЮ ВЫБОРА) ---

mode = st.sidebar.radio(
    "🌿 Выберите режим работы:",
    ["📅 АгроМетео: Календарь", "📷 АгроБио: AI Диагностика"],
    index=0
)

# ==========================================
# РЕЖИМ 1: КАЛЕНДАРЬ
# ==========================================
if mode == "📅 АгроМетео: Календарь":
    st.title("📅 АгроМетео: Планировщик посадок")
    
    with st.sidebar:
        st.subheader("Настройки")
        selected_city = st.selectbox("📍 Город:", list(CITIES_DATA.keys()))
        selected_crop = st.selectbox("🥕 Культура:", list(CROPS_DATA.keys()))

    today = datetime.now()
    year = today.year
    
    if st.button("🚀 Рассчитать план работ", type="primary"):
        city_info = CITIES_DATA[selected_city]
        crop_info = CROPS_DATA[selected_crop]

        last_frost = datetime(year, city_info["last_frost"][0], city_info["last_frost"][1])
        soil_warm = datetime(year, city_info["soil_warm_10c"][0], city_info["soil_warm_10c"][1])
        
        base_date = last_frost if crop_info["frost_sensitive"] else soil_warm
        planting_date = base_date + timedelta(days=crop_info["delay_days"])

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("📅 Старт", planting_date.strftime("%d %b"))
        with col2: st.metric("🌡 Почва", f"+{crop_info['min_temp']}°C")
        with col3: st.metric("🌙 Луна", get_moon_advice(today).split()[0])

        st.divider()
        st.subheader("📋 Календарь работ")
        
        plan_data = []
        for task in crop_info["plan"]:
            if "+" in task:
                days_add = int(task.split(":")[0].replace("+", "").replace(" дней", "").strip())
                desc = task.split(":")[1].strip()
                task_date = planting_date + timedelta(days=days_add)
                status = "✅ Выполнено" if task_date < today else "⏳ Впереди"
                plan_data.append({"Дата": task_date.strftime("%d.%m"), "Задача": desc, "Статус": status})
            else:
                plan_data.append({"Дата": planting_date.strftime("%d.%m"), "Задача": task.replace("🌱","").replace("🥔","").replace("🥒","").replace("🥕","").replace("🥬",""), "Статус": "🎯 СТАРТ"})

        df_plan = pd.DataFrame(plan_data)
        st.dataframe(df_plan, use_container_width=True, hide_index=True)

# ==========================================
# РЕЖИМ 2: AI ДИАГНОСТИКА
# ==========================================
else:
    st.title("📷 АгроБио: Диагностика болезней")
    st.caption("Загрузите фото листа, нейросеть определит болезнь и подскажет лечение.")

    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader("Загрузить фото 📸", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Ваше фото")

    with col2:
        if uploaded_file is not None:
            if st.button("🔍 Определить болезнь", type="primary"):
                with st.spinner("🧠 Нейросеть думает... (подождите 10-20 сек)"):
                    result = query_ai(uploaded_file.getvalue())
                    
                    if "error" in result:
                        st.error(f"❌ Ошибка: {result['error']}")
                        st.warning("Проверьте, настроен ли HF_TOKEN в Render.")
                    elif isinstance(result, list):
                        prediction = result[0]
                        raw_label = prediction["label"]
                        confidence = int(prediction["score"] * 100)
                        
                        # Извлекаем код болезни
                        disease_code = raw_label.split("___")[-1] if "___" in raw_label else raw_label
                        
                        # Ищем в базе советов
                        info = TREATMENT_DB.get(disease_code, {"name": f"Неизвестное ({disease_code})", "solution": "Попробуйте обработать универсальным Фитоспорином."})

                        st.success(f"🩺 **Диагноз:** {info['name']}")
                        st.info(f"💊 **Чем лечить:** {info['solution']}")
                        st.progress(confidence / 100, text=f"Уверенность ИИ: {confidence}%")
                    else:
                        st.error("Не удалось получить ответ от сервера.")
        else:
            st.info("👈 Загрузите фото в меню слева")

    st.divider()
    st.subheader("📖 Справочник препаратов")
    st.write("Всегда читайте инструкцию к препарату перед применением!")
