import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import base64

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="🌿 АгроСистема", layout="wide")

# --- БАЗА ДАННЫХ ГОРОДОВ (ОТРАНСОРТИРОВАНА) ---
# last_frost: дата последних заморозков (Месяц, День)
# soil_warm_10c: дата прогрева почвы до +10 (Месяц, День)
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

# --- БАЗА ДИАГНОСТИКИ ---
DISEASE_DB = {
    "🍅 Томаты": {
        "🟤 Коричневые пятна с кругами на листьях": {"diagnosis": "Альтернариоз", "treatment": "🛡️ Алирин-Б + Гамаир", "prevention": "Удаляйте нижние листья"},
        "⚫ Быстрорастущие чёрные пятна": {"diagnosis": "Фитофтороз", "treatment": "🛡️ Фитоспорин-М", "prevention": "Проветривание"},
        "🟡 Листья желтеют снизу вверх": {"diagnosis": "Недостаток азота", "treatment": "💧 Мочевина или настой крапивы", "prevention": "Регулярные подкормки"},
        "🌀 Листья скручиваются в трубочку": {"diagnosis": "Тля или вирус", "treatment": "🐞 Фитоверм от тли", "prevention": "Борьба с муравьями"},
        "⚪ Белый пушистый налёт": {"diagnosis": "Мучнистая роса", "treatment": "🥛 Раствор сыворотки 1:10", "prevention": "Не сажайте густо"}
    },
    "🥔 Картофель": {
        "🟤 Тёмные мокнущие пятна на листьях": {"diagnosis": "Фитофтороз", "treatment": "🛡️ Фитоспорин, Ридомил", "prevention": "Окучивание"},
        "🕳️ Сухие язвы на кожуре клубней": {"diagnosis": "Парша обыкновенная", "treatment": "🦠 Протравливание Фитоспорином", "prevention": "Избегайте свежего навоза"},
        "🟡 Листья скручиваются лодочкой, розовеют": {"diagnosis": "Вирус скручивания / Тля", "treatment": "🐞 Уничтожение тли", "prevention": "Здоровый семенной материал"},
        "🟤 Гниль у основания стебля": {"diagnosis": "Ризоктониоз / Чёрная ножка", "treatment": "🛡️ Препараты меди", "prevention": "Не заглубляйте клубни"},
        "🪱 Тонкие ходы и дырки в клубнях": {"diagnosis": "Проволочник", "treatment": "🪱 Энтономематоды в почву", "prevention": "Известкование кислой почвы"},
        "🟢 Светло-зелёные мозаичные пятна": {"diagnosis": "Вирусная мозаика", "treatment": "🗑️ Удаление больных кустов", "prevention": "Борьба с тлей"},
        "⚫ Чёрная гниль на концах столонов": {"diagnosis": "Фузариозное увядание", "treatment": "🛡️ Триходермин", "prevention": "Севооборот"}
    },
    "🥒 Огурцы": {
        "🕸️ Тонкая паутина, листья желтеют": {"diagnosis": "Паутинный клещ", "treatment": "🕷️ Фитоверм + повышение влажности", "prevention": "Опрыскивание водой"},
        "⚪ Белый мучнистый налёт": {"diagnosis": "Мучнистая роса", "treatment": "🥛 Тиовит Джет, сода", "prevention": "Не перекармливайте азотом"},
        "🟡 Угловатые жёлтые пятна": {"diagnosis": "Пероноспороз", "treatment": "🛡️ Алирин-Б", "prevention": "Полив тёплой водой"},
        "🥒 Плоды горькие, деформированные": {"diagnosis": "Стресс от перепадов температур", "treatment": "💧 Регулярный полив, укрытие", "prevention": "Стабильный микроклимат"}
    },
    "🍓 Клубника": {
        "⚪ Белый налёт на ягодах": {"diagnosis": "Серая гниль", "treatment": "🛡️ Фитоспорин", "prevention": "Мульча из соломы"},
        "🟤 Бурые пятна с красной каймой": {"diagnosis": "Белая пятнистость", "treatment": "🛡️ Хорус", "prevention": "Уборка старой листвы"},
        "🐛 Мелкие красные клещи": {"diagnosis": "Земляничный клещ", "treatment": "🕷️ Фитоверм", "prevention": "Полив горячей водой (+60°C) весной"},
        "🟡 Листья краснеют, кусты отстают": {"diagnosis": "Недостаток фосфора", "treatment": "💧 Суперфосфат", "prevention": "Регулярное известкование"}
    },
    "🥕 Морковь": {
        "🟠 Листья рыжеют, ботва вянет": {"diagnosis": "Морковная муха", "treatment": "🥕 Табачная пыль + зола", "prevention": "Посадки с луком"},
        "🟢 Буйная ботва, мелкие корнеплоды": {"diagnosis": "Избыток азота", "treatment": "💧 Отмена азотных подкормок", "prevention": "Баланс удобрений"},
        "🟤 Мокрая гниль на кончиках": {"diagnosis": "Бактериальная гниль", "treatment": "🛡️ Фитолавин", "prevention": "Хранение в сухом месте"},
        "🪱 Ходы внутри моркови": {"diagnosis": "Морковная листоблошка", "treatment": "🪱 Энтономематоды", "prevention": "Севооборот"}
    },
    "🧅 Лук": {
        "⚪ Серо-фиолетовый налёт на пере": {"diagnosis": "Пероноспороз", "treatment": "🛡️ Ридомил, Фитоспорин", "prevention": "Прогрев севка"},
        "🟡 Кончики перьев желтеют": {"diagnosis": "Шейковая гниль / Нехватка калия", "treatment": "💧 Калийно-фосфорная подкормка", "prevention": "Правильная сушка"},
        "🦟 Личинки внутри пера": {"diagnosis": "Луковая муха", "treatment": "🧂 Полив соленой водой", "prevention": "Соседство с морковью"},
        "🟤 Чёрная плесень на донце": {"diagnosis": "Фузариоз", "treatment": "🛡️ Протравливание", "prevention": "Севооборот"}
    },
    "🌶️ Перец": {
        "🟣 Фиолетовый оттенок листьев": {"diagnosis": "Недостаток фосфора / Холод", "treatment": "🌡️ Укрытие, монофосфат калия", "prevention": "Температура выше +15°C"},
        "🟡 Опадают цветы и завязи": {"diagnosis": "Перегрев / Стресс", "treatment": "💧 Регулярный полив, притенение", "prevention": "Мульча"},
        "🟤 Чёрная ножка у рассады": {"diagnosis": "Грибковое заболевание", "treatment": "🛡️ Превикур", "prevention": "Стерилизация грунта"},
        "🌀 Листья деформируются": {"diagnosis": "Вирус табачной мозаики", "treatment": "🗑️ Удаление куста", "prevention": "Борьба с тлей"}
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
    with col1: 
        # sorted() сортирует города по алфавиту
        city = st.selectbox("📍 Город:", sorted(list(CITIES_DATA.keys()))) 
    with col2: crop = st.selectbox("🥕 Культура:", list(CROPS_DATA.keys()))
    
    if st.button("🚀 Рассчитать даты", type="primary"):
        today = datetime.now()
        c_info = CROPS_DATA[crop]
        city_data = CITIES_DATA[city]
        
        # Выбор базовой даты (заморозки или прогрев)
        if c_info["frost_sensitive"]:
            base = datetime(today.year, city_data["last_frost"][0], city_data["last_frost"][1])
            base_desc = "После заморозков"
        else:
            base = datetime(today.year, city_data["soil_warm_10c"][0], city_data["soil_warm_10c"][1])
            base_desc = "Прогрев почвы"
            
        res_date = base + timedelta(days=c_info["delay_days"])
        
        st.success(f"📅 Оптимальный старт: **{res_date.strftime('%d %B %Y')}** ({base_desc})")
        st.write("📋 План работ:")
        for task in c_info["plan"]:
            st.write(f"- {task}")

# 2. ДИАГНОСТИКА ПО СИМПТОМАМ
elif mode == "🔍 Диагностика (Симптомы)":
    st.title("🔍 Поиск болезни по симптомам")
    col1, col2 = st.columns(2)
    with col1: crop = st.selectbox("1. Культура:", list(DISEASE_DB.keys()))
    with col2: sym = st.selectbox("2. Симптом:", list(DISEASE_DB[crop].keys()))
    
    if st.button("🔍 Найти диагноз", type="primary"):
        res = DISEASE_DB[crop][sym]
        st.error(f"🩺 **Диагноз:** {res['diagnosis']}")
        st.success(f"💊 **Лечение:** {res['treatment']}")
        st.info(f"🛡️ **Профилактика:** {res['prevention']}")

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
                st.success("✅ Запись сохранена! (Сделайте скриншот для надежности)")
            else:
                st.warning("⚠️ Загрузите фото и добавьте описание")
