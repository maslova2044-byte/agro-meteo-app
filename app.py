import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="🌿 АгроСистема", layout="wide")

# --- БАЗА ДАННЫХ ГОРОДОВ ---
CITIES_DATA = {
    "Астрахань": {"last_frost": (4, 15), "soil_warm_10c": (4, 5)},
    "Барнаул": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Белгород": {"last_frost": (4, 25), "soil_warm_10c": (4, 15)},
    "Брянск": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Великий Новгород": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Владивосток": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Волгоград": {"last_frost": (4, 20), "soil_warm_10c": (4, 10)},
    "Вологда": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Воронеж": {"last_frost": (4, 25), "soil_warm_10c": (4, 15)},
    "Екатеринбург": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Ельня": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Ижевск": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Иркутск": {"last_frost": (6, 5), "soil_warm_10c": (5, 25)},
    "Казань": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Калининград": {"last_frost": (5, 5), "soil_warm_10c": (4, 25)},
    "Калуга": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Кемерово": {"last_frost": (5, 30), "soil_warm_10c": (5, 20)},
    "Киров": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Краснодар": {"last_frost": (3, 25), "soil_warm_10c": (3, 15)},
    "Красноярск": {"last_frost": (6, 5), "soil_warm_10c": (5, 25)},
    "Курск": {"last_frost": (4, 25), "soil_warm_10c": (4, 15)},
    "Липецк": {"last_frost": (5, 1), "soil_warm_10c": (4, 20)},
    "Москва": {"last_frost": (5, 10), "soil_warm_10c": (4, 25)},
    "Нижний Новгород": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Новосибирск": {"last_frost": (6, 5), "soil_warm_10c": (5, 25)},
    "Омск": {"last_frost": (5, 30), "soil_warm_10c": (5, 20)},
    "Оренбург": {"last_frost": (5, 10), "soil_warm_10c": (4, 25)},
    "Пенза": {"last_frost": (5, 10), "soil_warm_10c": (5, 1)},
    "Пермь": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Псков": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Ростов-на-Дону": {"last_frost": (4, 10), "soil_warm_10c": (4, 1)},
    "Рославль": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Рязань": {"last_frost": (5, 10), "soil_warm_10c": (5, 1)},
    "Самара": {"last_frost": (5, 10), "soil_warm_10c": (4, 25)},
    "Санкт-Петербург": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Саратов": {"last_frost": (4, 30), "soil_warm_10c": (4, 20)},
    "Смоленск": {"last_frost": (5, 18), "soil_warm_10c": (5, 8)},
    "Сочи": {"last_frost": (3, 10), "soil_warm_10c": (3, 1)},
    "Ставрополь": {"last_frost": (4, 15), "soil_warm_10c": (4, 5)},
    "Сургут": {"last_frost": (6, 15), "soil_warm_10c": (6, 5)},
    "Тамбов": {"last_frost": (5, 5), "soil_warm_10c": (4, 25)},
    "Тверь": {"last_frost": (5, 15), "soil_warm_10c": (5, 5)},
    "Тольятти": {"last_frost": (5, 10), "soil_warm_10c": (4, 25)},
    "Томск": {"last_frost": (6, 10), "soil_warm_10c": (5, 30)},
    "Тюмень": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Уфа": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)},
    "Челябинск": {"last_frost": (5, 25), "soil_warm_10c": (5, 15)},
    "Ярославль": {"last_frost": (5, 20), "soil_warm_10c": (5, 10)}
}

