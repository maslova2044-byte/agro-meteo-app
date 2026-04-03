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
    "Ростов-на-
