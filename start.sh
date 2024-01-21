#!/usr/bin/env bash

# Обновление списка пакетов
sudo apt update

# Установка Python 3.10 и обновление pip
sudo apt-get install python3.10
sudo apt update
sudo apt install python3-pip
sudo apt install python3-distutils

# Установка необходимых пакетов
pip install streamlit telethon asyncio pandas torch transformers nltk wordcloud

# Переход в директорию models
cd models

# Создание директории local_tokenizer
mkdir "local_tokenizer"

# Запуск скрипта get_models.py
python3 get_models.py