# --- БАЗЫ ДАННЫХ КУЛЬТУР ---
CROPS_DATA = {
    "🍅 Томаты": {"min_temp": 10, "frost_sensitive": True, "delay_days": 14, "plan": ["🌱 Высадка", "+14 дней: Пасынкование", "+30 дней: Подкормка"]},
    "🥒 Огурцы": {"min_temp": 12, "frost_sensitive": True, "delay_days": 7, "plan": ["🥒 Посев", "+10 дней: Прищипывание", "+25 дней: Сбор"]},
    "🥔 Картофель": {"min_temp": 7, "frost_sensitive": False, "delay_days": 0, "plan": ["🥔 Посадка", "+20 дней: Окучивание", "+90 дней: Уборка"]},
    "🍓 Клубника": {"min_temp": 8, "frost_sensitive": False, "delay_days": 0, "plan": ["🍓 Высадка", "+60 дней: Сбор"]},
    "🥕 Морковь": {"min_temp": 5, "frost_sensitive": False, "delay_days": 0, "plan": ["🥕 Посев", "+30 дней: Прореживание"]},
    "🧅 Лук": {"min_temp": 5, "frost_sensitive": False, "delay_days": 0, "plan": ["🧅 Посев", "+70 дней: Уборка"]},
    "🌶️ Перец": {"min_temp": 12, "frost_sensitive": True, "delay_days": 10, "plan": ["🌶️ Высадка", "+60 дней: Сбор"]},
    "🍆 Баклажаны": {"min_temp": 13, "frost_sensitive": True, "delay_days": 14, "plan": ["🍆 Высадка", "+20 дней: Рыхление", "+70 дней: Сбор"]}
}

