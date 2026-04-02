import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# 1. НАСТРОЙКА
st.set_page_config(page_title="🌱 АгроМетео PRO", layout="wide")

# 2. БАЗА ДАННЫХ (ГОРОДА)
CITIES_DATA = {
    "Москва": {"last_frost": (5, 10), "soil_warm_10c": (4, 20)},
    "Краснодар": {"last_frost": (3, 25), "soil_warm_10c": (3, 10)},
    "Волгоград": {"last_frost": (4, 10), "soil_warm_10c": (4, 1)},
    "Казань": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Ярославль": {"last_frost": (5, 22), "soil_warm_10c": (5, 12)},
    "Смоленск": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Рославль": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Ельня": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Новосибирск": {"last_frost": (6, 5), "soil_warm_10c": (5, 25)}
}

# 3. БАЗА ДАННЫХ (КУЛЬТУРЫ + ПЛАНЫ)
CROPS_DATA = {
    "Томаты": {
        "min_temp": 10, "frost_sensitive": True, "delay_days": 14, 
        "plan": [
            "🌱 Высадка рассады", 
            "+14 дней: Пасынкование (удаление лишних побегов)", 
            "+30 дней: Первая подкормка (азот)", 
            "+60 дней: Сбор первых плодов"
        ]
    },
    "Картофель": {
        "min_temp": 7, "frost_sensitive": False, "delay_days": 0, 
        "plan": [
            "🥔 Посадка клубней", 
            "+20 дней: Первое окучивание", 
            "+40 дней: Обработка от колорадского жука", 
            "+90 дней: Уборка урожая"
        ]
    },
    "Огурцы": {
        "min_temp": 12, "frost_sensitive": True, "delay_days": 7, 
        "plan": [
            "🥒 Посев/Высадка в грунт", 
            "+10 дней: Прищипывание (для кустистости)", 
            "+25 дней: Сбор первых зеленцов"
        ]
    },
    "Морковь": {
        "min_temp": 5, "frost_sensitive": False, "delay_days": 0, 
        "plan": [
            "🥕 Посев семян", 
            "+30 дней: Прореживание (оставить 3-5 см между растениями)", 
            "+90 дней: Уборка на хранение"
        ]
    },
    "Капуста (Белокочанная)": {
        "min_temp": 5, "frost_sensitive": False, "delay_days": 0, 
        "plan": [
            "🥬 Посадка рассады", 
            "+15 дней: Окучивание", 
            "+30 дней: Обработка от бабочки-капустницы", 
            "+70 дней: Срезка кочанов"
        ]
    },
    "Редис": {
        "min_temp": 2, "frost_sensitive": False, "delay_days": 0, 
        "plan": [
            "🔴 Посев в открытый грунт", 
            "+25 дней: Сбор урожая"
        ]
    },
    "Кабачки": {
        "min_temp": 12, "frost_sensitive": True, "delay_days": 10, 
        "plan": [
            "🥒 Посев семян или высадка", 
            "+10 дней: Рыхление почвы", 
            "+40 дней: Сбор первых плодов"
        ]
    }
}

# 4. ЛУННЫЙ КАЛЕНДАРЬ
def get_moon_advice(date_obj):
    new_moon_ref = datetime(2026, 2, 17)
    days_diff = (date_obj - new_moon_ref).days
    moon_age = days_diff % 29.53
    
    if moon_age < 2 or moon_age > 27.5: return "🌑 Новолуние. Лучше заняться прополкой."
    elif 13 < moon_age < 16: return "🌕 Полнолуние. Не тревожить растения."
    elif moon_age < 14: return "🌒 Растущая луна. Сажаем всё, что растет ВВЕРХ."
    else: return "🌘 Убывающая луна. Сажаем всё, что растет ВНИЗ (корни)."

# 5. ИНТЕРФЕЙС (Сайдбар)
with st.sidebar:
    st.title("🌱 АгроМетео PRO")
    st.caption("Планировщик для садовода")
    st.divider()
    
    selected_city = st.selectbox("📍 Ваш город:", list(CITIES_DATA.keys()))
    selected_crop = st.selectbox("🥕 Выберите культуру:", list(CROPS_DATA.keys()))
    
    st.divider()
    if st.button("♻️ Сбросить выбор"):
        st.rerun()

# 6. ОСНОВНОЙ ЭКРАН
st.header(f"📊 Прогноз: {selected_crop} в г. {selected_city}")
today = datetime.now()

# Кнопка запуска
if st.button("🚀 Рассчитать даты и план работ", type="primary"):
    year = today.year
    city_info = CITIES_DATA[selected_city]
    crop_info = CROPS_DATA[selected_crop]

    # Расчет базовых дат
    last_frost = datetime(year, city_info["last_frost"][0], city_info["last_frost"][1])
    soil_warm = datetime(year, city_info["soil_warm_10c"][0], city_info["soil_warm_10c"][1])
    
    # Логика выбора старта
    if crop_info["frost_sensitive"]:
        base_date = last_frost
        reason = "После заморозков"
    else:
        base_date = soil_warm
        reason = "Прогрев почвы"

    planting_date = base_date + timedelta(days=crop_info["delay_days"])

    # --- ВИЗУАЛИЗАЦИЯ ---
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Старт работ", planting_date.strftime("%d %b"))
    with col2:
        st.metric("🌡 Почва (мин)", f"+{crop_info['min_temp']}°C")
    with col3:
        st.metric("🌙 Луна сегодня", get_moon_advice(today).split()[0]) # Только эмодзи

    # --- ГЕНЕРАЦИЯ ПЛАНА ---
    st.divider()
    st.subheader("📋 Ваш личный календарь работ")
    
    plan_data = []
    for task in crop_info["plan"]:
        # Если строка содержит "+Число дней", значит это будущее событие
        if "+" in task:
            try:
                days_add = int(task.split(":")[0].replace("+", "").replace(" дней", "").strip())
                desc = task.split(":")[1].strip()
                task_date = planting_date + timedelta(days=days_add)
                
                # Статус: прошло или нет
                if task_date < today:
                    status = "✅ Выполнено"
                elif (task_date - today).days <= 3:
                    status = "🔥 СКОРО (через 1-3 дня)"
                else:
                    status = "⏳ Впереди"
                
                plan_data.append({"Дата": task_date.strftime("%d.%m.%Y"), "Задача": desc, "Статус": status})
            except:
                pass
        else:
            # Это дата посадки (первый пункт списка)
            status = "✅ Прошло" if planting_date < today else "🎯 ЦЕЛЬ"
            plan_data.append({"Дата": planting_date.strftime("%d.%m.%Y"), "Задача": task.replace("🌱", "").replace("🥔", "").replace("🥒", "").replace("🥕", "").replace("🥬", "").replace("🔴", ""), "Статус": status})

    # Вывод таблицы
    if plan_data:
        df_plan = pd.DataFrame(plan_data)
        st.dataframe(df_plan, use_container_width=True, hide_index=True)

        # Кнопка скачивания
        csv = df_plan.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label="💾 Скачать план в Excel (CSV)",
            data=csv,
            file_name=f"Plan_{selected_crop}_{selected_city}.csv",
            mime="text/csv",
        )
    else:
        st.warning("Нет данных для построения плана.")

    # --- ЛУННЫЙ СОВЕТ ---
    with st.expander("🌑 Подробнее про лунный календарь"):
        st.info(get_moon_advice(today))
        st.caption("Данные носят рекомендательный характер.")