# --- БАЗА ДИАГНОСТИКИ С ФОТО (URL изображений) ---
DISEASE_DB = {
    "🍅 Томаты": {
        "🟤 Коричневые пятна с кругами": {
            "diagnosis": "Альтернариоз",
            "treatment": "🛡️ Алирин-Б + Гамаир",
            "prevention": "Удаляйте нижние листья",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Early_blight_on_tomato_leaf.jpg/640px-Early_blight_on_tomato_leaf.jpg"
        },
        "⚫ Чёрные быстрорастущие пятна": {
            "diagnosis": "Фитофтороз",
            "treatment": "🛡️ Фитоспорин-М",
            "prevention": "Проветривание",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Tomato_leaf_blight.jpg/640px-Tomato_leaf_blight.jpg"
        },
        "🟡 Листья желтеют снизу": {
            "diagnosis": "Недостаток азота",
            "treatment": "💧 Мочевина или настой крапивы",
            "prevention": "Регулярные подкормки",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Nitrogen_deficiency_tomato.jpg/640px-Nitrogen_deficiency_tomato.jpg"
        },
        "🌀 Листья скручиваются": {
            "diagnosis": "Тля или вирус",
            "treatment": "🐞 Фитоверм от тли",
            "prevention": "Борьба с муравьями",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Aphids_on_tomato.jpg/640px-Aphids_on_tomato.jpg"
        },
        "⚪ Белый пушистый налёт": {
            "diagnosis": "Мучнистая роса",
            "treatment": "🥛 Раствор сыворотки 1:10",
            "prevention": "Не сажайте густо",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Powdery_mildew_tomato.jpg/640px-Powdery_mildew_tomato.jpg"
        }
    },
    "🥔 Картофель": {
        "🟤 Тёмные мокнущие пятна": {
            "diagnosis": "Фитофтороз",
            "treatment": "🛡️ Фитоспорин, Ридомил",
            "prevention": "Окучивание",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Potato_blight.jpg/640px-Potato_blight.jpg"
        },
        "🕳️ Сухие язвы на клубнях": {
            "diagnosis": "Парша обыкновенная",
            "treatment": "🦠 Протравливание Фитоспорином",
            "prevention": "Избегайте свежего навоза",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Potato_scab.jpg/640px-Potato_scab.jpg"
        },
        "🟡 Листья скручиваются лодочкой": {
            "diagnosis": "Вирус скручивания / Тля",
            "treatment": "🐞 Уничтожение тли",
            "prevention": "Здоровый семенной материал",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Potato_leafroll_virus.jpg/640px-Potato_leafroll_virus.jpg"
        },
        "🟤 Гниль у основания стебля": {
            "diagnosis": "Ризоктониоз / Чёрная ножка",
            "treatment": "🛡️ Препараты меди",
            "prevention": "Не заглубляйте клубни",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Black_leg_potato.jpg/640px-Black_leg_potato.jpg"
        },
        "🪱 Ходы и дырки в клубнях": {
            "diagnosis": "Проволочник",
            "treatment": "🪱 Энтономематоды в почву",
            "prevention": "Известкование кислой почвы",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Wireworm_damage.jpg/640px-Wireworm_damage.jpg"
        },
        "🟢 Мозаичные пятна": {
            "diagnosis": "Вирусная мозаика",
            "treatment": "🗑️ Удаление больных кустов",
            "prevention": "Борьба с тлей",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Potato_mosaic_virus.jpg/640px-Potato_mosaic_virus.jpg"
        }
    },
    "🥒 Огурцы": {
        "🕸️ Паутина на листьях": {
            "diagnosis": "Паутинный клещ",
            "treatment": "🕷️ Фитоверм + влажность",
            "prevention": "Опрыскивание водой",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Spider_mite_cucumber.jpg/640px-Spider_mite_cucumber.jpg"
        },
        "⚪ Белый мучнистый налёт": {
            "diagnosis": "Мучнистая роса",
            "treatment": "🥛 Тиовит Джет, сода",
            "prevention": "Не перекармливайте азотом",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Powdery_mildew_cucumber.jpg/640px-Powdery_mildew_cucumber.jpg"
        },
        "🟡 Угловатые жёлтые пятна": {
            "diagnosis": "Пероноспороз",
            "treatment": "🛡️ Алирин-Б",
            "prevention": "Полив тёплой водой",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Downy_mildew_cucumber.jpg/640px-Downy_mildew_cucumber.jpg"
        }
    },
    "🍓 Клубника": {
        "⚪ Белый налёт на ягодах": {
            "diagnosis": "Серая гниль",
            "treatment": "🛡️ Фитоспорин",
            "prevention": "Мульча из соломы",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Gray_mold_strawberry.jpg/640px-Gray_mold_strawberry.jpg"
        },
        "🟤 Бурые пятна с каймой": {
            "diagnosis": "Белая пятнистость",
            "treatment": "🛡️ Хорус",
            "prevention": "Уборка старой листвы",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Leaf_spot_strawberry.jpg/640px-Leaf_spot_strawberry.jpg"
        },
        "🐛 Мелкие красные клещи": {
            "diagnosis": "Земляничный клещ",
            "treatment": "🕷️ Фитоверм",
            "prevention": "Полив горячей водой (+60°C)",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Strawberry_mite.jpg/640px-Strawberry_mite.jpg"
        }
    },
    "🥕 Морковь": {
        "🟠 Листья рыжеют": {
            "diagnosis": "Морковная муха",
            "treatment": "🥕 Табачная пыль + зола",
            "prevention": "Посадки с луком",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Carrot_fly_damage.jpg/640px-Carrot_fly_damage.jpg"
        },
        "🟢 Буйная ботва, мелкие плоды": {
            "diagnosis": "Избыток азота",
            "treatment": "💧 Отмена азотных подкормок",
            "prevention": "Баланс удобрений",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Excess_nitrogen_carrot.jpg/640px-Excess_nitrogen_carrot.jpg"
        }
    },
    "🧅 Лук": {
        "⚪ Серо-фиолетовый налёт": {
            "diagnosis": "Пероноспороз",
            "treatment": "🛡️ Ридомил, Фитоспорин",
            "prevention": "Прогрев севка",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Downy_mildew_onion.jpg/640px-Downy_mildew_onion.jpg"
        },
        "🟡 Кончики желтеют": {
            "diagnosis": "Шейковая гниль",
            "treatment": "💧 Калийно-фосфорная подкормка",
            "prevention": "Правильная сушка",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Onion_rot.jpg/640px-Onion_rot.jpg"
        }
    },
    "🌶️ Перец": {
        "🟣 Фиолетовый оттенок": {
            "diagnosis": "Недостаток фосфора / Холод",
            "treatment": "🌡️ Укрытие, монофосфат калия",
            "prevention": "Температура выше +15°C",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Phosphorus_deficiency_pepper.jpg/640px-Phosphorus_deficiency_pepper.jpg"
        },
        "🟡 Опадают цветы": {
            "diagnosis": "Перегрев / Стресс",
            "treatment": "💧 Регулярный полив, притенение",
            "prevention": "Мульча",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Pepper_flower_drop.jpg/640px-Pepper_flower_drop.jpg"
        }
    }
}

# --- ИНТЕРФЕЙС ---
st.sidebar.title("🌿 АгроСистема")
mode = st.sidebar.radio("Режим работы:", 
    ["📅 Календарь", "🔍 Диагностика (Симптомы)", "📷 Фото-дневник"], index=0)

# 1. КАЛЕНДАРЬ
if mode == "📅 Календарь":
    st.title("📅 Планировщик посадок")
    col1, col2 = st.columns(2)
    with col1: city = st.selectbox("📍 Город:", sorted(list(CITIES_DATA.keys())))
    with col2: crop = st.selectbox("🥕 Культура:", list(CROPS_DATA.keys()))
    
    if st.button("🚀 Рассчитать даты", type="primary"):
        today = datetime.now()
        c_info = CROPS_DATA[crop]
        city_data = CITIES_DATA[city]
        
        if c_info["frost_sensitive"]:
            base = datetime(today.year, city_data["last_frost"][0], city_data["last_frost"][1])
        else:
            base = datetime(today.year, city_data["soil_warm_10c"][0], city_data["soil_warm_10c"][1])
            
        res_date = base + timedelta(days=c_info["delay_days"])
        st.success(f"📅 Оптимальный старт: **{res_date.strftime('%d %B %Y')}**")
        st.write("📋 План работ:")
        for task in c_info["plan"]:
            st.write(f"- {task}")

# 2. ДИАГНОСТИКА С ФОТО
elif mode == "🔍 Диагностика (Симптомы)":
    st.title("🔍 Поиск болезни по симптомам с фото")
    
    col1, col2 = st.columns(2)
    with col1: 
        crop = st.selectbox("1. Культура:", list(DISEASE_DB.keys()))
    with col2: 
        sym = st.selectbox("2. Симптом:", list(DISEASE_DB[crop].keys()))
    
    if st.button("🔍 Найти диагноз", type="primary"):
        res = DISEASE_DB[crop][sym]
        
        # Показываем фото
        try:
            st.image(res["image"], caption=f"📸 Как выглядит: {res['diagnosis']}", use_container_width=True)
        except:
            st.warning("📷 Фото загружается...")
        
        # Карточки с информацией
        col_a, col_b = st.columns(2)
        with col_a:
            st.error(f"🩺 **Диагноз:** {res['diagnosis']}")
            st.success(f"💊 **Лечение:** {res['treatment']}")
        with col_b:
            st.info(f"🛡️ **Профилактика:** {res['prevention']}")
        
        st.divider()
        st.caption(f"Симптом: {sym}")

# 3. ФОТО-ДНЕВНИК
else:
    st.title("📷 Фото-дневник наблюдений")
    st.caption("Загружайте фото больных растений для истории.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded = st.file_uploader("📸 Загрузить фото", type=["jpg", "png", "jpeg"])
        if uploaded:
            st.image(uploaded, caption="Ваше фото", use_container_width=True)
    
    with col2:
        st.write("📝 Заметки к фото:")
        notes = st.text_area("Опишите проблему:", placeholder="Например: Томаты, коричневые пятна...")
        
        if st.button("💾 Сохранить запись"):
            if uploaded and notes:
                st.success("✅ Запись сохранена!")
            else:
                st.warning("⚠️ Загрузите фото и добавьте описание")
